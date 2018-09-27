import spider_bot_client
from spider_bot_client import types


def main():
    client = spider_bot_client.Client()
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
