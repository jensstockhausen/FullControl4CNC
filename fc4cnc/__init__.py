import math
import re
import fullcontrol as fc

def prefix(steps):
    steps.append(fc.ManualGcode(text="G21 ; millimeters"))
    steps.append(fc.ManualGcode(text="G90 ; absolute coordinate"))
    steps.append(fc.ManualGcode(text="G17 ; XY plane"))
    steps.append(fc.ManualGcode(text="G94 ; units per minute feed rate mode"))
    steps.append(fc.ManualGcode(text="M3 S1000 ; Turning on spindle"))
    steps.append(fc.Printer(print_speed=600, travel_speed=600))
    steps.append(fc.PlotAnnotation(point=fc.Point(x=0, y=0, z=0), label="Spindel on 100%"))
    steps.append(fc.ManualGcode(text="G0 Z5 ; Move to safe height"))
    steps.append(fc.ManualGcode(text="G0 X0 Y0 ; Move to start position"))
    steps.append(fc.Extruder(on=True))

    return steps

def suffix(steps):
    steps.append(fc.ManualGcode(text="G0 Z5 ; Go to safety height"))
    steps.append(fc.ManualGcode(text="M5 ; Turning off spindle"))
    steps.append(fc.PlotAnnotation(label="Spindel off"))

    return steps

# remove all E values from the gcode
def clean_gcode(gcode):
    lines = gcode.split("\n")
    new_gcode = ""
    for line in lines:
        new_gcode += re.sub(r"E[0-9.]+", "", line) + "\n"

    return new_gcode

