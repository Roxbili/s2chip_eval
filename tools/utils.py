# -*-coding: utf-8-*-
import logging
import time

class Logger(object):
    '''输出日志模块，用于控制台控制日志输出等级'''

    logger = logging.getLogger(__file__)
    logger.setLevel(logging.DEBUG)

    def __init__(self, level='DEBUG'):
        '''设置日志输出等级

            输入：
                level: DEBUG, INFO, WARN, ERROR, CRITICAL
        '''

        # handler设置
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self._get_level(level))
        formatter = logging.Formatter('[%(levelname)s] %(filename)s:%(lineno)d - %(message)s')
        console_handler.setFormatter(formatter)

        Logger.logger.addHandler(console_handler)

    def _get_level(self, level: str):
        log_level = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        return log_level[level.upper()]

    def get_logger() -> logging:
        return Logger.logger

class Timer(object):
    def __init__(self):
        self.total_time = 0.
        self.count = 0

    def start(self):
        self.start_time = time.time()

    def end(self):
        self.end_time = time.time()

        self.count += 1
        self.total_time += self.current_time()

    def current_time(self):
        return self.end_time - self.start_time

    def avg_time(self):
        return self.total_time / self.count



if __name__ == '__main__':
    logger = Logger('WARNING').get_logger()

    logger.debug("This is a debug log.")
    logger.info("This is a info log.")
    logger.warning("This is a warning log.")
    logger.error("This is a error log.")
    logger.critical("This is a critical log.")