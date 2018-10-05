import spider_bot_client
import argparse
from spider_bot_client import types


def main():
    parser = argparse.ArgumentParser(
        description='test tool for setup new geometry of spider bot')
    parser.add_argument(
        '--host',
        help="spider bot server ip, default:%s" % (spider_bot_client.HOST, ),
        default=spider_bot_client.HOST)

    parser.add_argument(
        '--port',
        help="spider bot server port, default:%s" % (spider_bot_client.PORT, ),
        default=spider_bot_client.PORT)

    args = parser.parse_args()

    client = spider_bot_client.Client(
        host=args.host, port=args.port)

    input('get bot state:')
    res = client.get_state()
    print("res:%s" % (res.header.error, ))

    if (res.header.error != types.NO_ERROR):
        return

    geometry = res.front_right_leg.geometry

    print(
        "geometry: pos:%s shoulder_offset:%s "
        "shoulder_lenght:%s forearm_lenght:%s" % (
            [v for v in geometry.pos],
            geometry.shoulder_offset,
            geometry.shoulder_lenght,
            geometry.forearm_lenght))

    # length in santimetrs
    shoulder_offset = 8
    shoulder_lenght = 8
    forearm_lenght = 4

    legs_geometry = [
        types.LegGeometry(
            (types.ctypes.c_float * 3)(10, -2, 5),
            shoulder_offset,
            shoulder_lenght,
            forearm_lenght),
        types.LegGeometry(
            (types.ctypes.c_float * 3)(-10, -2, 5),
            shoulder_offset,
            shoulder_lenght,
            forearm_lenght),
        types.LegGeometry(
            (types.ctypes.c_float * 3)(10, -2, -5),
            shoulder_offset,
            shoulder_lenght,
            forearm_lenght),
        types.LegGeometry(
            (types.ctypes.c_float * 3)(-10, -2, -5),
            shoulder_offset,
            shoulder_lenght,
            forearm_lenght)
    ]
    input('set legs geometry:')
    for leg_num, leg_geometry in enumerate(legs_geometry):
        print("set_leg geometry leg_num:%s res:%s" % (
            leg_num,
            client.set_leg_geometry(leg_num, leg_geometry).error))


if __name__ == '__main__':
    main()
