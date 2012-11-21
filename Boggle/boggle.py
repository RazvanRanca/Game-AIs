import trie

def readBoard(fileName):
  board = []
  with open(fileName, 'r') as f:
    for line in f:
      board.append(map(lambda x: x.lower(),line.strip().split()))
  return board

def initQueue(board, dc):
  q = []
  for r in range(len(board)):
    for c in range(len(board[r])):
      node = dc.find(board[r][c])
      if node != None:
        q.append((r, c, board[r][c], node, [(r,c)] ))
  return q

def getNeighbours(r, c, seen, board):
  neigh = []
  sr = len(board)
  sc = len(board[0])
  n = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)]
  for (ni, nj) in n:
    nr = r+ni
    nc = c+nj
    if nr >= 0 and nc >= 0 and nr < sr and nc < sc and (not (nr,nc) in seen):
      neigh.append((nr,nc,board[nr][nc]))
  return neigh

def solve(board, dc, minSize = 3):
  words = set()
  queue = initQueue(board, dc)
  oldLen = 0
  #print queue
  while len(queue) > 0:
    (oldRow, oldCol, oldString, oldNode, oldSeen) = queue.pop(0)
    if len(oldString) != oldLen:
      oldLen = len(oldString)
      print oldLen
    neighbours = getNeighbours(oldRow, oldCol, oldSeen, board)
    for (row, col, c) in neighbours:
      if oldNode.hasEdge(c):
        node = oldNode.getChild(c)
        string = oldString + c
        seen = oldSeen + [(row,col)]
        queue.append((row, col, string, node, seen))
        if node.isWord() and len(string) >= minSize and not string in words:
          words.add(string)
  return words

if __name__ == "__main__":
  with open('dictionary', 'r') as f:
    words = f.read().split()
    dc = trie.Trie(words)
    #print dc.find("decipherers").isWord()
    res = solve(readBoard("boggleBoard"), dc)
    lens = map(len, res)
    print map (lambda x : (x,lens.count(x)), set(lens))
    print res
    #print filter(lambda x: len(x)>10, res)
