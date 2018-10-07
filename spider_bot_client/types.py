import ctypes

SERVOS_COUNT = 12

##############################################
class Header(ctypes.Structure):
    _fields_ = (
        ('cmd', ctypes.c_int32),
        ('resp_flag', ctypes.c_int32),
        ('size', ctypes.c_uint32))
    _pack_ = 1


class ResHeader(ctypes.Structure):
    _fields_ = (
        ('header', Header),
        ('error', ctypes.c_int32))
    _pack_ = 1


class LegGeometry(ctypes.Structure):
    _fields_ = (
        ('pos', ctypes.c_float * 3),
        ('shoulder_offset', ctypes.c_float),
        ('shoulder_lenght', ctypes.c_float),
        ('forearm_lenght', ctypes.c_float),)
    _pack_ = 1


class LegDesc(ctypes.Structure):
    _fields_ = (
        ('geometry', LegGeometry),
        ('a_0', ctypes.c_float),
        ('a_1', ctypes.c_float),
        ('a_2', ctypes.c_float),)
    _pack_ = 1


class GetStateRes(ctypes.Structure):
    _fields_ = (
        ('header', ResHeader),
        ('body_mat', ctypes.c_float * 16),
        ('front_right_leg', LegDesc),
        ('front_left_leg', LegDesc),
        ('rear_right_leg', LegDesc),
        ('rear_left_leg', LegDesc))
    _pack_ = 1


class SetActionCmd(ctypes.Structure):
    # actions types
    NOT_MOVE = 0
    MOVE_FORWARD = 1
    MOVE_BACKWARD = 2
    ROTATE_LEFT = 3
    ROTATE_RIGHT = 4

    _fields_ = (
        ('header', Header),
        ('action', ctypes.c_int32))
    _pack_ = 1


class AddNotifyCmd(ctypes.Structure):
    _fields_ = (
        ('header', Header),
        ('port', ctypes.c_uint16))
    _pack_ = 1


RmNotifyCmd = AddNotifyCmd


class ManageServoCmd(ctypes.Structure):
    _fields_ = (
        ('header', Header),
        ('cmd', ctypes.c_uint8),
        ('address', ctypes.c_uint8),
        ('limmit', ctypes.c_float),)
    _pack_ = 1

    #
    # broadcast address, used in EnableReadAngles for read all servos
    BroadcastAddr = 0xFE

    # commands enums
    NoneCmd = 0
    ResetAddressesCmd = 1
    SetAddressCmd = 2
    ResetLimmits = 3
    SetMinLimmitCmd = 4
    SetMaxLimmitCmd = 5
    LoadServosCmd = 6
    UnloadServosCmd = 7
    EnableSteringCmd = 8
    DisableSteringCmd = 9
    EnableReadAngles = 10
    DisableReadAngles = 11
    MoveServo = 12
    MoveServoSin = 13
    SetLedErrorCmd = 14


class ManageServoRes(ctypes.Structure):
    _fields_ = (
        ('header', Header),
        ('error', ctypes.c_int32),
        ('state', ctypes.c_int32))
    _pack_ = 1

    # states
    NoneState = 0
    ReadAnglesState = 1
    MoveSinState = 2
    CalibrationProgressState = 3
    CompleteState = 4
    ReadRawState = 5
    SterringsProgress = 6

    ErrorState = 7
    ErrorNotActive = 8
    ErrorWrongAddress = 9
    ErrorWrondData = 10
    ErrorWrongServoPos = 11
    ErrorNotCalibrated = 12

    state_map = {
        NoneState: "NoneState",
        ReadAnglesState: "ReadAnglesState",
        MoveSinState: "MoveSinState",
        CalibrationProgressState: "CalibrationProgressState",
        CompleteState: "CompleteState",
        ReadRawState: "ReadRawState",
        SterringsProgress: "SterringsProgress",
        ErrorState: "ErrorState",
        ErrorNotActive: "ErrorNotActive",
        ErrorWrongAddress: "ErrorWrongAddress",
        ErrorWrondData: "ErrorWrondData",
        ErrorWrongServoPos: "ErrorWrongServoPos",
        ErrorNotCalibrated: "ErrorNotCalibrated"}

    @property
    def error_desc(self):
        return "error:%s state:%s %s" % (
            self.error,
            self.state,
            self.state_map.get(self.state, "unknown state"))


class SetLegGeometry(ctypes.Structure):
    _fields_ = (
        ('header', Header),
        ('leg_num', ctypes.c_uint32),
        ('geometry', LegGeometry),)
    _pack_ = 1


class LimmitDesc(ctypes.Structure):
    _fields_ = (
        ('servo_value', ctypes.c_uint16),
        ('model_value', ctypes.c_float))


class ServoLinkDesc(ctypes.Structure):
    _fields_ = (
        ('active', ctypes.c_uint8),
        ('calibrated', ctypes.c_uint8),
        ('min', LimmitDesc),
        ('max', LimmitDesc),
        ('servo_angle', ctypes.c_uint16),
        ('model_angle', ctypes.c_float))


class GetServoStateCmd(ctypes.Structure):
    _fields_ = (
        ('header', Header),
        ('servo_id', ctypes.c_uint8))
    _pack_ = 1


class GetServoStateRes(ctypes.Structure):
    _fields_ = (
        ('header', ResHeader),
        ('servo_id', ctypes.c_uint8),
        ('desc', ServoLinkDesc))
    _pack_ = 1


print("sizeof(GetServoStateCmd):%s" % (ctypes.sizeof(GetServoStateCmd)))
print("sizeof(GetServoStateRes):%s" % (ctypes.sizeof(GetServoStateRes)))
print("sizeof(LimmitDesc):%s" % (ctypes.sizeof(LimmitDesc)))
print("sizeof(ServoLinkDesc):%s" % (ctypes.sizeof(ServoLinkDesc)))

