import sys
from utils.helpers import get_current_data_and_time
from traceback import print_exception


def log_error_in_file():
    """
    Простой логгер ошибки функции в локальный файл
    Создает файл в пути /logs для текущей даты
    :return: None
    """
    data_for_file, time_for_file = get_current_data_and_time()
    error_file = f'logs/error_log_{data_for_file}.txt'

    try:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        with open(error_file, 'a') as file:
            print('_______________________________________', file=file)
            print(f'Current time {time_for_file}', file=file)
            print_exception(exc_type, exc_value, exc_traceback, file=file)
            print('_______________________________________', file=file)
    except Exception as e:
        print(e)
