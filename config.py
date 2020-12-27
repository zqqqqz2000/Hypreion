from core.core_types import Config
from logger.echo import Echo


class Default(Config):
    DOMAIN_SESSION_CLEAR_THRESHOLD = 5 * 60
    LOGGER = Echo
    MODULE_BASE_DIR = 'modules'
