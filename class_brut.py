import sys
from time import sleep
from uart import UartSerialPort
from modbus_crc16 import crc16
import config as cfg


class Exchange(UartSerialPort):
    def __init__(self, port_name, port_timeout):
        super().__init__(port_name, port_timeout)

        self.flag = True
        self.CALL = {'AT': 'AT\r', 'CBST': 'AT+CBST=71,0,1\r', 'CALL': f'ATD{cfg.PHONE}\r'}
        self.id = format(cfg.PK, '02X')

        self.timeout = cfg.SERIAL_TIMEOUT

        self.start_passwd = cfg.START_PASSWORD
        self.stop_passwd = cfg.STOP_PASSWORD

        self.pass_mode = cfg.PASS_MODE

        self.mode = cfg.MODE

        if self.test(self.id):
            self.init()
        else:
            print('Нет ответа от устройства')
            sys.exit()

    def set_flag(self, item):
        self.flag = item
        return self.flag

    def test(self, pk):
        test = f'{pk} 00 '
        transfer = bytearray.fromhex(test + crc16(bytearray.fromhex(test)))
        sys.stdout.write(f'Тест канала связи ...\r')
        self.write(transfer)
        buffer = self.read(4)
        while buffer:
            # print(f"Ответ от устройства >> {buffer.hex(' ', -1)}\n")
            sys.stdout.write(f'Тест канала связи - ОК.\n')
            print('-'*28)
            sleep(2)
            return True
        return False

    def init(self):
        if self.mode == 1:
            self.set_flag(False)
            print(self.CSD_send(self.CALL['AT']))
            print(self.CSD_send(self.CALL['CBST']))
            self.set_time(10)
            for _ in range(3):
                calling = self.CSD_send(self.CALL['CALL'])
                print(calling)
                if calling == 'Connect OK (9600)\n':
                    self.set_flag(True)
                    self.set_time(self.timeout)
                    break
            return self.flag

    def reading(self, pk, input_pass=None):
        test = f'{pk} 01 02 {input_pass} '
        transfer = bytearray.fromhex(test + crc16(bytearray.fromhex(test)))
        sys.stdout.write(f'Пробуем пароль - {input_pass}\r')
        self.write(transfer)
        buffer = self.read(4)
        while buffer:
            print(f"Ответ от устройства >> {buffer.hex(' ', -1)}\n")
            print(f'Пароль найден - {input_pass}')
            return True
        return False

    def brut_password(self):
        while self.start_passwd <= self.stop_passwd:
            if self.pass_mode == 'hex':
                hex_password = ' '.join((format(int(i), '02X')) for i in str(self.start_passwd))
            elif self.pass_mode == 'ascii':
                hex_password = ' '.join((format(ord(i), '02X')) for i in str(self.start_passwd))
            else:
                print('Pass_mode is None..')
                sys.exit()
            if self.flag:
                if self.reading(self.id, hex_password):
                    return
                if str(self.start_passwd)[3:] == '000':
                    print('Пауза 5 сек...')
                    sleep(5)
                    if not self.test(self.id):
                        sys.exit()
                # start_passwd += 2 if str(start_passwd)[5] == '9' else 1
                self.start_passwd += 1
            else:
                sys.exit()
