Quick Start
===========

SensorBridge Example
--------------------

Following example code shows how to use this driver with a Sensirion SFM3019
connected to the computer using a `Sensirion SEK-SensorBridge`_. The driver
for the SensorBridge can be installed with
``pip install sensirion-shdlc-sensorbridge``.


.. sourcecode:: python

    import time
    from sensirion_shdlc_driver import ShdlcSerialPort, ShdlcConnection
    from sensirion_shdlc_sensorbridge import SensorBridgePort, \
        SensorBridgeShdlcDevice, SensorBridgeI2cProxy
    from sensirion_i2c_driver import I2cConnection
    from sensirion_i2c_sfm.sfm3019 import Sfm3019I2cDevice

    # Connect to the SensorBridge with default settings:
    #  - baudrate:      460800
    #  - slave address: 0
    with ShdlcSerialPort(port='COM1', baudrate=460800) as port:
        bridge = SensorBridgeShdlcDevice(ShdlcConnection(port), slave_address=0)
        print("SensorBridge SN: {}".format(bridge.get_serial_number()))

        # Configure SensorBridge port 1 for SFM
        bridge.set_i2c_frequency(SensorBridgePort.ONE, frequency=400e3)
        bridge.set_supply_voltage(SensorBridgePort.ONE, voltage=3.3)
        bridge.switch_supply_on(SensorBridgePort.ONE)

        # Create SFM device
        sfm3019 = Sfm3019I2cSensorBridgeDevice(bridge, SensorBridgePort.ONE)
        pid_sn = sfm3019.read_product_identifier_and_serial_number()
        print("SFM3019 SN: {}".format(pid_sn[1]))

        # Measure
        sfm3019.start_continuous_measurement(measure_mode='Air')
        while True:
            time.sleep(0.1)
            print("Flow: {}, Temperature: {}".format(*sfm3019.read_continuous_measurement()))
