import logging
import logging.handlers

formatter = logging.Formatter('%(asctime)s :::: %(name)s :::: %(levelname)s :::: %(message)s')


def setup_logger(name: str, log_file: str, level="DEBUG", when='D', interval=1, backup_count=30):
    """
    Function to setup loggers
    :param backup_count: Number of instances of backups to keep.
    :param interval: Number of instances after which to rotate
    :param when: Unit of time to which interval will be multiplied.
    :param name: name of the logger
    :param log_file: Path where data has to be logged.
    :param level: Logging Level
    :return: logger instance.
    """
    if level.upper() == "DEBUG":
        level = logging.DEBUG
    elif level.upper() == "ERROR":
        level = logging.ERROR
    elif level.upper() == "WARN":
        level = logging.WARN
    elif level.upper() == "INFO":
        level = logging.INFO
    elif level.upper() == "CRITICAL":
        level = logging.CRITICAL
    handler = logging.handlers.TimedRotatingFileHandler(filename=log_file, when=when,
                                                        interval=interval, backupCount=backup_count)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
