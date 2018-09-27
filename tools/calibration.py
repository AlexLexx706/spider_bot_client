import spider_bot_client
from spider_bot_client import types
from spider_bot_client import errors
import math


def main():
    client = spider_bot_client.Client()
    cond = input('Start from last bad calibration:type yes or no?')
    first = 0
    if 'y' in cond.lower():
        try:
            with open('calib_num.txt', 'r') as file:
                first = int(file.read())
        except FileNotFoundError as e:
            print(e)

    calibrations_data = [
        {'address': 0, "min": -45, 'max': 45, "name": "front right leg 0"},
        {'address': 1, "min": -90, 'max': 90, "name": "front right leg 1"},
        {'address': 2, "min": 0, 'max': 100, "name": "front right leg 2"},
        {'address': 3, "min": -45, 'max': 45, "name": "rear right leg 0"},
        {'address': 4, "min": -90, 'max': 90, "name": "rear right leg 1"},
        {'address': 5, "min": 0, 'max': 100, "name": "rear right leg 2"},
        {'address': 6, "min": -45, 'max': 45, "name": "front left leg 0"},
        {'address': 7, "min": -90, 'max': 90, "name": "front left leg 1"},
        {'address': 8, "min": 0, 'max': 100, "name": "front left leg 2"},
        {'address': 9, "min": -45, 'max': 45, "name": "rear left leg 0"},
        {'address': 10, "min": -90, 'max': 90, "name": "rear left leg 1"},
        {'address': 11, "min": 0, 'max': 100, "name": "rear left leg 2"},
    ]
    # 1. get model state
    print("start calibration servos, first:%s" % (first, ))

    if first == 0:
        input('reset addresses:')
        print("res:%s\n" % (
            client.manage_servo(
                types.ManageServocmds.ResetAddressesCmd, 0, 0).error_desc, ))

    for index, calib_data in enumerate(calibrations_data):
        if index < first:
            continue
        # save last servo num:
        with open('calib_num.txt', 'w') as file:
            file.write(str(index))

        addr = calib_data['address']
        input('set address:%s, %s:' % (addr, calib_data['name']))
        print("res:%s\n" % (
            client.manage_servo(
                types.ManageServocmds.SetAddressCmd, addr, 0).error_desc, ))

        input('start EnableReadAngles, %s:' % (calib_data['name'], ))
        res = client.manage_servo(
            types.ManageServocmds.EnableReadAngles,
            addr,
            0).error_desc
        print("res:%s\n" % (res, ))

        angle = calib_data['min']
        input('calibrate min, turn servo to angle:%s, %s:' % (
            angle, calib_data['name']))
        res = client.manage_servo(
            types.ManageServocmds.SetMinLimmitCmd,
            addr,
            angle / 180. * math.pi)
        print("res:%s\n" % (res.error_desc, ))

        if res.error != errors.NO_ERROR:
            return

        angle = calib_data['max']
        input('calibrate max, turn servo to angle:%s, %s:' % (
            angle, calib_data['name']))
        res = client.manage_servo(
            types.ManageServocmds.SetMaxLimmitCmd,
            addr,
            angle / 180.0 * math.pi)
        print("res:%s\n" % (res.error_desc, ))

        if res.error != errors.NO_ERROR:
            return

        # test servo calibration:
        print('test servo calibration, %s:' % (calib_data['name'], ))

        angle = calib_data['min']
        input('move servo %d to:%s angle, %s' % (
            addr, angle, calib_data['name']))
        res = client.manage_servo(
            types.ManageServocmds.MoveServo,
            addr,
            angle / 180.0 * math.pi).error_desc

        print("res:%s\n" % (res, ))

        angle = calib_data['max']
        input('move servo %s to:%s angle, %s' % (
            addr, angle, calib_data['name']))
        res = client.manage_servo(
            types.ManageServocmds.MoveServo,
            addr,
            angle / 180.0 * math.pi).error_desc

        print("res:%s\n" % (res, ))

    input('enable read angles:')
    print(" res:%s" % (
        client.manage_servo(
            types.ManageServocmds.EnableReadAngles,
            addr,
            0).error_desc, ))

    input('unload servo')
    res = client.manage_servo(
        types.ManageServocmds.UnloadServosCmd,
        addr,
        angle).error_desc

    print("res:%s" % (res, ))
