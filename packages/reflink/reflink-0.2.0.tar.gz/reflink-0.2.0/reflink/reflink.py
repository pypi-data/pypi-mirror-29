# -*- coding: utf-8 -*-

"""Main module."""

import os

from . import backend

def reflink(oldpath, newpath):
    """ Create a reflink from ``newpath`` to ``oldpath``.
    Raises a ``NotImplementedError`` when the OS does not implement reflink.
    Raises a ``ReflinkImpossibleError`` when trying to reflink between devices,
    Raises an ``IOError`` when:

    * ``oldpath`` is a directory
    * The user has no permissions to create ``newpath``
    * Trying to reflink into a swapfile (ETXTBSY)

    For debugability's sake, ``reflink`` _can_ throw IOError in other cases,
    when the underlying system call fails for another reason.
    However, these reasons cannot be triggered with this basic call.
    See man `IOCTL-FICLONERANGE(2) <http://man7.org/linux/man-pages/man2/ioctl_ficlonerange.2.html>`__
    and ``backend.py`` for more details on these conditions.

    Example code:

        >>> from reflink import reflink
        >>> reflink("large_file.img", "copy_of_file.img") # doctest: +SKIP
        >>>
    """
    # raise NotImplementedError when OS does not implement reflink
    # raise ReflinkImpossibleError when trying to reflink across devices
    backend.clone(oldpath, newpath)

def supported_at(path):
    """ Returns ``True`` when a path on the filesystem supports reflinking,
    ``False`` otherwise.

    Please note that the current implementation verifies this by testing
    whether it's possible to reflink.
    """

    # Currently, there's no systemcall that tests whether a point in the VFS is supported or not.
    # We create a file at ``path``, and clone it.

    a = os.path.join(path, "i_hope_no_one_will_ever_try_this_name.txt")
    b = os.path.join(path, "i_hope_no_one_will_ever_try_that_name.txt")

    with open(a, 'w+') as f:
        f.write(u"abc")
    try:
        reflink(a, b)
        return True
    except:
        pass
        # TODO: there are probably specific exception that we can handle
    finally:
        os.unlink(a)
        if os.path.isfile(b):
            os.unlink(b)

    return False
