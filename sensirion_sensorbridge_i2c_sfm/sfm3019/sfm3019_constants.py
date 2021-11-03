from enum import Enum


class MeasurementMode(Enum):
    O2 = 0,
    Air = 1,
    AirO2Mix = 2,


SFM3019_DEFAULT_I2C_FREQUENCY = 400e3
SFM3019_DEFAULT_VOLTAGE = 3.3

FLOW_UNIT_PREFIX = {
    3: 'n',
    4: 'u',
    5: 'm',
    6: 'c',
    7: 'd',
    8: '',
    9: 'd',
    10: 'h',
    11: 'K',
    12: 'M',
    13: 'G',
}

FLOW_UNIT = {
    0: 'sl(0)',
    1: 'sl(20)',
    2: 'sl(15)',
    3: 'sl(25)',
    8: 'l',
    9: 'g',
}

FLOW_TIME_BASE = {
    0: '',
    1: '/us',
    2: '/ms',
    3: '/s',
    4: '/min',
    5: '/h',
    6: '/d',
}
