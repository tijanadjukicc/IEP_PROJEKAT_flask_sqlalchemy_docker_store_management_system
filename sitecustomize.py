# force Python SSL to use certifi instead of Windows cert store
import ssl, certifi

_orig_create_default_context = ssl.create_default_context

def _patched_create_default_context(purpose=ssl.Purpose.SERVER_AUTH, *, cafile=None, capath=None, cadata=None):
    # if no CA file was explicitly passed, use certifi's bundle
    if cafile is None and capath is None and cadata is None:
        cafile = certifi.where()
    return _orig_create_default_context(purpose=purpose, cafile=cafile, capath=capath, cadata=cadata)

ssl.create_default_context = _patched_create_default_context
