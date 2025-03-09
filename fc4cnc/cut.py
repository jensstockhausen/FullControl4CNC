from fc4cnc import prefix, suffix, clean_gcode
import fullcontrol as fc

class Cut():

    def __init__(self, length: int, depth: int):
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

    def _cut(self):

        # start point
        self.steps.append(fc.Point(x=0, y=0, z=0))
        
        max_step_down = 1.2

        z = 0
        z_layers = []
        while (z < self.depth):
            z += max_step_down
            if (z > self.depth):
                z = self.depth

            z_layers.append(z)
    
        dir = 1
        for z in z_layers:
            
            self.steps.append(fc.Point(z=-z))
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

