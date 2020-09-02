import logging


class LoggerCls:

    # Always instantiate a logger, do not use the root logger, the top in hierarchy.
    # Beware do use logging_utils.basicConfig, initializes the root logger and overwrites every logger
    def __init__(self, log_type, name, filename, filemode, formatter, level):

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.set_logger_type(log_type, filename, filemode, formatter)   # set type logger for each class instance

    def set_logger_type(self, log_type, filename, filemode, formatter):
        if log_type == "log_to_file":
            file_handler = logging.FileHandler(filename, filemode)
            formatter_ = logging.Formatter(formatter)
            file_handler.setFormatter(formatter_)
            self.logger.addHandler(file_handler)
        elif log_type == "log_to_stdout":
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
