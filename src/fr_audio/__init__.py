import logging

_OriginalFileHandler = logging.FileHandler


class _NullFileHandler(logging.NullHandler):
    def __init__(self, *args, **kwargs):
        super().__init__()


logging.FileHandler = _NullFileHandler
logging.disable(logging.INFO)

import verbecc  # noqa: F401, E402

logging.disable(logging.NOTSET)
logging.FileHandler = _OriginalFileHandler

for name, logger in logging.Logger.manager.loggerDict.items():
    if name.startswith("verbecc"):
        if isinstance(logger, logging.Logger):
            logger.setLevel(logging.ERROR)
            logger.propagate = False
            for handler in logger.handlers[:]:
                handler.close()
                logger.removeHandler(handler)
