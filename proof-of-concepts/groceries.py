import board
import busio
import adafruit_thermal_printer
import datetime

# Pick which version thermal printer class to use depending on the version of
# your printer.  Hold the button on the printer as it's powered on and it will
# print a test page that displays the firmware version, like 2.64, 2.68, etc.
# Use this version in the get_printer_class function below.
ThermalPrinter = adafruit_thermal_printer.get_printer_class(2.16)

# Define RX and TX pins for the board's serial port connected to the printer.
# Only the TX pin needs to be configued, and note to take care NOT to connect
# the RX pin if your board doesn't support 5V inputs.  If RX is left unconnected
# the only loss in functionality is checking if the printer has paper--all other
# functions of the printer will work.
RX = board.RX
TX = board.TX

# For a computer, use the pyserial library for uart access.
import serial
uart = serial.Serial("/dev/ttyS0", baudrate=19200, timeout=3000)

# Create the printer instance.
printer = ThermalPrinter(uart)

# Initialize the printer.  Note this will take a few seconds for the printer
# to warm up and be ready to accept commands (hence calling it explicitly vs.
# automatically in the initializer with the default auto_warm_up=True).
print("Warming up")
printer.warm_up()
print("Warmed up")

# Check if the printer has paper.  This only works if the RX line is connected
# on your board (but BE CAREFUL as mentioned above this RX line is 5V!)
# NOTE: THIS DOES NOT WORK
# if printer.has_paper():
    # print("Printer has paper!")
# else:
    # print("Printer might be out of paper, or RX is disconnected!")

# TODO: Format links as QR codes
# https://pypi.org/project/qrcode/

# Easy improvement: cache printer settings, make changes, restore cached
def processLine(line, printer):
    if line.startswith("# "):
        printer.bold = True
        printer.double_height = True
        printer.size = adafruit_thermal_printer.SIZE_LARGE
        printer.print(line[2:])
        printer.bold = False
        printer.double_height = False
        printer.size = adafruit_thermal_printer.SIZE_SMALL
    elif line.startswith("## "):
        printer.size = adafruit_thermal_printer.SIZE_LARGE
        printer.print(line[3:])
        printer.size = adafruit_thermal_printer.SIZE_SMALL
        pass
    elif line.startswith("### "):
        printer.underline = adafruit_thermal_printer.UNDERLINE_THICK
        printer.size = adafruit_thermal_printer.SIZE_MEDIUM
        printer.print(line[4:])
        printer.underline = None
        printer.size = adafruit_thermal_printer.SIZE_SMALL
        pass
    elif line.startswith("#### "):
        printer.underline = adafruit_thermal_printer.UNDERLINE_THIN
        printer.size = adafruit_thermal_printer.SIZE_MEDIUM
        printer.print(line[5:])
        printer.underline = None
        printer.size = adafruit_thermal_printer.SIZE_SMALL
    elif line.startswith("##### "):
        printer.size = adafruit_thermal_printer.SIZE_MEDIUM
        printer.print(line[6:])
        printer.size = adafruit_thermal_printer.SIZE_SMALL
    elif line.startswith("###### "):
        printer.bold = True
        printer.print(line[7:])
        printer.bold = False
    elif line.startswith("- "):
        printer.print("  " + line)
    # elif line == None or line == "":
    else:
        printer.print(line)

with open('/home/pi/notes/personal/groceries.md') as f:
    processLine("# Groceries", printer)
    printer.justify = adafruit_thermal_printer.JUSTIFY_RIGHT
    processLine("##### " + str(datetime.datetime.now().date()), printer)
    printer.justify = adafruit_thermal_printer.JUSTIFY_LEFT
    for line in f:
        processLine(line.rstrip(), printer)
    printer.feed(4)
