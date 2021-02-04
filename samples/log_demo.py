from nb_log import LogManager

logger = LogManager('LALALA').get_logger_and_add_handlers(is_add_stream_handler=True, log_filename='ha.log')
logger.info('蓝色')


a = 1.0
b = str(a)
c = int(b)
print(c)
print(type(c))
