import spider_bot_client
from spider_bot_client import types
import argparse
import time


def main():
    parser = argparse.ArgumentParser(
        description='send command read angles to spider bot')
    parser.add_argument(
        '--host',
        help="spider bot server ip, default:%s" % (spider_bot_client.HOST, ),
        default=spider_bot_client.HOST)

    parser.add_argument(
        '--port',
        help="spider bot server port, default:%s" % (spider_bot_client.PORT, ),
        default=spider_bot_client.PORT)

    parser.add_argument(
        '--timeout',
        help="read timout",
        type=float,
        default=0.3)

    parser.add_argument(
        '--servo_id',
        help="servio id number, default: 0",
        type=int,
        default=0)

    args = parser.parse_args()

    client = spider_bot_client.Client(host=args.host, port=args.port)
    addr = 0
    input('unload servo')

    addr = 2
    res = client.manage_servo(
        types.ManageServoCmd.UnloadServosCmd,
        addr,
        0).error
    print("res:%s" % (res, ))

    input('start read servo state:')
    print("res:%s" % (client.manage_servo(
        types.ManageServoCmd.EnableReadAngles,
        types.ManageServoCmd.BroadcastAddr,
        0).error, ))

    try:
        while 1:
            res = client.get_servo_state(args.servo_id)
            print(
                "id:%s "
                "active:%s "
                "calibrated:%s "
                "min:(servo:%s angle:%s)"
                "max:(servo:%s angle:%s)"
                "servo:%s "
                "angle:%s " % (
                    res.servo_id,
                    res.desc.active,
                    res.desc.calibrated,
                    res.desc.min.servo_value, res.desc.min.model_value,
                    res.desc.max.servo_value, res.desc.max.model_value,
                    res.desc.servo_angle,
                    res.desc.model_angle))
            time.sleep(args.timeout)
    except KeyboardInterrupt:
        pass
    exit(0)


if __name__ == "__main__":
    main()
