import math
import re
import fullcontrol as fc

def prefix(steps, speed=400,  safe_height=2, spindel_speed=1000):
    steps.append(fc.ManualGcode(text="G21 ; millimeters"))
    steps.append(fc.ManualGcode(text="G90 ; absolute coordinate"))
    steps.append(fc.ManualGcode(text="G17 ; XY plane"))
    steps.append(fc.ManualGcode(text="G94 ; units per minute feed rate mode"))
    steps.append(fc.ManualGcode(text=f"M3 S{spindel_speed} ; Turning on spindle"))
    steps.append(fc.Printer(print_speed=speed, travel_speed=speed))
    steps.append(fc.PlotAnnotation(point=fc.Point(x=0, y=0, z=0), label="Spindel on 100%"))
    steps.append(fc.ManualGcode(text=f"G0 Z{safe_height} ; Move to safe height"))
    steps.append(fc.ManualGcode(text="G0 X0 Y0 ; Move to start position"))
    steps.append(fc.Extruder(on=True))

    return steps

def suffix(steps, safe_height=2):
    steps.append(fc.ManualGcode(text=f"G0 Z{safe_height} ; Go to safety height"))
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

