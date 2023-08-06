#include <sys/clonefile.h> /* for clonefile(2) */
#include <errno.h>

int reflink_clone_file(char *oldpath, char *newpath) {
    int rc;
    rc = clonefile(oldpath, newpath, 0);
    if (rc == 0) return 0;
    if (errno == ENOTSUP) {
        return -4;
    }
    return rc;
}
