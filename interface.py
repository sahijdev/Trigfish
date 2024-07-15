class Button:
    def __init__(self, topLeft, bottomRight):
        self.x1 = topLeft[0]
        self.x2 = bottomRight[0]
        self.y1 = topLeft[1]
        self.y2 = bottomRight[1]
        self.width = self.x2 - self.x1
        self.height = self.y2 - self.y1

    def display(self, message, fontSize, colour = [12, 204, 83]):
        fill(colour[0], colour[1], colour[2])
        rect(self.x1, self.y1, self.width, self.height)
        fill(255)
        textSize(fontSize)
        text(message, (self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2 + self.height / 4)
    
    def insideButton(self):
        # Checks if mouse is inside button
        if self.x1 < mouseX < self.x2 and self.y1 < mouseY < self.y2: 
            return True
        else:
            return False

class Card:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.selected = False
        self.flipped = False
        self.border = [0, 0, 0]

    def __str__(self):
        return str(self.x) + ", " + str(self.y) + ": " + str(self.value)

    # Used to handle printing of an array of objects
    def __repr__(self):
        return str(self)

    def display(self, cardback):
        # What to show if card is not flipped
        image(cardback, self.x, self.y, 60, 80)
        
        # What to show if card gets selected or permanently flipped
        if self.selected or self.flipped:
            stroke(0)
            noStroke()
            fill(255)
            rect(self.x, self.y, 60, 80)
            noFill()
            # Only show if card is scored
            if self.flipped:
                strokeWeight(5)
                stroke(self.border[0], self.border[1], self.border[2])
                rect(self.x - 5, self.y - 5, 70, 90)
            fill(0)
            textSize(20)
            text(self.value, self.x + 30, self.y + 40)
            
    def insideCard(self):
        # Checks if mouse is inside card
        if self.x < mouseX < self.x + 60 and self.y < mouseY < self.y + 80: 
            return True
        else:
            return False  
    
class Player:
    def __init__(self, colour):
        self.turn = False
        self.score = 0
        self.colour = colour
