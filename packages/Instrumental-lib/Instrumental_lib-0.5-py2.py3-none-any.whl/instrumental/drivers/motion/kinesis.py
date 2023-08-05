# -*- coding: utf-8 -*-
# Copyright 2016-2018 Christopher Rogers, Dodd Gray, and Nate Bogdanowicz
"""
Driver for controlling Thorlabs Kinesis devices. Currently only directs the K10CR1 rotation stage.
"""
from __future__ import division
from enum import Enum
from nicelib import NiceLib, Sig, NiceObject, load_lib, RetHandler, ret_return, ret_ignore

from . import Motion
from .. import ParamSet
from ..util import check_units
from ... import u
from ...log import get_logger
from ...util import to_str

log = get_logger(__name__)

__all__ = ['K10CR1']


# Message Enums
#
class MessageType(Enum):
    GenericDevice = 0
    GenericPiezo = 1
    GenericMotor = 2
    GenericDCMotor = 3
    GenericSimpleMotor = 4
    RackDevice = 5
    Laser = 6
    TECCtlr = 7
    Quad = 8
    NanoTrak = 9
    Specialized = 10
    Solenoid = 11


class GenericDevice(Enum):
    SettingsInitialized = 0
    SettingsUpdated = 1
    Error = 2
    Close = 3


class GenericMotor(Enum):
    Homed = 0
    Moved = 1
    Stopped = 2
    LimitUpdated = 3


class GenericDCMotor(Enum):
    Error = 0
    Status = 1


MessageIDs = {
    MessageType.GenericDevice: GenericDevice,
    MessageType.GenericMotor: GenericMotor,
    MessageType.GenericDCMotor: GenericDCMotor
}


def list_instruments():
    NiceKinesisISC.BuildDeviceList()
    serial_nums = to_str(NiceKinesisISC.GetDeviceListExt()).split(',')
    return [ParamSet(K10CR1, serial=serial)
            for serial in serial_nums
            if serial]


class KinesisError(Exception):
    messages = {
        0: 'Success',
        1: 'The FTDI functions have not been initialized',
        2: 'The device could not be found. Make sure to call TLI_BuildDeviceList().',
        3: 'The device must be opened before it can be accessed',
        4: 'An I/O Error has occured in the FTDI chip',
        5: 'There are insufficient resources to run this application',
        6: 'An invalid parameter has been supplied to the device',
        7: 'The device is no longer present',
        8: 'The device detected does not match that expected',
        32: 'The device is already open',
        33: 'The device has stopped responding',
        34: 'This function has not been implemented',
        35: 'The device has reported a fault',
        36: 'The function could not be completed because the device is disconnected',
        41: 'The firmware has thrown an error',
        42: 'The device has failed to initialize',
        43: 'An invalid channel address was supplied',
        37: 'The device cannot perform this function until it has been Homed',
        38: 'The function cannot be performed as it would result in an illegal position',
        39: 'An invalid velocity parameter was supplied. The velocity must be greater than zero',
        44: 'This device does not support Homing. Check the Limit switch parameters are correct',
        45: 'An invalid jog mode was supplied for the jog function',
    }

    def __init__(self, code=None, msg=''):
        if code is not None and not msg:
            msg = '(0x{:X}) {}'.format(code, self.messages[code])
        super(KinesisError, self).__init__(msg)
        self.code = code


@RetHandler(num_retvals=0)
def ret_errcheck(ret):
    if ret != 0:
        raise KinesisError(ret)


@RetHandler(num_retvals=0)
def ret_success(ret, funcname):
    if not ret:
        raise KinesisError(msg="Call to function '{}' failed".format(funcname))


class NiceKinesisISC(NiceLib):
    """Mid-level wrapper for Thorlabs.MotionControl.IntegratedStepperMotors.dll"""
    _info_ = load_lib('kinesis', __package__)
    _prefix_ = 'TLI_'
    _ret_ = ret_errcheck

    BuildDeviceList = Sig()
    GetDeviceListSize = Sig(ret=ret_return)
    GetDeviceListExt = Sig('buf', 'len')
    GetDeviceListByTypeExt = Sig('buf', 'len', 'in')
    GetDeviceListByTypesExt = Sig('buf', 'len', 'in', 'in')
    GetDeviceInfo = Sig('in', 'out')

    # GetDeviceList = Sig('out')
    # GetDeviceListByType = Sig('out', 'in', dict(first_arg=False))
    # GetDeviceListByTypes = Sig('out', 'in', 'in', dict(first_arg=False))

    class Device(NiceObject):
        _prefix_ = 'ISC_'

        Open = Sig('in')
        Close = Sig('in', ret=ret_return)
        Identify = Sig('in', ret=ret_ignore)
        GetHardwareInfo = Sig('in', 'buf', 'len', 'out', 'out', 'buf', 'len', 'out', 'out', 'out')
        GetFirmwareVersion = Sig('in', ret=ret_return)
        GetSoftwareVersion = Sig('in', ret=ret_return)
        LoadSettings = Sig('in', ret=ret_success)
        PersistSettings = Sig('in', ret=ret_success)
        GetNumberPositions = Sig('in', ret=ret_return)
        CanHome = Sig('in', ret=ret_return)
        Home = Sig('in')
        NeedsHoming = Sig('in', ret=ret_return)
        MoveToPosition = Sig('in', 'in')
        GetPosition = Sig('in', ret=ret_return)
        GetPositionCounter = Sig('in', ret=ret_return)
        RequestStatus = Sig('in')
        RequestStatusBits = Sig('in')
        GetStatusBits = Sig('in', ret=ret_return)
        StartPolling = Sig('in', 'in', ret=ret_success)
        PollingDuration = Sig('in', ret=ret_return)
        StopPolling = Sig('in', ret=ret_ignore)
        RequestSettings = Sig('in')
        ClearMessageQueue = Sig('in', ret=ret_ignore)
        RegisterMessageCallback = Sig('in', 'in', ret=ret_ignore)
        MessageQueueSize = Sig('in', ret=ret_return)
        GetNextMessage = Sig('in', 'out', 'out', 'out', ret=ret_success)
        WaitForMessage = Sig('in', 'out', 'out', 'out', ret=ret_success)
        GetMotorParamsExt = Sig('in', 'out', 'out', 'out')
        SetJogStepSize = Sig('in', 'in')
        GetJogVelParams = Sig('in', 'out', 'out')
        GetBacklash = Sig('in', ret=ret_return)
        SetBacklash = Sig('in', 'in')
        GetLimitSwitchParams = Sig('in', 'out', 'out', 'out', 'out', 'out')
        GetLimitSwitchParamsBlock = Sig('in', 'out')


STATUS_MOVING_CW = 0x10
STATUS_MOVING_CCW = 0x20
STATUS_JOGGING_CW = 0x40
STATUS_JOGGING_CCW = 0x80


class K10CR1(Motion):
    """ Class for controlling Thorlabs K10CR1 integrated stepper rotation stages

    Takes the serial number of the device as a string as well as the gear box ratio,
    steps per revolution and microsteps per step as integers. It also takes the polling
    period as a pint quantity.

    The polling period, which is how often the device updates its status, is
    passed as a pint pint quantity with units of time and is optional argument,
    with a default of 200ms
    """
    _INST_PARAMS_ = ['serial']

    _lib = NiceKinesisISC

    # Enums
    MessageType = MessageType
    GenericDevice = GenericDevice
    GenericMotor = GenericMotor
    GenericDCMotor = GenericDCMotor

    @check_units(polling_period='ms')
    def _initialize(self, gear_box_ratio=120, steps_per_rev=200, micro_steps_per_step=2048,
                    polling_period='200ms'):
        offset = self._paramset.get('offset', '0 deg')

        self.serial = self._paramset['serial']
        self.offset = offset
        self._unit_scaling = (gear_box_ratio * micro_steps_per_step *
                              steps_per_rev / (360.0 * u.deg))
        self._open()
        self._start_polling(polling_period)
        self._wait_for_message(GenericDevice.SettingsInitialized)

    def _open(self):
        NiceKinesisISC.BuildDeviceList()  # Necessary?
        self.dev = NiceKinesisISC.Device(self.serial)
        self.dev.Open()

    def close(self):
        self.dev.StopPolling()
        self.dev.Close()

    @check_units(polling_period='ms')
    def _start_polling(self, polling_period='200ms'):
        """Starts polling the device to update its status with the given period provided, rounded
        to the nearest millisecond

        Parameters
        ----------
        polling_period: pint quantity with units of time
        """
        self.polling_period = polling_period
        self.dev.StartPolling(self.polling_period.m_as('ms'))

    @check_units(angle='deg')
    def move_to(self, angle, wait=False):
        """Rotate the stage to the given angle

        Parameters
        ----------
        angle : Quantity
            Angle that the stage will rotate to. Takes the stage offset into account.
        """
        log.debug("Moving stage to {}".format(angle))
        log.debug("Current position is {}".format(self.position))
        self.dev.ClearMessageQueue()
        self.dev.MoveToPosition(self._to_dev_units(angle + self.offset))
        if wait:
            self.wait_for_move()

    def _decode_message(self, msg_tup):
        msg_type_int, msg_id_int, msg_data_int = msg_tup
        msg_type = MessageType(msg_type_int)
        msg_id = MessageIDs[msg_type](msg_id_int)
        return (msg_id, msg_data_int)

    def _wait_for_message(self, match_id):
        if not isinstance(match_id, (GenericDevice, GenericMotor, GenericDCMotor)):
            raise ValueError("Must specify message ID via enum")

        msg_id, msg_data = self._decode_message(self.dev.WaitForMessage())
        log.debug("Received kinesis message ({}: {})".format(msg_id, msg_data))
        while msg_id is not match_id:
            msg_id, msg_data = self._decode_message(self.dev.WaitForMessage())
            log.debug("Received kinesis message ({}: {})".format(msg_id, msg_data))

    def _check_for_message(self, match_id):
        """Check if a message of the given type and id is in the queue"""
        if not isinstance(match_id, (GenericDevice, GenericMotor, GenericDCMotor)):
            raise ValueError("Must specify message ID via enum")

        while True:
            try:
                msg_id, msg_data = self._decode_message(self.dev.GetNextMessage())
            except KinesisError:
                return False

            log.debug("Received kinesis message ({}: {})".format(msg_id, msg_data))
            if msg_id is match_id:
                return True

    def wait_for_move(self):
        """Wait for the most recent move to complete"""
        self._wait_for_message(GenericMotor.Moved)

    def move_finished(self):
        """Check if the most recent move has finished"""
        return self._check_for_message(GenericMotor.Moved)

    def _to_real_units(self, dev_units):
        return (dev_units / self._unit_scaling).to('deg')

    @check_units(real_units='deg')
    def _to_dev_units(self, real_units):
        return int(round(float(real_units * self._unit_scaling)))

    def home(self, wait=False):
        """Home the stage

        Parameters
        ----------
        wait : bool, optional
            Wait until the stage has finished homing to return
        """
        self.dev.ClearMessageQueue()
        self.dev.Home()

        if wait:
            self.wait_for_home()

    def wait_for_home(self):
        """Wait for the most recent homing operation to complete"""
        self._wait_for_message(GenericMotor.Homed)

    def homing_finished(self):
        """Check if the most recent homing operation has finished"""
        return self._check_for_message(GenericMotor.Homed)

    @property
    def needs_homing(self):
        """True if the device needs to be homed before a move can be performed"""
        return bool(self.dev.NeedsHoming())

    @property
    def offset(self):
        return self._offset

    @offset.setter
    @check_units(offset='deg')
    def offset(self, offset):
        self._offset = offset

    @property
    def position(self):
        return self._to_real_units(self.dev.GetPosition()) - self.offset

    @property
    def is_homing(self):
        return bool(self.dev.GetStatusBits() & 0x00000200)

    @property
    def is_moving(self):
        return bool(self.dev.GetStatusBits() & 0x00000030)

    def get_next_message(self):
        msg_type, msg_id, msg_data = self.dev.GetNextMessage()
        type = MessageType(msg_type)
        id = MessageIDs[type](msg_id)
        return (type, id, msg_data)

    def get_messages(self):
        messages = []
        while True:
            try:
                messages.append(self.get_next_message())
            except Exception:
                break
        return messages
