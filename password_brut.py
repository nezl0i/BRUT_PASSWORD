from serial_port import UartSerialPort
from modbus_crc16 import crc16
from timeit import timeit
from colors import Colors
import config as cfg

c = Colors()
port = UartSerialPort(port_name='/dev/ttyUSB0', port_timeout=cfg.SERIAL_TIMEOUT)


def exchange(id_pu, input_pass, serial_port):
    tmp_buffer = ''
    test = id_pu + ' 01 02 ' + input_pass
    transfer = bytearray.fromhex(test + ' ' + crc16(bytearray.fromhex(test)))

    get_hex_line = ' '.join(format(x, '02x') for x in transfer)
    print(f'{c.WARNING}Пробуем пароль - {input_pass}{c.END}')
    serial_port.write(transfer)
    buffer = serial_port.read(4)
    while buffer:
        if len(buffer) == 4:
            tmp_buffer = buffer.hex(' ', -1)
            print(f'{c.GREEN}{tmp_buffer}{c.END}')
            print(f'{c.GREEN}Пароль найден - {input_pass}{c.END}')
            return True, get_hex_line, tmp_buffer
        break
    return False, get_hex_line, tmp_buffer


def brut_password(passwd, stop_password):
    while passwd <= stop_password:
        hex_password = ' '.join((format(int(i), '02X')) for i in str(int(passwd)))
        if exchange(hex_id, hex_password, port)[0]:
            break
        if str(passwd)[5] == '9':
            passwd += 2
        else:
            passwd += 1


if __name__ == '__main__':

    # 100000 паролей
    # Время поиска - 4377.486616813 сек. (1 ч. 20 мин.)

    password = int(cfg.START_PASSWORD)
    hex_id = format(cfg.ID_PU, '02X')

    print(
        f"{c.BLUE}"
        f"Время поиска - {timeit('brut_password(password, cfg.STOP_PASSWORD)', globals=globals(), number=1)} "
        f"сек.{c.END}"
    )
