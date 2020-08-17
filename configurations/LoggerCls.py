import logging


class LoggerCls:

    # Always instantiate a logger, do not use the root logger, the top in hierarhy.
    # Beware do use logging.basicConfig, initializes the root logger and overwrites every logger
    def __init__(self, logger_type, logger_name, logger_filename, logger_filemode, formatter, logger_level):

        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logger_level)

        if logger_type == "log_to_file":
            file_handler = logging.FileHandler(logger_filename, logger_filemode)
            formatter_ = logging.Formatter(formatter)
            file_handler.setFormatter(formatter_)
            self.logger.addHandler(file_handler)
        elif logger_type == "log_to_stdout":
            stream_handler = logging.StreamHandler()
            formatter_ = logging.Formatter(formatter)
            stream_handler.setFormatter(formatter_)
            self.logger.addHandler(stream_handler)

    def debug(self, msg, **kwargs):
        self.logger.debug(msg, **kwargs)

    def info(self, msg, **kwargs):
        self.logger.info(msg, **kwargs)

    def warning(self, msg, **kwargs):
        self.logger.warning(msg, **kwargs)

    def error(self, msg, **kwargs):
        self.logger.error(msg, **kwargs)