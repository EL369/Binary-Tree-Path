##############################################################################
#Game: Finding longest path
#Author: Fan, Evelyn
#Date: Jan 22 2018


#Variable Map
#NAME               TYPE               RESTRICTIONS                 USE
#page               int                0 - 3                        To determine what page we are on and to display the correct content
#player1            string             A - Z                        To store the names
#player2            string             A - Z                        To store the names
#turn               int                1 - 43                       To figure out whose turn it is and to use for resetting the board when its a tie
#winner             int                1 or 2                       To display who wins
#instructions       list of strings    -                            To display instructions of the game
#board              array              0 - 2                        To store the players pieces
#startpage          image              -                            Start page image
#startbutton        image              -                            Start buttons for the start page so we can place it in the correct place
#cloud              image              -                            Another background image for game
#boardpic           image              -                            Image for the game board 
#piece1             image              -                            Image for a piece for the board
#piece2             image              -                            Image for a piece for the board
#winningpage        image              -                            Another background image for the game
#tie                image              -                            An image that overlays in winning page to represent a tie
#music              .mp3               -                            Used with minim library to import sound to game
#time               library            -                            Used to add delay when someone wins
#lbfile             string             -                            File name of leaderboard file


#array list for setting up the board
graph = {}
class Board:
    board = [[2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2]]
    turn = 0
    def gameover(self):
        isgameover = False
        for i in self.board[0]:
            if i != 2:
                isgameover = True
                break
        return isgameover
    
    def restriction(self):
        candrop = True
        for i in range(150,850,100):    # These codes are used to make sure that no same kinds of coins are beside each other
            if mouseX > i and mouseX < i+100:
                for x in range(6):
                    row = 5-x
                    col = (i-150)//100
                    if self.board[row][col] == 2:
                        if col < 6 and self.board[row][col+1] == self.turn % 2:
                            candrop = False
                        if col > 0 and self.board[row][col-1] == self.turn % 2:
                            candrop = False
                        break
        if candrop and 150<= mouseX <= 850:
            return self.drop_piece(row,col)
                            

    def drop_piece(self,row,col):
        '''To change the item in board and create piece object'''
        self.board[row][col] = self.turn % 2 # drop piece on the board
        graph[(row,col)] = Piece(row,col,self.turn) # create object of that piece
        self.turn += 1
    
    def dfs(self, graph, node, visited): 
        ''' To find every place that node can go to and return them as a list'''
        if node not in visited:
            visited.append(node)
            for n in graph[node].path:
                self.dfs(graph, n, visited)
        return visited
    
    def find_all_paths(self, graph, start, end, path=[]):
        '''receives the start and ends. Finds all the path between them'''
        path = path + [start]
        if start == end:
            return [path]
        if start not in graph:
            return []
        paths = []
        for node in graph[start].path:
            if node not in path:
                newpaths = self.find_all_paths(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths
    

class Piece:
    def __init__ (self,row, col, turn):
        self.row = row
        self.col = col
        self.kind = turn % 2
        self.path = []
    def adjacent(self,board):
        '''To find the adjacent(top, upleft, upright) coins'''
        if self.row > 0:
            if self.col > 0 and board[self.row - 1][self.col - 1] == self.kind:
                self.path.append((self.row - 1, self.col - 1))
            if self.col < 6 and board[self.row - 1][self.col + 1] == self.kind:
                self.path.append((self.row - 1, self.col + 1))
            if board[self.row - 1][self.col] == self.kind:
                self.path.append((self.row - 1,self.col))


def readFileToList(filename):
    # Read item from file to list
    file = open(filename)
    listfromfile = []
    text = file.readlines()
    for line in text:
        line = line.strip()
        row = ""
        for c in line:
            row = row + c
        addrow = row.split(",")
        listfromfile.append( addrow )
    return ( listfromfile )
    
    
def sort2D(datalist, numitems, whichcolumn ):
    for i in range (1, numitems):
        swap = False
        for j in range (numitems - i):
            if datalist[j][whichcolumn] < datalist[j+1][whichcolumn]:
                temp = datalist[j]
                datalist[j] = datalist [j+1]
                datalist [j+1] = temp
                swap = True
        if not swap :
            break
    return (datalist) 


def AppendToFile(filename, data):
    file = open(filename, "a")
    file.write(data + "\n")
    file.close()
    
gameboard = Board() # Create board object
page = 0   #starts at the start page
turn = 0   #start's off with player 2
winner = 0 #used to know who the winner is


def setup():
    global startpage,startbutton,cloud,page,boardpic,piece1,piece2,winningpage, tie, backg, rules, lb
    global instructions,graph,visited, root,paths
    global playername, lbfile
    visited = []
    root = []
    paths = []
    playername="" #Name of player
    #list all the instructions
    instructions=["Players cannot put a coin beside the same type.", 
                  "Game ends when a coin reaches the top.", 
                  "Finds the longest path of white coins",
                  "Shows it on the screen with lines connected",
                  "Press ENTER to return"]
                  

    # Initializing images ############################################
    startpage=loadImage("startpage.PNG")
    startbutton=loadImage("start.png")
    cloud=loadImage("boardbackground.jpg")
    boardpic=loadImage("board.png")
    piece1 = loadImage("piece1.png")
    piece2 = loadImage("piece2.png")
    # winningpage = loadImage("winningpage.jpg")
    # tie = loadImage("tiegame.jpg")
    backg = loadImage("background.jpg")
    rules = loadImage("qmark.png")
    lb = loadImage("lb.png")
    open("leaderboard.txt", "w")
    lbfile = "leaderboard.txt"
    
    size (1000,700)
    
    #Importing sound library, minim
    add_library("minim")
    minim = Minim(this)
    music = minim.loadFile("music.mp3")
    music.play()
    music.loop()
    
def draw():
    global playername,lbfile
    global page,startpage,startbutton,cloud,boardpic,piece1,piece2,turn,winningpage,winner,instructions, tie, backg, rules, lb
    #Starting page for set of rules and requires enter to start the game
    if page == 0:
       #This page is for:Name input
       #                 Mouse Press confirmation
       #                 Start Button
       
       #Code for layout of images and text on this page
       image(startpage,0,0,1000,700)
       image(startbutton,400,500,200,100)
       textSize(40)
       textAlign(LEFT)
       stroke(500)
       text("Player:",100,300,200,50)
       stroke(50)
       stroke(255)
       line(100,300,900,300)
       line(100,350,900,350)
       #Display's player name here
       text(playername,280,300,800,50)
       image(rules,150,500,100,100)
       image(lb,750,500,100,100)
        
        
    if page == 1:
        # Instruction page
        image(backg,0,0,1000,700)
        
        #Display instructions on the pages
        for i in range(len(instructions)):
            textSize(40)
            textAlign(CENTER)
            stroke(115)
            text(instructions[i],0,(i*50)+250,1000,700)



    if page == 2:
            #Page 2 is for: The visuals of where the game occur
            #               An animation of where the pieces are about to be dropped            
            
            # Displays the image on the top of the game board
            if not gameboard.gameover():
                image(cloud,0,0,1000,700)
                image(boardpic,150,100)
                for i in range(150,850,100):
                    if mouseX > i and mouseX < i+100:
                        if gameboard.turn%2 == 0:
                            image(piece1,i,10)
                            image(piece1,15,200)
                        else:
                            image(piece2,i,10)
                            image(piece2,885,200)
                            
                # To put the pieces on the board
            for x in range (7):
                for y in range (6):
                    if gameboard.board[y][x] == 0:
                        image(piece1,155+x*100,105+y*100)
                    if gameboard.board[y][x] == 1:
                        image(piece2,155+x*100,105+y*100)
            
                
    if page == 3:
        # Read from file and shows the leaderboard
        leaderboard = readFileToList(lbfile)
        print leaderboard  
        for i in range (len(leaderboard)):  # this for loop chagnes the scores from string into an integer
            leaderboard [i][1] = int(leaderboard[i][1])
        leaderboard = sort2D(leaderboard, len(leaderboard) , 1) # sorts by score
        print ("lb,", leaderboard)
    
        image(backg,0,0,1000,700)
        text("Current Leaderbaord Top 5", 100, 100)
        text ("Press Enter to return", 520, 600)
        lblineLocation = 250
        if len(leaderboard) != 0:
            for i in range (len(leaderboard)):
                if i >= 5:
                    break
                text (leaderboard[i][0], 100, lblineLocation)
                text (leaderboard[i][1], 300, lblineLocation)
                lblineLocation = lblineLocation + 50
                
                
def mousePressed():
    global page,startpage,startbutton,cloud,turn,winner,lbfile,playername
    global board,graph, visited,root,paths
    if gameboard.gameover():
        #Board and winner are reset here to start another game and page changes to 0
        winner = 0
        page = 0
        gameboard.board = [[2,2,2,2,2,2,2],
                           [2,2,2,2,2,2,2],
                           [2,2,2,2,2,2,2],
                           [2,2,2,2,2,2,2],
                           [2,2,2,2,2,2,2],
                           [2,2,2,2,2,2,2]]
        gameboard.turm = 0
        graph = {}
        root = []
        visited = []
        paths = []
        small = []
        longest = []
        playername = ""             
        
    elif not gameboard.gameover() and page == 2:
        gameboard.restriction()
        
        
    if gameboard.gameover():
        # Find the longest path and shows it on the screen
        for i in graph:
            graph[i].adjacent(gameboard.board)
            #print("This is the path: ",i,graph[i].path)
        for i in graph:
            if i[0] == 5 and graph[i].kind == (gameboard.turn + 1) % 2:
                root.append([i])
                print("haa",graph[i].path)
        for i in range(len(root)):
            small = root[i][0]
            visited.append(gameboard.dfs(graph,root[i][0], [])) #def dfs(self, graph, node, visited):
            for x in range(len(visited[i]) - 1):
                if small[0] > visited [i][x + 1][0]:
                    small = visited[i][x + 1]
            root[i].append(small)
        print("root:",root)
        print("visited:",visited)
        
        for i in root:
            paths += gameboard.find_all_paths(graph,i[0],i[1])  # def find_all_paths(self, graph, start, end, path=[]):
        print(paths)
        if len(paths) != 0:
            longest = paths[0]
            for i in range(len(paths) - 1):
                if len(longest) < len(paths[i + 1]):
                    longest = paths[i + 1]
            print(longest)
            for i in range(len(longest)- 1):     #Shows the longest path by connecting the coins
                stroke(25,252,250)
                line(205 + longest[i][1] * 100, 155 + longest[i][0] * 100, 205 + longest[i + 1][1] * 100, 155 + longest[i + 1][0] * 100)

            output = playername + "," + str(len(longest))
            AppendToFile (lbfile, output)   
        

        
    
def mouseReleased():
    global page,board,winner
    
    #Location for the start/rule/leaderboard button
    if page == 0:
        if mouseX>400 and mouseX<600 and mouseY>500 and mouseY<600:
            page = 2 
        elif mouseX>150 and mouseX<250 and mouseY>500 and mouseY<600:
            page = 1
        elif mouseX>750 and mouseX<850 and mouseY>500 and mouseY<600:
            page = 3
        
                            
def keyPressed():
     global playername, page
     
     #For player name input in page one, error trapping included along with backspace
     if page == 0:
         if mouseX>100 and mouseY>300 and mouseY<350:
            if key>="A" and key<="z":
                playername +=key
            if key==BACKSPACE:
                playername=playername[0:len(playername)-1]
     if page == 1 or page == 3:
         if key==ENTER:
            page=0
    
            
    
    

                 
