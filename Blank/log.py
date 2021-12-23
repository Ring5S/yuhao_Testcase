import logging


def create_logger(name, level, filename):
    """
    创建日记对象
    :param name:日记名称，在日记文件中体现
    :param level:日记等级
    :param filename:日记文件所在目录及名称
    :return:日记对象
    """
    logger = logging.getLogger(name)
    if level == 'info':
        logger.setLevel(logging.INFO)
    elif level == 'debug':
        logger.setLevel(logging.DEBUG)
    elif level == 'error':
        logger.setLevel(logging.ERROR)
    elif level == 'warning':
        logger.setLevel(logging.WARNING)
    elif level == 'critical':
        logger.setLevel(logging.CRITICAL)
    else:
        return 'level is error'
    fh = logging.FileHandler(filename)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
