import serial
import time


def powertek_test_loop(port_name, baud_rate, setting_temp):
    # Open the serial port connection
    ser = serial.Serial(
        port_name,
        baud_rate,
        parity=serial.PARITY_NONE,
        bytesize=serial.EIGHTBITS,
        stopbits=serial.STOPBITS_ONE,
    )

    temp_step_delay = 600
    # Initialize the temperature to -30 degrees Celsius
    print(
        "Setting temperature to -30 degrees Celsius then stepping up 10 degrees "
        "every 6 secs to 70 degrees"
    )
    print("\r\n")

    ser.write("SYST:REM\r\n".encode())
    time.sleep(2)
    ser.write("SOUR:PLAT -30\r\n".encode())
    time.sleep(2)

    # Step through the temperature values in ten-degree increments
    while setting_temp <= 70:
        print("Setting temperature to {} degrees Celsius".format(setting_temp))
        ser.write("SOUR:PLAT {}\r\n".format(setting_temp).encode())

        # Wait for 6 secs
        time.sleep(temp_step_delay)

        # Increment the temperature by 10 degrees
        setting_temp += 10

        # Step through the temperature values in ten-degree increments
    while setting_temp >= -30:
        print("Setting temperature to {} degrees Celsius".format(setting_temp))
        ser.write("SOUR:PLAT {}\r\n".format(setting_temp).encode())

        # Wait for --- secs
        time.sleep(temp_step_delay)

        # Increment the temperature by 10 degrees
        setting_temp -= 10

    # Close the serial port connection
    ser.close()


if __name__ == "__main__":
    powertek_test_loop("COM6", 9600, setting_temp=-30)
