from class_brut import Exchange
from timeit import timeit
import config as cfg


if __name__ == '__main__':
    try:
        e = Exchange(cfg.UART_PORT, cfg.UART_PORT_TIMEOUT)
        print(f"Время поиска - {timeit('e.brut_password()', globals=globals(), number=1)} ")
    except IndexError:
        print('Ошибка открытия порта. Порт занят или недоступен')
    # e.brut_password()

    # 100000 паролей
    # Время поиска - 4377.486616813 сек. (1 ч. 20 мин.)


