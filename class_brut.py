import sys
from uart import UartSerialPort
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


class Exchange(UartSerialPort):
    def __init__(self, port_name, port_timeout):
        super().__init__(port_name, port_timeout)

        self.cfg = cfg
        self.flag = True

        self.CALL = {'AT': 'AT\r', 'CBST': 'AT+CBST=71,0,1\r', 'CALL': f'ATD{self.cfg.PHONE}\r'}

    def ex_form(self, id_pu, input_pass):
        test = f'{id_pu} 01 02 {input_pass}'
        transfer = bytearray.fromhex(test + ' ' + crc16(bytearray.fromhex(test)))
        sys.stdout.write(f'{c.WARNING}Пробуем пароль - {input_pass}{c.END}\r')
        sys.stdout.flush()
        self.write(transfer)
        buffer = self.read(4)
        while buffer:
            print('\n')
            print(f'{c.GREEN}Пароль найден - {input_pass}{c.END}')
            return True
        return False

    def brut_password(self):
        start_passwd = self.cfg.START_PASSWORD
        stop_passwd = self.cfg.STOP_PASSWORD
        while start_passwd <= stop_passwd:
            if self.cfg.PASS_MODE == 'hex':
                hex_password = ' '.join((format(int(i), '02X')) for i in str(start_passwd))
            elif self.cfg.PASS_MODE == 'ascii':
                hex_password = ' '.join((format(ord(i), '02X')) for i in str(start_passwd))
            else:
                print('Non pass_mode..')
                sys.exit()
            if self.cfg.CSD:
                self.flag = False
                print(self.CSD_send(self.CALL['AT']))
                print(self.CSD_send(self.CALL['CBST']))
                self.set_time(10)
                for _ in range(3):
                    calling = self.CSD_send(self.CALL['CALL'])
                    print(calling)
                    if calling == 'Connect OK (9600)\n':
                        self.flag = True
                        self.cfg.CSD = False
                        break
            if self.flag:
                if self.ex_form(self.cfg.ID_PU, hex_password):
                    return
                start_passwd += 2 if str(start_passwd)[5] == '9' else 1
            else:
                sys.exit()

    def print_cfg(self):
        return self.cfg.START_PASSWORD
