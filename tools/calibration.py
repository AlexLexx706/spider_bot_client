import spider_bot_client
from spider_bot_client import types
from spider_bot_client import errors
import math
import os
import argparse
import curses
import time
import threading


CALIB_NUM_FILE = 'calib_num.txt'
CALIBRATIONS_DATA = [
    {'address': 0, "min": -45, 'max': 45, "name": "front right leg 0 (servo 0)"},
    {'address': 1, "min": -90, 'max': 90, "name": "front right leg 1 (servo 1)"},
    {'address': 2, "min": 0, 'max': 100, "name": "front right leg 2 (servo 2)"},
    {'address': 3, "min": -45, 'max': 45, "name": "rear right leg 0 (servo 3)"},
    {'address': 4, "min": -90, 'max': 90, "name": "rear right leg 1 (servo 4)"},
    {'address': 5, "min": 0, 'max': 100, "name": "rear right leg 2 (servo 5)"},
    {'address': 6, "min": -45, 'max': 45, "name": "front left leg 0 (servo 6)"},
    {'address': 7, "min": -90, 'max': 90, "name": "front left leg 1 (servo 7)"},
    {'address': 8, "min": 0, 'max': 100, "name": "front left leg 2 (servo 8)"},
    {'address': 9, "min": -45, 'max': 45, "name": "rear left leg 0 (servo 9)"},
    {'address': 10, "min": -90, 'max': 90, "name": "rear left leg 1 (servo 10)"},
    {'address': 11, "min": 0, 'max': 100, "name": "rear left leg 2 (servo 11)"},
]


def menu(stdscr):
    """Process user startup dialog
        return: (first_servo_id, only_one, args)
    """
    parser = argparse.ArgumentParser(
        description='run calibration procedure of spider bot')
    parser.add_argument(
        '--host',
        help="spider bot server ip, default:%s" % (spider_bot_client.HOST, ),
        default=spider_bot_client.HOST)

    parser.add_argument(
        '--port',
        help="spider bot server port, default:%s" % (spider_bot_client.PORT, ),
        default=spider_bot_client.PORT)

    args = parser.parse_args()

    curses.echo()
    stdscr.addstr('Are you sure to start calibration, yes or not? ')
    cond = stdscr.getstr().decode('utf8').lower()
    if 'n' in cond:
        raise RuntimeError()

    only_one = False
    first = 0

    # calibrate only one servo
    stdscr.addstr('Do you want to calibrate a specific servo, yes or not? ')
    cond = stdscr.getstr().decode('utf8').lower()
    if 'y' in cond:
        while 1:
            try:
                stdscr.addstr('enter servo number: ')
                first = int(stdscr.getstr().decode('utf8').lower())
                if first >= 0 and first < types.SERVOS_COUNT:
                    only_one = True
                    break
            except ValueError:
                pass
            stdscr.addstr("Invalid value, try again 'y' or quit 'n'? ")
            cond = stdscr.getstr().decode('utf8').lower()
            if 'y' in cond:
                continue
            raise RuntimeError()

    # read last servo
    if not only_one:
        if os.path.isfile(CALIB_NUM_FILE):
            stdscr.addstr('Start from last bad calibration:type yes or no? ')
            cond = stdscr.getstr().decode('utf8').lower()
            if 'y' in cond.lower():
                try:
                    with open(CALIB_NUM_FILE, 'r') as file:
                        first = int(file.read())
                except FileNotFoundError as e:
                    print(e)
    curses.noecho()
    return first, only_one, args


def read_servo_state_proc(wnd):
    counter = 0
    while 1:
        wnd.addstr(0, 0, "counter:%s" % (counter, ))
        counter += 1
        wnd.refresh()
        time.sleep(1)


def main_proc(stdscr):
    try:
        first, only_one, args = menu(stdscr)
    except RuntimeError:
        return 1

    # split interface into 2 parts
    width = int(curses.COLS / 2)
    main_wnd = curses.newwin(curses.LINES, width, 0, 0)
    main_wnd.scrollok(True)

    # create wnd for read servo state
    servo_state_wnd = curses.newwin(curses.LINES, width, 0, width)
    thread = threading.Thread(
        target=read_servo_state_proc, args=(servo_state_wnd, ))
    thread.start()

    # 1. get model state
    client = spider_bot_client.Client(host=args.host, port=args.port)
    main_wnd.addstr("start calibration servos, first:%s\n" % (first, ))

    if first == 0:
        main_wnd.addstr('reset addresses:\n')
        main_wnd.getch()
        main_wnd.addstr("res:%s\n" % (
            client.manage_servo(
                types.ManageServoCmd.ResetAddressesCmd, 0, 0).error_desc, ))

    for index, calib_data in enumerate(CALIBRATIONS_DATA):
        if index < first:
            continue
        # save last servo num:
        with open('calib_num.txt', 'w') as file:
            file.write(str(index))

        addr = calib_data['address']
        main_wnd.addstr('set address:%s, %s:\n' % (addr, calib_data['name']))
        main_wnd.getch()
        main_wnd.addstr("res:%s\n" % (
            client.manage_servo(
                types.ManageServoCmd.SetAddressCmd, addr, 0).error_desc, ))

        main_wnd.addstr('start EnableReadAngles, %s:\n' % (calib_data['name'], ))
        main_wnd.getch()
        res = client.manage_servo(
            types.ManageServoCmd.EnableReadAngles,
            addr,
            0).error_desc
        main_wnd.addstr("res:%s\n" % (res, ))

        angle = calib_data['min']
        main_wnd.addstr('calibrate min, turn servo to angle:%s, %s:\n' % (
            angle, calib_data['name']))
        main_wnd.getch()

        res = client.manage_servo(
            types.ManageServoCmd.SetMinLimmitCmd,
            addr,
            angle / 180. * math.pi)
        main_wnd.addstr("res:%s\n" % (res.error_desc, ))

        if res.error != errors.NO_ERROR:
            return 1

        angle = calib_data['max']
        main_wnd.addstr('calibrate max, turn servo to angle:%s, %s:\n' % (
            angle, calib_data['name']))
        main_wnd.getch()
        res = client.manage_servo(
            types.ManageServoCmd.SetMaxLimmitCmd,
            addr,
            angle / 180.0 * math.pi)
        main_wnd.addstr("res:%s\n" % (res.error_desc, ))

        if res.error != errors.NO_ERROR:
            return 1

        # test servo calibration:
        main_wnd.addstr('test servo calibration, %s:\n' % (calib_data['name'], ))

        angle = calib_data['min']
        main_wnd.addstr('move servo %d to:%s angle, %s\n' % (
            addr, angle, calib_data['name']))
        main_wnd.getch()
        res = client.manage_servo(
            types.ManageServoCmd.MoveServo,
            addr,
            angle / 180.0 * math.pi).error_desc

        main_wnd.addstr("res:%s\n" % (res, ))

        angle = calib_data['max']
        main_wnd.addstr('move servo %s to:%s angle, %s\n' % (
            addr, angle, calib_data['name']))
        main_wnd.getch()
        res = client.manage_servo(
            types.ManageServoCmd.MoveServo,
            addr,
            angle / 180.0 * math.pi).error_desc

        main_wnd.addstr("res:%s\n" % (res, ))

    main_wnd.addstr('enable read angles:\n')
    main_wnd.getch()
    main_wnd.addstr(" res:%s\n" % (
        client.manage_servo(
            types.ManageServoCmd.EnableReadAngles,
            addr,
            0).error_desc, ))

    main_wnd.addstr('unload servo\n')
    res = client.manage_servo(
        types.ManageServoCmd.UnloadServosCmd,
        addr,
        angle).error_desc
    main_wnd.getch()
    main_wnd.addstr("res:%s\n" % (res, ))
    exit(0)


def main():
    exit(curses.wrapper(main_proc))


if __name__ == "__main__":
    main()
