#!/bin/python

def mapChar(c):
  if c == 'X':
    return 1
  if c == 'O':
    return 2
  return -1

p = mapChar(raw_input())
row1 = map(lambda x: mapChar(x), raw_input())
row2 = map(lambda x: mapChar(x), raw_input())
row3 = map(lambda x: mapChar(x), raw_input())
b = [row1,row2,row3]

def getLine(board,line):
  if line < 3:
    return board[line]
  elif line < 6:
    line -= 3
    return [board[0][line],board[1][line],board[2][line]]
  elif line == 6:
    return [board[0][0],board[1][1],board[2][2]]
  else:
    return [board[0][2],board[1][1],board[2][0]]

def winner(board):
  for l in range(8):
    line = getLine(board,l)
    # print board, l, line, line[0], line[0] == line[1] and line[1] == line[2]
    if line[0] != -1 and line[0] == line[1] and line[1] == line[2]:
      return line[0]
  if complete(board):
    return -1
  return 0

def complete(board):
  return not(-1 in board[0] or -1 in board[1] or -1 in board[2])

def availPos(board):
  pos = []
  for i in range(3):
    for j in range(3):
      if board[i][j] == -1:
        pos.append((i,j))
  return pos

def other(player):
  if player == 1:
    return 2
  else:
    return 1

def value(board,player,tp):
  rez = (-4,-4)
  w = winner(board)
  avgVal = 0.0
  if w == 0:
    pos = availPos(board)
    retVal = -3
    retPos = -3
    curAvgVal = 0.0
    count = 0
    unique = True
    for p in pos:
        count += 1
        newBoard = [[0,0,0],[0,0,0],[0,0,0]]
        for i in range(3):
          for j in range(3):
            newBoard[i][j] = board[i][j]
        newBoard[p[0]][p[1]] = player
        val = value(newBoard,other(player),tp*-1)
        rVal = val[0]
        aVal = val[1]
        avgVal += aVal
        if rVal == retVal:
          unique = False

        #if board == b:
          #print p, val
        if retVal == -3:
          retVal = rVal
          retPos = p
          curAvgVal = aVal
        elif tp == 1 and (rVal > retVal or (rVal == retVal and aVal > curAvgVal)):
          if rVal > retVal:
            unique = True
          retVal = rVal
          retPos = p
          curAvgVal = aVal
        elif tp == -1 and (rVal < retVal or (rVal == retVal and aVal < curAvgVal)):
          if rVal < retVal:
            unique = True
          retVal = rVal
          retPos = p
          curAvgVal = aVal

    avgVal /= count
    if tp == 1 or unique:
      rez =  (retVal, curAvgVal, retPos)
    else:
      rez =  (retVal, avgVal, retPos)

  elif w == player:
    rez = (tp,tp,-3)
  elif w == other(player):
    rez = (-1*tp,-1*tp,-3)
  else:
    rez = (0,0,-3)
  return rez


rez = value(b,p,1)
#print rez
if rez[1] != -3:
  print "%d %d" % (rez[2][0], rez[2][1])
