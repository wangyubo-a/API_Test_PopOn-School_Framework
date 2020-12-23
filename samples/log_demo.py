from nb_log import LogManager

logger = LogManager('LALALA').get_logger_and_add_handlers(is_add_stream_handler=True, log_filename='ha.log')
logger.info('蓝色')




