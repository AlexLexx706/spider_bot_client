import argparse
import spider_bot_client
from spider_bot_client import types


def main():
    parser = argparse.ArgumentParser(
        description='send command enable_sterring to spider bot')
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
    input('unload servo')

    addr = 0
    client.manage_servo(
        types.ManageServoCmd.UnloadServosCmd,
        addr,
        0,
        get_responce=False)

    input('enable sterring:')
    client.manage_servo(
        types.ManageServoCmd.EnableSteringCmd,
        addr,
        0,
        get_responce=False)


if __name__ == "__main__":
    main()
