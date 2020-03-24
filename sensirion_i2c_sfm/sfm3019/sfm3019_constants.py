from enum import Enum


class MeasurementMode(Enum):
    O2 = 0,
    Air = 1,
    AirO2Mix = 2,


flow_unit_prefix = {3: 'n',
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

flow_unit = {0: 'sl(0)',
             1: 'sl(20)',
             2: 'sl(15)',
             3: 'sl(25)',
             8: 'l',
             9: 'g',
             }

flow_time_base = {0: '',
                  1: '/us',
                  2: '/ms',
                  3: '/s',
                  4: '/min',
                  5: '/h',
                  6: '/d',
                  }
