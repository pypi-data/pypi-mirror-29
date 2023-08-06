#include <sys/stat.h>
#include <fcntl.h>
#include <linux/fs.h>
#include <sys/ioctl.h>
#include <assert.h>
#include <errno.h>

int clone_permissions(char *oldpath, char *newpath) {
    struct stat st;
    int rc;

    rc = stat(oldpath, &st);
    if (rc) {
        return rc;
    }
    return chmod(newpath, st.st_mode);
}

int reflink_clone_file(char *oldpath, char *newpath) {
#ifdef FICLONE
    int old_fd = open(oldpath, O_RDONLY);
    if (old_fd < 0) {
        return -2;
    }
    int new_fd = open(newpath, O_WRONLY | O_CREAT, S_IRUSR | S_IWUSR);
    if (new_fd < 0) {
        close(old_fd);
        return -3;
    }

    int result = ioctl (new_fd, FICLONE, old_fd);

    close(new_fd);
    close(old_fd);

    if (result != 0) {
        unlink(newpath);
        return result;
    }

    if (clone_permissions(oldpath, newpath)) {
        unlink(newpath);
        return -5;
    }

    return result;
#else
    return -4;
#endif
}
