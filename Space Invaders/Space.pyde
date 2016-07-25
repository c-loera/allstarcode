enemies = []
bullets = []

class Bullet(object):
  
    def __init__(self,x1,y1,size1,xvel1,yvel1,damage1,owner1):
        self.x = x1
        self.y = y1
        self.Size = size1
        self.xvel = xvel1
        self.yvel = yvel1
        self.damage = damage1
        self.Owner = owner1
        bullets.append(self)
        
    def render(self):
        fill(0,0,255)
        ellipse(self.x,self.y,self.Size,self.Size)
    def move(self):
        self.x += self.xvel
        self.y += self.yvel
    def kill(self):
        del bullets[bullets.index(self)]
    def run(self):
        self.render()
        self.move()
        self.collide()
        if(self.x > width or self.x < 0 or self.y > height or self.y < 0):
            self.kill()
    def collide(self):
        for i in enemies:
            withinX = self.x < i.x + i.Size/2 and self.x > i.x - i.Size
            withinY = self.y < i.y + i.Size/2 and self.y > i.y - i.Size
            if withinX and withinY and i != self.Owner:
                i.health -= self.damage
                self.kill()
        i = player
        withinX = self.x < i.x + i.Size/2 and self.x > i.x - i.Size
        withinY = self.y < i.y + i.Size/2 and self.y > i.y - i.Size
        if withinX and withinY and i != self.Owner:
            i.health -= self.damage
            self.kill()

class Enemy(object):

    def __init__(self,x1,y1,xvel1,yvel1,health1,size1):
        self.health = health1
        self.maxhealth = health1
        self.x = x1
        self.y = y1
        self.Size = size1
        enemies.append(self)
        self.xvel = xvel1
        self.yvel = yvel1
    
    def render(self):
        # fill(0,255,0)
        img = loadImage("enemyshipblueee.png")
        image(img, self.x - 7.5, self.y)
        #ellipse(self.x,self.y,self.Size,self.Size)
    
    def movement(self):
        self.x += self.xvel
        self.y += self.yvel
    
    def run(self):
        self.render() 
        self.movement()
        self.die()
        self.drawHealth()
        if self.y > height :
            gameEnd()
        
    def die(self):
        if self.health <= 0:
            del enemies[enemies.index(self)]
    
    def drawHealth(self):
        stroke(255, 0, 0)
        line(self.x-self.Size, self.y-self.Size, self.x+self.Size, self.y-self.Size)
        stroke(0, 255, 0)
        line(self.x-self.Size, self.y-self.Size, (self.health*((self.x+self.Size)-(self.x-self.Size)))/self.maxhealth + (self.x-self.Size), self.y-self.Size)  
        stroke(0, 0, 0)
        

class Player(object):
   
    def __init__(self,health1,x1,y1,size1):
        self.health = health1
        self.maxhealth = health1
        self.x = x1
        self.y = y1
        self.Size = size1
        
        
    def run(self):
        self.render()
        self.drawHealth() 
        self.die()
            
    def render(self):
        img = loadImage("URSHIP.png")
        image(img, self.x - 15, self.y)
        # fill(255,0,0)
        # ellipse(self.x,self.y,self.Size,self.Size)
        
    def drawHealth(self):
        stroke(255, 0, 0)
        line(self.x-self.Size, self.y-self.Size, self.x+self.Size, self.y-self.Size)
        stroke(0, 255, 0)
        line(self.x-self.Size, self.y-self.Size, (self.health*((self.x+self.Size)-(self.x-self.Size)))/self.maxhealth + (self.x-self.Size), self.y-self.Size)  
        stroke(0, 0, 0)
    
    def die(self):
        if self.health <= 0:
            gameEnd()
    
    

            
def setup():
    size(600,680)
    global player,shotDelay,spawnDelay,spawned,test,wavesMade,currentLevel,notSpawned,levelList,gameOver,enemyDelay
    gameOver = False
    player = Player(5,width/2,height - 50,10)
    currentLevel = 0
    enemyDelay = 0
    wavesMade = 0
    shotDelay = 0 
    spawnDelay = 0
    notSpawned = True
    levelList = [[2,3],[4,2],[5,2],[3,4],[7,2],[5,3],[4,4],[3,6],[4,5]]
    
    
def makeWave(enemies,amount): 
    global wavesMade,spawnDelay,notSpawned
    if wavesMade < amount:
        while millis() > spawnDelay:
            for i in range(enemies-1):
                Enemy((i+1)*((width)/enemies),50,0,.5,1,10)
            spawnDelay = millis() + 750
            wavesMade += 1
    else:
        notSpawned = False
        wavesMade = 0
def gameEnd():
    global gameOver
    gameOver = True
def draw(): 
    noStroke()
    textMode(CENTER)   
    background(255)
    global player,shotDelay,spawnDelay,spawned,test,wavesMade,currentLevel,notSpawned,levelList,gameOver,enemyDelay
    player.run()
    for i in enemies:
        i.run()
    for i in bullets:
        i.run()    
    if keyPressed:
        if keyCode == 39: 
            player.x += 3
        if keyCode == 37:
            player.x -= 3
        if keyCode == 38:
            if notSpawned == False and currentLevel != len(levelList) -1 and len(enemies) == 0:
                currentLevel += 1 
                print(currentLevel)
                print(len(levelList))
                notSpawned = True
        if keyCode == 40:
            if(millis() > shotDelay):
                bullet = Bullet(player.x,player.y,5,0,-3,1,player)
                shotDelay = millis() + 400
    if currentLevel == len(levelList) - 1 and len(enemies) == 0:
        fill(0,255,0)            
        textSize(72)            
        textMode(CENTER)            
        text("You Win!",width/4,100)
    if notSpawned:
        makeWave(levelList[currentLevel][0],levelList[currentLevel][1])
    if gameOver:
        background(0)
        fill(255,0,0)            
        textSize(72)            
        textMode(CENTER)            
        text("Game Over",0,100)
        textSize(48)
        text("Restart Game To Try Again",0,200)
    if millis() > enemyDelay and len(enemies) != 0:
        print(random(0,len(enemies) - 1))
        i = enemies[int(random(0,len(enemies) - 1))]
        bullet = Bullet(i.x,i.y,5,0,3,1,i)
        enemyDelay = millis() + 3000
            
        


 

            
        

        