import pygame

import gamebox
from collections import deque
from levels import levels
from pygame.locals import QUIT

def get_valid_sides(type, orientation):
  if type == "STRAIGHT":
    if orientation == 1 or orientation == 3:
      return [0, 1, 0, 1]
    else:
      return [1, 0, 1, 0]

  elif type == "CORNER":
    if orientation == 1:
      return [0, 0, 1, 1]
    elif orientation == 2:
      return [1, 0, 0, 1]
    elif orientation == 3:
      return [1, 1, 0, 0]
    elif orientation == 4:
      return [0, 1, 1, 0]

  elif type == "T":
    if orientation == 1:
      return [0, 1, 1, 1]
    elif orientation == 2:
      return [1, 0, 1, 1]
    elif orientation == 3:
      return [1, 1, 0, 1]
    elif orientation == 4:
      return [1, 1, 1, 0]

  else: return [1, 1, 1, 1]


def get_def_box(i, j):
    if i % 2 == 0:
      if j % 2 == 0:
          return [gamebox.from_color(j * xScale + inputBoxWidth, i * yScale, "white", xScale, yScale), 'NO_POWER', 'NONE', 'NO_WIRE', [0, 0, 0, 0], 0, i, j]
      else:
          return [gamebox.from_color(j * xScale + inputBoxWidth, i * yScale, "black", xScale, yScale), 'NO_POWER', 'NONE', 'NO_WIRE', [0, 0, 0, 0], 0, i, j]
    elif i % 2 == 1:
      if j % 2 == 1:
        return [gamebox.from_color(j * xScale + inputBoxWidth, i * yScale, "white", xScale, yScale), 'NO_POWER', 'NONE', 'NO_WIRE', [0, 0, 0, 0], 0, i, j]
      else:
        return [gamebox.from_color(j * xScale + inputBoxWidth, i * yScale, "black", xScale, yScale), 'NO_POWER', 'NONE', 'NO_WIRE', [0, 0, 0, 0], 0, i, j]
    else:
      return [gamebox.from_color(j * xScale + inputBoxWidth, i * yScale, "black", xScale, yScale), 'NO_POWER', 'NONE', 'NO_WIRE', [0, 0, 0, 0], 0, i, j]

width =1200
height = 600
camera = gamebox.Camera(width, height)

circuitBoardWidth = width
circuitBoardYOffset = height - 150

inputBoxWidth = 150
inputBoxHeight = circuitBoardYOffset


rows = 9
cols = 21

xScale = 50
yScale = 50

selection = -1

#Create grid (simplify later)
grid = []
for i in range(rows):
  grid.insert(i, [])  
  for j in range(cols):
    if i % 2 == 0:
      if j % 2 == 0:
        grid[i].insert(j, [gamebox.from_color(j * xScale + inputBoxWidth, i * yScale, "white", xScale, yScale), 'NO_POWER', 'NONE', 'NO_WIRE', [0, 0, 0, 0], 0, i, j])
      else:
        grid[i].insert(j, [gamebox.from_color(j * xScale + inputBoxWidth, i * yScale, "black", xScale, yScale), 'NO_POWER', 'NONE', 'NO_WIRE', [0, 0, 0, 0], 0, i, j])  

    elif i % 2 == 1:
      if j % 2 == 1:
        grid[i].insert(j, [gamebox.from_color(j * xScale + inputBoxWidth, i * yScale, "white", xScale, yScale), 'NO_POWER', 'NONE', 'NO_WIRE', [0, 0, 0, 0], 0, i, j])
      else:
        grid[i].insert(j, [gamebox.from_color(j * xScale + inputBoxWidth, i * yScale, "black", xScale, yScale), 'NO_POWER', 'NONE', 'NO_WIRE', [0, 0, 0, 0], 0, i, j])
    else:
      grid[i].insert(j, [gamebox.from_color(j * xScale + inputBoxWidth, i * yScale, "black", xScale, yScale), 'NO_POWER', 'NONE', 'NO_WIRE', [0, 0, 0, 0], 0, i, j])


grid[4][20] = [gamebox.from_image(20 * xScale + inputBoxWidth, 4 * yScale, 'light_off.png'), 'NO_POWER', 'NONE', 'LIGHT', [1, 1, 1, 1], 0, i, j]

inputBox = gamebox.from_color(0, 0, "#818181", inputBoxWidth, inputBoxHeight)

# input grid
input_grid = []
for i in range(9):
  input_grid.insert(i, [])  


#Frame for circuit UI box
borderBoxTop = gamebox.from_color(0, 450, "black", 1200, 20)
borderBoxLeft = gamebox.from_color(0, 450, "black", 20, 150)
borderBoxBottom = gamebox.from_color(0, 580, "black",1200,20)
borderBoxRight = gamebox.from_color(1180,450, "black", 20,150)

uiBoxes = []
uiElements = []
#Seleciton boxes for wires
boxOne = gamebox.from_color(50, 450 + (150/2 - 60/2), "#282828", 60, 60)
boxTwo = gamebox.from_color(50 + 60 + 10, 450 + (150/2 - 60/2), "#282828", 60, 60)
boxThree = gamebox.from_color(50 + 60 * 2 + 10 * 2, 450 + (150/2 - 60/2), "#282828", 60, 60)
boxFour = gamebox.from_color(50 + 60 * 3 + 10 * 3, 450 + (150/2 - 60/2), "#282828", 60, 60)


uiBoxes.insert(0, boxOne)
uiBoxes.insert(1, boxTwo)
uiBoxes.insert(2, boxThree)
uiBoxes.insert(3, boxFour)

boxFive = gamebox.from_color(50 + 60 * 4 + 10 * 4, 450 + (150/2 - 60/2), "#282828", 60 * 2, 60)
boxSix = gamebox.from_color(50 + 60 * 6 + 10 * 6, 450 + (150/2 - 60/2), "#282828", 60 * 2, 60)
boxSeven = gamebox.from_color(50 + 60 * 8 + 10 * 8, 450 + (150/2 - 60/2), "#282828", 60 * 2, 60)
boxEight = gamebox.from_color(50 + 60 * 10 + 10 * 10, 450 + (150/2 - 60/2), "#282828", 60 * 1, 60)
boxNine = gamebox.from_color(50 + 60 * 11 + 10 * 11, 450 + (150/2 - 60/2), "#282828", 60 * 1, 60)
boxTen = gamebox.from_color(50 + 60 * 12 + 10 * 12, 450 + (150/2 - 60/2), "#282828", 60 * 1, 60)

uiBoxes.insert(4, boxFive)
uiBoxes.insert(5, boxSix)
uiBoxes.insert(6, boxSeven)
uiBoxes.insert(7, boxEight)
uiBoxes.insert(8, boxNine)
uiBoxes.insert(9, boxTen)

#Wire UI elements
straightWireUI = gamebox.from_image(boxOne.x + 5 - boxOne.width/2, boxOne.y + 5 - boxOne.height/2, 'straight_wire_off.png')
cornerWireUI = gamebox.from_image(boxTwo.x + 5 - boxTwo.width/2, boxTwo.y + 5 - boxTwo.height/2, 'corner_wire_off.png')
tWireUI = gamebox.from_image(boxThree.x + 5 - boxThree.width/2, boxThree.y + 5 - boxThree.height/2, 't_wire_off.png')
crossWireUI = gamebox.from_image(boxFour.x + 5 - boxFour.width/2, boxFour.y + 5 - boxFour.height/2, "cross_wire_off.png")
uiElements.insert(0, 'straight_wire_off.png')
uiElements.insert(1, 'corner_wire_off.png')
uiElements.insert(2, 't_wire_off.png')
uiElements.insert(3, 'cross_wire_off.png')

#Circuit UI elements
andGateUI = gamebox.from_image(boxFive.x + 5 - boxFive.width/4, boxFive.y + 10 - boxFive.height, 'AND.png')
andGateUI.rotate(90)

orGateUI = gamebox.from_image(boxSix.x + 5 - boxSix.width/4, boxSix.y + 10 - boxSix.height, 'Or.png')
orGateUI.rotate(90)

xorGateUI = gamebox.from_image(boxSeven.x + 5 - boxSeven.width/4, boxSeven.y + 10 - boxSeven.height, 'XOR.png')
xorGateUI.rotate(90)

notGateUI = gamebox.from_image(boxEight.x + 5 - boxEight.width/2, boxEight.y + 5 - boxEight.height/2, 'NOT.png')

deleteUI = gamebox.from_image(boxNine.x + 5 - boxNine.width/2, boxNine.y + 5 - boxNine.height/2, 'delete.png')

resetUI = gamebox.from_image(boxTen.x + 5 - boxTen.width/2, boxTen.y + 5 - boxTen.height/2, 'reset.png')

uiElements.insert(4, 'AND.png')
uiElements.insert(5, 'Or.png')
uiElements.insert(6, 'XOR.png')
uiElements.insert(7, 'NOT.png')

uiElements.insert(8, 'delete.png')
uiElements.insert(9, 'reset.png')

currentLevel = 0
state = "wait for level to load"

def tick(keys):
  global selection
  global uiBoxes
  global state
  global input_grid
  camera.clear("#767676")
  camera.draw(inputBox)
  
  level_input_data = levels.get(str(currentLevel))
  input_list = level_input_data[0]

  #handle mouse input
  pos = 0
  ev = pygame.event.get()
  for event in ev:
    if event.type == pygame.MOUSEBUTTONUP:
      pos = pygame.mouse.get_pos()
  
  if state == "wait for level to load":
    input_grid = []
    for i in range(9):
      input_grid.insert(i, [])  
      
    for i in range(9):
      if input_list[i] == "TOGGLE":
          input_grid[i].insert(0, [gamebox.from_image(50,50*i,"OFF.png"), 'OFF'])
          input_grid[i].insert(1, [gamebox.from_image(100,50*i,"straight_wire_off.png"), 'OFF'])
      elif input_list[i] == "OFF":
        input_grid[i].insert(0, [gamebox.from_image(50,50*i,"POWOFF.png"), 'NULL'])
        input_grid[i].insert(1, [gamebox.from_image(100,50*i,"straight_wire_off.png"), 'OFF'])
      elif input_list[i] == "ON":
        input_grid[i].insert(0, [gamebox.from_image(50,50*i,"POWON.png"), 'NULL'])
        input_grid[i].insert(1,  [gamebox.from_image(100,50*i,"straight_wire_on.png"), 'ON'])
      else:
        input_grid[i].insert(0, 0)
        input_grid[i].insert(1, 0)
    state = "playing"

  for i in range(rows):
    for j in range(cols):
      grid[i][j][1] = 'NO_POWER'

      if (grid[i][j][3] != 'NO_WIRE'):
        if grid[i][j][3] == 'STRAIGHT':
          grid[i][j][0] = gamebox.from_image(j * xScale + inputBoxWidth, i * yScale, 'straight_wire_off.png')
          grid[i][j][0].rotate(360 - (90 * (grid[i][j][5] - 1)))
        elif grid[i][j][3] == 'CORNER':
          grid[i][j][0] = gamebox.from_image(j * xScale + inputBoxWidth, i * yScale, 'corner_wire_off.png')
          grid[i][j][0].rotate(360 - (90 * (grid[i][j][5] - 1)))
        elif grid[i][j][3] == 'T':
          grid[i][j][0] = gamebox.from_image(j * xScale + inputBoxWidth, i * yScale, 't_wire_off.png')
          grid[i][j][0].rotate(360 - (90 * (grid[i][j][5] - 1)))
        elif grid[i][j][3] == 'CROSS':
          grid[i][j][0] = gamebox.from_image(j * xScale + inputBoxWidth, i * yScale, 'cross_wire_off.png')
          grid[i][j][0].rotate(360 - (90 * (grid[i][j][5] - 1)))
        elif grid[i][j][3] == 'LIGHT':
          grid[i][j][0] = gamebox.from_image(j * xScale + inputBoxWidth, i * yScale, 'light_off.png')
  
  for i in range(9):
    if input_grid[i][0] != 0:
      if input_list[i] == 'TOGGLE':
        if pos != 0:
          if input_grid[i][0][0].contains(pos[0], pos[1]):
            if input_grid[i][0][1] == 'OFF':
              input_grid[i][0][0] = gamebox.from_image(50,50*i,"ON.png")
              input_grid[i][0][1] = 'ON'
              input_grid[i][1][0] = gamebox.from_image(100,50*i,"straight_wire_on.png")
              input_grid[i][1][1] = 'ON'
            else:
              input_grid[i][0][0] = gamebox.from_image(50,50*i,"OFF.png")
              input_grid[i][0][1] = 'OFF'
              input_grid[i][1][0] = gamebox.from_image(100,50*i,"straight_wire_off.png")  
              input_grid[i][1][1] = 'OFF'
      camera.draw(input_grid[i][0][0])
      camera.draw(input_grid[i][1][0])
    
      wires_to_check = deque()
      if input_grid[i][1][1] == 'ON':
        current_i = i
        current_j = 0
        if grid[i][0][4][4-1] == 1: 
          grid[i][0][4][4-1] = -1
          grid[i][0][1] = 'POWERED'
          wires_to_check.append(grid[current_i][current_j])
          while wires_to_check.__len__() > 0:
            current_wire = wires_to_check.pop()
            current_i = current_wire[6]
            current_j = current_wire[7]
            
            src = 0;
            for l in range(4):
              if current_wire[4][l] == -1:
                src = l

            if current_wire[3] == 'LIGHT':
              current_wire[4][src] = 1
              continue
            
            if current_wire[3] == 'UP_AND':
              if current_wire[1] == 'POWERED' and grid[current_wire[6] + 1][current_wire[7]][1] == 'POWERED':
                next_i = current_i + 2
                next_j = current_j 
                if next_i > -1 and next_i < rows and next_j > -1 and next_j < cols:
                  if (grid[next_i][next_j][1] != 'POWERED' and grid[next_i][next_j][4][0] == 1):
                    grid[next_i][next_j][1] = 'POWERED'
                    grid[next_i][next_j][4][0] = -1
                    wires_to_check.append(grid[next_i][next_j])              
            elif current_wire[3] == 'DOWN_AND':
              if current_wire[1] == 'POWERED' and grid[current_wire[6] - 1][current_wire[7]][1] == 'POWERED':
                next_i = current_i + 1
                next_j = current_j 
                if next_i > -1 and next_i < rows and next_j > -1 and next_j < cols:
                  if (grid[next_i][next_j][1] != 'POWERED' and grid[next_i][next_j][4][0] == 1):
                    grid[next_i][next_j][1] = 'POWERED'
                    grid[next_i][next_j][4][0] = -1
                    wires_to_check.append(grid[next_i][next_j])


            if current_wire[3] == 'UP_OR':
              if current_wire[1] == 'POWERED' or grid[current_wire[6] + 1][current_wire[7]][1] == 'POWERED':
                next_i = current_i + 2
                next_j = current_j 
                if next_i > -1 and next_i < rows and next_j > -1 and next_j < cols:
                  if (grid[next_i][next_j][1] != 'POWERED' and grid[next_i][next_j][4][0] == 1):
                    grid[next_i][next_j][1] = 'POWERED'
                    grid[next_i][next_j][4][0] = -1
                    wires_to_check.append(grid[next_i][next_j])              
            elif current_wire[3] == 'DOWN_OR':
              if current_wire[1] == 'POWERED' or grid[current_wire[6] - 1][current_wire[7]][1] == 'POWERED':
                next_i = current_i + 1
                next_j = current_j 
                if next_i > -1 and next_i < rows and next_j > -1 and next_j < cols:
                  if (grid[next_i][next_j][1] != 'POWERED' and grid[next_i][next_j][4][0] == 1):
                    grid[next_i][next_j][1] = 'POWERED'
                    grid[next_i][next_j][4][0] = -1
                    wires_to_check.append(grid[next_i][next_j])

            if current_wire[3] == 'UP_XOR':
              if current_wire[1] != grid[current_wire[6] + 1][current_wire[7]][1]:
                next_i = current_i + 2
                next_j = current_j 
                if next_i > -1 and next_i < rows and next_j > -1 and next_j < cols:
                  if (grid[next_i][next_j][1] != 'POWERED' and grid[next_i][next_j][4][0] == 1):
                    grid[next_i][next_j][1] = 'POWERED'
                    grid[next_i][next_j][4][0] = -1
                    wires_to_check.append(grid[next_i][next_j])     
              else:
                next_i = current_i + 2
                next_j = current_j 
                if next_i > -1 and next_i < rows and next_j > -1 and next_j < cols:
                  grid[next_i][next_j][1] = 'NO_POWER'
            elif current_wire[3] == 'DOWN_XOR':
              if current_wire[1] != grid[current_wire[6] - 1][current_wire[7]][1]:
                next_i = current_i + 1
                next_j = current_j 
                if next_i > -1 and next_i < rows and next_j > -1 and next_j < cols:
                  if (grid[next_i][next_j][1] != 'POWERED' and grid[next_i][next_j][4][0] == 1):
                    grid[next_i][next_j][1] = 'POWERED'
                    grid[next_i][next_j][4][0] = -1
                    wires_to_check.append(grid[next_i][next_j])
              else:
                next_i = current_i + 1
                next_j = current_j 
                if next_i > -1 and next_i < rows and next_j > -1 and next_j < cols:
                  grid[next_i][next_j][1] = 'NO_POWER'

                    
          
            if current_wire[3] != 'NO_WIRE' and current_wire[3] != 'DOWN_AND' and current_wire[3] != 'DOWN_XOR' and current_wire[3] != 'DOWN_OR':
              for z in range(4):
                if current_wire[4][z] == 1:
                  #redirect north case
                  if z == 0:
                    next_i = current_i - 1
                    next_j = current_j
                    if next_i > -1 and next_i < rows and next_j > -1 and next_j < cols:
                      if (grid[next_i][next_j][1] != 'POWERED' and grid[next_i][next_j][4][2] == 1):
                        grid[next_i][next_j][1] = 'POWERED'
                        grid[next_i][next_j][4][2] = -1
                        wires_to_check.append(grid[next_i][next_j])
                  #redirect east case
                  if z == 1:
                    next_i = current_i
                    next_j = current_j + 1
                    if next_i > -1 and next_i < rows and next_j > -1 and next_j < cols:
                      if (grid[next_i][next_j][1] != 'POWERED' and grid[next_i][next_j][4][3] == 1):
                        grid[next_i][next_j][1] = 'POWERED'
                        grid[next_i][next_j][4][3] = -1
                        wires_to_check.append(grid[next_i][next_j])
                  #Redirect south case
                  if z == 2:
                    next_i = current_i + 1
                    next_j = current_j 
                    if next_i > -1 and next_i < rows and next_j > -1 and next_j < cols:
                      if (grid[next_i][next_j][1] != 'POWERED' and grid[next_i][next_j][4][0] == 1):
                        grid[next_i][next_j][1] = 'POWERED'
                        grid[next_i][next_j][4][0] = -1
                        wires_to_check.append(grid[next_i][next_j])
                  #Redirect west case
                  if z == 3:
                    next_i = current_i
                    next_j = current_j - 1
                    if next_i > -1 and next_i < rows and next_j > -1 and next_j < cols:
                      if (grid[next_i][next_j][1] != 'POWERED' and grid[next_i][next_j][4][1] == 1):
                        grid[next_i][next_j][1] = 'POWERED'
                        grid[next_i][next_j][4][1] = -1
                        wires_to_check.append(grid[next_i][next_j])
            current_wire[4][src] = 1         
            


  for i in range(rows):
    for j in range(cols):
      if grid[i][j][3] == 'NOT':
        next_i = i
        next_j = j - 1
        if (next_i > -1 and next_i < rows and next_j > -1 and next_j < cols) or (next_j == -1):
          run_algo = False
          if next_j == -1:
            if input_grid[next_i][1][1] == 'NO_POWER':
              run_algo = True
          
          if grid[next_i][next_j][1] == 'NO_POWER':
            run_algo = True
          if run_algo == True:
            current_i = i
            current_j = j + 1
            if grid[current_i][current_j][4][4-1] == 1: 
              grid[current_i][current_j][4][4-1] = -1
              grid[current_i][current_j][1] = 'POWERED'
              wires_to_check.append(grid[current_i][current_j])
              while wires_to_check.__len__() > 0:
                current_wire = wires_to_check.pop()
                current_i = current_wire[6]
                current_j = current_wire[7]
                
                src = 0;
                for l in range(4):
                  if current_wire[4][l] == -1:
                    src = l

                if current_wire[3] == 'LIGHT':
                  current_wire[4][src] = 1
                  continue
                
                if current_wire[3] == 'UP_AND':
                  if current_wire[1] == 'POWERED' and grid[current_wire[6] + 1][current_wire[7]][1] == 'POWERED':
                    next_i = current_i + 2
                    next_j = current_j 
                    if next_i > -1 and next_i < rows and next_j > -1 and next_j < cols:
                      if (grid[next_i][next_j][1] != 'POWERED' and grid[next_i][next_j][4][0] == 1):
                        grid[next_i][next_j][1] = 'POWERED'
                        grid[next_i][next_j][4][0] = -1
                        wires_to_check.append(grid[next_i][next_j])              
                elif current_wire[3] == 'DOWN_AND':
                  if current_wire[1] == 'POWERED' and grid[current_wire[6] - 1][current_wire[7]][1] == 'POWERED':
                    next_i = current_i + 1
                    next_j = current_j 
                    if next_i > -1 and next_i < rows and next_j > -1 and next_j < cols:
                      if (grid[next_i][next_j][1] != 'POWERED' and grid[next_i][next_j][4][0] == 1):
                        grid[next_i][next_j][1] = 'POWERED'
                        grid[next_i][next_j][4][0] = -1
                        wires_to_check.append(grid[next_i][next_j])
    
    
                if current_wire[3] == 'UP_OR':
                  if current_wire[1] == 'POWERED' or grid[current_wire[6] + 1][current_wire[7]][1] == 'POWERED':
                    next_i = current_i + 2
                    next_j = current_j 
                    if next_i > -1 and next_i < rows and next_j > -1 and next_j < cols:
                      if (grid[next_i][next_j][1] != 'POWERED' and grid[next_i][next_j][4][0] == 1):
                        grid[next_i][next_j][1] = 'POWERED'
                        grid[next_i][next_j][4][0] = -1
                        wires_to_check.append(grid[next_i][next_j])              
                elif current_wire[3] == 'DOWN_OR':
                  if current_wire[1] == 'POWERED' or grid[current_wire[6] - 1][current_wire[7]][1] == 'POWERED':
                    next_i = current_i + 1
                    next_j = current_j 
                    if next_i > -1 and next_i < rows and next_j > -1 and next_j < cols:
                      if (grid[next_i][next_j][1] != 'POWERED' and grid[next_i][next_j][4][0] == 1):
                        grid[next_i][next_j][1] = 'POWERED'
                        grid[next_i][next_j][4][0] = -1
                        wires_to_check.append(grid[next_i][next_j])
    
                if current_wire[3] == 'UP_XOR':
                  if current_wire[1] != grid[current_wire[6] + 1][current_wire[7]][1]:
                    next_i = current_i + 2
                    next_j = current_j 
                    if next_i > -1 and next_i < rows and next_j > -1 and next_j < cols:
                      if (grid[next_i][next_j][1] != 'POWERED' and grid[next_i][next_j][4][0] == 1):
                        grid[next_i][next_j][1] = 'POWERED'
                        grid[next_i][next_j][4][0] = -1
                        wires_to_check.append(grid[next_i][next_j])     
                  else:
                    next_i = current_i + 2
                    next_j = current_j 
                    if next_i > -1 and next_i < rows and next_j > -1 and next_j < cols:
                      grid[next_i][next_j][1] = 'NO_POWER'
                elif current_wire[3] == 'DOWN_XOR':
                  if current_wire[1] != grid[current_wire[6] - 1][current_wire[7]][1]:
                    next_i = current_i + 1
                    next_j = current_j 
                    if next_i > -1 and next_i < rows and next_j > -1 and next_j < cols:
                      if (grid[next_i][next_j][1] != 'POWERED' and grid[next_i][next_j][4][0] == 1):
                        grid[next_i][next_j][1] = 'POWERED'
                        grid[next_i][next_j][4][0] = -1
                        wires_to_check.append(grid[next_i][next_j])
                  else:
                    next_i = current_i + 1
                    next_j = current_j 
                    if next_i > -1 and next_i < rows and next_j > -1 and next_j < cols:
                      grid[next_i][next_j][1] = 'NO_POWER'
    
                        
              
                if current_wire[3] != 'NO_WIRE' and current_wire[3] != 'DOWN_AND' and current_wire[3] != 'DOWN_XOR' and current_wire[3] != 'DOWN_OR':
                  for z in range(4):
                    if current_wire[4][z] == 1:
                      #redirect north case
                      if z == 0:
                        next_i = current_i - 1
                        next_j = current_j
                        if next_i > -1 and next_i < rows and next_j > -1 and next_j < cols:
                          if (grid[next_i][next_j][1] != 'POWERED' and grid[next_i][next_j][4][2] == 1):
                            grid[next_i][next_j][1] = 'POWERED'
                            grid[next_i][next_j][4][2] = -1
                            wires_to_check.append(grid[next_i][next_j])
                      #redirect east case
                      if z == 1:
                        next_i = current_i
                        next_j = current_j + 1
                        if next_i > -1 and next_i < rows and next_j > -1 and next_j < cols:
                          if (grid[next_i][next_j][1] != 'POWERED' and grid[next_i][next_j][4][3] == 1):
                            grid[next_i][next_j][1] = 'POWERED'
                            grid[next_i][next_j][4][3] = -1
                            wires_to_check.append(grid[next_i][next_j])
                      #Redirect south case
                      if z == 2:
                        next_i = current_i + 1
                        next_j = current_j 
                        if next_i > -1 and next_i < rows and next_j > -1 and next_j < cols:
                          if (grid[next_i][next_j][1] != 'POWERED' and grid[next_i][next_j][4][0] == 1):
                            grid[next_i][next_j][1] = 'POWERED'
                            grid[next_i][next_j][4][0] = -1
                            wires_to_check.append(grid[next_i][next_j])
                      #Redirect west case
                      if z == 3:
                        next_i = current_i
                        next_j = current_j - 1
                        if next_i > -1 and next_i < rows and next_j > -1 and next_j < cols:
                          if (grid[next_i][next_j][1] != 'POWERED' and grid[next_i][next_j][4][1] == 1):
                            grid[next_i][next_j][1] = 'POWERED'
                            grid[next_i][next_j][4][1] = -1
                            wires_to_check.append(grid[next_i][next_j])
                current_wire[4][src] = 1 

  #draw grid of boxes
  for i in range(rows):
    for j in range(cols):
      if pos != 0 and (i != 4 or j != 20):
        if grid[i][j][0].contains(pos[0], pos[1]):
          if selection != -1:
            if selection != 5 and selection != 6 and selection != 7:
              grid[i][j][0] = gamebox.from_image(j * xScale + inputBoxWidth, i * yScale, uiElements[selection - 1])

            if i > 0:
              if grid[i][j][3] == "DOWN_AND" or grid[i][j][3] == "DOWN_OR" or grid[i][j][3] == "DOWN_XOR":
                grid[i-1][j] = get_def_box(i-1, j)
              if selection == 5 or selection == 6 or selection == 7:
                if i == rows - 1:
                  grid[i][j] = get_def_box(i, j)
            if selection == 1:
              if grid[i][j][3] == 'STRAIGHT':
                grid[i][j][5] += 1;
                if (grid[i][j][5] == 5):
                  grid[i][j][5] = 1
                grid[i][j][0].rotate(360 - (90 * (grid[i][j][5] - 1)))
                grid[i][j][4] = get_valid_sides(grid[i][j][3], grid[i][j][5])
              else:
                grid[i][j][3] = 'STRAIGHT'
                grid[i][j][5] = 1
                grid[i][j][4] = get_valid_sides(grid[i][j][3], grid[i][j][5])
            elif selection == 2:
              if grid[i][j][3] == 'CORNER':
                grid[i][j][5] += 1;
                if (grid[i][j][5] == 5):
                  grid[i][j][5] = 1
                grid[i][j][4] = get_valid_sides(grid[i][j][3], grid[i][j][5])
                grid[i][j][0].rotate(360 - (90 * (grid[i][j][5] - 1)))
              else:
                grid[i][j][3] = 'CORNER'
                grid[i][j][5] = 1
                grid[i][j][4] = get_valid_sides(grid[i][j][3], grid[i][j][5])
            elif selection == 3:
              if grid[i][j][3] == 'T':
                grid[i][j][5] += 1;
                if (grid[i][j][5] == 5):
                  grid[i][j][5] = 1
                grid[i][j][4] = get_valid_sides(grid[i][j][3], grid[i][j][5])
                grid[i][j][0].rotate(360 - (90 * (grid[i][j][5] - 1)))
              else:
                grid[i][j][3] = 'T'
                grid[i][j][5] = 1
                grid[i][j][4] = get_valid_sides(grid[i][j][3], grid[i][j][5])
            elif selection == 4:
              if grid[i][j][3] == 'CROSS':
                grid[i][j][5] += 1;
                if (grid[i][j][5] == 5):
                  grid[i][j][5] = 1
                grid[i][j][4] = get_valid_sides(grid[i][j][3], grid[i][j][5])
                grid[i][j][0].rotate(360 - (90 * (grid[i][j][5] - 1)))
              else:
                grid[i][j][3] = 'CROSS'
                grid[i][j][5] = 1
                grid[i][j][4] = get_valid_sides(grid[i][j][3], grid[i][j][5])
            elif selection == 5:
              if i < rows - 1:
                if grid[i+1][j][3] == 'NO_WIRE':
                  grid[i][j][3] = 'UP_AND'
                  grid[i+1][j][3] = 'DOWN_AND'
                  grid[i][j][0] = gamebox.from_image(j * xScale + inputBoxWidth, i * yScale, uiElements[selection - 1])
                  grid[i][j][4] = [0, 0, 0, 1]
                  grid[i+1][j][4] = [0, 0, 1, 1]
            elif selection == 6:
              if i < rows - 1:
                if grid[i+1][j][3] == 'NO_WIRE':
                  grid[i][j][3] = 'UP_OR'
                  grid[i+1][j][3] = 'DOWN_OR'
                  grid[i][j][0] = gamebox.from_image(j * xScale + inputBoxWidth, i * yScale, uiElements[selection - 1])
                  grid[i][j][4] = [0, 0, 0, 1]
                  grid[i+1][j][4] = [0, 0, 1, 1]                
            elif selection == 7:
              if i < rows - 1:
                if grid[i+1][j][3] == 'NO_WIRE':
                  grid[i][j][3] = 'UP_XOR'
                  grid[i+1][j][3] = 'DOWN_XOR'
                  grid[i][j][0] = gamebox.from_image(j * xScale + inputBoxWidth, i * yScale, uiElements[selection - 1])
                  grid[i][j][4] = [0, 0, 0, 1]
                  grid[i+1][j][4] = [0, 0, 1, 1]
            elif selection == 8:
              grid[i][j][4] = [0, 1, 0, 0]
              grid[i][j][3] = 'NOT'
            elif selection == 9:
              if i != 4 or j != 20:
                if grid[i][j][3] == 'DOWN_AND' or grid[i][j][3] == 'DOWN_XOR' or grid[i][j][3] == 'DOWN_OR':
                  grid[i-1][j] = get_def_box(i-1, j)
                if grid[i][j][3] == 'UP_AND' or grid[i][j][3] == 'UP_XOR' or grid[i][j][3] == 'UP_OR':
                  grid[i+1][j] = get_def_box(i+1, j)
                grid[i][j] = get_def_box(i, j)
      
      if (grid[i][j][3] != 'NO_WIRE' and grid[i][j][1] == 'POWERED'):
        if grid[i][j][3] == 'STRAIGHT':
          grid[i][j][0] = gamebox.from_image(j * xScale + inputBoxWidth, i * yScale, 'straight_wire_on.png')
          grid[i][j][0].rotate(360 - (90 * (grid[i][j][5] - 1)))
        elif grid[i][j][3] == 'CORNER':
          grid[i][j][0] = gamebox.from_image(j * xScale + inputBoxWidth, i * yScale, 'corner_wire_on.png')
          grid[i][j][0].rotate(360 - (90 * (grid[i][j][5] - 1)))
        elif grid[i][j][3] == 'T':
          grid[i][j][0] = gamebox.from_image(j * xScale + inputBoxWidth, i * yScale, 't_wire_on.png')
          grid[i][j][0].rotate(360 - (90 * (grid[i][j][5] - 1)))
        elif grid[i][j][3] == 'CROSS':
          grid[i][j][0] = gamebox.from_image(j * xScale + inputBoxWidth, i * yScale, 'cross_wire_on.png')
          grid[i][j][0].rotate(360 - (90 * (grid[i][j][5] - 1)))
        elif grid[i][j][3] == 'LIGHT':
          grid[i][j][0] = gamebox.from_image(j * xScale + inputBoxWidth, i * yScale, 'light_on.png')
      if (grid[i][j][3] != 'DOWN_AND' and grid[i][j][3] != 'DOWN_OR' and grid[i][j][3] != 'DOWN_XOR'):
        camera.draw(grid[i][j][0])

  #add ui border
  camera.draw(borderBoxTop)
  camera.draw(borderBoxLeft)
  camera.draw(borderBoxBottom)
  camera.draw(borderBoxRight)

  #draw wire selection boxes and update them
  if pos != 0:
    if boxOne.contains(pos[0], pos[1]):
      boxOne.color = 'green'
      if selection != -1 or selection != 1:
        uiBoxes[selection - 1].color = '#282828'
      selection = 1
  camera.draw(boxOne)
  camera.draw(straightWireUI)
  
  if pos != 0:
    if boxTwo.contains(pos[0], pos[1]):
      if selection != -1 or selection != 2:
        uiBoxes[selection - 1].color = '#282828'
      boxTwo.color = 'green'
      selection = 2
  camera.draw(boxTwo)
  camera.draw(cornerWireUI)
  
  if pos != 0:
    if boxThree.contains(pos[0], pos[1]):
      if selection != -1 or selection != 3:
        uiBoxes[selection - 1].color = '#282828'
      boxThree.color = 'green'
      selection = 3
  camera.draw(boxThree)
  camera.draw(tWireUI)
  
  if pos != 0:
    if boxFour.contains(pos[0], pos[1]):
      if selection != -1 or selection != 4:
        uiBoxes[selection - 1].color = '#282828'
      boxFour.color = 'green'
      selection = 4
  camera.draw(boxFour)
  camera.draw(crossWireUI)

  #Draw Circuit Selection UI Elements
  if pos != 0:
    if boxFive.contains(pos[0], pos[1]):
      if selection != -1 or selection != 5:
        uiBoxes[selection - 1].color = '#282828'
      boxFive.color = 'green'
      selection = 5
  camera.draw(boxFive)
  camera.draw(andGateUI)

  if pos != 0:
    if boxSix.contains(pos[0], pos[1]):
      if selection != -1 or selection != 6:
        uiBoxes[selection - 1].color = '#282828'
      boxSix.color = 'green'
      selection = 6
  camera.draw(boxSix)
  camera.draw(orGateUI)

  if pos != 0:
    if boxSeven.contains(pos[0], pos[1]):
      if selection != -1 or selection != 7:
        uiBoxes[selection - 1].color = '#282828'
      boxSeven.color = 'green'
      selection = 7
  camera.draw(boxSeven)
  camera.draw(xorGateUI)

  if pos != 0:
    if boxEight.contains(pos[0], pos[1]):
      if selection != -1 or selection != 8:
        uiBoxes[selection - 1].color = '#282828'
      boxEight.color = 'green'
      selection = 8
  camera.draw(boxEight)
  camera.draw(notGateUI)

  if pos != 0:
    if boxNine.contains(pos[0], pos[1]):
      if selection != -1 or selection != 9:
        uiBoxes[selection - 1].color = '#282828'
      boxNine.color = 'green'
      selection = 9
  camera.draw(boxNine)
  camera.draw(deleteUI)

  if pos != 0:
    if boxTen.contains(pos[0], pos[1]):
      for w in range(rows):
        for t in range(cols):
          if w != 4 or t != 20:
            grid[w][t] = get_def_box(w, t)
  camera.draw(boxTen)
  camera.draw(resetUI)
  
  camera.display()

gamebox.timer_loop(180, tick)
