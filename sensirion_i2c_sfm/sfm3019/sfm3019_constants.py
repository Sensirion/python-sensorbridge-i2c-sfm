from sensirion_i2c_sfm.sfm3019.commands import Sfm3019I2cCmdStartMeasO2, Sfm3019I2cCmdStartMeasAir, \
    Sfm3019I2cCmdStartMeasAirO2Mix

MeasurementModes = {
    'O2': Sfm3019I2cCmdStartMeasO2,
    'Air': Sfm3019I2cCmdStartMeasAir,
    'AirO2Mix': Sfm3019I2cCmdStartMeasAirO2Mix,
}

MeasurementCmds = {
    'O2': Sfm3019I2cCmdStartMeasO2.COMMAND,
    'Air': Sfm3019I2cCmdStartMeasAir.COMMAND,
    'AirO2Mix': Sfm3019I2cCmdStartMeasAirO2Mix.COMMAND,
}
