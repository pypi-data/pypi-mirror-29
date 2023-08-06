import re
from taliabeeio import TaliaBeeIO
from xbee import ZigBee
from pprint import pprint
from time import sleep

DATA_PATTERN = re.compile('([0-9]+)\|([CNR])\|(.*)')
COMMAND_PATTERN = re.compile('([ADR])([0-9]{2})([0-9]+)')
SLEEP_PATTERN = re.compile('S([0-9]{1,2}(\.[0-9])?)')


class TaliaBeeZ(object):

    def __init__(self, port):
        super(TaliaBeeZ, self).__init__()
        self.port = port
        self._zigbee = None
        self.io_controller = TaliaBeeIO()

    @property
    def running(self):
        return self._zigbee is not None

    @staticmethod
    def parse_raw_data(data):
        parsed = DATA_PATTERN.match(data)
        msg_id, dtype, message = parsed.groups()

        return {'msg_id': int(msg_id),
                'dtype': dtype,
                'message': message}

    @staticmethod
    def generate_raw_data(msg_id, dtype, message):
        return '{}|{}|{}'.format(msg_id, dtype, message)

    def send(self, addr, data):
        return self._zigbee.tx(dest_addr_long=addr, data=bytes(data, 'utf-8'))

    def process_data(self, data):
        pprint(data)
        if data['id'] == 'rx_explicit':
            try:
                received_data = self.parse_raw_data(data['rf_data'].decode())
                response_data = self.data_handler(received_data['message'])
                response = self.generate_raw_data(received_data['msg_id'],
                                                  'R', response_data)
                self.send(addr=data['source_addr_long'], data=response)

            except Exception as e:
                print('err', str(e))
                raise
        else:
            self.sink_data()

    def sink_data(self):
        return

    def run(self):
        print('Working')
        self._zigbee = ZigBee(self.port, callback=self.process_data)

    def halt(self):
        self._zigbee.halt()
        self._zigbee = None
        self.port.close()

    def data_handler(self, message):
        commands = message.split(',')
        for c in commands:
            # Is that a command?
            mc, ms = COMMAND_PATTERN.match(c), SLEEP_PATTERN.match(c)
            if mc:
                output_type, pin, val = mc.groups()
                val = int(val)
                pin = int(pin)
                if output_type == 'D':
                    setattr(self.io_controller, 'do' + str(pin), val)
                elif output_type == 'R':
                    pin += 12
                    setattr(self.io_controller, 'ro' + str(pin), val)

                elif output_type == 'A':
                    setattr(self.io_controller, 'ao' + str(pin), val)
            elif ms:
                sleep(float(ms.groups()[0]))

        status = self.io_controller.status
        di_values = ''.join([str(status['di'][str(di)])
                             for di in range(1, 17)])
        do_values = ''.join([str(status['do'][str(do)])
                             for do in range(1, 13)])
        ro_values = ''.join([str(status['ro'][str(ro)])
                             for ro in range(13, 17)])
        ai_values = ''.join([str(status['ai'][str(int(ai))]).zfill(4)
                             for ai in range(1, 5)])
        ao_values = ''.join([str(status['ao'][str(int(ao))]).zfill(4)
                             for ao in range(1, 5)])
        temp = str(status['temperature'])
        r1 = ','.join((di_values, do_values + ro_values,
                       ai_values, ao_values, temp))
        return r1
