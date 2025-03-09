import typer 
from fc4cnc.cut import Cut

app = typer.Typer()

@app.command()
def cut(length: int, depth: int):
    print(f"Creating a cut starting at X,Y home {length}mm long {depth}mm deep")
    c = Cut(length, depth)

    gcode = c.gcode()
    print(gcode)

    fc.transform(c.steps, 'plot', fc.PlotControls(style='line'))

@app.command()
def plot():
    print("Creating a plot")

if __name__ == "__main__":
    app()

