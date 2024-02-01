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

    # Initialize the temperature to -30 degrees Celsius
    print(
        "Setting temperature to -30 degrees Celsius then stepping up 10 degrees "
        "every 6 secs to 70 degrees"
    )
    print("\r\n")

    # Step through the temperature values in ten-degree increments
    while setting_temp <= 70:
        print("Setting temperature to {} degrees Celsius".format(setting_temp))
        ser.write("SOUR:PLAT {}\r\n".format(setting_temp).encode())

        # Wait for 6 secs
        time.sleep(6)

        # Increment the temperature by 10 degrees
        setting_temp += 10

    # Close the serial port connection
    ser.close()


if __name__ == "__main__":
    powertek_test_loop("/dev/tty.usbserial-B002XUJU", 9600, setting_temp=-30)
