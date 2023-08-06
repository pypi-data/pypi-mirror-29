=====
Usage
=====

To use Python reflink in a project::

    import reflink

    from reflink import reflink
    reflink("large_file.img", "copy_of_file.img")

Raises a ``NotImplementedError`` when the OS does not implement reflink.
Raises a ``ReflinkImpossibleError`` when trying to reflink between devices,
