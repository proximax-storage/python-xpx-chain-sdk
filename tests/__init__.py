import warnings

# We want to catch all non-user warnings, which are emitted
# from the fallback ED25519 implementation.
warnings.filterwarnings('error')
warnings.filterwarnings('default', category=UserWarning)
