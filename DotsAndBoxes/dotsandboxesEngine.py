import sys
import dotsandboxes as db

gameState = [[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0]]

wallCount = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]

def prettyPrint(player):
  with open("dotsandboxesLog",'a') as f:
    f.write("=============== Player: " + str(player) + " =================\n")
    for i in range(len(gameState)):
      row = gameState[i]
      for j in range(len(row)):
        cell = row[j]
        if i%2 == 0 and j%2 == 0:
          f.write(".")
        elif i%2 == 1 and j%2 == 1:
          f.write(str(cell))
        elif i%2 == 0 and j%2 == 1:
          if cell == 1:
            f.write("_")
          else:
            f.write(" ")
        else:
          if cell == 1:
            f.write("|")
          else:
            f.write(" ")
      f.write("\n")

def winner():
  c1 = 0
  c2 = 0
  for i in range(len(gameState)):
    row = gameState[i]
    for j in range(len(row)):
      cell = row[j]
      if i%2 == 1 and j%2 == 1:
        if cell == 0:
          return -1
        elif cell == 1:
          c1 += 1
        else:
          c2 += 1
  return (c1,c2)

def valid(move):
  if move[0] % 2 == move[1] % 2:
    return False
  if move[0] < 0 or move[0] > 10 or move[1] < 0 or move[1] > 10:
    return False
  if not gameState[move[0]][move[1]] == 0:
    return False

  return True

def makeMove(move, player):
  capture = False
  gameState[move[0]][move[1]] = 1
  c1 = -1
  c2 = -1
  r1 = -1
  r2 = -1
  if move[0] % 2 == 1 and move[1] % 2 == 0:
    r1 = (move[0] - 1)/2
    r2 = r1
    c2 = move[1] / 2
    c1 = c2 - 1
  elif move[0] % 2 == 0 and move[1] % 2 == 1:
    c1 = (move[1] - 1)/2
    c2 = c1
    r2 = move[0] / 2
    r1 = r2 - 1
  else:
    raise Exception("Invalid move should have been previously detected")
  if r1 > -1 and r1 < 5 and c1 > -1 and c1 < 5:
    wallCount[r1][c1] += 1
    if wallCount[r1][c1] == 4:
      capture = True
      gameState[r1*2+1][c1*2+1] = player
  if r2 > -1 and r2 < 5 and c2 > -1 and c2 < 5:
    wallCount[r2][c2] += 1
    if wallCount[r2][c2] == 4:
      capture = True
      gameState[r2*2+1][c2*2+1] = player
  return capture
 

def play(style, count = 1):
  open("dotsandboxesLog",'w')
  c = 0
  w0 = 0
  w1 = 0
  w2 = 0
  fs1 = 0
  fs2 = 0
  global gameState
  global wallCount
  while c < count:
    with open("dotsandboxesLog",'a') as f:
      f.write("++++++++++" + str(c) + "+++++++++++++\n")
    c += 1
    gameState = [[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0]]

    wallCount = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]

    player = 1
    capture = False
    if style == 0:
      while winner() == -1:
        print "Input player " + str(player) + " move:"
        move = map(int, raw_input().split())
        while not valid(move):
          print "Move invalid, input player " + str(player) + " move again:"
          move = map(int, raw_input().split())
        capture = makeMove(move, player)
        prettyPrint(player)
        if not capture:
          player = player % 2 + 1

    elif style == 1:
      if c == 1:
        print "Are you player 1 or player 2?"
        human = int(raw_input())
        print "What type of bot?"
        bot = raw_input()

      while winner() == -1:
        if player == human:
          print "Input player " + str(player) + " move:"
          move = map(int, raw_input().split())
          while not valid(move):
            print "Move invalid, input player " + str(player) + " move again:"
            move = map(int, raw_input().split())
          capture = makeMove(move, player)
        else:
          move = db.engineMove(player, gameState, wallCount, bot)
          if not valid(move):
            raise Exception("Bot gave invalid move: " + str(move) )
          capture = makeMove(move, player)
        prettyPrint(player)
        if not capture:
          player = player % 2 + 1

    elif style == 2:
      if c == 1:
        print "What type of bot is the first player?"
        bot1 = raw_input()
        print "What type of bot is the second player?"
        bot2 = raw_input()

      while winner() == -1:
        if player == 1:
          move = db.engineMove(player, gameState, wallCount, bot1)
        else:
          move = db.engineMove(player, gameState, wallCount, bot2)
        if not valid(move):
          raise Exception("Bot gave invalid move: " + str(move) )
        capture = makeMove(move, player)
        prettyPrint(player)
        if not capture:
          player = player % 2 + 1

    (c1,c2) = winner()
    fs1 += c1
    fs2 += c2
    print str(c) + "------------------"
    print "Player 1: " + str(c1)
    print "Player 2: " + str(c2)
    if c1 > c2:
      w1 += 1
      print "Player 1 wins"
    elif c1 < c2:
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

