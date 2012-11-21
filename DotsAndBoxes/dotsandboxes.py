#!/bin/python

import random
import copy
import time

neigh = [(1,0),(-1,0),(0,1),(0,-1)]

def validMoves(game):
  moves = []
  for i in range(len(game)):
    row = game[i]
    for j in range(len(row)):
      cell = row[j]
      if i%2 != j%2 and cell == 0:
        moves.append((i,j))
  return moves

def chainExtraLength( chain ):
  nec = 2
  if chain[1] == True:
    nec = 4
  return len(chain[0]) - nec

def handout( chain, count, game ):
  if chainExtraLength( chain ) != 0:
    raise Exception("Chain isn't correct length for handout")
  if chain[1]:
    cell1 = chain[0][1]
    cell2 = chain[0][2]
    nr = cell2[0] - cell1[0]
    nc = cell2[1] - cell1[1]
    r = cell1[0]*2+1 + nr
    c = cell1[1]*2+1 + nc
  else:
    cell1 = chain[0][0]
    cell2 = chain[0][1]
    nr = cell2[0] - cell1[0]
    nc = cell2[1] - cell1[1]
    notr = cell1[0]*2+1 + nr
    notc = cell1[1]*2+1 + nc
    for (ni,nj) in neigh:
      r = cell2[0]*2+1 + ni
      c = cell2[1]*2+1 + nj
      if game[r][c] == 0 and (r,c) != (notr,notc):
        break

  return (r,c)
  
def prettyPrint(gameState):
  for i in range(len(gameState)):
    row = gameState[i]
    for j in range(len(row)):
      cell = row[j]
      if i%2 == 0 and j%2 == 0:
        print ".",
      elif i%2 == 1 and j%2 == 1:
        print cell,
      elif i%2 == 0 and j%2 == 1:
        if cell == 1:
          print "_",
        else:
          print " ",
      else:
        if cell == 1:
          print "|",
        else:
          print " ",
    print "\n",

def getChains(game, count):
  chains = []
  copyCount = copy.deepcopy(count)
  copyGame = copy.deepcopy(game)
  for i in range(len(copyCount)):
    for j in range(len(copyCount[i])):
      cell = copyCount[i][j]
      if cell == 3:
        ri = i
        rj = j
        copyCount[ri][rj] = 0
        chain = [(ri,rj)]
        closed = 0
        count = 0
        while cell > 1:
          count += 1
          if count == 1000:
            prettyPrint(game)
            print count
          for (ni,nj) in neigh:
            ci = ri + ni
            cj = rj + nj
            r = ri*2 + 1 + ni
            c = rj*2 + 1 + nj
            if r%2 != c%2 and copyGame[r][c] == 0:
              if ci > -1 and ci < 5 and cj > -1 and cj < 5 and copyCount[ci][cj] > 1:
                # print "Hello",i,j,ci,cj,chain,chains
                chain.append((ci,cj))
                if copyCount[ci][cj] == 3:
                  closed = True
                  cell = 0
                copyGame[r][c] = 1
                ri = ci
                rj = cj
              else:
                # print "Hello2",i,j,ci,cj,chain,chains
                closed = False
                cell = 0
              break
          copyCount[ri][rj] = 0
        chains.append((chain, closed))
  return chains

def simulateChainMove(chain,game,count,player = 0):
  for (r,c) in chain[0]:
    count[r][c] = 4
    game[r*2+1][c*2+1] = player
    for (ni,nj) in neigh:
      if game[r*2+1+ni][c*2+1+nj] == 0:
        game[r*2+1+ni][c*2+1+nj] = 1
        if r+ni > -1 and r+ni < 5 and c+nj > -1 and c+nj < 5:
          count[r+ni][c+nj] += 1

def simulateCapturableMove(game,count, player = 0):
  for r in range(len(count)):
    for c in range(len(count[r])):
      if count[r][c] == 3:
        count[r][c] = 4
        game[r*2+1][c*2+1] = player
        for (ni,nj) in neigh:
          if game[r*2+1+ni][c*2+1+nj] == 0:
            game[r*2+1+ni][c*2+1+nj] = 1
            if r+ni > -1 and r+ni < 5 and c+nj > -1 and c+nj < 5:
              count[r+ni][c+nj] += 1

def simulateMove(r,c,game,count, player = 0):
  game[r][c] = 1
  c1 = -1
  c2 = -1
  r1 = -1
  r2 = -1
  if r % 2 == 1 and c % 2 == 0:
    r1 = (r - 1)/2
    r2 = r1
    c2 = c / 2
    c1 = c2 - 1
  elif r % 2 == 0 and c % 2 == 1:
    c1 = (c - 1)/2
    c2 = c1
    r2 = r / 2
    r1 = r2 - 1
  else:
    raise Exception("Invalid move in medBot")
  if r1 > -1 and r1 < 5 and c1 > -1 and c1 < 5:
    count[r1][c1] += 1
    if count[r1][c1] == 4:
      game[r1*2+1][c1*2+1] = player
  if r2 > -1 and r2 < 5 and c2 > -1 and c2 < 5:
    count[r2][c2] += 1
    if count[r2][c2] == 4:
      game[r2*2+1][c2*2+1] = player

def getNoCapturable(game, count):
  cap = []
  for i in range(len(count)):
    row = count[i]
    for j in range(len(row)):
      cell = row[j]
      if cell == 3:
        for (nr,nc) in neigh:
          r = i*2+1 + nr
          c = j*2+1 + nc
          if r%2 != c%2 and game[r][c] == 0:
            cap.append((r,c))
            break
  if len(cap) == 0:
    return 0
  else:
    for (r,c) in cap:
      simulateMove(r,c,game,count)
    return len(cap) + getNoCapturable(game, count)

def existsSafe(game, count):
  for i in range(len(count) - 1):
    row = count[i]
    for j in range(len(row) - 1):
      cell = row[j]
      if cell < 2:
        if count[i][j+1] < 2:
          if game[i*2+1][j*2+2] == 0:
            return True
        if count[i+1][j] < 2:
          if game[i*2+2][j*2+1] == 0:
            return True 

  l = len(count[i])-1
  for i in range(len(count)):
    cell = count[i][0]
    if cell < 2:
      if game[i*2+1][0] == 0:
        return True
    cell = count[i][l]
    if cell < 2:
      if game[i*2+1][l*2+2] == 0:
        return True

    cell = count[0][i]
    if cell < 2:
      if game[0][i*2+1] == 0:
        return True
    cell = count[l][i]
    if cell < 2:
      if game[l*2+2][i*2+1] == 0:
        return True

  return False

def existsCapturable(game, count):
  for i in range(len(count)):
    row = count[i]
    for j in range(len(row)):
      cell = row[j]
      if cell == 3:
        return True 
  return False

def cellsLeft( count ):
  no = 0
  for row in count:
    for cell in row:
      if cell < 4:
        no += 1
  return no

def randomBot( game ):
  moves = validMoves( game )
  index = random.randint(0,len(moves) - 1)
  return moves[index]

def basicBot( game, count ): # always takes a box, tries to avoid offering any boxes
  moves = validMoves( game )
  for i in range(len(count)):
    row = count[i]
    for j in range(len(row)):
      cell = row[j]
      if cell == 3:
        for (nr,nc) in neigh:
          r = i*2+1 + nr
          c = j*2+1 + nc
          if (r,c) in moves:
            return (r,c)
      elif cell == 2:
        for (nr,nc) in neigh:
          r = i*2+1 + nr
          c = j*2+1 + nc
          if (r,c) in moves:
            if len(moves) == 1:
              return (r,c)
            else:
              moves.remove((r,c))
  index = random.randint(0,len(moves) - 1)
  return moves[index]

def medBot( game, count ): # same as basic bot, except is aware of chains and hard hearted handouts
  moves = validMoves( game )
  safe = existsSafe(game, count)
  capturable = existsCapturable(game, count)
  
  if safe and capturable:
    # print "Move 1"
    for i in range(len(count)):
      row = count[i]
      for j in range(len(row)):
        cell = row[j]
        if cell == 3:
          for (nr,nc) in neigh:
            r = i*2+1 + nr
            c = j*2+1 + nc
            if (r,c) in moves:
              return (r,c)

  elif capturable:
    # print "Move 2"
    chains = getChains(game, count)
    final = -1
    for c in range(len(chains)):
      if final == -1 and chainExtraLength(chains[c]) >= 0:
        final = c
      else:
        (i,j) = chains[c][0][0]
        for (nr,nc) in neigh:
          r = i*2+1 + nr
          c = j*2+1 + nc
          if (r,c) in moves:
            # print "Not Final", (r,c), chains
            return (r,c)
    if final == -1:
      raise Exception("Final should never be -1")
    else:
      sacrifice = 2
      if chains[final][1]:
        sacrifice = 4
      if chainExtraLength(chains[final]) > 0 or 2*sacrifice > cellsLeft(count):
        (i,j) = chains[final][0][0]
        for (nr,nc) in neigh:
          r = i*2+1 + nr
          c = j*2+1 + nc
          if (r,c) in moves:
            # print "Final",(r,c), chains
            return (r,c)
      else:
        r = handout(chains[final], count, game)
        # print "Handout",r,chains
        return r

  else:
    # print "Move 3"
    bestDefense  = 100
    bestDefenseMove = (-1,-1)
    for i in range(len(count)):
      row = count[i]
      for j in range(len(row)):
        cell = row[j]
        if cell == 2:
          for (nr,nc) in neigh:
            r = i*2+1 + nr
            c = j*2+1 + nc
            if (r,c) in moves:
              gameCopy = copy.deepcopy(game)
              countCopy = copy.deepcopy(count)
              simulateMove(r,c,gameCopy,countCopy)
              cost = getNoCapturable(gameCopy, countCopy)
              if cost < bestDefense:
                bestDefense = cost
                bestDefenseMove = (r,c)
              moves.remove((r,c))
              if len(moves) == 0:
                #print bestDefense, bestDefenseMove
                return bestDefenseMove
  # print "Move 4"
  #index = random.randint(0,len(moves) - 1)
  return moves[0]

def goodBot( game, count ): # same as med bot, except it tries to estimate if it is worth it to give a handout or take it
  moves = validMoves( game )
  safe = existsSafe(game, count)
  capturable = existsCapturable(game, count)
  
  if safe and capturable:
    # print "Move 1"
    for i in range(len(count)):
      row = count[i]
      for j in range(len(row)):
        cell = row[j]
        if cell == 3:
          for (nr,nc) in neigh:
            r = i*2+1 + nr
            c = j*2+1 + nc
            if (r,c) in moves:
              return (r,c)

  elif capturable:
    # print "Move 2"
    chains = getChains(game, count)
    final = -1
    for c in range(len(chains)):
      if final == -1 and chainExtraLength(chains[c]) >= 0:
        final = c
      else:
        (i,j) = chains[c][0][0]
        for (nr,nc) in neigh:
          r = i*2+1 + nr
          c = j*2+1 + nc
          if (r,c) in moves:
            # print "Not Final", (r,c), chains
            return (r,c)
    if final == -1:
      raise Exception("Final should never be -1")
    else:
      sacrifice = len(chains[final][0])
      possibleHandout = (chains[final][1] and sacrifice == 4) or ((not chains[final][1]) and sacrifice == 2)
      if chainExtraLength(chains[final]) > 0 or not possibleHandout or 2*sacrifice > cellsLeft(count):
        (i,j) = chains[final][0][0]
        for (nr,nc) in neigh:
          r = i*2+1 + nr
          c = j*2+1 + nc
          if (r,c) in moves:
            # print "Final",(r,c), chains
            return (r,c)
      else:
        gameCopy = copy.deepcopy(game)
        countCopy = copy.deepcopy(count)
        simulateChainMove(chains[final],gameCopy,countCopy)
        nextMoves = validMoves( gameCopy )
        minCost = 100
        for nm in nextMoves:
          gameCopyCopy = copy.deepcopy(gameCopy)
          countCopyCopy = copy.deepcopy(countCopy)
          simulateMove(nm[0],nm[1],gameCopyCopy,countCopyCopy)
          cost = getNoCapturable(gameCopyCopy, countCopyCopy)
          if cost < minCost:
            minCost = cost

        if sacrifice >= minCost:
          (i,j) = chains[final][0][0]
          for (nr,nc) in neigh:
            r = i*2+1 + nr
            c = j*2+1 + nc
            if (r,c) in moves:
              # print "Final Sacrifice too big",(r,c), chains
              return (r,c)
        else:
          r = handout(chains[final], count, game)
          # print "Handout",r,chains
          return r

  else:
    # print "Move 3"
    bestDefense  = 100
    bestDefenseMove = (-1,-1)
    for i in range(len(count)):
      row = count[i]
      for j in range(len(row)):
        cell = row[j]
        if cell == 2:
          for (nr,nc) in neigh:
            r = i*2+1 + nr
            c = j*2+1 + nc
            if (r,c) in moves:
              gameCopy = copy.deepcopy(game)
              countCopy = copy.deepcopy(count)
              simulateMove(r,c,gameCopy,countCopy)
              cost = getNoCapturable(gameCopy, countCopy)
              if cost < bestDefense:
                bestDefense = cost
                bestDefenseMove = (r,c)
              moves.remove((r,c))
              if len(moves) == 0:
                #print bestDefense, bestDefenseMove
                return bestDefenseMove
  # print "Move 4"
  index = random.randint(0,len(moves) - 1)
  return moves[index]

def lastBot( player, game, count ): # same as good bot, but uses minimax to look forward a couple turns
  #print "---"
  moves = validMoves( game )
  safe = existsSafe(game, count)
  capturable = existsCapturable(game, count)
  
  if safe and capturable: # if holds this is always optimal
    # print "Move 1"
    for i in range(len(count)):
      row = count[i]
      for j in range(len(row)):
        cell = row[j]
        if cell == 3:
          for (nr,nc) in neigh:
            r = i*2+1 + nr
            c = j*2+1 + nc
            if (r,c) in moves:
              return (r,c)

  elif capturable: # if holds we have chains
    # print "Move 2"
    chains = getChains(game, count)
    final = -1
    for c in range(len(chains)):
      if final == -1 and chainExtraLength(chains[c]) >= 0:
        final = c
      else:                      # if holds we have > 1 chain left of sufficient length => this is optimal
        (i,j) = chains[c][0][0] 
        for (nr,nc) in neigh:
          r = i*2+1 + nr
          c = j*2+1 + nc
          if (r,c) in moves:
            # print "Not Final", (r,c), chains
            return (r,c)
    if final == -1:
      raise Exception("Final should never be -1")
    else:
      sacrifice = len(chains[final][0])
      possibleHandout = (chains[final][1] and sacrifice == 4) or ((not chains[final][1]) and sacrifice == 2)
      if chainExtraLength(chains[final]) > 0 or not possibleHandout or 2*sacrifice > cellsLeft(count): # if holds chain is too long, sacrifice is no longer possible or not worth it => this is optimal
        (i,j) = chains[final][0][0]
        for (nr,nc) in neigh:
          r = i*2+1 + nr
          c = j*2+1 + nc
          if (r,c) in moves:
            # print "Final",(r,c), chains
            return (r,c)
      else:
        gameCopy = copy.deepcopy(game)
        countCopy = copy.deepcopy(count)
        simulateChainMove(chains[final],gameCopy,countCopy,player)
        nextMoves = validMoves( gameCopy )
        minCost = 100
        for nm in nextMoves:
          gameCopyCopy = copy.deepcopy(gameCopy)
          countCopyCopy = copy.deepcopy(countCopy)
          simulateMove(nm[0],nm[1],gameCopyCopy,countCopyCopy,player)
          cost = getNoCapturable(gameCopyCopy, countCopyCopy)
          if cost < minCost:
            minCost = cost

        if sacrifice >= minCost: # if holds chain sacrifice is bigger than next sacrifice. Not optimal
          (i,j) = chains[final][0][0]
          for (nr,nc) in neigh:
            r = i*2+1 + nr
            c = j*2+1 + nc
            if (r,c) in moves:
              # print "Final Sacrifice too big",(r,c), chains
              return (r,c)
        else:
          r = handout(chains[final], count, game)
          # print "Handout",r,chains
          return r

  else: 
    totalTime = 2.0
    timePerBranch = totalTime / len(moves)
    startTime = time.time()

    bestScore = -1000
    bestMoves = []

    minl = 1000
    maxl = -1
    #moves = [(10,3)]
    for i in range(len(moves)):
      move = moves[i]
      gameCopy = copy.deepcopy(game)
      countCopy = copy.deepcopy(count)
      simulateMove(move[0],move[1], gameCopy, countCopy,player)
      #print move, getScore(player, gameCopy)
      (score,l,ll) = minMax(player%2 + 1, gameCopy, countCopy, startTime + (i+1)*timePerBranch, 0, -1)
      if l < minl:
        minl = l
      if ll > maxl:
        maxl = ll

      #print move, score
      if score > bestScore:
        bestScore = score
        bestMoves = [move]
      elif score == bestScore:
        bestMoves.append(move)
    
    print minl,maxl
    if len(bestMoves) == 1:
      return bestMoves[0]
    else:
      index = random.randint(0,len(bestMoves) - 1)
      return bestMoves[index]
    # print "Move 3"
    """bestDefense  = 100 # no capturable moves, tries to avoid bad moves, not optimal
    bestDefenseMove = (-1,-1)
    for i in range(len(count)):   # if move which allows oponent to capture next turn needs to be made, move which costs lest next turn is made
      row = count[i]
      for j in range(len(row)):
        cell = row[j]
        if cell == 2:
          for (nr,nc) in neigh:
            r = i*2+1 + nr
            c = j*2+1 + nc
            if (r,c) in moves:
              gameCopy = copy.deepcopy(game)
              countCopy = copy.deepcopy(count)
              simulateMove(r,c,gameCopy,countCopy)
              cost = getNoCapturable(gameCopy, countCopy)
              if cost < bestDefense:
                bestDefense = cost
                bestDefenseMove = (r,c)
              moves.remove((r,c))
              if len(moves) == 0:
                #print bestDefense, bestDefenseMove
                return bestDefenseMove
  # print "Move 4"
  index = random.randint(0,len(moves) - 1)
  return moves[index]"""


def reallyLastBot( player, game, count ): # same as good bot, but uses minimax to look forward a couple turns
  #print "---"
  moves = validMoves( game )
  safe = existsSafe(game, count)
  capturable = existsCapturable(game, count)
  
  if safe and capturable: # if holds this is always optimal
    #print "Move 1"
    for i in range(len(count)):
      row = count[i]
      for j in range(len(row)):
        cell = row[j]
        if cell == 3:
          for (nr,nc) in neigh:
            r = i*2+1 + nr
            c = j*2+1 + nc
            if (r,c) in moves:
              return (r,c)

  elif capturable: # if holds we have chains
    #print "Move 2"
    chains = getChains(game, count)
    final = -1
    for c in range(len(chains)):
      if final == -1 and chainExtraLength(chains[c]) >= 0:
        final = c
      else:                      # if holds we have > 1 chain left of sufficient length => this is optimal
        (i,j) = chains[c][0][0] 
        for (nr,nc) in neigh:
          r = i*2+1 + nr
          c = j*2+1 + nc
          if (r,c) in moves:
            # print "Not Final", (r,c), chains
            return (r,c)
    if final == -1:
      raise Exception("Final should never be -1")
    else:
      sacrifice = len(chains[final][0])
      possibleHandout = (chains[final][1] and sacrifice == 4) or ((not chains[final][1]) and sacrifice == 2)
      if chainExtraLength(chains[final]) > 0 or not possibleHandout or 2*sacrifice > cellsLeft(count): # if holds chain is too long, sacrifice is no longer possible or not worth it => this is optimal
        (i,j) = chains[final][0][0]
        for (nr,nc) in neigh:
          r = i*2+1 + nr
          c = j*2+1 + nc
          if (r,c) in moves:
            # print "Final",(r,c), chains
            return (r,c)
      else:
        gameCopy = copy.deepcopy(game)
        countCopy = copy.deepcopy(count)
        simulateChainMove(chains[final],gameCopy,countCopy,player)
        nextMoves = validMoves( gameCopy )
        minCost = 100
        for nm in nextMoves:
          gameCopyCopy = copy.deepcopy(gameCopy)
          countCopyCopy = copy.deepcopy(countCopy)
          simulateMove(nm[0],nm[1],gameCopyCopy,countCopyCopy,player)
          cost = getNoCapturable(gameCopyCopy, countCopyCopy)
          if cost < minCost:
            minCost = cost

        if sacrifice >= minCost: # if holds chain sacrifice is bigger than next sacrifice. Not optimal
          (i,j) = chains[final][0][0]
          for (nr,nc) in neigh:
            r = i*2+1 + nr
            c = j*2+1 + nc
            if (r,c) in moves:
              # print "Final Sacrifice too big",(r,c), chains
              return (r,c)
        else:
          r = handout(chains[final], count, game)
          # print "Handout",r,chains
          return r

  else: 
    #print "Move 3"
    bestDefense  = 100 # no capturable moves, tries to avoid bad moves, not optimal
    bestDefenseMove = (-1,-1)
    for i in range(len(count)):   # if move which allows oponent to capture next turn needs to be made, move which costs lest next turn is made
      row = count[i]
      for j in range(len(row)):
        cell = row[j]
        if cell == 2:
          for (nr,nc) in neigh:
            r = i*2+1 + nr
            c = j*2+1 + nc
            if (r,c) in moves:
              gameCopy = copy.deepcopy(game)
              countCopy = copy.deepcopy(count)
              simulateMove(r,c,gameCopy,countCopy)
              cost = getNoCapturable(gameCopy, countCopy)
              if cost < bestDefense:
                bestDefense = cost
                bestDefenseMove = (r,c)
              moves.remove((r,c))
              if len(moves) == 0:
                #print bestDefense, bestDefenseMove
                return bestDefenseMove
    #print "Move 4"
    totalTime = 10.0
    timePerBranch = totalTime / len(moves)
    startTime = time.time()

    bestScore = -1000
    bestMoves = []

    minl = 1000
    maxl = -1
    #moves = [(10,3)]
    for i in range(len(moves)):
      move = moves[i]
      gameCopy = copy.deepcopy(game)
      countCopy = copy.deepcopy(count)
      simulateMove(move[0],move[1], gameCopy, countCopy,player)
      #print move, getScore(player, gameCopy)
      (score,l,ll) = minMax(player%2 + 1, gameCopy, countCopy, startTime + (i+1)*timePerBranch, 0, -1)
      if l < minl:
        minl = l
      if ll > maxl:
        maxl = ll

      #print move, score
      if score > bestScore:
        bestScore = score
        bestMoves = [move]
      elif score == bestScore:
        bestMoves.append(move)
    
    print minl,maxl
    if len(bestMoves) == 1:
      return bestMoves[0]
    else:
      index = random.randint(0,len(bestMoves) - 1)
      return bestMoves[index]

def getScore(player, game): #evaluation function of min-max search. my line count - oponent's line count
  p1 = 0
  p2 = 0
  for i in range(len(game)):
    for j in range(len(game[i])):
      if i%2 == 1 and j%2 == 1:
        cell = game[i][j]
        if cell == 1:
          p1 += 1
        elif cell == 2:
          p2 += 1

  if player == 1:
    return p1 - p2
  else:
    return p2 - p1

def minMax (player, game, count, stopTime, level = 0, tp = 1, best1 = -1000, best2 = 1000):
  #print level
  
  ppp = False
  while existsSafe(game, count) and existsCapturable(game, count): # if holds this is always optimal, take all capturable pieces
    simulateCapturableMove(game,count,player)
    ppp = True

  if not ppp and existsCapturable(game, count): # if holds we have chains

   # print "Move 2", count
    #prettyPrint(game)
    chains = getChains(game, count)
    #print chains
    final = -1
    for c in range(len(chains)):
      if final == -1 and chainExtraLength(chains[c]) >= 0:
        final = c
      else:                      # if holds we have > 1 chain left of sufficient length => this is optimal, take whole chain
        #print "ChainMove", chains[c]
        simulateChainMove(chains[c],game,count,player)
    #prettyPrint(game)
    #print count
    sacrifice = 2
    if chains[final][1]:
      sacrifice = 4

    possibleHandout = (chains[final][1] and len(chains[final][0]) == 4) or ((not chains[final][1]) and len(chains[final][0]) == 2)
    if chainExtraLength(chains[final]) > 0 or not possibleHandout or 2*sacrifice > cellsLeft(count): # if holds chain is too long, sacrifice is no longer possible or not worth it => this is optimal, take pieces from chain till this condition fails
      takeLen = chainExtraLength(chains[final])
      if not possibleHandout or 2*sacrifice > cellsLeft(count):
        takeLen = len(chains[final][0])
      #print takeLen, possibleHandout
      for ttt in range(takeLen):
        (i,j) = chains[final][0][ttt]
        #print ttt, (i,j)
        for (nr,nc) in neigh:
          r = i*2+1 + nr
          c = j*2+1 + nc
          if game[r][c] == 0:
            #print "Final",(r,c), chains
            simulateMove(r,c,game,count,player)
            break

    else:
      #prettyPrint(game)
      #print "Handout",chains
      minl = 1000
      maxl = -1
      r = handout(chains[final], count, game)
      gameCopy = copy.deepcopy(game)
      countCopy = copy.deepcopy(count)
      simulateMove(r[0],r[1], gameCopy, countCopy,player)
      (score1,l,ll) = minMax (player%2+1, gameCopy, countCopy, stopTime, level +1, tp*-1,best1,best2)
      if l < minl:
        minl = l
      if ll > maxl:
        maxl = ll

      if tp == 1 and score1 >= best1:
        best1 = score1
     
      if tp == -1 and score1 <= best2:
        best2 = score1

      gameCopy = copy.deepcopy(game)
      countCopy = copy.deepcopy(count)
      simulateChainMove(chains[final], gameCopy, countCopy, player)
      (score2,l,ll) = minMax (player, gameCopy, countCopy, stopTime, level, tp,best1,best2)
      if l < minl:
        minl = l
      if ll > maxl:
        maxl = ll

      if tp == 1:
        if score1 > score2:
          return (score1,minl,maxl)
        else:
          return (score2,minl,maxl)
      else:
        if score1 > score2:
          return (score2,minl,maxl)
        else:
          return (score1,minl,maxl)
   
  if level > 1 and (level >= 4 or time.time() > stopTime):
    return (tp*getScore(player, game), level, level)
  else:
    cb1 = -1000
    cb2 = 1000

    moves = validMoves( game )
    #if level == 0:
    #  prettyPrint(game)
    #  print count, existsSafe(game, count)
    minl = 1000
    maxl = -1
    for move in moves:
      gameCopy = copy.deepcopy(game)
      countCopy = copy.deepcopy(count)
      simulateMove(move[0],move[1], gameCopy, countCopy,player)
      (score,l,ll) = minMax(player%2+1, gameCopy, countCopy, stopTime, level + 1, tp*-1,best1,best2)
      #if level == 0:
      #  print move, score
      if l < minl:
        minl = l
      if ll > maxl:
        maxl = ll

      if tp == 1 and score >= best1:
        best1 = score

      if tp == 1 and score >= cb1:
        cb1 = score
     
      if tp == -1 and score <= best2:
        best2 = score
      
      if tp == -1 and score <= cb2:
        cb2 = score
          
      if best1 >= best2:
          break # alfa beta pruning

    bestScore = cb1
    if tp == -1:
      bestScore = cb2

    return (bestScore, minl, maxl)

def engineMove(player, game, count, style):
  if style == "r":
    return randomBot( game )
  elif style == "b":
    return basicBot( game, count )
  elif style == "m":
    return medBot( game, count )
  elif style == "g":
    return goodBot( game, count )
  elif style == "l":
    return lastBot( player, game, count )
  elif style == "rl":
    return reallyLastBot( player, game, count )


def getCount( game ):
  count = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
  for i in range(5):
    for j in range(5):
      for (nr,nc) in neigh:
        r = i*2+1 + nr
        c = j*2+1 + nc
        if game[r][c] == 1:
          count[i][j] += 1
  return count

def translate( row ):
  tr = ""
  for j in range(len(row)):
    cell = row[j]
    if cell == '.' or cell == ' ':
      tr += "0 "
    elif cell == '_' or cell == '|':
      tr += "1 "
    elif cell == '1' or cell == '2' or cell == '0':
      tr = tr + cell + " "
  return tr

if __name__ == "__main__":
  p = int(raw_input())
  trans = False  
  if p == 0:
    trans = True
    p = int(raw_input())
  game = []
  for i in range(11):
    inp = raw_input()
    if trans:
      inp = translate(inp)
    game.append(map(int, inp.split()))
  c = getCount( game )
  move = engineMove(p, game, c, "rl")
  print "%d %d" % (move[0], move[1])
