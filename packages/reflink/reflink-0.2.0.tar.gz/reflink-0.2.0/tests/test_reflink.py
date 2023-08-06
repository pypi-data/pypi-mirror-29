#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `reflink` package."""

import pytest
import os
import subprocess
import random
import string
import unittest
import sys


from reflink import reflink, ReflinkImpossibleError, supported_at


@pytest.fixture
def btrfs_volume(tmpdir):
    path = tmpdir.join("volume")
    with open(path, 'bw+') as f:
        f.truncate(512 * 1024 ** 2)

    process = subprocess.call(["mkfs.btrfs", path])
    assert process == 0

    yield path
    os.remove(path)

@pytest.fixture
def btrfs_mount(tmpdir, btrfs_volume):
    mount = tmpdir.join("mount")
    os.mkdir(mount)
    process = subprocess.call(["mount", btrfs_volume, mount])
    assert process == 0

    yield mount

    process = subprocess.call(["umount", btrfs_volume])
    assert process == 0
    os.rmdir(mount)

@pytest.fixture
def file_on_mount(btrfs_mount):
    name = ''.join(random.choices(string.ascii_lowercase, k=8))
    path = os.path.join(btrfs_mount, name)
    with open(path, 'bw+') as f:
        f.write(''.join(random.choices(string.ascii_lowercase, k=100)).encode('utf-8'))

    yield path

    os.remove(path)


@pytest.mark.btrfs
def test_reflink(btrfs_mount, file_on_mount):
    target = os.path.join(btrfs_mount, "target")
    reflink(file_on_mount, target)

    assert os.path.isfile(target)

@pytest.mark.btrfs
def test_reflink(btrfs_mount):
    source = os.path.join(btrfs_mount, "source")
    target = os.path.join(btrfs_mount, "target")
    with pytest.raises(FileNotFoundError):
        reflink(source, target)

    assert not os.path.isfile(source)
    assert not os.path.isfile(target)

@pytest.mark.btrfs
def test_reflink_across_devices(btrfs_mount, file_on_mount, tmpdir):
    target = os.path.join(tmpdir, "target")

    with pytest.raises(ReflinkImpossibleError):
        reflink(file_on_mount, target)

    assert not os.path.isfile(target)

@pytest.mark.btrfs
def test_supported_at_btrfs(btrfs_mount):
    assert supported_at(btrfs_mount)

@pytest.mark.btrfs
def test_btrfs_permissions(btrfs_mount, file_on_mount):
    target = os.path.join(btrfs_mount, "target")
    reflink(file_on_mount, target)

    a = os.stat(file_on_mount)
    b = os.stat(target)
    assert a.st_mode == b.st_mode

@unittest.skipUnless(sys.platform in ['linux', 'freebsd'], "No /dev support")
def test_not_supported_at_dev():
    assert not supported_at("/dev")
