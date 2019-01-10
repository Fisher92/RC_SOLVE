import Cube
x=Cube.cube()
while True:
    test = input("direction")
    if int(test) == 0:
        print("Turning CLowckwise")
        x.turn_Y("R","CW")
    if int(test) == 1:
        print("Turning CounterCLowckwise")
        x.turn_Y("R","CCW")