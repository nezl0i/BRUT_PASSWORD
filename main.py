from class_brut import Exchange
from timeit import timeit
import config as cfg


if __name__ == '__main__':
    e = Exchange(cfg.PORT, cfg.SERIAL_TIMEOUT)
    # e.brut_password()

    # 100000 паролей
    # Время поиска - 4377.486616813 сек. (1 ч. 20 мин.)

    print(f"Время поиска - {timeit('e.brut_password()', globals=globals(), number=1)} ")
