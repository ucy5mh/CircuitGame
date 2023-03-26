# A Logic Gate and Circuit Sandbox and Simulator.

You can access the game here: https://replit.com/@KevinSandoval8/CircuitGame?v=1 <br>
Click the 'run' button on the right side
You can move the pygame window by dragging the top bar if you needed to see more of the screen. (You can also fork the Replit which allows you to run the Replit without the information tab with the project description (I know no other way of minimizing that))


Use the user interface to select wires and place them on the checkerboard grid. Connect the sources (ON/OFF switches, or the power sources), using wires to logic gates.
You can rotate wires by clicking on a cell with the same wire selected. (The UI elements are highlighted in green to indicate which object/option is selected)

Logic Gates:
- AND: Takes in two input wires and outputs a power signal if both input wires are on <br>
![AND gate](/AND.png)
- OR: Takes in two input wires and outputs a power signal if at least one input wire is on <br>
![OR gate](/Or.png)
- XOR: Takes in two input wires and outputs a power signal if only one input signal is on <br>
![XOR gate](/XOR.png)
- NOT: Takes in one input wire and outputs the inverse power signal (output wire is on if input wire is off, and vice versa) <br>
![NOT gate](/NOT.png)

Use the X icon to delete any placed objects. Use the R icon to reset the grid.

The light Object on the right side accepts an input from any side, and lights up if an "ON" wire is connected to it.
