from fc4cnc import prefix, suffix, clean_gcode
import fullcontrol as fc
from fc4cnc.operation import Operation
class Cut(Operation):

    def __init__(self, length: float, depth: float, step_down: float = 1.2, speed: int = 400, safe_height: float = 2):
        Operation.__init__(self, speed = speed, safe_height = safe_height)

        self.step_down = step_down
        self.length = length
        self.depth = depth
        self.steps = []

    def gcode(self):
        self.steps = prefix(self.steps)
        self.steps = self._cut()
        self.steps = suffix(self.steps)
        self.gcode = fc.transform(self.steps, 'gcode', fc.GcodeControls(printer_name='custom'))
        self.gcode = clean_gcode(self.gcode)

        return self.gcode

    def display(self):
        fc.transform(self.steps, 'plot', fc.PlotControls(style='line'))

    def _cut(self):

        # start point
        self.steps.append(fc.Point(x=0, y=0, z=0))
        self.steps.append(fc.Printer(print_speed=self.speed))
    
        z = 0
        z_layers = []
        while (z < self.depth):
            z += self.step_down
            if (z > self.depth):
                z = self.depth

            z_layers.append(z)
    
        dir = 1
        for z in z_layers:
            
            self.steps.append(fc.Printer(print_speed=200))
            self.steps.append(fc.Point(z=-z))
            self.steps.append(fc.Printer(print_speed=self.speed))

            if (1 == dir):
                # fw
                self.steps.append(fc.Point(x=self.length, y=0))
            else:
                # bw
                self.steps.append(fc.Point(x=0, y=0))
            dir *= -1

        # safe height & back to x,y home
        self.steps.append(fc.Point(z=2))
        self.steps.append(fc.Point(x=0, y=0))

        return self.steps

