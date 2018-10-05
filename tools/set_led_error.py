import spider_bot_client
from spider_bot_client import types
import argparse

ERROR_MAP = {
    0: 'No alarm',
    1: 'Over temperature',
    2: 'Over voltage',
    3: 'Over temperature and over voltage',
    4: 'Locked-rotor',
    5: 'Over temperature and stalled',
    6: 'Over voltage and stalled',
    7: 'Over temperature, over voltage and stalled'}


def main():
    parser = argparse.ArgumentParser(
        description='set led error for all servos, '
        'user can understand error type by led blinking')
    parser.add_argument(
        '--host',
        help="spider bot server ip, default:%s" % (spider_bot_client.HOST, ),
        default=spider_bot_client.HOST)

    parser.add_argument(
        '--port',
        help="spider bot server port, default:%s" % (spider_bot_client.PORT, ),
        default=spider_bot_client.PORT)

    parser.add_argument(
        'error',
        type=int,
        help="led error type, can be:\n%s" % (
            '; '.join(['%s - %s' % (k, d) for k, d in ERROR_MAP.items()]), ))

    args = parser.parse_args()
    print('check error:%s desc:%s' % (args.error, ERROR_MAP[args.error]))

    client = spider_bot_client.Client(host=args.host, port=args.port)
    res = client.manage_servo(
        types.ManageServoCmd.SetLedErrorCmd,
        0,
        args.error).error
    print("res:%s" % (res, ))


if __name__ == '__main__':
    main()
