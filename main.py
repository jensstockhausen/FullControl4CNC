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

def scanline(steps, x0, x1, y0, y1, n_steps):

    safe_z = 2

    for j in range(n_steps):
        y = y0 + (y1 - y0) * j / n_steps

        for i in range(n_steps):
            x = x0 + (x1 - x0) * i / n_steps
            
            if (0 == x):
                steps.append(fc.Point(x=x, y=y, z=0))
                steps.append(fc.Extruder(on=True))

            z = math.cos(x * math.pi * 2 / (x1 - x0)*2 + math.pi * y/(x1-y0)*2 ) * 0.5 - 1.0

            steps.append(fc.Point(x=x, y=y, z=z))
        
        steps.append(fc.Extruder(on=False))
        steps.append(fc.Point(z=safe_z))
        steps.append(fc.Point(x=x0, y=y, z=safe_z))

    return steps

def main():
    # first, create an empty list
    steps = []

    steps = prefix(steps)
    steps = scanline(steps, 0, 20, 0, 20, 20)
    steps = suffix(steps)

    # transform the design to gcode and print to screen
    gcode = fc.transform(steps, 'gcode', fc.GcodeControls(printer_name='custom'))

    gcode = clean_gcode(gcode)
    print(gcode)

    fc.transform(steps, 'plot', fc.PlotControls(style='line'))
    
    return



if "__main__" == __name__:
    main()