import telnetlib
import time

HOST = "192.168.1.10"
PORT = 23
START_TEMP = -30  # The test starting temperature
END_TEMP = 70  # The test ending temperature
TEMP_INTERVAL = 10  # The temperature interval between each step
STEP_TIME_DELAY = 600  # The time delay between each step (seconds


def run_temp_test(host, port, start_temp, end_temp, step_time_delay, temp_interval):
    """Sends commands to a Powertek RTD instrument ethernet interface to change its output
    temperature simulation across a defined range of temperatures, temperature step and
    time interval - an up and down cycle through the temperature cycle is performed"""

    print("Starting Powertek temperature cycle test...")

    # Send the SYST:REM command initially to the instrument to set it into remote
    # mode so that it will accept temperature change commands. Sleep for 3 secs to allow
    # the instrument to process the 'remote control' command.
    with telnetlib.Telnet(host, port) as tn:
        print("Putting Powertek RTD instrument into remote command mode")
        tn.write(b"SYST:REM\r\n")
        # print(tn.read_all().decode("ascii"))
        time.sleep(3)

        # Ramp up through the temperature range
        for temp in range(start_temp, end_temp, temp_interval):
            set_temp(tn, temp)
            time.sleep(step_time_delay)

        # Ramp down through the temperature range
        for temp in range(end_temp, (start_temp - temp_interval), -temp_interval):
            set_temp(tn, temp)
            time.sleep(step_time_delay)

    print("Powertek RTD temperature test cycle Done.")


def set_temp(tn, temp):
    """Function to set device temperature using the SOUR:PLAT temp command."""
    command = f"SOUR:PLAT {temp}\r\n"
    tn.write(bytes(command))
    print(f"Setting temperature to {temp}C")


if __name__ == "__main__":
    run_temp_test(HOST, PORT, START_TEMP, END_TEMP, STEP_TIME_DELAY, TEMP_INTERVAL)
