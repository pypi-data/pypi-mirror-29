.. -*- rst -*-

opengrokfs
==========

opengrokfs implements a FUSE filesystem backed by the OpenGrok web interface.
A cscope clone which uses the OpenGrok web interface as the backend is also
included.

Install with pip::

    pip3 install opengrokfs

Run ``opengrokfs`` with the URL of the OpenGrok start page and the local
directory where the filesystem should be mounted::

    mkdir -p mnt
    opengrokfs http://androidxref.com/7.1.1_r6/ mnt

Now you can access the files::

    $ ls mnt/
    Android.bp  bootable        bionic  development  external
    art         bootstrap.bash  dalvik  device       frameworks
    ...

Use ``oggrep`` to search using OpenGrok's "Full Search"::

    $ cd mnt/bionic/
    mnt/bionic$ oggrep O_LARGEFILE
    libc/kernel/uapi/asm-arm/asm/fcntl.h:#define O_LARGEFILE 0400000
    libc/kernel/uapi/asm-arm64/asm/fcntl.h:#define O_LARGEFILE 0400000
    libc/bionic/lfs64_support.cpp:// are already 64-bit ready. In particular, we don't have non-O_LARGEFILE
    libc/bionic/open.cpp:  return flags | O_LARGEFILE;
    libc/kernel/uapi/asm-mips/asm/fcntl.h:#define O_LARGEFILE 0x2000
    libc/kernel/uapi/asm-generic/fcntl.h:#ifndef O_LARGEFILE
    libc/kernel/uapi/asm-generic/fcntl.h:#define O_LARGEFILE 00100000
    tests/stdlib_test.cpp:  ASSERT_EQ(O_LARGEFILE, fcntl(tf.fd, F_GETFL) & O_LARGEFILE);

``ogcscope`` emulates cscope's line-oriented interface but uses OpenGrok as the
backend::

    mnt/bionic$ ogcscope -dl
    >> 1CLONE_CHILD_SETTID
    cscope: 1 lines
    libc/kernel/uapi/linux/sched.h <unknown> 41 #define CLONE_CHILD_SETTID 0x01000000
    >> 0CLONE_CHILD_SETTID
    cscope: 5 lines
    libc/bionic/clone.cpp <unknown> 53   if ((flags & (CLONE_PARENT_SETTID|CLONE_SETTLS|CLONE_CHILD_SETTID|CLONE_CHILD_CLEARTID)) != 0) {
    libc/bionic/clone.cpp <unknown> 56   if ((flags & (CLONE_SETTLS|CLONE_CHILD_SETTID|CLONE_CHILD_CLEARTID)) != 0) {
    libc/bionic/clone.cpp <unknown> 59   if ((flags & (CLONE_CHILD_SETTID|CLONE_CHILD_CLEARTID)) != 0) {
    libc/bionic/fork.cpp <unknown> 34 #define FORK_FLAGS (CLONE_CHILD_SETTID | CLONE_CHILD_CLEARTID | SIGCHLD)
    libc/kernel/uapi/linux/sched.h <unknown> 41 #define CLONE_CHILD_SETTID 0x01000000

``ogcscope`` can be used from within any editor which supports cscope.  For
example, for ``vim``::

    mnt/bionic$ vim -c 'set cscopeprg=ogcscope' -c 'cs add .opengrokfs'
