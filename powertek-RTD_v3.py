import serial
import time

COM_PORT = "/dev/tty.usbserial-B002XUJU"
# COM_PORT = "COM6"
DEFAULT_BAUD = 9600  # Default Powetek RTD baud rate is 9600
START_TEMP = -30  # The test starting temperature
END_TEMP = 70  # The test ending temperature
TEMP_INTERVAL = 10  # The temperature interval between each step
STEP_TIME_DELAY = 2  # The time delay between each step (seconds


def run_temp_test(port, baud, start_temp, end_temp, step_time_delay, temp_interval):
    """Sends commands to a Powertek RTD instrument to change its output temperature
    simulation across a defined range of temperatures, temperature step and time
    interval - an up and down cycle through the temperature cycle is performed"""

    print("Starting Powertek temperature cycle test...")

    # Send the SYST:REM command initially to the instrument to set it into remote
    # mode so that it will accept temperature change commands. Sleep for 3 secs to allow
    # the instrument to process the 'remote control' command.
    with serial.Serial(port, baud) as ser:
        print("Putting Powertek RTD instrument into remote command mode")
        ser.write("SYST:REM\r\n".encode())
        time.sleep(3)

        # Ramp up through the temperature range
        for temp in range(start_temp, end_temp, temp_interval):
            set_temp(ser, temp)
            time.sleep(step_time_delay)

        # Ramp down through the temperature range
        for temp in range(end_temp, (start_temp - temp_interval), -temp_interval):
            set_temp(ser, temp)
            time.sleep(step_time_delay)

    print("Powertek RTD temperature test cycle Done.")


def set_temp(ser, temp):
    """Function to set device temperature using the SOUR:PLAT temp command."""
    command = f"SOUR:PLAT {temp}\r\n".encode()
    ser.write(command)
    print(f"Setting temperature to {temp}C")


if __name__ == "__main__":
    run_temp_test(COM_PORT, DEFAULT_BAUD, START_TEMP, END_TEMP, STEP_TIME_DELAY, TEMP_INTERVAL)
