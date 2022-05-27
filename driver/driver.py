import argparse
import logging
from enum import Enum
import serial
import pyautogui

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(funcName)s:%(lineno)d %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger()
logger.level = logging.INFO

class Command(Enum):
    PLAY = "space"
    FASTF = "right"
    REWIND = "left"
    VOLUP = "up"
    VOLDOWN = "down"
    FULLSCREEN = "f"
    SYSVOLUP = "volumeup"
    SYSVOLDOWN = "volumedown"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--port",
        "-p",
        nargs="?",
        default="COM1",
        help="specify port number to use [COM4]",
        type=str,
    )
    parser.add_argument(
        "--baudrate",
        "-b",
        nargs="?",
        default="9600",
        help="specify baudrate [9600]",
        type=str,
    )
    parser.add_argument(
        "--timeout",
        "-t",
        nargs="?",
        default=0.1,
        help="specify port read/write timeout [0.1]",
        type=float,
    )
    parser.add_argument(
        "--write_timeout",
        "-wt",
        nargs="?",
        default=0.1,
        help="specify write timeout [0.1]",
        type=float,
    )
    args = parser.parse_args()
    try:
        port = serial.Serial(
                port=args.port,
                baudrate=args.baudrate,
                timeout=args.timeout,
                write_timeout=args.write_timeout,
        )
        logger.info(f"PORT({args.port}) is found")
    except serial.SerialException:
        logger.error("Cannot find port")
        exit(-1)

    window = pyautogui.getWindowsWithTitle("Youtube")
    if not window:
        logging.warning("No YouTube window is detected!!")
    if window:
        window[0].activate() # Choose first window as default
        logger.info("Activated YouTube window")

    while True:
        window = pyautogui.getWindowsWithTitle("Youtube")
        try:
            command = port.readline().decode().strip(" \r\n\b")
            if command not in Command.__members__:
                continue

            pyautogui.press(Command[command].value)
            logger.info(f"Command:{Command[command].name} is sent")
        except KeyboardInterrupt:
            logger.info("Exiting...")
            break
        except serial.SerialException:
            logger.error("Arduino disconnected from the machine")
            break

