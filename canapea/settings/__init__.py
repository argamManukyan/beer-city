try:
    from .local_settings import *
except ImportError:
    from .production_settings import *
