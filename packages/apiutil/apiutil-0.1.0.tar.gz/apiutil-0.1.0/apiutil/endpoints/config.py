# encoding: utf-8

import logging_helper
from configurationutil import Configuration, cfg_params
from .._metadata import __version__, __authorshort__, __module_name__
from ..resources import templates, schema
from ._constants import HOST_CONFIG, ENDPOINT_CONFIG, API_CONFIG, ENVIRONMENT_CONFIG

logging = logging_helper.setup_logging()

# Register Config details (These are expected to be overwritten by an importing app)
cfg_params.APP_NAME = __module_name__
cfg_params.APP_AUTHOR = __authorshort__
cfg_params.APP_VERSION = __version__

HOSTS_TEMPLATE = templates.host_config
ENDPOINTS_TEMPLATE = templates.endpoint_config
APIS_TEMPLATE = templates.api_config
ENVIRONMENTS_TEMPLATE = templates.environment_config


def register_host_config():

    # Retrieve configuration instance
    cfg = Configuration()

    # Register configuration
    cfg.register(config=HOST_CONFIG,
                 config_type=cfg_params.CONST.yaml,
                 template=HOSTS_TEMPLATE,
                 schema=schema.host_config)

    return cfg


def register_endpoint_config():

    # Retrieve configuration instance
    cfg = Configuration()

    # Register configuration
    cfg.register(config=ENDPOINT_CONFIG,
                 config_type=cfg_params.CONST.yaml,
                 template=ENDPOINTS_TEMPLATE,
                 schema=schema.endpoint_config)

    return cfg


def register_api_config():

    # Retrieve configuration instance
    cfg = Configuration()

    # Register configuration
    cfg.register(config=API_CONFIG,
                 config_type=cfg_params.CONST.yaml,
                 template=APIS_TEMPLATE,
                 schema=schema.api_config)

    return cfg


def register_environment_config():

    # Retrieve configuration instance
    cfg = Configuration()

    # Register configuration
    cfg.register(config=ENVIRONMENT_CONFIG,
                 config_type=cfg_params.CONST.yaml,
                 template=ENVIRONMENTS_TEMPLATE,
                 schema=schema.environment_config)

    return cfg
