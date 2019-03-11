import contextlib

# Use a faster event loop, if available.
with contextlib.suppress(ImportError):
    import uvloop
    uvloop.install()
