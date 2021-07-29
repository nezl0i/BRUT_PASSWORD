import sys
from serial_port import UartSerialPort
from modbus_crc16 import crc16
from timeit import timeit
import config as cfg
from sys import platform

if platform.startswith('win'):
    from colors import WinColors
    c = WinColors()
else:
    from colors import Colors
    c = Colors()
    
    
port = UartSerialPort(port_name='COM9', port_timeout=cfg.SERIAL_TIMEOUT)


def exchange(id_pu, input_pass, serial_port):
    test = id_pu + ' 01 02 ' + input_pass
    transfer = bytearray.fromhex(test + ' ' + crc16(bytearray.fromhex(test)))
    sys.stdout.write(f'{c.WARNING}Пробуем пароль - {input_pass}{c.END}\r')
    sys.stdout.flush()
    serial_port.write(transfer)
    buffer = serial_port.read(4)
    while buffer:
        print('\n')
        print(f'{c.GREEN}Пароль найден - {input_pass}{c.END}')
        return True
    return False


def brut_password(passwd, stop_password, pass_mode=None):
    while passwd <= stop_password:
        if pass_mode == 'hex':
            hex_password = ' '.join((format(int(i), '02X')) for i in str(passwd))
        elif pass_mode == 'ascii':
            hex_password = ' '.join((format(ord(i), '02X')) for i in str(passwd))
        else:
            print('Non pass_mode..')
            sys.exit()
        if exchange(hex_id, hex_password, port):
            return
        if str(passwd)[5] == '9':
            passwd += 2
        else:
            passwd += 1


if __name__ == '__main__':

    # 100000 паролей
    # Время поиска - 4377.486616813 сек. (1 ч. 20 мин.)

    password = cfg.START_PASSWORD
    hex_id = format(cfg.ID_PU, '02X')
    mode = 'ascii'

    print(
        f"{c.BLUE}"
        f"Время поиска - {timeit('brut_password(password, cfg.STOP_PASSWORD, mode)', globals=globals(), number=1)} "
        f"сек.{c.END}"
    )
