import logging


class LoggerCls:
    def __init__(self, logger_name, logger_filename, logger_filemode, logger_level):
        logging.basicConfig(filename= logger_filename, filemode=logger_filemode, level=logger_level)
        self.logger = logging.getLogger(logger_name) # always instantiate a logger, do use the default saysy the manual(to find why..)

    def debug(self, msg, **kwargs):
        self.logger.debug(msg, **kwargs)

    def info(self, msg, **kwargs):
        self.logger.info(msg, **kwargs)

    def warning(self, msg, **kwargs):
        self.logger.warning(msg, **kwargs)

    def error(self, msg, **kwargs):
        self.logger.error(msg, **kwargs)