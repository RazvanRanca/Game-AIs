#!/bin/python

import random
import copy
import time

def isCapturable(r, c, player, gameState):
  return (player == 1 and gameState[r][c].isupper()) or (player == 2 and gameState[r][c].islower())
  
def inBounds(r, c):
  return r > -1 and r < 8 and c > -1 and c < 8

def pawnMove(r, c, player, gameState):
  moves = []
  if player == 1:
    if inBounds(r+1,c):
      if gameState[r+1][c] == '.':
        moves.append((r,c,r+1,c))
      if inBounds(r+1,c-1) and gameState[r+1][c-1].isupper():
        moves.append((r,c,r+1,c-1))
      if inBounds(r+1,c+1) and gameState[r+1][c+1].isupper():
        moves.append((r,c,r+1,c+1))
  elif player == 2:
    if inBounds(r-1,c):
      if gameState[r-1][c] == '.':
        moves.append((r,c,r-1,c))
      if inBounds(r-1,c-1) and gameState[r-1][c-1].islower():
        moves.append((r,c,r-1,c-1))
      if inBounds(r-1,c+1) and gameState[r-1][c+1].islower():
        moves.append((r,c,r-1,c+1))
  else:
    raise Exception("There should only be 2 players, in pawnMove")
  return moves

def pawnCapture(r, c, player, gameState):
  moves = []
  if player == 1:
    if inBounds(r+1,c):
      if inBounds(r+1,c-1) and gameState[r+1][c-1].isupper():
        moves.append((r,c,r+1,c-1))
      if inBounds(r+1,c+1) and gameState[r+1][c+1].isupper():
        moves.append((r,c,r+1,c+1))
  elif player == 2:
    if inBounds(r-1,c):
      if inBounds(r-1,c-1) and gameState[r-1][c-1].islower():
        moves.append((r,c,r-1,c-1))
      if inBounds(r-1,c+1) and gameState[r-1][c+1].islower():
        moves.append((r,c,r-1,c+1))
  else:
    raise Exception("There should only be 2 players, in pawnMove")
  return moves
  
def rookMove(r, c, player, gameState):
  moves = []
  for i in range(r+1,8):
    if gameState[i][c] == '.':
      moves.append((r,c,i,c))
    else:
      if isCapturable(i,c,player,gameState):
        moves.append((r,c,i,c))
      break
  for i in range(r-1,-1,-1):
    if gameState[i][c] == '.':
      moves.append((r,c,i,c))
    else:
      if isCapturable(i,c,player,gameState):
        moves.append((r,c,i,c))
      break
  for i in range(c+1,8):
    if gameState[r][i] == '.':
      moves.append((r,c,r,i))
    else:
      if isCapturable(r,i,player,gameState):
        moves.append((r,c,r,i))
      break
  for i in range(c-1,-1,-1):
    if gameState[r][i] == '.':
      moves.append((r,c,r,i))
    else:
      if isCapturable(r,i,player,gameState):
        moves.append((r,c,r,i))
      break
  return moves

def knightMove(r, c, player, gameState):
  moves = []
  xm = [-2,-2,-1,-1,1,1,2,2]
  ym = [1,-1,2,-2,2,-2,1,-1]
  for i in range(len(xm)):
    nr = r + xm[i]
    nc = c + ym[i]
    if not inBounds(nr,nc):
      continue
    if gameState[nr][nc] == '.' or isCapturable(nr,nc,player,gameState):
      moves.append((r,c,nr,nc))
      
  return moves

def bishopMove(r, c, player, gameState):
  moves = []
  for i in range(1,8):
    if not inBounds(r+i,c+i):
      break
    if gameState[r+i][c+i] == '.':
      moves.append((r,c,r+i,c+i))
    else:
      if isCapturable(r+i,c+i,player,gameState):
        moves.append((r,c,r+i,c+i))
      break
  for i in range(1,8):
    if not inBounds(r+i,c-i):
      break
    if gameState[r+i][c-i] == '.':
      moves.append((r,c,r+i,c-i))
    else:
      if isCapturable(r+i,c-i,player,gameState):
        moves.append((r,c,r+i,c-i))
      break
  for i in range(1,8):
    if not inBounds(r-i,c+i):
      break
    if gameState[r-i][c+i] == '.':
      moves.append((r,c,r-i,c+i))
    else:
      if isCapturable(r-i,c+i,player,gameState):
        moves.append((r,c,r-i,c+i))
      break
  for i in range(1,8):
    if not inBounds(r-i,c-i):
      break
    if gameState[r-i][c-i] == '.':
      moves.append((r,c,r-i,c-i))
    else:
      if isCapturable(r-i,c-i,player,gameState):
        moves.append((r,c,r-i,c-i))
      break
  return moves

def queenMove(r, c, player, gameState):
  return rookMove(r,c,player,gameState) + bishopMove(r,c,player,gameState)

def kingMove(r, c, player, gameState):
  moves = []
  for i in range(-1,2):
    for j in range(-1,2):
      if (i == 0 and j == 0) or not inBounds(r+i,c+j):
        continue
      if gameState[r+i][c+j] == '.' or isCapturable(r+i,c+j,player,gameState):
        moves.append((r,c,r+i,c+j))
  return moves

def validMovesPiece(r, c, player, game):
  moves = []
  if not inBounds(r,c):
    raise Exception("Invalid position in -validMoves-")
  cell = game[r][c]
  if cell == '.':
    raise Exception("Trying to move empty square")
  elif (player == 1 and cell.isupper()) or (player == 2 and cell.islower()):
    raise Exception("Player doesn't match cell case " + str(player) + " - " + cell)
  elif cell == 'p' or cell == 'P':
    moves = pawnMove(r,c,player,game)
  elif cell == 'r' or cell == 'R':
    moves = rookMove(r,c,player,game)
  elif cell == 'b' or cell == 'B':
    moves = bishopMove(r,c,player,game)
  elif cell == 'n' or cell == 'N':
    moves = knightMove(r,c,player,game)
  elif cell == 'q' or cell == 'Q':
    moves = queenMove(r,c,player,game)
  elif cell == 'k' or cell == 'K':
    moves = kingMove(r,c,player,game)
  else:
    raise Exception("WTF is this shit: " + str(cell))

  return moves

def capturingMovesPiece(r, c, cell, player, game):
  moves = []
  if not inBounds(r,c):
    raise Exception("Invalid position in -validMoves-")
  if cell == 'p' or cell == 'P':
    moves = pawnCapture(r,c,player,game)
  elif cell == 'r' or cell == 'R':
    moves = rookMove(r,c,player,game)
  elif cell == 'b' or cell == 'B':
    moves = bishopMove(r,c,player,game)
  elif cell == 'n' or cell == 'N':
    moves = knightMove(r,c,player,game)
  elif cell == 'q' or cell == 'Q':
    moves = queenMove(r,c,player,game)
  elif cell == 'k' or cell == 'K':
    moves = kingMove(r,c,player,game)

  return map(lambda (fx,fy,tx,ty) : (tx,ty), moves)

def validMoves(player, game):
  moves = []
  for r in range(8):
    for c in range(8):
      cell = game[r][c]
      if (player == 1 and cell.islower()) or (player == 2 and cell.isupper()):
        moves += validMovesPiece(r,c,player,game)
          
  capturingMoves = filter(lambda (fx,fy,tx,ty): isCapturable(tx,ty,player,game), moves)
  if capturingMoves == []:
    return moves
  else:
    return capturingMoves

def getCapturablePos(player, game):
  cap = []
  for r in range(8):
    for c in range(8):
      cell = game[r][c]
      if (player == 1 and cell.islower()) or (player == 2 and cell.isupper()):
        cap += capturingMovesPiece(r,c,game[r][c],player,game)
  return cap

def getNextPos(player, game): # all positions where a player may have a piece on your next turn
  pos = []
  for r in range(8):
    for c in range(8):
      cell = game[r][c]
      if (player == 1 and cell.islower()) or (player == 2 and cell.isupper()):
        pos.append((r,c))
        pos += map(lambda (fx,fy,tx,ty) : (tx,ty), validMovesPiece(r,c,player,game))
  return pos

def hasValidMove(player, game):
  for r in range(8):
    for c in range(8):
      cell = game[r][c]
      if (player == 1 and cell.islower()) or (player == 2 and cell.isupper()):
        if len(validMovesPiece(r,c,player,game)) > 0:
          return True
  return False

def countPieces(game):
  p1 = 0
  p2 = 0
  for row in game:
    for cell in row:
      if cell.islower():
        p1 += 1
      elif cell.isupper():
        p2 += 1
  return (p1,p2)

def getScore(player, game): #evaluation function of min-max search. oponent's piece count - my piece count or -20/20 for lost/won
  (c1,c2) = countPieces(game)
  if c1 == 0:
    if player == 1:
      return 20
    else:
      return -20
  if c2 == 0:
    if player == 1:
      return -20
    else:
      return 20

  #if not hasValidMove(player, game):
  #  return -20

  if player == 1:
    return c2 - c1
  else:
    return c1 - c2

def simulateMove(move, game):
  fx = move[0]
  fy = move[1]
  tx = move[2]
  ty = move[3]
  cell = game[fx][fy]
  game[fx][fy] = '.'
  game[tx][ty] = cell
 
def removePieces( player ):
  for i in range(len(gameState)):
    row = gameState[i]
    for j in range(len(row)):
      cell = row[j]
      if (player == 1 and cell.islower()) or (player == 2 and cell.isupper()):
        gameState[i][j] = '.'

def randomBot( player, game ):
  moves = validMoves( player, game )
  if len(moves) > 0:
    index = random.randint(0,len(moves) - 1)
    return moves[index]
  else:
    return (-100,-100)

def basicBot( player, game ): # always makes the oponent take a piece if possible and try to make it so that him taking a piece doesn't force you to take it back
  moves = validMoves( player, game )
  if len(moves) > 0:
    mt = getCapturablePos( player, game )
    ht = getCapturablePos( player%2 + 1, game )
    forced = filter(lambda (fx,fy,tx,ty): (tx,ty) in ht, moves)
    if len(forced) > 0:
      betterForced = filter(lambda (fx,fy,tx,ty) : not (tx,ty) in mt, forced)
      if len(betterForced) > 0:
        index = random.randint(0,len(betterForced) - 1)
        return betterForced[index]
      else:
        index = random.randint(0,len(forced) - 1)
        return forced[index]
    else:
      index = random.randint(0,len(moves) - 1)
      return moves[index]
  else:
    return (-100,-100)

def medBot( player, game ): # same as basic bot, except it also tries to avoid moving somewhere that will cause him to capture a piece next turn
  moves = validMoves( player, game )
  if len(moves) > 0:
    mt = getCapturablePos( player, game )
    ht = getCapturablePos( player%2 + 1, game )
    #mp = getNextPos( player, game )
    hp = getNextPos( player%2 + 1, game )

    forced = filter(lambda (fx,fy,tx,ty): (tx,ty) in ht, moves)
    if len(forced) > 0:
      betterForced = filter(lambda (fx,fy,tx,ty) : not (tx,ty) in mt, forced)
      if len(betterForced) > 0:
        index = random.randint(0,len(betterForced) - 1)
        return betterForced[index]
      else:
        index = random.randint(0,len(forced) - 1)
        return forced[index]
    else:
      defenseMoves = filter(lambda (fx,fy,tx,ty): not any([(a in hp) for a in capturingMovesPiece(tx,ty,game[fx][fy],player,game)]) , moves)
      if len(defenseMoves) > 0:
        index = random.randint(0,len(defenseMoves) - 1)
        return defenseMoves[index]
      else:
        index = random.randint(0,len(moves) - 1)
        return moves[index]
  else:
    return (-100,-100)

def decentBot( player, game, level=0, stopTime=0): # does stupid min-max brute search. Should simulate at least the same as medBot(i.e. 2 moves deep), hopefully more
  moves = validMoves( player, game )
  if len(moves) == 0:
    if level > 1:
      return (0, -30, level, level)
    elif level == 1:
      return (0, -30, level, level, time.time())
    else:
      return (-100,-100)
  bestScore = -100
  bestMove = 0
  minlevel = 100
  maxlevel = -1
  if level == 0:
    totalTime = 4.0
    timePerBranch = totalTime / len(moves)
    startTime = time.time()
    for i in range(len(moves)):
      move = moves[i]
      gameCopy = copy.deepcopy(game)
      simulateMove(move, gameCopy)
      (mv,score,l,ll,t) = decentBot(player%2+1, gameCopy, level+1, startTime + timePerBranch)
      # print i, l, ll, t - startTime
      startTime = t
      score *= -1
      if l < minlevel:
        minlevel = l
      if ll > maxlevel:
        maxlevel = ll
      if score >= bestScore:
        bestScore = score
        bestMove = move

    #print minlevel, maxlevel
    if bestMove == 0:
      # print "FUCKUP"
      return moves[0]
    else:
      return bestMove
  else:  
    if level > 1 and (time.time() > stopTime or level == 5):
      for move in moves:
        gameCopy = copy.deepcopy(game)
        simulateMove(move, gameCopy)
        score = getScore(player, gameCopy)
        minlevel = level
        maxlevel = level
        if score >= bestScore:
          bestScore = score
          bestMove = move
    else:
      for move in moves:
        gameCopy = copy.deepcopy(game)
        simulateMove(move, gameCopy)
        (mv,score,l,ll) = decentBot(player%2+1, gameCopy, level+1, stopTime)
        score *= -1
        if l < minlevel:
          minlevel = l
        if ll > maxlevel:
          maxlevel = ll
        if score >= bestScore:
          bestScore = score
          bestMove = move
    if level > 1:
      return (bestMove,bestScore, minlevel, maxlevel)
    else:
      return (bestMove,bestScore, minlevel, maxlevel, time.time())

def alfabetaBot( player, game, level=0, stopTime=0, best1 = -1000, best2 = 1000, turn = 1 ): # same as decent bot except does alfa beta prunning
  moves = validMoves( player, game )
  if len(moves) == 0:
    score = getScore(player, game)  
    if score > 0:
      score = 20
    elif score < 0:
      score = -20
    if level > 1:
      return ([], score*turn, level, level)
    elif level == 1:
      return ([], score*turn, level, level, time.time())
    else:
      return (-100,-100)
  bestMove = []
  bestScore = -1337
  minlevel = 100
  maxlevel = -1
  if level == 0:
    totalTime = 10.0
    timePerBranch = totalTime / len(moves)
    startTime = time.time()
    for i in range(len(moves)):
      move = moves[i]

      gameCopy = []
      for l in game:
        gameCopy.append(list(l))

      simulateMove(move, gameCopy)
      (mv,score,l,ll,t) = alfabetaBot(player%2+1, gameCopy, level+1, startTime + timePerBranch, best1, best2, -1)
      #print i,score, move,mv,l, ll, t - startTime
      startTime = t
      if l < minlevel:
        minlevel = l
      if ll > maxlevel:
        maxlevel = ll
      if score > best1:
        best1 = score
        bestMove = move

    #print minlevel, maxlevel
    if bestMove == []:
      # print "FUCKUP"
      return moves[0]
    else:
      return bestMove
  else:  
    if level > 4 and (time.time() > stopTime or level == 10):
      bestScore = getScore(player, game)
      bestScore *= turn
      #if score > 0:
      #  print score, turn, best1, best2, move
      minlevel = level
      maxlevel = level
      bestMove = []        
    else:
      cb1 = -1000
      cb2 = 1000
      for move in moves:
        gameCopy = []
        for l in game:
          gameCopy.append(list(l))

        simulateMove(move, gameCopy)
        (mv,score,l,ll) = alfabetaBot(player%2+1, gameCopy, level+1, stopTime, best1, best2, turn*-1)
        #if level == 1:
        #  print "---1---",score, move,mv
        #if level == 2:
        #  print "---2---",score, move,mv, best1, best2           
        #  prettyPrint(gameCopy)
        if l < minlevel:
          minlevel = l
        if ll > maxlevel:
          maxlevel = ll
        if turn == 1 and score >= best1:
          best1 = score
          cb1 = score

        if turn == 1 and score >= cb1:
          cb1 = score
          bestMove = [(move,score)] + mv

        if turn == -1 and score <= best2:
          best2 = score
          cb2 = score

        if turn == -1 and score <= cb2:
          cb2 = score
          bestMove = [(move,score)] + mv

        if best1 >= best2:
          break # alfa beta pruning
      bestScore = cb1
      if turn == -1:
        bestScore = cb2

    if level > 1:
      return (bestMove,bestScore, minlevel, maxlevel)
    else:
      return (bestMove,bestScore, minlevel, maxlevel, time.time())
    
def prettyPrint(gameState):
  for i in range(len(gameState)):
    row = gameState[i]
    for j in range(len(row)):
      cell = row[j]
      print cell,
    print""
  print "=================================\n"

def engineMove(player, game, style):
  if style == "r":
    return randomBot( player, game )
  elif style == "b":
    return basicBot( player, game )
  elif style == "m":
    return medBot( player, game )
  elif style == "d":
    return decentBot( player, game )
  elif style == "a":
    return alfabetaBot( player, game )

if __name__ == "__main__":
  p = int(raw_input())
  game = []
  for i in range(8):
    game.append(list(raw_input()))
  startTime = time.time()
  move = engineMove(p, game, "a")
  print "%d %d %d %d" % (move[0], move[1], move[2], move[3])
  #print time.time() - startTime
