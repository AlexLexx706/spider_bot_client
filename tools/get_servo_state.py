import spider_bot_client
import argparse


def main():
    parser = argparse.ArgumentParser(
        description='get servo state value')
    parser.add_argument(
        '--host',
        help="spider bot server ip, default:%s" % (spider_bot_client.HOST, ),
        default=spider_bot_client.HOST)

    parser.add_argument(
        '--port',
        help="spider bot server port, default:%s" % (spider_bot_client.PORT, ),
        default=spider_bot_client.PORT)

    parser.add_argument(
        'servo_id',
        help="servo id", type=int)

    args = parser.parse_args()

    client = spider_bot_client.Client(
        host=args.host, port=args.port)
    res = client.get_servo_state(args.servo_id)
    desc = res.desc
    print(
        "active:%s, calibrated:%s, min_servo:%s, min_angle:%s,"
        "max_servo:%s, max_angle:%s servo_angle:%s, model_angle:%s" % (
            desc.active, desc.calibrated,
            desc.min.servo_value, desc.min.model_value,
            desc.max.servo_value, desc.max.model_value,
            desc.servo_angle, desc.model_angle))


if __name__ == '__main__':
    main()
