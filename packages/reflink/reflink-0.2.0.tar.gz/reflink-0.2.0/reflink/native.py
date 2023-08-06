import sys

from cffi import FFI

REFLINK_ATTR_PRESERVE = 0x1
REFLINK_ATTR_NONE = 0x0

platform = sys.platform
if platform == 'linux2':
    platform = 'linux'

ffibuilder = FFI()
with open("reflink/%s.c" % platform) as source_file:
    ffibuilder.set_source("reflink._backend", source_file.read())

ffibuilder.cdef("""
int reflink_clone_file(char *oldpath, char *newpath);
int errno;
""")

if __file__ == '__main__':
    ffibuilder.compile(verbose=True)
