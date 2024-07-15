from interface import Button
from interface import Card
from interface import Player

def setup():
    global titleButton, titleScreen, instructionsScreen, instructionsButton, gameplayScreen, cards, selectedCards, ratios, players, playerIndex, table, endingScreen, replayButton, winner, wood, viewTableButton, trigChart, tableScreen, startTime, backButton, delayClick, trigFish, cardback
    size(500,500)

    # Object, screen, array initialization
    player1 = Player([255, 0, 0])
    player2 = Player([0, 0, 255])
    player1.turn = True
    players = [player1, player2]
    titleScreen = True
    titleButton = Button([50, 300], [450, 400]) 
    instructionsScreen = False
    instructionsButton = Button([30, 440], [470, 490])
    viewTableButton = Button([30, 390], [470, 440])
    gameplayScreen = False
    endingScreen = False
    tableScreen = False
    replayButton = Button([30, 400], [470, 450])
    backButton = Button([width / 2 - 50, 10], [width / 2 + 50, 40])
    cards = []
    
    # Image initialization
    wood = loadImage("wood.jpg")
    table = loadImage("table.jpeg")
    trigChart = loadImage("trigtable.jpeg")
    cardback = loadImage("cardback.png")
    trigFish = loadImage("trigfish.png")
    
    # Variable initialization
    winner = ""
    startTime = 0
    delayClick = 0
    playerIndex = 0

    # All pairs of special angles and their respective ratios stored in 2D array
    ratios = [["sin0", "0"], ["sin30", "1/2"], ["sin45", "sqrt2/2"], ["sin60", "sqrt3/2"], ["sin90", "1"], ["cos0", "1"], ["cos30", "sqrt3/2"], 
              ["cos45", "sqrt2/2"], ["cos60", "1/2"], ["cos90", "0"], ["tan0", "0"], ["tan30", "sqrt3/3"], ["tan45", "1"], ["tan60", "sqrt3"], ["tan90", "undef."]]
    spotsLeft = []
    selectedCards = []
    
    # Grid setup for cards
    for r in range(1, 6):
        for c in range(1, 7):
            spotsLeft.append([c * 80 - 55, r * 90 - 50])

    # Card shuffle/randomization into grid
    for i in range(len(ratios)):
        for z in range(len(ratios[i])):
            rand = int(random(len(spotsLeft)))
            randX = spotsLeft[rand][0]
            randY = spotsLeft[rand][1]
            cards.append(Card(randX, randY, ratios[i][z]))
            spotsLeft.pop(rand)
            
    for i in range(len(cards)):
        print(cards[i])

def draw():
    global titleButton, titleScreen, instructionsScreen, instructionsButton, gameplayScreen, cards, selectedCards, ratios, startTime, playerIndex, table, endingScreen, replayButton, winner, wood, viewTableButton, backButton, trigFish, cardback

    if titleScreen:
        background(255, 165, 0)
        textSize(70)
        textAlign(CENTER)
        fill(255)
        text("Trigfish", width / 2, 100)
        titleButton.display("Start Game", 50)
        image(trigFish, 150, 110, 200, 200)

    if instructionsScreen:
        background(255, 165, 0)
        textSize(50)
        textAlign(CENTER)
        fill(255)
        text("Instructions", width / 2, 85)
        rect(30, 100, 440, 285)
        textSize(20)
        fill(0)
        text("Trigfish is a 2-player game that helps\nstudents reinforce the different special\nangles in trig. Just like the card game\n'Goldfish', each player takes turn\nflipping cards until they find a matching\ntrig ratio. The turn only switches to\nthe next player once you get an inccorect\npair. The player with the most pairs\nat the end will win the game.", width / 2, 130)
        instructionsButton.display("Play", 30)  
        viewTableButton.display("View Trig Ratios", 30, [80, 80, 80])

    if tableScreen:
        image(trigChart, 0, 40, width, height - 40)
        backButton.display("Back", 20, [0, 0, 243])

    if gameplayScreen:
        # Background content
        stroke(0)
        strokeWeight(1)
        background(255, 165, 0)
        
        image(table, 0, 0, width, height)
        fill(255)
        rect(0, 0, width, 33)
        image(wood, 0, 0, width, 33)

        # Score display
        textSize(20)
        fill(players[0].colour[0], players[0].colour[1], players[0].colour[2])
        text(players[0].score, 30, 25)
        fill(players[1].colour[0], players[1].colour[1], players[1].colour[2])
        text(players[1].score, width - 30, 25)

        # Turn display (index 0 = player 1; index 1 = player 2)
        if players[0].turn:
            textSize(20)
            fill(players[0].colour[0], players[0].colour[1], players[0].colour[2])
            text("Player 1 Turn", width / 2, 25)
        else:
            textSize(20)
            fill(players[1].colour[0], players[1].colour[1], players[1].colour[2])
            text("Player 2 Turn", width / 2, 25)

        # Cards display
        for i in range(len(cards)):
            cards[i].display(cardback)

        # Selection of a pair of cards
        if len(selectedCards) == 2:
            if players[playerIndex].turn:
                for i in range(len(ratios)):
                    if selectedCards[0].value in ratios[i] and selectedCards[1].value in ratios[i] and selectedCards[0].value != selectedCards[1].value and selectedCards[0].flipped == False:
                        players[playerIndex].score += 1
                        selectedCards[0].flipped = True
                        selectedCards[1].flipped = True
                        selectedCards[0].border = players[playerIndex].colour
                        selectedCards[1].border = players[playerIndex].colour

            # Wait 1.5 seconds before flipping card/next turn        
            if millis() - startTime > 1500:
                selectedCards[0].selected = False
                selectedCards[1].selected = False
                if selectedCards[0].flipped == False:
                    players[playerIndex].turn = False
                    players[playerIndex * -1 + 1].turn = True
                    playerIndex = playerIndex * -1 + 1
                selectedCards = []
        
        # Finish game when all cards flipped
        if players[0].score + players[1].score == len(ratios):
            if players[0].score > players[1].score:
                winner = "Player 1"
            else:
                winner = "Player 2"
            gameplayScreen = False
            endingScreen = True

    # Ending of game
    if endingScreen:
        background(255, 165, 0)
        stroke(0)
        textAlign(CENTER)
        textSize(45)
        fill(255)
        text("Congratulations,\n" + winner + "!\nYou are the winner!", width / 2, 100)
        textSize(80)
        text("vs", width / 2, 350)
        fill(players[0].colour[0], players[0].colour[1], players[0].colour[2])
        text(str(players[0].score), 100, 350)
        fill(players[1].colour[0], players[1].colour[1], players[1].colour[2])
        text(str(players[1].score), width - 100, 350)
        replayButton.display("Play Again", 30)
        

def mouseClicked():
    global titleButton, titleScreen, instructionsScreen, instructionsButton, gameplayScreen, cards, selectedCards, startTime, endingScreen, replayButton, viewTableButton, trigChart, tableScreen, backButton, delayClick

    # Used to track time between second card selection and when to go to next turn
    if len(selectedCards) == 1:
        startTime = millis()

    # Start button for title screen into instructions screen
    if titleScreen and titleButton.insideButton():
        titleScreen = False
        instructionsScreen = True
        delayClick = millis()

    # Card selection
    if gameplayScreen and len(selectedCards) < 2:
        for i in range(len(cards)):
            if cards[i].insideCard() and cards[i].selected == False and cards[i].flipped == False:
                cards[i].selected = True
                selectedCards.append(cards[i])        

    # View trig ratios button
    if instructionsScreen and viewTableButton.insideButton() and millis() - delayClick > 50:
        tableScreen = True
        instructionsScreen = False
        
    # Click back button to leave trig chart
    if tableScreen and backButton.insideButton():
        tableScreen = False
        instructionsScreen = True

    # Play button from instructions screen into gameplay screen
    if instructionsScreen and instructionsButton.insideButton():
        instructionsScreen = False
        gameplayScreen = True
    
    # Play again button
    if endingScreen and replayButton.insideButton():
        print("Restarting Game...")
        setup()
