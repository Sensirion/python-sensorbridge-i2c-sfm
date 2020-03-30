# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function

from sensirion_sensorbridge_i2c_sfm.crc_calculator import CrcCalculator
from sensirion_sensorbridge_i2c_sfm.sensirion_word_command import SensirionWordI2cCommand


def int16(word):
    assert 0 <= word <= 0xFFFF, "Not an unsigned 16b word"
    if word & 0x8000:
        return word - 0x10000
    return word


class Sfm3019I2cCmdBase(SensirionWordI2cCommand):
    """
    SFM3019 I²C base command.
    """

    def __init__(self, command, tx_words, rx_length, read_delay, timeout):
        """
        Constructs a new SFM3019 I²C command.

        :param int/None command:
            The command word to be sent to the device. None means that no
            command will be sent, i.e. only ``tx_words`` (if not None) will
            be sent.
        :param list/None tx_words:
            Words (list of integers) to be sent to the I²C device. None means
            that no write header will be sent at all (if ``command`` is None
            too). An empty list means to send the write header (even if
            ``command`` is None), but without data following it.
        :param int/None rx_length:
            Number of bytes to be read from the I²C device, including CRC
            bytes. None means that no read header is sent at all. Zero means
            to send the read header, but without reading any data.
        :param float read_delay:
            Delay (in Seconds) to be inserted between the end of the write
            operation and the beginning of the read operation. This is needed
            if the device needs some time to prepare the RX data, e.g. if it
            has to perform a measurement. Set to 0.0 to indicate that no delay
            is needed, i.e. the device does not need any processing time.
        :param float timeout:
            Timeout (in Seconds) to be used in case of clock stretching. If the
            device stretches the clock longer than this value, the transceive
            operation will be aborted with a timeout error. Set to 0.0 to indicate
            that the device will not stretch the clock for this command.
        """
        super(Sfm3019I2cCmdBase, self).__init__(
            command=command,
            tx_words=tx_words,
            rx_length=rx_length,
            read_delay=read_delay,
            timeout=timeout,
            crc=CrcCalculator(8, 0x31, 0xFF),
            command_bytes=2,
        )


class Sfm3019I2cCmdReadProductIdentifierAndSerialNumber(Sfm3019I2cCmdBase):
    """
    SFM3019 I²C command "Read Product Identifier and Serial Number".
    """

    def __init__(self):
        """
        Constructs a new command.
        """
        super(Sfm3019I2cCmdReadProductIdentifierAndSerialNumber,
              self).__init__(command=0xE102,
                             tx_words=[],
                             rx_length=18,
                             read_delay=0,
                             timeout=0,
                             )

    """
    Interprets the raw response from the device and returns it in the proper data type.

    :param bytes data: Received raw bytes from the read operation.
    :return: Product identifier and serial number
    :rtype: tuple (int)
    """

    def interpret_response(self, data):
        words = Sfm3019I2cCmdBase.interpret_response(self, data)
        product_id = words[0] << 16 | words[1]
        serial_number = words[2] << 48 | words[3] << 32 | words[4] << 16 | words[5]
        return product_id, serial_number


class Sfm3019I2cCmdStartMeasO2(Sfm3019I2cCmdBase):
    """
    SFM3019 I²C command "Start continuous Measurement of O2"
    """

    COMMAND = 0x3603

    def __init__(self):
        """
        Constructs a new command.
        """
        super(Sfm3019I2cCmdStartMeasO2, self).__init__(
            command=Sfm3019I2cCmdStartMeasO2.COMMAND,
            tx_words=[],
            rx_length=None,
            read_delay=0.012,
            timeout=0,
        )


class Sfm3019I2cCmdStartMeasAir(Sfm3019I2cCmdBase):
    """
    SFM3019 I²C command "Start continuous Measurement of Air"
    """

    COMMAND = 0x3608

    def __init__(self):
        """
        Constructs a new command.
        """
        super(Sfm3019I2cCmdStartMeasAir, self).__init__(
            command=Sfm3019I2cCmdStartMeasAir.COMMAND,
            tx_words=[],
            rx_length=None,
            read_delay=0.012,
            timeout=0,
        )


class Sfm3019I2cCmdStartMeasAirO2Mix(Sfm3019I2cCmdBase):
    """
    SFM3019 I²C command "Start continuous Measurement of Air/O2 with Volume
    fraction of O2 (in ‰)"
    """

    COMMAND = 0x3632

    def __init__(self, o2_volume_fraction_in_permille):
        """
        Constructs a new command.
        """
        if not (0 <= o2_volume_fraction_in_permille <= 1000):
            raise ValueError("O2 volume fraction not in valid range 0-1000")

        super(Sfm3019I2cCmdStartMeasAirO2Mix, self).__init__(
            command=Sfm3019I2cCmdStartMeasAirO2Mix.COMMAND,
            tx_words=[o2_volume_fraction_in_permille],
            rx_length=None,
            read_delay=0.012,
            timeout=0,
        )


class Sfm3019I2cCmdReadMeas(Sfm3019I2cCmdBase):
    """
    SFM3019 I²C command "Read continuous measurement"
    """

    def __init__(self):
        """
        Constructs a new command.
        """
        super(Sfm3019I2cCmdReadMeas, self).__init__(
            command=None,
            tx_words=None,
            rx_length=6,
            read_delay=0,
            timeout=0,
        )

    """
    Interprets the raw response from the device and returns it in the proper data type.

    :param bytes data: Received raw bytes from the read operation.
    :return: Flow raw ADC value and temperature raw ADC value
    :rtype: tuple (int)
    """

    def interpret_response(self, data):
        words = Sfm3019I2cCmdBase.interpret_response(self, data)
        return int16(words[0]), int16(words[1])


class Sfm3019I2cCmdStopMeas(Sfm3019I2cCmdBase):
    """
    SFM3019 I²C command "Stop continuous measurements"
    """

    def __init__(self):
        """
        Constructs a new command.
        """
        super(Sfm3019I2cCmdStopMeas, self).__init__(
            command=0x3FF9,
            tx_words=[],
            rx_length=None,
            read_delay=0.0005,
            timeout=0,
        )


class Sfm3019I2cCmdGetUnitAndFactors(Sfm3019I2cCmdBase):
    """
    SFM3019 I²C command "Get the currently set scale factor and unit for the
    defined measurement mode"
    """

    def __init__(self, measure_cmd):
        """
        Constructs a new command.
        """
        super(Sfm3019I2cCmdGetUnitAndFactors, self).__init__(
            command=0x3661,
            tx_words=[measure_cmd],
            rx_length=9,
            read_delay=0.0005,
            timeout=0,
        )

    """
    Interprets the raw response from the device and returns it in the proper data type.

    :param bytes data: Received raw bytes from the read operation.
    :return: Flow scale factor, offset and unit according to datasheet
    :rtype: triple (float, float, int)
    """

    def interpret_response(self, data):
        words = Sfm3019I2cCmdBase.interpret_response(self, data)
        return float(int16(words[0])), float(int16(words[1])), int16(words[2])
