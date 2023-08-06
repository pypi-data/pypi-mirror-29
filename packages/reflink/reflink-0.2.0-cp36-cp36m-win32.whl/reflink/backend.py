import errno
import sys

from ._backend import ffi, lib
from .error import ReflinkImpossibleError


def clone(oldpath, newpath):
    if isinstance(oldpath, str):
        oldpath = oldpath.encode(sys.getfilesystemencoding())
    if isinstance(newpath, str):
        newpath = newpath.encode(sys.getfilesystemencoding())

    newpath_c = ffi.new('char[]', newpath)
    oldpath_c = ffi.new('char[]', oldpath)

    rc = lib.reflink_clone_file(oldpath_c, newpath_c)

    if rc == 0:
        return # Success!

    if rc == -1:
        # ioctl returned an error.
        # We investigate in Python and throw
        if lib.errno == errno.EBADF:
            raise NotImplementedError("BUG: errno EBADF when handling ioctl error")
        if lib.errno == errno.EINVAL:
            raise IOError("EINVAL when handling ioctl: The filesystem does not support reflinking the ranges of the given files.")
        if lib.errno == errno.EISDIR:
            raise IOError("Cannot reflink directories")
        if lib.errno == errno.EOPNOTSUPP:
            raise ReflinkImpossibleError("EOPNOTSUPP")
        if lib.errno == errno.EPERM:
            raise IOError("EPERM: no permission to write to %s" % newpath)
        if lib.errno == errno.ETXTBSY:
            raise IOError("ETXTBSY: cannot reflink from/to swapfiles")
        if lib.errno == errno.EXDEV:
            raise ReflinkImpossibleError("EXDEV")
        if lib.errno == errno.ENOENT:
            raise FileNotFoundError("Cannot open source file %s (%i)" % (oldpath, lib.errno))

        raise Exception("BUG: errno %s not implemented" % errno.errorcode[lib.errno])

    if rc == -3:
        raise IOError("Cannot open file %s for writing (%i)" % (newpath, lib.errno))
    if rc == -2:
        if lib.errno == errno.ENOENT:
            raise FileNotFoundError("No such file %s (%i)" % (oldpath, lib.errno))
        raise IOError("Cannot open source file %s (%i)" % (oldpath, lib.errno))
    if rc == -4:
        raise NotImplementedError()
    if rc == -5:
        raise IOError("Could not copy permissions (errno %s)" % errno.errorcode[lib.errno])
    raise IOError("Unknown exception (errno %s)" % errno.errorcode[lib.errno])
