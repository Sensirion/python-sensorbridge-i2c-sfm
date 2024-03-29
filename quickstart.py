import logging
import time

from sensirion_shdlc_driver import ShdlcSerialPort, ShdlcConnection
from sensirion_shdlc_sensorbridge import SensorBridgePort, SensorBridgeShdlcDevice

from sensirion_sensorbridge_i2c_sfm.sfm3019 import Sfm3019I2cSensorBridgeDevice, MeasurementMode
from sensirion_sensorbridge_i2c_sfm.sfm3019.sfm3019_constants import SFM3019_DEFAULT_I2C_FREQUENCY, \
    SFM3019_DEFAULT_VOLTAGE

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=logging.ERROR)

# Connect to the SensorBridge with default settings:
#  - baudrate:      460800
#  - slave address: 0
with ShdlcSerialPort(port='/dev/ttyUSB0', baudrate=460800) as port:
    # Initialize Sensorbridge
    bridge = SensorBridgeShdlcDevice(ShdlcConnection(port), slave_address=0)
    print("SensorBridge SN: {}".format(bridge.get_serial_number()))

    # Configure SensorBridge port 1 for SFM
    bridge.set_i2c_frequency(SensorBridgePort.ONE, frequency=SFM3019_DEFAULT_I2C_FREQUENCY)
    bridge.set_supply_voltage(SensorBridgePort.ONE, voltage=SFM3019_DEFAULT_VOLTAGE)
    bridge.switch_supply_on(SensorBridgePort.ONE)

    # Create SFM device
    sfm3019 = Sfm3019I2cSensorBridgeDevice(bridge, SensorBridgePort.ONE, slave_address=0x2E)

    # Define gas (or gas mixes)
    measure_mode = MeasurementMode.Air
    permille = 200  # only applies for gas mixes

    # Initialize sensor:
    # 1.) Stop any running measurement
    # 2.) Request scale factors and unit set on sensor
    sfm3019.initialize_sensor(measure_mode)

    # Read out product information
    pid, sn = sfm3019.read_product_identifier_and_serial_number()
    print("SFM3019 SN: {}".format(sn))
    print("Flow unit of sensor: {} (Volume at temperature in degree Centigrade)".format(sfm3019.flow_unit))

    # Start measurements
    sfm3019.start_continuous_measurement(measure_mode, air_o2_mix_fraction_permille=permille)

    # Read them out continuously
    while True:
        time.sleep(0.1)
        print("Flow: {}, Temperature: {}".format(*sfm3019.read_continuous_measurement()))
