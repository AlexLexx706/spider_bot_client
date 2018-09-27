import spider_bot_client
from spider_bot_client import types


def test_set_leg_geometry():
    client = spider_bot_client.Client()
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
