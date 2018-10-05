import spider_bot_client
from spider_bot_client import types
import argparse


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

    input('start EnableReadAngles:')
    print("res:%s" % (client.manage_servo(
        types.ManageServoCmd.EnableReadAngles,
        types.ManageServoCmd.BroadcastAddr,
        0).error, ))


if __name__ == "__main__":
    main()
