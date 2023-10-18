class Space:
    def __init__(self, name):
        self.Up=None
        self.Down=None
        self.Left=None
        self.Right=None
        self.upLeft=None
        self.upRight=None
        self.downLeft=None
        self.downRight=None
        self.Name=name
        self.Piece=None

class Board:
    def __init__(self, s):
        #Adds all spaces and connects them together
        #self.spaces=[[Space("a1"), Space("a2"), Space("a3"), Space("a4"), Space("a5"), Space("a6"), Space("a7"), Space("a8")], [Space("b1"), Space("b2"), Space("b3"), Space("b4"), Space("b5"), Space("b6"), Space("b7"), Space("b8")],[Space("c1"), Space("c2"), Space("c3"), Space("c4"), Space("c5"), Space("c6"), Space("c7"), Space("c8")],[Space("d1"), Space("d2"), Space("d3"), Space("d4"), Space("d5"), Space("d6"), Space("d7"), Space("d8")],[Space("e1"), Space("e2"), Space("e3"), Space("e4"), Space("e5"), Space("e6"), Space("e7"), Space("e8")],[Space("f1"), Space("f2"), Space("f3"), Space("f4"), Space("f5"), Space("f6"), Space("f7"), Space("f8")],[Space("g1"), Space("g2"), Space("g3"), Space("g4"), Space("g5"), Space("g6"), Space("g7"), Space("g8")],[Space("h1"), Space("h2"), Space("h3"), Space("h4"), Space("h5"), Space("h6"), Space("h7"), Space("h8")]]
        self.spaces=[[s[0],s[8],s[16],s[24],s[32],s[40],s[48],s[56]],[s[1],s[9],s[17],s[25],s[33],s[41],s[49],s[57]],[s[2],s[10],s[18],s[26],s[34],s[42],s[50],s[58]],[s[3],s[11],s[19],s[27],s[35],s[43],s[51],s[59]],[s[4],s[12],s[20],s[28],s[36],s[44],s[52],s[60]],[s[5],s[13],s[21],s[29],s[37],s[45],s[53],s[61]],[s[6],s[14],s[22],s[30],s[38],s[46],s[54],s[62]],[s[7],s[15],s[23],s[31],s[39],s[47],s[55],s[63]]]
        for x in range(len(self.spaces)):
            for y in range(len(self.spaces[x])):
                if self.spaces[x][y]!=self.spaces[x][-1]:
                    self.spaces[x][y].Right=self.spaces[x][y+1]
                    self.spaces[x][y+1].Left=self.spaces[x][y]
                    
                if x+1<len(self.spaces):
                    self.spaces[x][y].Up=self.spaces[x+1][y]
                    self.spaces[x+1][y].Down=self.spaces[x][y]
                    #print("Space up:", self.spaces[x+1][y].Name)
                    if y>0:
                        self.spaces[x][y].upLeft=self.spaces[x+1][y-1]
                        self.spaces[x+1][y-1].downRight=self.spaces[x][y]
                        #print("Space up left:", self.spaces[x+1][y-1].Name)
                    if y<len(self.spaces[x]) and self.spaces[x][y]!=self.spaces[x][-1]:
                        self.spaces[x][y].upRight=self.spaces[x+1][y+1]
                        self.spaces[x+1][y+1].downLeft=self.spaces[x][y]
                        #print("Space up right:", self.spaces[x+1][y+1].Name)
            
            self.Pieces=None

            
    def search(self, root, space, right):
        #Go right along board checking spaces until you reach end; then go up a row, and go left until end,
        #and vice versa
        if root.Name!=space.Name:
            if right==True:
                if root.Right!=None:
                    ans=self.search(root.Right, space, True)
                elif root.Up!=None:
                    ans=self.search(root.Up, space, False)
                else:
                    return None
            else:
                if root.Left!=None:
                    ans=self.search(root.Left, space, False)
                elif root.Up!=None:
                    ans=self.search(root.Up, space, True)
                else:
                    return None
        else:
            ans=root
            return ans
        return ans
    
    def validMove(self, piece):

        originalSpace=piece.Space
        print(piece.Moves)
        possibleMoves=[]
        for x in piece.Moves:
            valid=True
            if piece.Name!="Knight":
                for y in x:
                    piece.Space=originalSpace
                    if y is None or (y.Piece is not None and y.Piece.Color==piece.Color):
                        valid=False 
                        break
            else:
                if x[-1] is None or (x[-1].Piece is not None and x[-1].Piece.Color==piece.Color):
                    valid=False

            if valid==True:
                possibleMoves.append(x[-1])

        piece.Space=originalSpace
        return possibleMoves


class Piece:
    def __init__(self, name, color, space, spaceName, madeFirstMove):
        self.Name=name
        self.SpaceName=spaceName
        self.Space=space
        self.Color=color
        self.Moved=madeFirstMove
        self.knightMoves=[[self.Space.Up, self.Space.Up.upLeft if self.Space.Up!=None else None], [self.Space.Up, self.Space.Up.upRight if self.Space.Up!=None else None], [self.Space.Left, self.Space.Left.upRight if self.Space.Left!=None else None], [self.Space.Left, self.Space.Left.downLeft if self.Space.Left!=None else None], [self.Space.Right, self.Space.Right.upRight if self.Space.Right!=None else None], [self.Space.Right, self.Space.Right.downRight if self.Space.Right!=None else None], [self.Space.Down, self.Space.Down.downLeft if self.Space.Down!=None else None], [self.Space.Down, self.Space.Down.downRight if self.Space.Down!=None else None]]
        self.rookMoves=[]
        self.bishopMoves=[]
        self.queenMoves=[]
        moves=[self.Space.Up, self.Space.Down, self.Space.Left, self.Space.Right]
        arr=[]
        num=0
        if self.Name=="Rook" or self.Name=="Queen":
            for w in range(len(moves)):
                #print('w',w)
                #print("right",self.Space.Right)
                #arr.append([moves[w]])
                for x in range(len(arr),len(arr)+8):
                    num+=1
                    arr.append([moves[w]])
                    #print(arr)
                    #print('x',x)
                    for y in range(num):
                        #print('y',y)
                        if moves[w]!=None:
                            #print('not null')
                            if w==0:
                                if arr[x][y]!=None and arr[x][y].Up!=None:
                                    arr[x].append(arr[x][y].Up)
                                    #for l in range(len(arr[w])):
                                    #    print("Arr",arr[w][l].Name)
                                    #print("First",arr[w][y].Name)
                                    #print('up',arr[x][y].Up.Name)
                                else:
                                    break
                            elif w==1:
                                #print('sdgsadg')
                                if arr[x][y]!=None and arr[x][y].Down!=None:
                                    arr[x].append(arr[x][y].Down)
                                    #print('down',arr[x][y].Down.Name)
                                else:
                                    break
                            elif w==2:
                                #print('sfsdgwdg')
                                if arr[x][y]!=None and arr[x][y].Left!=None:
                                    arr[x].append(arr[x][y].Left)
                                    #print('left',arr[x][y].Left.Name)
                                else:
                                    break
                            else:
                                #print('asadfasd')
                                if arr[x][y]!=None and arr[x][y].Right!=None:
                                    arr[x].append(arr[x][y].Right)
                                    #print('right',arr[x][y].Right.Name)
                                else:
                                    break
                        else:
                            #print('null')
                            break
                num=0
            self.rookMoves=arr
            print(len(self.rookMoves))
            for t in range(len(self.rookMoves)):
                print("Rook moves:",len(self.rookMoves[t]))
                for u in range(len(self.rookMoves[t])):
                    if self.rookMoves[t][u]!=None:
                        print(self.rookMoves[t][u].Name)
                    else:
                        print(None)

        moves=[self.Space.upLeft, self.Space.upRight, self.Space.downLeft, self.Space.downRight]
        if self.Name=="Bishop" or self.Name=="Queen":
            w=0
            x=0
            y=0
            for w in range(len(moves)):
                #print('w',w)
                #print("right",self.Space.Right)
                #arr.append([moves[w]])
                for x in range(len(arr),len(arr)+8):
                    arr.append([moves[w]])
                    #print(arr)
                    #print('x',x)
                    for y in range(x):
                        #print('y',y)
                        if moves[w]!=None:
                            #print('not null')
                            if w==0:
                                if arr[x][y]!=None and arr[x][y].upLeft!=None:
                                    arr[x].append(arr[x][y].upLeft)
                                    #for l in range(len(arr[w])):
                                    #    print("Arr",arr[w][l].Name)
                                    #print("First",arr[w][y].Name)
                                    #print('up',arr[x][y].Up.Name)
                                else:
                                    break
                            elif w==1:
                                #print('sdgsadg')
                                if arr[x][y]!=None and arr[x][y].upRight!=None:
                                    arr[x].append(arr[x][y].upRight)
                                    #print('down',arr[x][y].Down.Name)
                                else:
                                    break
                            elif w==2:
                                #print('sfsdgwdg')
                                if arr[x][y]!=None and arr[x][y].downLeft!=None:
                                    arr[x].append(arr[x][y].downLeft)
                                    #print('left',arr[x][y].Left.Name)
                                else:
                                    break
                            else:
                                #print('asadfasd')
                                if arr[x][y]!=None and arr[x][y].downRight!=None:
                                    arr[x].append(arr[x][y].downRight)
                                    #print('right',arr[x][y].Right.Name)
                                else:
                                    break
                        else:
                            #print('null')
                            break
            self.bishopMoves=arr
        if self.Name=="Queen": 
            w=0
            x=0
            y=0
            self.queenMoves=[]
            for x in range(len(self.bishopMoves)):
                self.queenMoves.append(self.bishopMoves[x])
            for y in range(len(self.rookMoves)):
                self.queenMoves.append(self.rookMoves[y])
        
        #self.bishopMoves=[[self.Space.upLeft], [self.Space.upLeft, self.Space.upLeft.upLeft if self.Space.upLeft!=None else None], [self.Space.upLeft,self.Space.upLeft.upLeft if self.Space.upLeft!=None else None,self.Space.upLeft.upLeft.upLeft if self.Space.upLeft.upLeft!=None else None],[self.Space.upLeft,self.Space.upLeft.upLeft if self.Space.upLeft!=None else None,self.Space.upLeft.upLeft.upLeft if self.Space.upLeft.upLeft!=None else None,self.Space.upLeft.upLeft.upLeft.upLeft if self.Space.upLeft.upLeft.upLeft!=None else None],[self.Space.upLeft,self.Space.upLeft.upLeft if self.Space.upLeft!=None else None,self.Space.upLeft.upLeft.upLeft if self.Space.upLeft.upLeft!=None else None,self.Space.upLeft.upLeft.upLeft.upLeft if self.Space.upLeft.upLeft.upLeft!=None else None,self.Space.upLeft.upLeft.upLeft.upLeft.upLeft if self.Space.upLeft.upLeft.upLeft.upLeft!=None else None],[self.Space.upLeft,self.Space.upLeft.upLeft if self.Space.upLeft!=None else None,self.Space.upLeft.upLeft.upLeft if self.Space.upLeft.upLeft!=None else None,self.Space.upLeft.upLeft.upLeft.upLeft if self.Space.upLeft.upLeft.upLeft!=None else None,self.Space.upLeft.upLeft.upLeft.upLeft.upLeft if self.Space.upLeft.upLeft.upLeft.upLeft!=None else None,self.Space.upLeft.upLeft.upLeft.upLeft.upLeft.upLeft if self.Space.upLeft.upLeft.upLeft.upLeft.upLeft!=None else None],[self.Space.upLeft,self.Space.upLeft.upLeft if self.Space.upLeft!=None else None,self.Space.upLeft.upLeft.upLeft if self.Space.upLeft.upLeft!=None else None,self.Space.upLeft.upLeft.upLeft.upLeft if self.Space.upLeft.upLeft.upLeft!=None else None,self.Space.upLeft.upLeft.upLeft.upLeft.upLeft if self.Space.upLeft.upLeft.upLeft.upLeft!=None else None,self.Space.upLeft.upLeft.upLeft.upLeft.upLeft.upLeft if self.Space.upLeft.upLeft.upLeft.upLeft.upLeft!=None else None,self.Space.upLeft.upLeft.upLeft.upLeft.upLeft.upLeft.upLeft if self.Space.upLeft.upLeft.upLeft.upLeft.upLeft.upLeft!=None else None],[self.Space.upRight], [self.Space.upRight, self.Space.upRight.upRight if self.Space.upRight!=None else None], [self.Space.upRight,self.Space.upRight.upRight if self.Space.upRight!=None else None,self.Space.upRight.upRight.upRight if self.Space.upRight.upRight!=None else None],[self.Space.upRight,self.Space.upRight.upRight if self.Space.upRight!=None else None,self.Space.upRight.upRight.upRight if self.Space.upRight.upRight!=None else None,self.Space.upRight.upRight.upRight.upRight if self.Space.upRight.upRight.upRight!=None else None],[self.Space.upRight,self.Space.upRight.upRight if self.Space.upRight!=None else None,self.Space.upRight.upRight.upRight if self.Space.upRight.upRight!=None else None,self.Space.upRight.upRight.upRight.upRight if self.Space.upRight.upRight.upRight!=None else None,self.Space.upRight.upRight.upRight.upRight.upRight if self.Space.upRight.upRight.upRight.upRight!=None else None],[self.Space.upRight,self.Space.upRight.upRight if self.Space.upRight!=None else None,self.Space.upRight.upRight.upRight if self.Space.upRight.upRight!=None else None,self.Space.upRight.upRight.upRight.upRight if self.Space.upRight.upRight.upRight!=None else None,self.Space.upRight.upRight.upRight.upRight.upRight if self.Space.upRight.upRight.upRight.upRight!=None else None,self.Space.upRight.upRight.upRight.upRight.upRight.upRight if self.Space.upRight.upRight.upRight.upRight.upRight!=None else None],[self.Space.upRight,self.Space.upRight.upRight if self.Space.upRight!=None else None,self.Space.upRight.upRight.upRight if self.Space.upRight.upRight!=None else None,self.Space.upRight.upRight.upRight.upRight if self.Space.upRight.upRight.upRight!=None else None,self.Space.upRight.upRight.upRight.upRight.upRight if self.Space.upRight.upRight.upRight.upRight!=None else None,self.Space.upRight.upRight.upRight.upRight.upRight.upRight if self.Space.upRight.upRight.upRight.upRight.upRight!=None else None,self.Space.upRight.upRight.upRight.upRight.upRight.upRight.upRight if self.Space.upRight.upRight.upRight.upRight.upRight.upRight!=None else None], [self.Space.downLeft], [self.Space.downLeft, self.Space.downLeft.downLeft if self.Space.downLeft!=None else None], [self.Space.downLeft,self.Space.downLeft.downLeft if self.Space.downLeft!=None else None,self.Space.downLeft.downLeft.downLeft if self.Space.downLeft.downLeft!=None else None],[self.Space.downLeft,self.Space.downLeft.downLeft if self.Space.downLeft!=None else None,self.Space.downLeft.downLeft.downLeft if self.Space.downLeft.downLeft!=None else None,self.Space.downLeft.downLeft.downLeft.downLeft if self.Space.downLeft.downLeft.downLeft!=None else None],[self.Space.downLeft,self.Space.downLeft.downLeft if self.Space.downLeft!=None else None,self.Space.downLeft.downLeft.downLeft if self.Space.downLeft.downLeft!=None else None,self.Space.downLeft.downLeft.downLeft.downLeft if self.Space.downLeft.downLeft.downLeft!=None else None,self.Space.downLeft.downLeft.downLeft.downLeft.downLeft if self.Space.downLeft.downLeft.downLeft.downLeft!=None else None],[self.Space.downLeft,self.Space.downLeft.downLeft if self.Space.downLeft!=None else None,self.Space.downLeft.downLeft.downLeft if self.Space.downLeft.downLeft!=None else None,self.Space.downLeft.downLeft.downLeft.downLeft if self.Space.downLeft.downLeft.downLeft!=None else None,self.Space.downLeft.downLeft.downLeft.downLeft.downLeft if self.Space.downLeft.downLeft.downLeft.downLeft!=None else None,self.Space.downLeft.downLeft.downLeft.downLeft.downLeft.downLeft if self.Space.downLeft.downLeft.downLeft.downLeft.downLeft!=None else None],[self.Space.downLeft,self.Space.downLeft.downLeft if self.Space.downLeft!=None else None,self.Space.downLeft.downLeft.downLeft if self.Space.downLeft.downLeft!=None else None,self.Space.downLeft.downLeft.downLeft.downLeft if self.Space.downLeft.downLeft.downLeft!=None else None,self.Space.downLeft.downLeft.downLeft.downLeft.downLeft if self.Space.downLeft.downLeft.downLeft.downLeft!=None else None,self.Space.downLeft.downLeft.downLeft.downLeft.downLeft.downLeft if self.Space.downLeft.downLeft.downLeft.downLeft.downLeft!=None else None,self.Space.downLeft.downLeft.downLeft.downLeft.downLeft.downLeft.downLeft if self.Space.downLeft.downLeft.downLeft.downLeft.downLeft.downLeft!=None else None],[self.Space.downRight], [self.Space.downRight, self.Space.downRight.downRight if self.Space.downRight!=None else None], [self.Space.downRight,self.Space.downRight.downRight if self.Space.downRight!=None else None,self.Space.downRight.downRight.downRight if self.Space.downRight.downRight!=None else None],[self.Space.downRight,self.Space.downRight.downRight if self.Space.downRight!=None else None,self.Space.downRight.downRight.downRight if self.Space.downRight.downRight!=None else None,self.Space.downRight.downRight.downRight.downRight if self.Space.downRight.downRight.downRight!=None else None],[self.Space.downRight,self.Space.downRight.downRight if self.Space.downRight!=None else None,self.Space.downRight.downRight.downRight if self.Space.downRight.downRight!=None else None,self.Space.downRight.downRight.downRight.downRight if self.Space.downRight.downRight.downRight!=None else None,self.Space.downRight.downRight.downRight.downRight.downRight if self.Space.downRight.downRight.downRight.downRight!=None else None],[self.Space.downRight,self.Space.downRight.downRight if self.Space.downRight!=None else None,self.Space.downRight.downRight.downRight if self.Space.downRight.downRight!=None else None,self.Space.downRight.downRight.downRight.downRight if self.Space.downRight.downRight.downRight!=None else None,self.Space.downRight.downRight.downRight.downRight.downRight if self.Space.downRight.downRight.downRight.downRight!=None else None,self.Space.downRight.downRight.downRight.downRight.downRight.downRight if self.Space.downRight.downRight.downRight.downRight.downRight!=None else None],[self.Space.downRight,self.Space.downRight.downRight if self.Space.downRight!=None else None,self.Space.downRight.downRight.downRight if self.Space.downRight.downRight!=None else None,self.Space.downRight.downRight.downRight.downRight if self.Space.downRight.downRight.downRight!=None else None,self.Space.downRight.downRight.downRight.downRight.downRight if self.Space.downRight.downRight.downRight.downRight!=None else None,self.Space.downRight.downRight.downRight.downRight.downRight.downRight if self.Space.downRight.downRight.downRight.downRight.downRight!=None else None,self.Space.downRight.downRight.downRight.downRight.downRight.downRight.downRight if self.Space.downRight.downRight.downRight.downRight.downRight.downRight!=None else None]]
        #self.rookMoves=[[self.Space.Up], [self.Space.Up, self.Space.Up.Up if self.Space.Up!=None else None], [self.Space.Up,self.Space.Up.Up if self.Space.Up!=None else None,self.Space.Up.Up.Up if self.Space.Up.Up!=None else None],[self.Space.Up,self.Space.Up.Up if self.Space.Up!=None else None,self.Space.Up.Up.Up if self.Space.Up.Up!=None else None,self.Space.Up.Up.Up.Up if self.Space.Up.Up.Up!=None else None],[self.Space.Up,self.Space.Up.Up if self.Space.Up!=None else None,self.Space.Up.Up.Up if self.Space.Up.Up!=None else None,self.Space.Up.Up.Up.Up if self.Space.Up.Up.Up!=None else None,self.Space.Up.Up.Up.Up.Up if self.Space.Up.Up.Up.Up!=None else None],[self.Space.Up,self.Space.Up.Up if self.Space.Up!=None else None,self.Space.Up.Up.Up if self.Space.Up.Up!=None else None,self.Space.Up.Up.Up.Up if self.Space.Up.Up.Up!=None else None,self.Space.Up.Up.Up.Up.Up if self.Space.Up.Up.Up.Up!=None else None,self.Space.Up.Up.Up.Up.Up.Up if self.Space.Up.Up.Up.Up.Up!=None else None],[self.Space.Up,self.Space.Up.Up if self.Space.Up!=None else None,self.Space.Up.Up.Up if self.Space.Up.Up!=None else None,self.Space.Up.Up.Up.Up if self.Space.Up.Up.Up!=None else None,self.Space.Up.Up.Up.Up.Up if self.Space.Up.Up.Up.Up!=None else None,self.Space.Up.Up.Up.Up.Up.Up if self.Space.Up.Up.Up.Up.Up!=None else None,self.Space.Up.Up.Up.Up.Up.Up.Up if self.Space.Up.Up.Up.Up.Up.Up!=None else None],[self.Space.Down], [self.Space.Down, self.Space.Down.Down if self.Space.Down!=None else None], [self.Space.Down,self.Space.Down.Down if self.Space.Down!=None else None,self.Space.Down.Down.Down if self.Space.Down.Down!=None else None],[self.Space.Down,self.Space.Down.Down if self.Space.Down!=None else None,self.Space.Down.Down.Down if self.Space.Down.Down!=None else None,self.Space.Down.Down.Down.Down if self.Space.Down.Down.Down!=None else None],[self.Space.Down,self.Space.Down.Down if self.Space.Down!=None else None,self.Space.Down.Down.Down if self.Space.Down.Down!=None else None,self.Space.Down.Down.Down.Down if self.Space.Down.Down.Down!=None else None,self.Space.Down.Down.Down.Down.Down if self.Space.Down.Down.Down.Down!=None else None],[self.Space.Down,self.Space.Down.Down if self.Space.Down!=None else None,self.Space.Down.Down.Down if self.Space.Down.Down!=None else None,self.Space.Down.Down.Down.Down if self.Space.Down.Down.Down!=None else None,self.Space.Down.Down.Down.Down.Down if self.Space.Down.Down.Down.Down!=None else None,self.Space.Down.Down.Down.Down.Down.Down if self.Space.Down.Down.Down.Down.Down!=None else None],[self.Space.Down,self.Space.Down.Down if self.Space.Down!=None else None,self.Space.Down.Down.Down if self.Space.Down.Down!=None else None,self.Space.Down.Down.Down.Down if self.Space.Down.Down.Down!=None else None,self.Space.Down.Down.Down.Down.Down if self.Space.Down.Down.Down.Down!=None else None,self.Space.Down.Down.Down.Down.Down.Down if self.Space.Down.Down.Down.Down.Down!=None else None,self.Space.Down.Down.Down.Down.Down.Down.Down if self.Space.Down.Down.Down.Down.Down.Down!=None else None], [self.Space.Left], [self.Space.Left, self.Space.Left.Left if self.Space.Left!=None else None], [self.Space.Left,self.Space.Left.Left if self.Space.Left!=None else None,self.Space.Left.Left.Left if self.Space.Left.Left!=None else None],[self.Space.Left,self.Space.Left.Left if self.Space.Left!=None else None,self.Space.Left.Left.Left if self.Space.Left.Left!=None else None,self.Space.Left.Left.Left.Left if self.Space.Left.Left.Left!=None else None],[self.Space.Left,self.Space.Left.Left if self.Space.Left!=None else None,self.Space.Left.Left.Left if self.Space.Left.Left!=None else None,self.Space.Left.Left.Left.Left if self.Space.Left.Left.Left!=None else None,self.Space.Left.Left.Left.Left.Left if self.Space.Left.Left.Left.Left!=None else None],[self.Space.Left,self.Space.Left.Left if self.Space.Left!=None else None,self.Space.Left.Left.Left if self.Space.Left.Left!=None else None,self.Space.Left.Left.Left.Left if self.Space.Left.Left.Left!=None else None,self.Space.Left.Left.Left.Left.Left if self.Space.Left.Left.Left.Left!=None else None,self.Space.Left.Left.Left.Left.Left.Left if self.Space.Left.Left.Left.Left.Left!=None else None],[self.Space.Left,self.Space.Left.Left if self.Space.Left!=None else None,self.Space.Left.Left.Left if self.Space.Left.Left!=None else None,self.Space.Left.Left.Left.Left if self.Space.Left.Left.Left!=None else None,self.Space.Left.Left.Left.Left.Left if self.Space.Left.Left.Left.Left!=None else None,self.Space.Left.Left.Left.Left.Left.Left if self.Space.Left.Left.Left.Left.Left!=None else None,self.Space.Left.Left.Left.Left.Left.Left.Left if self.Space.Left.Left.Left.Left.Left.Left!=None else None],[self.Space.Right], [self.Space.Right, self.Space.Right.Right if self.Space.Right!=None else None], [self.Space.Right,self.Space.Right.Right if self.Space.Right!=None else None,self.Space.Right.Right.Right if self.Space.Right.Right!=None else None],[self.Space.Right,self.Space.Right.Right if self.Space.Right!=None else None,self.Space.Right.Right.Right if self.Space.Right.Right!=None else None,self.Space.Right.Right.Right.Right if self.Space.Right.Right.Right!=None else None],[self.Space.Right,self.Space.Right.Right if self.Space.Right!=None else None,self.Space.Right.Right.Right if self.Space.Right.Right!=None else None,self.Space.Right.Right.Right.Right if self.Space.Right.Right.Right!=None else None,self.Space.Right.Right.Right.Right.Right if self.Space.Right.Right.Right.Right!=None else None],[self.Space.Right,self.Space.Right.Right if self.Space.Right!=None else None,self.Space.Right.Right.Right if self.Space.Right.Right!=None else None,self.Space.Right.Right.Right.Right if self.Space.Right.Right.Right!=None else None,self.Space.Right.Right.Right.Right.Right if self.Space.Right.Right.Right.Right!=None else None,self.Space.Right.Right.Right.Right.Right.Right if self.Space.Right.Right.Right.Right.Right!=None else None],[self.Space.Right,self.Space.Right.Right if self.Space.Right!=None else None,self.Space.Right.Right.Right if self.Space.Right.Right!=None else None,self.Space.Right.Right.Right.Right if self.Space.Right.Right.Right!=None else None,self.Space.Right.Right.Right.Right.Right if self.Space.Right.Right.Right.Right!=None else None,self.Space.Right.Right.Right.Right.Right.Right if self.Space.Right.Right.Right.Right.Right!=None else None,self.Space.Right.Right.Right.Right.Right.Right.Right if self.Space.Right.Right.Right.Right.Right.Right!=None else None]]
        self.pawnMovesWhite=[[self.Space.Up]]
        self.pawnMovesBlack=[[self.Space.Down]]
        self.kingMoves=[[self.Space.Up],[self.Space.Down],[self.Space.Left],[self.Space.Right],[self.Space.upLeft],[self.Space.upRight],[self.Space.downLeft],[self.Space.downRight]]
        #self.queenMoves=[[self.Space.upLeft], [self.Space.upLeft, self.Space.upLeft.upLeft if self.Space.upLeft!=None else None], [self.Space.upLeft,self.Space.upLeft.upLeft if self.Space.upLeft!=None else None,self.Space.upLeft.upLeft.upLeft if self.Space.upLeft.upLeft!=None else None],[self.Space.upLeft,self.Space.upLeft.upLeft if self.Space.upLeft!=None else None,self.Space.upLeft.upLeft.upLeft if self.Space.upLeft.upLeft!=None else None,self.Space.upLeft.upLeft.upLeft.upLeft if self.Space.upLeft.upLeft.upLeft!=None else None],[self.Space.upLeft,self.Space.upLeft.upLeft if self.Space.upLeft!=None else None,self.Space.upLeft.upLeft.upLeft if self.Space.upLeft.upLeft!=None else None,self.Space.upLeft.upLeft.upLeft.upLeft if self.Space.upLeft.upLeft.upLeft!=None else None,self.Space.upLeft.upLeft.upLeft.upLeft.upLeft if self.Space.upLeft.upLeft.upLeft.upLeft!=None else None],[self.Space.upLeft,self.Space.upLeft.upLeft if self.Space.upLeft!=None else None,self.Space.upLeft.upLeft.upLeft if self.Space.upLeft.upLeft!=None else None,self.Space.upLeft.upLeft.upLeft.upLeft if self.Space.upLeft.upLeft.upLeft!=None else None,self.Space.upLeft.upLeft.upLeft.upLeft.upLeft if self.Space.upLeft.upLeft.upLeft.upLeft!=None else None,self.Space.upLeft.upLeft.upLeft.upLeft.upLeft.upLeft if self.Space.upLeft.upLeft.upLeft.upLeft.upLeft!=None else None],[self.Space.upLeft,self.Space.upLeft.upLeft if self.Space.upLeft!=None else None,self.Space.upLeft.upLeft.upLeft if self.Space.upLeft.upLeft!=None else None,self.Space.upLeft.upLeft.upLeft.upLeft if self.Space.upLeft.upLeft.upLeft!=None else None,self.Space.upLeft.upLeft.upLeft.upLeft.upLeft if self.Space.upLeft.upLeft.upLeft.upLeft!=None else None,self.Space.upLeft.upLeft.upLeft.upLeft.upLeft.upLeft if self.Space.upLeft.upLeft.upLeft.upLeft.upLeft!=None else None,self.Space.upLeft.upLeft.upLeft.upLeft.upLeft.upLeft.upLeft if self.Space.upLeft.upLeft.upLeft.upLeft.upLeft.upLeft!=None else None],[self.Space.upRight], [self.Space.upRight, self.Space.upRight.upRight if self.Space.upRight!=None else None], [self.Space.upRight,self.Space.upRight.upRight if self.Space.upRight!=None else None,self.Space.upRight.upRight.upRight if self.Space.upRight.upRight!=None else None],[self.Space.upRight,self.Space.upRight.upRight if self.Space.upRight!=None else None,self.Space.upRight.upRight.upRight if self.Space.upRight.upRight!=None else None,self.Space.upRight.upRight.upRight.upRight if self.Space.upRight.upRight.upRight!=None else None],[self.Space.upRight,self.Space.upRight.upRight if self.Space.upRight!=None else None,self.Space.upRight.upRight.upRight if self.Space.upRight.upRight!=None else None,self.Space.upRight.upRight.upRight.upRight if self.Space.upRight.upRight.upRight!=None else None,self.Space.upRight.upRight.upRight.upRight.upRight if self.Space.upRight.upRight.upRight.upRight!=None else None],[self.Space.upRight,self.Space.upRight.upRight if self.Space.upRight!=None else None,self.Space.upRight.upRight.upRight if self.Space.upRight.upRight!=None else None,self.Space.upRight.upRight.upRight.upRight if self.Space.upRight.upRight.upRight!=None else None,self.Space.upRight.upRight.upRight.upRight.upRight if self.Space.upRight.upRight.upRight.upRight!=None else None,self.Space.upRight.upRight.upRight.upRight.upRight.upRight if self.Space.upRight.upRight.upRight.upRight.upRight!=None else None],[self.Space.upRight,self.Space.upRight.upRight if self.Space.upRight!=None else None,self.Space.upRight.upRight.upRight if self.Space.upRight.upRight!=None else None,self.Space.upRight.upRight.upRight.upRight if self.Space.upRight.upRight.upRight!=None else None,self.Space.upRight.upRight.upRight.upRight.upRight if self.Space.upRight.upRight.upRight.upRight!=None else None,self.Space.upRight.upRight.upRight.upRight.upRight.upRight if self.Space.upRight.upRight.upRight.upRight.upRight!=None else None,self.Space.upRight.upRight.upRight.upRight.upRight.upRight.upRight if self.Space.upRight.upRight.upRight.upRight.upRight.upRight!=None else None], [self.Space.downLeft], [self.Space.downLeft, self.Space.downLeft.downLeft if self.Space.downLeft!=None else None], [self.Space.downLeft,self.Space.downLeft.downLeft if self.Space.downLeft!=None else None,self.Space.downLeft.downLeft.downLeft if self.Space.downLeft.downLeft!=None else None],[self.Space.downLeft,self.Space.downLeft.downLeft if self.Space.downLeft!=None else None,self.Space.downLeft.downLeft.downLeft if self.Space.downLeft.downLeft!=None else None,self.Space.downLeft.downLeft.downLeft.downLeft if self.Space.downLeft.downLeft.downLeft!=None else None],[self.Space.downLeft,self.Space.downLeft.downLeft if self.Space.downLeft!=None else None,self.Space.downLeft.downLeft.downLeft if self.Space.downLeft.downLeft!=None else None,self.Space.downLeft.downLeft.downLeft.downLeft if self.Space.downLeft.downLeft.downLeft!=None else None,self.Space.downLeft.downLeft.downLeft.downLeft.downLeft if self.Space.downLeft.downLeft.downLeft.downLeft!=None else None],[self.Space.downLeft,self.Space.downLeft.downLeft if self.Space.downLeft!=None else None,self.Space.downLeft.downLeft.downLeft if self.Space.downLeft.downLeft!=None else None,self.Space.downLeft.downLeft.downLeft.downLeft if self.Space.downLeft.downLeft.downLeft!=None else None,self.Space.downLeft.downLeft.downLeft.downLeft.downLeft if self.Space.downLeft.downLeft.downLeft.downLeft!=None else None,self.Space.downLeft.downLeft.downLeft.downLeft.downLeft.downLeft if self.Space.downLeft.downLeft.downLeft.downLeft.downLeft!=None else None],[self.Space.downLeft,self.Space.downLeft.downLeft if self.Space.downLeft!=None else None,self.Space.downLeft.downLeft.downLeft if self.Space.downLeft.downLeft!=None else None,self.Space.downLeft.downLeft.downLeft.downLeft if self.Space.downLeft.downLeft.downLeft!=None else None,self.Space.downLeft.downLeft.downLeft.downLeft.downLeft if self.Space.downLeft.downLeft.downLeft.downLeft!=None else None,self.Space.downLeft.downLeft.downLeft.downLeft.downLeft.downLeft if self.Space.downLeft.downLeft.downLeft.downLeft.downLeft!=None else None,self.Space.downLeft.downLeft.downLeft.downLeft.downLeft.downLeft.downLeft if self.Space.downLeft.downLeft.downLeft.downLeft.downLeft.downLeft!=None else None],[self.Space.downRight], [self.Space.downRight, self.Space.downRight.downRight if self.Space.downRight!=None else None], [self.Space.downRight,self.Space.downRight.downRight if self.Space.downRight!=None else None,self.Space.downRight.downRight.downRight if self.Space.downRight.downRight!=None else None],[self.Space.downRight,self.Space.downRight.downRight if self.Space.downRight!=None else None,self.Space.downRight.downRight.downRight if self.Space.downRight.downRight!=None else None,self.Space.downRight.downRight.downRight.downRight if self.Space.downRight.downRight.downRight!=None else None],[self.Space.downRight,self.Space.downRight.downRight if self.Space.downRight!=None else None,self.Space.downRight.downRight.downRight if self.Space.downRight.downRight!=None else None,self.Space.downRight.downRight.downRight.downRight if self.Space.downRight.downRight.downRight!=None else None,self.Space.downRight.downRight.downRight.downRight.downRight if self.Space.downRight.downRight.downRight.downRight!=None else None],[self.Space.downRight,self.Space.downRight.downRight if self.Space.downRight!=None else None,self.Space.downRight.downRight.downRight if self.Space.downRight.downRight!=None else None,self.Space.downRight.downRight.downRight.downRight if self.Space.downRight.downRight.downRight!=None else None,self.Space.downRight.downRight.downRight.downRight.downRight if self.Space.downRight.downRight.downRight.downRight!=None else None,self.Space.downRight.downRight.downRight.downRight.downRight.downRight if self.Space.downRight.downRight.downRight.downRight.downRight!=None else None],[self.Space.downRight,self.Space.downRight.downRight if self.Space.downRight!=None else None,self.Space.downRight.downRight.downRight if self.Space.downRight.downRight!=None else None,self.Space.downRight.downRight.downRight.downRight if self.Space.downRight.downRight.downRight!=None else None,self.Space.downRight.downRight.downRight.downRight.downRight if self.Space.downRight.downRight.downRight.downRight!=None else None,self.Space.downRight.downRight.downRight.downRight.downRight.downRight if self.Space.downRight.downRight.downRight.downRight.downRight!=None else None,self.Space.downRight.downRight.downRight.downRight.downRight.downRight.downRight if self.Space.downRight.downRight.downRight.downRight.downRight.downRight!=None else None],[self.Space.Up], [self.Space.Up, self.Space.Up.Up if self.Space.Up!=None else None], [self.Space.Up,self.Space.Up.Up if self.Space.Up!=None else None,self.Space.Up.Up.Up if self.Space.Up.Up!=None else None],[self.Space.Up,self.Space.Up.Up if self.Space.Up!=None else None,self.Space.Up.Up.Up if self.Space.Up.Up!=None else None,self.Space.Up.Up.Up.Up if self.Space.Up.Up.Up!=None else None],[self.Space.Up,self.Space.Up.Up if self.Space.Up!=None else None,self.Space.Up.Up.Up if self.Space.Up.Up!=None else None,self.Space.Up.Up.Up.Up if self.Space.Up.Up.Up!=None else None,self.Space.Up.Up.Up.Up.Up if self.Space.Up.Up.Up.Up!=None else None],[self.Space.Up,self.Space.Up.Up if self.Space.Up!=None else None,self.Space.Up.Up.Up if self.Space.Up.Up!=None else None,self.Space.Up.Up.Up.Up if self.Space.Up.Up.Up!=None else None,self.Space.Up.Up.Up.Up.Up if self.Space.Up.Up.Up.Up!=None else None,self.Space.Up.Up.Up.Up.Up.Up if self.Space.Up.Up.Up.Up.Up!=None else None],[self.Space.Up,self.Space.Up.Up if self.Space.Up!=None else None,self.Space.Up.Up.Up if self.Space.Up.Up!=None else None,self.Space.Up.Up.Up.Up if self.Space.Up.Up.Up!=None else None,self.Space.Up.Up.Up.Up.Up if self.Space.Up.Up.Up.Up!=None else None,self.Space.Up.Up.Up.Up.Up.Up if self.Space.Up.Up.Up.Up.Up!=None else None,self.Space.Up.Up.Up.Up.Up.Up.Up if self.Space.Up.Up.Up.Up.Up.Up!=None else None],[self.Space.Down], [self.Space.Down, self.Space.Down.Down if self.Space.Down!=None else None], [self.Space.Down,self.Space.Down.Down if self.Space.Down!=None else None,self.Space.Down.Down.Down if self.Space.Down.Down!=None else None],[self.Space.Down,self.Space.Down.Down if self.Space.Down!=None else None,self.Space.Down.Down.Down if self.Space.Down.Down!=None else None,self.Space.Down.Down.Down.Down if self.Space.Down.Down.Down!=None else None],[self.Space.Down,self.Space.Down.Down if self.Space.Down!=None else None,self.Space.Down.Down.Down if self.Space.Down.Down!=None else None,self.Space.Down.Down.Down.Down if self.Space.Down.Down.Down!=None else None,self.Space.Down.Down.Down.Down.Down if self.Space.Down.Down.Down.Down!=None else None],[self.Space.Down,self.Space.Down.Down if self.Space.Down!=None else None,self.Space.Down.Down.Down if self.Space.Down.Down!=None else None,self.Space.Down.Down.Down.Down if self.Space.Down.Down.Down!=None else None,self.Space.Down.Down.Down.Down.Down if self.Space.Down.Down.Down.Down!=None else None,self.Space.Down.Down.Down.Down.Down.Down if self.Space.Down.Down.Down.Down.Down!=None else None],[self.Space.Down,self.Space.Down.Down if self.Space.Down!=None else None,self.Space.Down.Down.Down if self.Space.Down.Down!=None else None,self.Space.Down.Down.Down.Down if self.Space.Down.Down.Down!=None else None,self.Space.Down.Down.Down.Down.Down if self.Space.Down.Down.Down.Down!=None else None,self.Space.Down.Down.Down.Down.Down.Down if self.Space.Down.Down.Down.Down.Down!=None else None,self.Space.Down.Down.Down.Down.Down.Down.Down if self.Space.Down.Down.Down.Down.Down.Down!=None else None], [self.Space.Left], [self.Space.Left, self.Space.Left.Left if self.Space.Left!=None else None], [self.Space.Left,self.Space.Left.Left if self.Space.Left!=None else None,self.Space.Left.Left.Left if self.Space.Left.Left!=None else None],[self.Space.Left,self.Space.Left.Left if self.Space.Left!=None else None,self.Space.Left.Left.Left if self.Space.Left.Left!=None else None,self.Space.Left.Left.Left.Left if self.Space.Left.Left.Left!=None else None],[self.Space.Left,self.Space.Left.Left if self.Space.Left!=None else None,self.Space.Left.Left.Left if self.Space.Left.Left!=None else None,self.Space.Left.Left.Left.Left if self.Space.Left.Left.Left!=None else None,self.Space.Left.Left.Left.Left.Left if self.Space.Left.Left.Left.Left!=None else None],[self.Space.Left,self.Space.Left.Left if self.Space.Left!=None else None,self.Space.Left.Left.Left if self.Space.Left.Left!=None else None,self.Space.Left.Left.Left.Left if self.Space.Left.Left.Left!=None else None,self.Space.Left.Left.Left.Left.Left if self.Space.Left.Left.Left.Left!=None else None,self.Space.Left.Left.Left.Left.Left.Left if self.Space.Left.Left.Left.Left.Left!=None else None],[self.Space.Left,self.Space.Left.Left if self.Space.Left!=None else None,self.Space.Left.Left.Left if self.Space.Left.Left!=None else None,self.Space.Left.Left.Left.Left if self.Space.Left.Left.Left!=None else None,self.Space.Left.Left.Left.Left.Left if self.Space.Left.Left.Left.Left!=None else None,self.Space.Left.Left.Left.Left.Left.Left if self.Space.Left.Left.Left.Left.Left!=None else None,self.Space.Left.Left.Left.Left.Left.Left.Left if self.Space.Left.Left.Left.Left.Left.Left!=None else None],[self.Space.Right], [self.Space.Right, self.Space.Right.Right if self.Space.Right!=None else None], [self.Space.Right,self.Space.Right.Right if self.Space.Right!=None else None,self.Space.Right.Right.Right if self.Space.Right.Right!=None else None],[self.Space.Right,self.Space.Right.Right if self.Space.Right!=None else None,self.Space.Right.Right.Right if self.Space.Right.Right!=None else None,self.Space.Right.Right.Right.Right if self.Space.Right.Right.Right!=None else None],[self.Space.Right,self.Space.Right.Right if self.Space.Right!=None else None,self.Space.Right.Right.Right if self.Space.Right.Right!=None else None,self.Space.Right.Right.Right.Right if self.Space.Right.Right.Right!=None else None,self.Space.Right.Right.Right.Right.Right if self.Space.Right.Right.Right.Right!=None else None],[self.Space.Right,self.Space.Right.Right if self.Space.Right!=None else None,self.Space.Right.Right.Right if self.Space.Right.Right!=None else None,self.Space.Right.Right.Right.Right if self.Space.Right.Right.Right!=None else None,self.Space.Right.Right.Right.Right.Right if self.Space.Right.Right.Right.Right!=None else None,self.Space.Right.Right.Right.Right.Right.Right if self.Space.Right.Right.Right.Right.Right!=None else None],[self.Space.Right,self.Space.Right.Right if self.Space.Right!=None else None,self.Space.Right.Right.Right if self.Space.Right.Right!=None else None,self.Space.Right.Right.Right.Right if self.Space.Right.Right.Right!=None else None,self.Space.Right.Right.Right.Right.Right if self.Space.Right.Right.Right.Right!=None else None,self.Space.Right.Right.Right.Right.Right.Right if self.Space.Right.Right.Right.Right.Right!=None else None,self.Space.Right.Right.Right.Right.Right.Right.Right if self.Space.Right.Right.Right.Right.Right.Right!=None else None]]
        self.possibleMoves={"Rook": self.rookMoves,"Knight":self.knightMoves,"Bishop":self.bishopMoves,"King":self.kingMoves,"Queen":self.queenMoves,"Pawn":self.pawnMovesWhite}
        if self.Name=="Pawn":
            if self.Color=="Black":
                self.possibleMoves["Pawn"]=self.pawnMovesBlack
        self.Moves=self.possibleMoves[self.Name]
        #Below is an original copy of moves list in case list is added to or removed from
        self.originalMoves=self.Moves
        self.Space.Piece=self
class Pawn(Piece):
    def moveTwo(self):
        if self.Color=="White":
            if self.Moved==False:
                if [self.Space.Up, self.Space.Up.Up] not in self.Moves:
                    self.Moves.append([self.Space.Up, self.Space.Up.Up])
            else:
                if [space.Up, space.Up.Up] in self.Moves:
                    self.Moves.remove([self.Space.Up, self.Space.Up.Up])
        else:
            if self.Moved==False:
                if [self.Space.Down, self.Space.Down.Down] not in self.Moves:
                    self.Moves.append([self.Space.Down, self.Space.Down.Down])
            else:
                if [self.Space.Down, self.Space.Down.Down] in self.Moves:
                    self.Moves.remove([self.Space.Down, self.Space.Down.Down])
    def captureMove(self):
        if self.Color=="White":
            if self.Space.upLeft!=None and self.Space.upLeft.Piece!=None and self.Space.upLeft.Piece.Name!=self.Name:
                if [self.Space.upLeft] not in self.Moves:
                    self.Moves.append([self.Space.upLeft])
            else:
                if [self.Space.upLeft] in self.Moves:
                    self.Moves.remove([self.Space.upLeft])
            if self.Space.upRight!=None and self.Space.upRight.Piece!=None and self.Space.upRight.Piece.Name!=self.Name:
                if [self.Space.upRight] not in self.Moves:
                    self.Moves.append([self.Space.upRight])
            else:
                if [self.Space.upRight] in self.Moves:
                    self.Moves.remove([self.Space.upRight])
        else:
            if self.Space.downLeft!=None and self.Space.downLeft.Piece!=None and self.Space.downLeft.Piece.Name!=self.Name:
                if [self.Space.downLeft] not in self.Moves:
                    self.Moves.append([self.Space.downLeft])
            else:
                if [self.Space.downLeft] in self.Moves:
                    self.Moves.remove([self.Space.downLeft])
            if self.Space.downRight!=None and self.Space.downRight.Piece!=None and self.Space.downRight.Piece.Name!=self.Name:
                if [self.Space.downRight] not in self.Moves:
                    self.Moves.append([self.Space.downRight])
            else:
                if [self.Space.downRight] in self.Moves:
                    self.Moves.remove([self.Space.downRight])
    def enPassant(self, otherPiece):
        pass

class King(Piece):

    def canCastle(self, rook):
        if rook!=None:
            if self.Moved==False and rook.Moved==False:
                if self.Space.Name=="a1" or self.Space.Name=="a8":
                    if [Space.Left, Self.Left] not in self.Moves:
                        self.Moves.append([self.Space.Left, self.Space.Left.Left])
                elif self.Space.Name=="h1" or self.Space.Name=="h8":
                     if [self.Space.Right, self.Self.Right.Right] not in king.Moves:
                        self.Moves.append([self.Space.Right, self.Space.Right.Right])
    def moveInCheck(self, board):
        for x in board.Pieces:
            if x!=None and x.Name!=self.Name:
                moves=board.validMove(x)
        for y in range(len(self.Moves)):
            for z in range(len(moves)):
                if self.Moves[y]==moves[z]:
                    self.Moves.remove(moves[z])

s=[Space("a1"), Space("a2"), Space("a3"), Space("a4"), Space("a5"), Space("a6"), Space("a7"), Space("a8"),Space("b1"), Space("b2"), Space("b3"), Space("b4"), Space("b5"), Space("b6"), Space("b7"), Space("b8"),Space("c1"), Space("c2"), Space("c3"), Space("c4"), Space("c5"), Space("c6"), Space("c7"), Space("c8"),Space("d1"), Space("d2"), Space("d3"), Space("d4"), Space("d5"), Space("d6"), Space("d7"), Space("d8"),Space("e1"), Space("e2"), Space("e3"), Space("e4"), Space("e5"), Space("e6"), Space("e7"), Space("e8"),Space("f1"), Space("f2"), Space("f3"), Space("f4"), Space("f5"), Space("f6"), Space("f7"), Space("f8"),Space("g1"), Space("g2"), Space("g3"), Space("g4"), Space("g5"), Space("g6"), Space("g7"), Space("g8"),Space("h1"), Space("h2"), Space("h3"), Space("h4"), Space("h5"), Space("h6"), Space("h7"), Space("h8")]
b=Board(s)


WRook1=Piece("Rook", "White", s[0], "a1", False)
WKnight1=Piece("Knight", "White", s[8], "b1", False)
WBishop1=Piece("Bishop", "White", s[16], "c1", False)
WQueen=Piece("Queen","White", s[24], "d1",False)
WKing=King("King","White", s[32], "e1",False)
WBishop2=Piece("Bishop", "White", s[40], "f1", False)
WKnight2=Piece("Knight", "White", s[48], "g1", False)
WRook2=Piece("Rook", "White", s[56], "h1", False)
WPawn1=Pawn("Pawn","White", s[1], "a2",False)
WPawn2=Pawn("Pawn","White", s[9], "b2",False)
WPawn3=Pawn("Pawn","White", s[17], "c2",False)
WPawn4=Pawn("Pawn","White", s[25], "d2",False)
WPawn5=Pawn("Pawn","White", s[33], "e2",False)
WPawn6=Pawn("Pawn","White", s[41], "f2",False)
WPawn7=Pawn("Pawn","White", s[49], "g2",False)
WPawn8=Pawn("Pawn","White", s[57], "h2",False)

BRook1=Piece("Rook", "Black", s[7], "a8", False)
BKnight1=Piece("Knight", "Black", s[15], "b8", False)
BBishop1=Piece("Bishop", "Black", s[23], "c8", False)
BQueen=Piece("Queen","Black", s[31], "d8",False)
BKing=King("King","Black", s[39], "e8",False)
BBishop2=Piece("Bishop", "Black", s[47], "f8", False)
BKnight2=Piece("Knight", "Black", s[55], "g8", False)
BRook2=Piece("Rook", "Black", s[63], "h8", False)
BPawn1=Pawn("Pawn","Black", s[6], "a7",False)
BPawn2=Pawn("Pawn","Black", s[14], "b7",False)
BPawn3=Pawn("Pawn","Black", s[22], "c7",False)
BPawn4=Pawn("Pawn","Black", s[30], "d7",False)
BPawn5=Pawn("Pawn","Black", s[38], "e7",False)
BPawn6=Pawn("Pawn","Black", s[46], "f7",False)
BPawn7=Pawn("Pawn","Black", s[54], "g7",False)
BPawn8=Pawn("Pawn","Black", s[62], "h7",False)


chessmen=[WRook1,WKnight1,WBishop1,WKing,WQueen,WBishop2,WKnight2,WRook2,WPawn1,WPawn2,WPawn3,WPawn4,WPawn5,WPawn6,WPawn7,WPawn8,BRook1,BKnight1,BBishop1,BKing,BQueen,BBishop2,BKnight2,BRook2,BPawn1,BPawn2,BPawn3,BPawn4,BPawn5,BPawn6,BPawn7,BPawn8]
b.Pieces=chessmen
b.search(b.spaces[0][0], Space("d5"), True)
for m in range(len(b.Pieces)):
    if b.Pieces[m].Name=="Pawn":
        b.Pieces[m].moveTwo()
        b.Pieces[m].captureMove()
    elif b.Pieces[m].Name=="King" and b.Pieces[m].Color=="White":
        b.Pieces[m].moveInCheck(b)
        b.Pieces[m].canCastle(b.Pieces[0])
        b.Pieces[m].canCastle(b.Pieces[7])
    elif b.Pieces[m].Name=="King" and b.Pieces[m].Color=="Black":
        b.Pieces[m].moveInCheck(b)
        b.Pieces[m].canCastle(b.Pieces[16])
        b.Pieces[m].canCastle(b.Pieces[23])
    b.validMove(b.Pieces[m])