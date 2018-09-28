import spider_bot_client
from spider_bot_client import types


def main():
    client = spider_bot_client.Client()
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
