import typer 
from fc4cnc.cut import Cut

app = typer.Typer()

@app.command()
def cut(length: float, depth: float, 
        step_down: float = 1.2, speed: float = 400, safe_height: float = 2):
    print(f"Creating a cut starting at X,Y home {length}mm long {depth}mm deep")
    print(f"using step down {step_down}mm feed{speed}mm/min safe height {safe_height}mm" )
    c = Cut(length=length, depth=depth, step_down=step_down, speed=speed, safe_height=safe_height)

    gcode = c.gcode()
    print(gcode)

    c.display()

@app.command()
def plot():
    print("Creating a plot")

if __name__ == "__main__":
    app()

