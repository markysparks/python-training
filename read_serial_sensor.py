import serial

Temperature = None


def read_serial_hmp(port, baud):
    """ Opens a serial port and reads a line of data when it arrives from the sensor.
    Then splits the line in elements"""
    serial_port = serial.Serial(port=port, baudrate=baud)
    try:
        while True:
            # Read a line of data from the serial port
            data_line = serial_port.readline().decode().strip()
            if data_line:
                print(data_line)
                # Split the line into elements
                elements = split_line_into_tokens(data_line)
                print("Second element is:", elements[1])
    except serial.SerialException as e:
        print(f"Error reading from serial port: {e}")


def split_line_into_tokens(data_line):
    elements = data_line.split("  ")  # Double space as the delimiter
    return elements


# Example usage:
if __name__ == "__main__":
    read_serial_hmp("/dev/tty.usbserial-B002XUJU", 19200,)
