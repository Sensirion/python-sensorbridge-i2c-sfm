# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function

from .commands import Sfm3019I2cCmdReadMeas, \
    Sfm3019I2cCmdReadProductIdentifierAndSerialNumber, \
    Sfm3019I2cCmdStartMeasAir, Sfm3019I2cCmdStartMeasAirO2Mix, \
    Sfm3019I2cCmdStartMeasO2, Sfm3019I2cCmdStopMeas, \
    Sfm3019I2cCmdGetUnitAndFactors
from .sfm3019_constants import MeasurementMode, FLOW_UNIT_PREFIX, FLOW_UNIT, FLOW_TIME_BASE


class Sfm3019I2cSensorBridgeDevice:
    """
    SFM3019 I²C device class to allow executing I²C commands via Sensirion's SensorBridge.
    """

    MeasurementCmds = {
        MeasurementMode.O2: Sfm3019I2cCmdStartMeasO2,
        MeasurementMode.Air: Sfm3019I2cCmdStartMeasAir,
        MeasurementMode.AirO2Mix: Sfm3019I2cCmdStartMeasAirO2Mix,
    }

    def __init__(self, sensor_bridge, sensor_bridge_port, slave_address=0x2E):
        """
        Constructs a new SFM3019 I²C device.

        :param ~sensirion_shdlc_sensorbridge.device.SensorBridgeShdlcDevice sensor_bridge:
            The I²C SHDLC SensorBridge connection to use for communication.
        :param int sensor_bridge_port:
            The port on the SensorBridge which the sensor is connected to.
        :param byte slave_address:
            The I²C slave address, defaults to 0x2E.
        """
        self._sensor_bridge = sensor_bridge
        self._sensor_bridge_port = sensor_bridge_port
        self._slave_address = slave_address

        self._flow_scale_factor = None
        self._flow_offset = None
        self._flow_unit = None

    def _execute(self, command):
        """
        Perform read and write operations of an I²C command.
        :param ~SensirionWordI2cCommand command:
            The command to execute.
        :return:
            - In single channel mode: The interpreted data of the command.
            - In multi-channel mode: A list containing either interpreted data
              of the command (on success) or an Exception object (on error)
              for every channel.
        :raise:
            In single-channel mode, an exception is raised in case of
            communication errors.
        """
        # SensorBridge does not support a read delay, but it automatically
        # retries reading data until the timeout is elapsed. Thus we can just
        # use the read delay as timeout (resp. whichever is greater).
        total_timeout_us = max(command.read_delay, command.timeout) * 1e6
        tx_data = command.tx_data or b""
        rx_length = command.rx_length or 0
        response = self._sensor_bridge.transceive_i2c(self._sensor_bridge_port,
                                                      address=self._slave_address,
                                                      tx_data=tx_data,
                                                      rx_length=rx_length,
                                                      timeout_us=total_timeout_us,
                                                      )
        return command.interpret_response(response)

    def _get_factors_and_unit(self, measure_mode):
        """
        Read the sensor programmed scale factor and the set unit
        :param MeasurementMode measure_mode:
            Current measurement mode used to perform measurements.
        :return:
          - The flow scale factor and offset as floats
          - The flow unit as int
        :rtype:
            triple
        """
        return self._execute(Sfm3019I2cCmdGetUnitAndFactors(self.MeasurementCmds[measure_mode].COMMAND))

    def _convert_measurement_data(self, params):
        """Apply offset and scaling to measurement data"""
        return (float(params[0]) - self._flow_offset) / self._flow_scale_factor, float(params[1] / 200.)

    @property
    def flow_unit(self):
        """
        :return: The flow unit as a string according to datasheet
        :rtype: str
        """
        unit = FLOW_UNIT[self._flow_unit >> 8 & 0xf]
        time = FLOW_TIME_BASE[self._flow_unit >> 4 & 0xf]
        prefix = FLOW_UNIT_PREFIX[self._flow_unit & 0xf]

        return "{}{}{}".format(prefix, unit, time)

    def initialize_sensor(self, measure_mode):
        """
        Stop any running continuous measurement that may execute on the sensor
        and read out some sensor parameters.

        Needs to be done before any measurement call is executed.
        """
        self.stop_continuous_measurement()
        self._flow_scale_factor, self._flow_offset, self._flow_unit = self._get_factors_and_unit(measure_mode)

    def read_product_identifier_and_serial_number(self):
        """
        Read the product identifier and serial number.

        :return:
            The product identifier (4b) and serial number (12b), both formatted
            as decimal number (int).
        :rtype:
            tuple
        """
        return self._execute(Sfm3019I2cCmdReadProductIdentifierAndSerialNumber())

    def start_continuous_measurement(self, measure_mode=MeasurementMode.Air,
                                     air_o2_mix_fraction_permille=None):
        """
        Start a continuous measurement with the specified gas

        :param MeasurementMode measure_mode:
            Configure the type of measurement to perform. Check the datasheet
            for more information.
        :param int air_o2_mix_fraction_permille:
            Fraction (in permille 0-1000) of O2 contained in the Air/O2 Mix.
            This parameter is only used when measure_mode is 'AirO2Mix'.
        """
        if measure_mode == MeasurementMode.AirO2Mix:
            cmd = self.MeasurementCmds[measure_mode]
            return self._execute(cmd(air_o2_mix_fraction_permille))

        return self._execute(self.MeasurementCmds[measure_mode]())

    def stop_continuous_measurement(self):
        return self._execute(Sfm3019I2cCmdStopMeas())

    def read_continuous_measurement(self):
        """
        Read a single measurement from the running measurement

        :return:
            The measured flow and temperature

            - flow (float) -
              flow in unit specified by sensor.
            - temperature (float) -
              Temperature in degree C.
        :rtype:
            tuple
        """
        return self._convert_measurement_data(self._execute(Sfm3019I2cCmdReadMeas()))
