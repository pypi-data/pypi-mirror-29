import logging
import sys

logger = logging.getLogger(__name__)

root_logger = logging.getLogger()

package_name = '.'.join(__name__.split('.')[:-1])
sensenet_logger = logging.getLogger(package_name)

# Should be modified only by official plugins. This is an
# unsupported API and may be removed in future versions.
_extra_loggers = [sensenet_logger]

# Set up the default handler
formatter = logging.Formatter('[%(asctime)s] %(message)s')
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(formatter)

# We need to take in the sensenet logger explicitly since this is called
# at initialization time.
def logger_setup(_=None):
    # This used to take in an argument; we still take an (ignored)
    # argument for compatibility.
    root_logger.addHandler(handler)
    for logger in _extra_loggers:
        logger.setLevel(logging.INFO)

def undo_logger_setup():
    """Undoes the automatic logging setup done by sensenet. You should call
    this function if you want to manually configure logging
    yourself. Typical usage would involve putting something like the
    following at the top of your script:

    sensenet.undo_logger_setup()
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler(sys.stderr))
    """
    root_logger.removeHandler(handler)
    for logger in _extra_loggers:
        logger.setLevel(logging.NOTSET)
