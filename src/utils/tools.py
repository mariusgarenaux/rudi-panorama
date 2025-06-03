import yaml
import json
import logging
import os
import streamlit as st


# ---------------------------
# Access specific conf fields
# and set global variables
# ---------------------------
@st.cache_data
def get_config_file():
    # custom logging for config loading
    init_logger = logging.getLogger(__name__)

    try:
        with open("../conf/conf.yaml") as yaml_config:
            config = yaml.safe_load(yaml_config)
    except Exception as e:
        init_logger.error("Could not load config file.", e)
        raise Exception(
            f"Can not load config file. Reminder, config file is located at ../config/config.yaml from main.py",
            e,
        )

    init_logger.info(f"Successfully loaded config file.")
    return config


CONFIG = get_config_file()


@st.cache_data
def get_logging_level():
    if "logging_level" not in CONFIG:
        return logging.INFO
    match CONFIG["logging_level"]:
        case "INFO":
            return logging.INFO
        case "DEBUG":
            return logging.DEBUG
        case "WARNING":
            return logging.WARNING
        case "ERROR":
            return logging.ERROR
        case "CRITICAL":
            return logging.CRITICAL
        case _:
            raise Exception(
                f"Unexpected value for logging level : {CONFIG['logging_level']}"
            )


def get_logger(name: str):
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(message)s",
        level=get_logging_level(),
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger(name)


logger = get_logger("tools")
