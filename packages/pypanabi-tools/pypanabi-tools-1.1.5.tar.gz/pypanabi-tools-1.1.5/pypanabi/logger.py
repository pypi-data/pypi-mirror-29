#!/usr/bin/env python

import logging


class Logger(object):
    def __init__(self, logger_name, level=None, format=None, filename=None, filemode='a'):
        """
        Constructor
        :param logger_name: Logger Name [String]
        :param level: Logging level DEBUG, INFO, WARNING, ERROR, CRITICAL, ERROR [String]
        :param format: Format for logging output [String]
        :param filename: Filepath in case that output must be redirected to file [String]
        :param filemode: Write mode: a, w [String]
        """
        if not format:
            format = '%(asctime)s - %(name)s [%(levelname)s] %(message)s'

        if filename:
            logging.basicConfig(format=format, level=self._get_logging_level(level),
                                filename=filename, filemode=filemode)
        else:
            logging.basicConfig(format=format, level=self._get_logging_level(level))
        self.logger = logging.getLogger(logger_name)

    @staticmethod
    def _get_logging_level(level):
        """
        Get logging level
        :param level: Logging level [String]
        :return: Loggin level [Logging.Level]
        """
        level = level.upper()
        try:
            if level == 'INFO':
                return logging.INFO

            if level == 'WARNING':
                return logging.WARNING

            if level == 'ERROR':
                return logging.ERROR

            if level == 'CRITICAL':
                return logging.CRITICAL

            if level == 'DEBUG':
                return logging.DEBUG

            raise Exception('Invalid logging level {}'.format(level))
        except Exception as ex:
            print(repr(ex))
            raise

    def info(self, message):
        """
        Info message
        :param message: Message [String]
        :return: None
        """
        self.logger.info(message)

    def warning(self, message):
        """
        Warning message
        :param message: Message [String]
        :return: None
        """
        self.logger.warning(message)

    def error(self, message):
        """
        Error message
        :param message: Message [String]
        :return: None
        """
        self.logger.error(message)

    def critical(self, message):
        """
        Critical message
        :param message: Message [String]
        :return: None
        """
        self.logger.critical(message)

    def debug(self, message):
        """
        Debug message
        :param message: Message [String]
        :return: None
        """
        self.logger.debug(message)
