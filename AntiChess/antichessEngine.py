import sys
import antichess as ac
import time

gameState = [list("rnbqkbnr"),list("pppppppp"),list("........"),list("........"),list("........"),list("........"),list("PPPPPPPP"),list("RNBQKB.R")]

def prettyPrint(rnd):
  with open("antichessLog",'a') as f:
    for i in range(len(gameState)):
      row = gameState[i]
      for j in range(len(row)):
        cell = row[j]
        f.write(str(cell))
      f.write("\n")
    f.write("================" + str(rnd) + "=================\n")

def getPiecesCount():
  c1 = 0
  c2 = 0
  for i in range(len(gameState)):
    row = gameState[i]
    for j in range(len(row)):
      cell = row[j]
      if not cell == '.':
        if cell.isupper():
          c2 += 1
        elif cell.islower():
          c1 += 1
        else:
          raise Exception("WTF is " + str(cell) + " doing here?")
  return (c1,c2)

def existsCapture( player ):
  for r in range(8):
    for c in range(8):
      cell = gameState[r][c]
      if (player == 1 and cell.islower()) or (player == 2 and cell.isupper()):
        if len(filter(lambda (fx,fy,tx,ty): ac.isCapturable(tx,ty,player,gameState), ac.validMovesPiece(r,c,player,gameState))) > 0:
          return True
  return False
  
def isValid(move, player):
  fx = move[0]
  fy = move[1]
  tx = move[2]
  ty = move[3]

  if not ac.inBounds(tx,ty) or not ac.inBounds(fx,fy):
    return False

  cell = gameState[fx][fy]
  if cell == '.':
    return False
  if not (fx,fy,tx,ty) in ac.validMovesPiece(fx,fy,player,gameState):
    return False
  if gameState[tx][ty] == '.' and existsCapture(player):
    return False

  return True  

def makeMove(move, player):
  if not isValid(move, player):
    raise Exception("Attempted move " + str(move) + " by player " + str(player) + " is NOT VALID")
    
  fx = move[0]
  fy = move[1]
  tx = move[2]
  ty = move[3]
  cell = gameState[fx][fy]
  gameState[fx][fy] = '.'
  gameState[tx][ty] = cell
 
def removePieces( player ):
  for i in range(len(gameState)):
    row = gameState[i]
    for j in range(len(row)):
      cell = row[j]
      if (player == 1 and cell.islower()) or (player == 2 and cell.isupper()):
        gameState[i][j] = '.'

def play(style, count = 1):
  open("antichessLog",'w')
  c = 0
  w0 = 0
  w1 = 0
  w2 = 0
  fs1 = 0
  fs2 = 0
  global gameState
  while c < count:
    print str(c) + "------------------"
    with open("antichessLog",'a') as f:
      f.write("++++++++++" + str(c) + "+++++++++++++\n")
    c += 1
    gameState = [list("rnbqkbnr"),list("pppppppp"),list("........"),list("........"),list("........"),list("........"),list("PPPPPPPP"),list("RNBQKBNR")]

    player = 1
    rounds = 0

    if style == 0:
      while rounds < 100 and min(getPiecesCount()) > 0:
        prettyPrint(rounds)
        print "Input player " + str(player) + " move:"
        move = map(int, raw_input().split())
        while not isValid(move,player):
          print "Move invalid, input player " + str(player) + " move again:"
          move = map(int, raw_input().split())
        makeMove(move, player)
        player = player % 2 + 1
        rounds += 1

    elif style == 1:
      if c == 1:
        print "Are you player 1 or player 2?"
        human = int(raw_input())
        print "What type of bot?"
        bot = raw_input()

      while rounds < 100 and min(getPiecesCount()) > 0:
        prettyPrint(rounds)
        if player == human:
          print "Input player " + str(player) + " move:"
          move = map(int, raw_input().split())
          while not isValid(move,player):
            print "Move invalid, input player " + str(player) + " move again:"
            move = map(int, raw_input().split())
          capture = makeMove(move, player)
        else:
          move = ac.engineMove(player, gameState, bot)
          if move == (-100,-100):
            print "Player " + str(player) + "has no available moves left"
            removePieces(player%2 + 1)
            break
          if not isValid(move,player):
            raise Exception("Bot gave invalid move: " + str(move) )
          makeMove(move, player)
          #print "Player " + str(player) + " makes move: " + str(move)

        player = player % 2 + 1
        rounds += 1

    elif style == 2:
      if c == 1:
        print "What type of bot is the first player?"
        bot1 = raw_input()
        print "What type of bot is the second player?"
        bot2 = raw_input()

      while rounds < 100 and min(getPiecesCount()) > 0:
        prettyPrint(rounds)
        if player == 1:
          move = ac.engineMove(player, gameState, bot1)
        else:
          move = ac.engineMove(player, gameState, bot2)
        if move == (-100,-100):
          print "Player " + str(player) + "has no available moves left"
          #removePieces(player%2 + 1)
          break
        if not isValid(move,player):
          raise Exception("Bot gave invalid move: " + str(move) )
        makeMove(move, player)
        #print "Player " + str(player) + " makes move: " + str(move)

        player = player % 2 + 1
        rounds += 1

    (c1,c2) = getPiecesCount()
    fs1 += c1
    fs2 += c2
    print "Player 1: " + str(c1)
    print "Player 2: " + str(c2)
    if c1 < c2:
      w1 += 1
      print "Player 1 wins"
    elif c1 > c2:
      w2 += 1
      print "Player 2 wins"
    else:
      w0 += 1
      print "Game is a tie"
  if c > 1:
    print "=============================="
    print "Wins: P1/P2/Tie: " + str(w1) + "/" + str(w2) + "/" + str(w0)
    print "Score: P1/P2: " + str(fs1) + "/" + str(fs2)

count = 1
if len(sys.argv) > 2:
  count = int(sys.argv[2])
play(int(sys.argv[1]), count)
