
################################
#                              #
# SNAKE.PY                     #
#                              #
# Author:  Lenny Jakobsen      #
# Date:    16 november 2020    #
#                              #
################################

###########
# IMPORTS #
###########


from gturtle import *
from entrydialog import *
import random


#####################
# GLOBAL PROPERTIES #
#####################


# Key codes
keyCodeLeft = 37
keyCodeRight = 39
keyCodeUp = 38
keyCodeDown = 40
keyCodeEnter = 10
keyCodeEsc = 27

# Constant settings
mapSize = [500, 500] #size of the map (x, y)
frameSize = [500, 500] #size of the window (x, y)
setFramePositionCenter()
setPlaygroundSize(frameSize[0], frameSize[1]) 
stoneSize = [32, 32] #size of an imaginary box around the stones
stoneCloneNames = ["stoneTurtle1","stoneTurtle2","stoneTurtle3","stoneTurtle4","stoneTurtle5","stoneTurtle6","stoneTurtle7", "stoneTurtle8","stoneTurtle9"] #the names with that the stones can be called
numberOfStones = 3 #number of stones that are generated


# General properties
points = 0
highScore = 0
lastKey = None
name = ""
startingMovementSpeed = 6
movementSpeed = startingMovementSpeed
msScaling = 1 #the value added to the movementSpeed 
snakePos = [None, None]
isAlive = None



#EntryItems 
#(Objects of diverse Entry-classes)
wasdSteuerung = CheckEntry("WASD-Steuerung", False) 
startingSpeed = FloatEntry("Anfangsgeschwindigkeit", 6) 
stoneSlider = SliderEntry(0,10,3,1,1) 
applyChangesButton = ButtonEntry("Änderungen übernehmen")  
stoneBeschriftung = StringEntry("Anzahl Steine                                                         ") #creates a StringEntry as a title for the stoneSlider
stoneBeschriftung.setEditable(False) 

#Panes
#(Objects of the EntryPane-class, that can show the EntryItems)
wasdSteuerungPane = EntryPane(wasdSteuerung) 
stoneSliderPane = EntryPane(stoneSlider) 
startingSpeedPane = EntryPane(startingSpeed) 
applyChangesButtonPane = EntryPane(applyChangesButton) 
stoneBeschriftungPane = EntryPane(stoneBeschriftung) 



#Turtle properties
    #FrameTurtle
frameTurtle = makeTurtle()
frameTurtle.hideTurtle()
addStatusBar(110) 
    #snakeTurtle
snakeTurtle = Turtle(frameTurtle, "snake.png")
snakeTurtle.penUp()
snakeTurtle.speed(60)
    #appleTurtle
appleTurtle = Turtle(frameTurtle, "apple.png") 
appleTurtle.hideTurtle()
    #stoneTurtle
stoneTurtle = Turtle(frameTurtle, "stone.png")
stoneTurtle.setPos(-1000, -1000)


#############
# FUNCTIONS #
#############




#opens a window with options
def openOptions(): 
    global wasdSteuerung
    global startingSpeed
    global stoneSlider
    global startingMovementSpeed
    global movementSpeed
    global numberOfStones
    global keyCodeLeft
    global keyCodeRight
    global keyCodeUp
    global keyCodeDown
    
    #creates the window
    options = EntryDialog(wasdSteuerungPane, startingSpeedPane, stoneBeschriftungPane, stoneSliderPane, applyChangesButtonPane) #uses the Panes defined above to make a window with options
    options.setTitle("Optionen") #sets the title of the window
    options.setAlwaysOnTop(True) #makes it impossible for the window to go to the background
    
    #applies the changes
    optionsAreOpened = True
    while optionsAreOpened: #waits till the apply-changes-button is pressed
        if applyChangesButton.isTouched(): #checks if the button has been pressed
            #WASD-Steuerung
            #checks if the WASD-Steuerung-Box is sellected
            if wasdSteuerung.getValue(): 
                #changes the values to A, D, W & S
                keyCodeLeft = 65
                keyCodeRight = 68
                keyCodeUp = 87
                keyCodeDown = 83
            #checks if the WASD-Steuerung-Box is not sellected
            if wasdSteuerung.getValue() == False: 
                #changes the values to left, right, up & down
                keyCodeLeft = 37
                keyCodeRight = 39
                keyCodeUp = 38
                keyCodeDown = 40
            
            #startingSpeed
            startingSpeedValue = startingSpeed.getValue() 
            #increases the movementspeed if its bellow the maximum
            if startingSpeedValue > 37:
                movementSpeed = 37 
                snakeTurtle.speed(movementSpeed * 10) #increases the turtle speed as well to avoid lag
            #sets movementspeed to its maximum if its above that
            if startingSpeedValue <= 37:
                startingMovementSpeed = startingSpeedValue
                movementSpeed = startingSpeedValue
                snakeTurtle.speed(movementSpeed * 10) #adjusts the turtle speed to avoid it being to fast
            
            #numberOfStones
            numberOfStones = stoneSlider.getValue() #changes the global numberOfStones-value
            
            #close Options
            options.dispose() #closes the window
            optionsAreOpened = False #ends the loop





#generates stones based on the numberOfStones-value
def generateStones(numberOfStones):
    i = 0
    while i <= numberOfStones - 1:
        stoneTurtle.setPos(random.randint(-1 * (mapSize[0]/2 - 10), mapSize[0]/2 - 10), random.randint(-1 * (mapSize[1]/2 - 10), (mapSize[1]/2 - 10))) #sets the stoneTurtle to a random position
        globals()[stoneCloneNames[i]] = stoneTurtle.clone() #automatically takes the slot with the number i from the stoneClonesNames-list and creates a stoneTurtle-clone with its current value as its name
        i += 1

#deletes all the before generated stones        
def deleteStones(numberOfStones):
    i = 0
    while i < numberOfStones:
        globals()[stoneCloneNames[i]].hideTurtle() #hides the soon deleted clone to avoid a graphic bug, in wich the stone is still visible, even tho the object is deleted
        del globals()[stoneCloneNames[i]] #deletes the clone
        i += 1
                    
    
    

#prepares the map 
def drawMap (color): 
    clearScreen() 
    
    #draw the border of the map with given color
    frameTurtle.setPos(-1 * mapSize[0]/2, -1 * mapSize[1]/2)
    frameTurtle.setPenColor(color)
    frameTurtle.setPenWidth(10)
    repeat(2):
        frameTurtle.fd(mapSize[0])
        frameTurtle.rt(90)
        frameTurtle.fd(mapSize[1])
        frameTurtle.rt(90)
        
    #prepares the statusbar
    setStatusText("Press esc to open the options\nPress enter to start")
    showStatusBar(True)
    
    #waits in the "starting menu"
    waitingToStartGame = True
    while waitingToStartGame:
        waitForInput = getKeyCodeWait()
        #opens the options
        if waitForInput == keyCodeEsc:
            openOptions()
            waitingToStartGame = False
        #ignores all input ecxept Esc & Enter
        if waitForInput != keyCodeEnter:
            continue
        #starts the game
        if waitForInput == keyCodeEnter:
            waitingToStartGame = False
            
    #generates some stones that can be deleted by the deleteStones message later (to avoid errors)
    generateStones(numberOfStones)
    
    


#checks witch key was pressed and turns the turtle in this direction if its not against the rules (like 180-degree-turns)
def turn():
    heading = snakeTurtle.heading()
    lastKey = getKeyCode()
       
    if lastKey == keyCodeRight:
        if heading == 0 or heading == 180:
            snakeTurtle.heading(90)
    if lastKey == keyCodeLeft:
        if heading == 0 or heading == 180:
            snakeTurtle.heading(270)
    if lastKey == keyCodeUp:
        if heading == 90 or heading == 270:
            snakeTurtle.heading(0)
    if lastKey == keyCodeDown:
        if heading == 90 or heading == 270:
            snakeTurtle.heading(180)





#checks if the given coordinates are touching a stone
def TouchesStone(PosX, PosY): 
    i = 0
    while i < numberOfStones - 1: #repeats once for every generated stone
        #checks if the stoneTurtle is touched
        if PosX >= stoneTurtle.getX() - stoneSize[0]/2 and PosX <= stoneTurtle.getX() + stoneSize[0]/2 and PosY >= stoneTurtle.getY() - stoneSize[1]/2 and PosY <= stoneTurtle.getY() + stoneSize[1]/2: 
            return True
        #checks if the stone with the name, that equals to the name in the stoneCloneNames-list in the slot with the number i, is touched
        elif PosX >= globals()[stoneCloneNames[i]].getX() - stoneSize[0]/2 and PosX <= globals()[stoneCloneNames[i]].getX() + stoneSize[0]/2 and PosY >= globals()[stoneCloneNames[i]].getY() - stoneSize[1]/2 and PosY <= globals()[stoneCloneNames[i]].getY() + stoneSize[1]/2: 
            return True
        #repeats the loop with the next number
        else: 
            i+=1
    return False

#checks if the given coordinates are touching the apple
def touchesApple (PosX, PosY): 
    if PosX >= appleTurtle.getX() - stoneSize[0]/2 and PosX <= appleTurtle.getX() + stoneSize[0]/2 and PosY >= appleTurtle.getY() - stoneSize[1]/2 and PosY <= appleTurtle.getY() + stoneSize[1]/2:
        return True
    else:
        return False

#randomly changes the apples position, repeats process if stone is touched
def shuffleApple (): 
    appleTurtle.setPos(random.randint(-1 * (mapSize[0]/2 -10), mapSize[0]/2 - 10), random.randint(-1 * (mapSize[1]/2 - 10), mapSize[1]/2 - 10))
    if TouchesStone(appleTurtle.getX, appleTurtle.getY):
        shuffleApple()
    




#checks if the snake is alive
def snakeTurtleIsAlive(PosX, PosY):
    #Is the snake still inside the map
    if PosX >= mapSize[0]/2 - 10 or PosX <= -1 * (mapSize[0]/2 - 10) or PosY >= mapSize[1]/2 - 10 or PosY <= -1 * (mapSize[1]/2 -10):
        return False
    #Is the snake touching stone
    if TouchesStone(PosX, PosY):
        return False
    else:
        return True


#lets you input a name if you achieve a new highscore and saves it
def waitForInputName(): 
    global name
    
    if points > highScore:
        name = inputString("Name eingeben")
        if name == "" or  name == None:
            name = "Anonymus"
        else:
            print "Name entered: " + name 




#runs the game
def play(): 
    global points 
    global movementSpeed
    global snakePos
    global highScore
    global isAlive

    #resets the snake & apple
    snakeTurtle.setPos(0,0)
    snakeTurtle.heading(0)
    shuffleApple()
    appleTurtle.showTurtle()

    #resets the points and displays them
    points = 0
        #checks if the highscore is 0 and doesnt display it if thats case
    if highScore != 0:
        setStatusText("score: " + str(points) + "\nhighscore: " + name + "(" + str(highScore) + ")")
    else:
        setStatusText("score: " + str(points))

    
    isAlive = True
    while (isAlive): #repeats while snake is alive
        
        
        #moves the snake
        turn()
        snakeTurtle.fd(movementSpeed)
        
        #updates the Position of the snake
        snakePos = [snakeTurtle.getX(), snakeTurtle.getY()]

        #checks if the snake is still alive
        isAlive = snakeTurtleIsAlive(snakePos[0], snakePos[1])
        
        #checks if the snake has colected an apple
        if touchesApple(snakePos[0], snakePos[1]):
            playTone("a", 10, block = False, instrument = "piano")
            #manages points and highscore
            points += 100
                #hides the highscore if no one has achieved one yet
            if highScore == 0:
                setStatusText("score: " + str(points))
                #shows the highscore if its more than 0
            else:
                setStatusText("score: " + str(points) + "\nhighscore: " + name + "(" + str(highScore) + ")")
            shuffleApple()
            #increase movementSpeed
                #increses movementSpeed by its scaling if its below the maximum
            if movementSpeed < 37:
                movementSpeed += msScaling
                snakeTurtle.speed(movementSpeed * 10) #increases the turtles speed as well to reduce lag
                #checks if the movementSpeed is now above the maximum value and resets it if thats the case
            if movementSpeed + msScaling > 37:
                movementSpeed = 37
                snakeTurtle.speed(movementSpeed * 10) #adjusts the turtles speed so that its not to fast
        
    #the snake died
    playTone("g", 100, instrument = "tuba")
    setStatusText("GAME OVER!\nPress Esc for options & Enter to play again")
    waitForInputName()
        #changes highscore
    if points > highScore:
        highScore = points
        #waits for the player to restart
    waitingToRestart = True
    while waitingToRestart:
        keyInput = getKeyCodeWait()
        #opens Options
        if keyInput == keyCodeEsc:
            #stones & changes
            deleteStones(numberOfStones) #clears the old stones
            openOptions()
            generateStones(numberOfStones) #generates new stones with the maibe new value from options 
            #prepares everything
            movementSpeed = startingMovementSpeed
            setStatusText("score: " + str(points) + "\nhighscore: " + name + "(" + str(highScore) + ")")
                #resets snake
            snakeTurtle.setPos(0, 0)
            snakeTurtle.heading(0)
                #stops the loop and restart
            waitingToRestart = False
            play()
            
        #instantly restart
        if keyInput == keyCodeEnter:
            #stones
            deleteStones(numberOfStones) #clears the old stones
            generateStones(numberOfStones) #generates new stones
            #prepare everything
            movementSpeed = startingMovementSpeed
            setStatusText("score: " + str(points) + "\nhighscore: " + name + "(" + str(highScore) + ")")
                #reset snake
            snakeTurtle.setPos(0, 0)
            snakeTurtle.heading(0)
                #stop the loop and restart
            waitingToRestart = False
            play()
            
    
    
        
        
        
    

#the function where the program starts
def main(): 

    drawMap("blue")

    play()





#############
# MAIN CODE #
#############

main()