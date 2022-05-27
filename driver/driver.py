from enum import Enum
import serial
import pyautogui
import time

PORT = "COM4"

class Command(Enum):
    PLAY = "space"
    FASTF = "right"
    REWIND = "left"
    VOLUP = "up"
    VOLDOWN = "down"

if __name__ == "__main__":
    try:
        port = serial.Serial(
                port=PORT,
                baudrate=115200,
                timeout=0.1,
                write_timeout=0.1,
        )
    except serial.SerialException:
        print("Cannot find port")

    pyautogui.getWindowsWithTitle("Youtube")[0].activate()
    pyautogui.press("f") #fullscreen
    while True:
        try:
            command = port.readline().decode().strip(" \r\n\b")
            if command not in Command.__members__:
                continue

            pyautogui.press(Command[command].value)
        except KeyboardInterrupt:
            break

