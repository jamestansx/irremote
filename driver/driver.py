import argparse
import logging
from enum import Enum, auto
import serial
import pyautogui

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(funcName)s:%(lineno)d %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger()

last_win = None


class Command(Enum):
    PLAY = "space"
    FASTF = "right"
    REWIND = "left"
    VOLUP = "up"
    VOLDOWN = "down"
    FULLSCREEN = "f"
    SYSVOLUP = "volumeup"
    SYSVOLDOWN = "volumedown"
    CYCLEWIN = auto()


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
    parser.add_argument(
            "--debug",
            "-d",
            action=argparse.BooleanOptionalAction
            
    )
    args = parser.parse_args()
    logger.level = logging.DEBUG if args.debug else logging.INFO

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
    logging.warning("No YouTube window is detected!!") if not window else None

    while True:
        window = pyautogui.getWindowsWithTitle("Youtube")
        try:
            command = port.readline().decode().strip(" \r\n\b")
            logging.debug(f"command: {command} is pressed")
            if command not in Command.__members__:
                continue

            if isinstance(Command[command].value, int):
                try:
                    window[-1].activate()
                    last_win = pyautogui.getActiveWindow()
                except IndexError:
                    pass
                finally:
                    continue

            pyautogui.press(Command[command].value)
            logger.info(f"Command:{Command[command].name} is sent")
        except KeyboardInterrupt:
            logger.info("Exiting...")
            break
        except serial.SerialException:
            logger.error("Arduino disconnected from the machine")
            break

