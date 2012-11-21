import sys
sys.setrecursionlimit(20000)

class Node:
  def __init__(self, **kw): #left, right, up, down, (col, row, [name, size])
    for k,v in kw.iteritems():
      setattr(self,k,v)

  def __str__(self):
    return str(self.__dict__.keys())

class DancingLinks:
  def __init__(self, mat):
    self.head = Node(size = (len(mat),len(mat[0])), name = -1)
    self.output = {}
    self.solutions = set()
    self.noSols = 0
    self.startDance = 0
    self.tl = []
    prevLeft = self.head
    prevUp = self.head
    rowList = []
    colList = []

    self.tl += [((-1,i),(-1,i+1)) for i in range(-1, len(mat[0]) - 1)] + [((-1,len(mat[0]) -1),(-1,-1))] # column row
    self.tl += [((i,-1),(i+1,-1)) for i in range(-1, len(mat) - 1)] + [((len(mat)-1,-1),(-1,-1))] # row column

    for i in range(len(mat)): # create row headers
      cur = Node(up = prevUp, col = self.head, name = i)
      cur.row = cur
      rowList.append(cur)
      prevUp.down = cur
      prevUp = cur

    for i in range(len(mat[0])): # create column headers
      cur = Node(left = prevLeft, row = self.head, name = i, size = 0)
      cur.col = cur
      colList.append(cur)
      prevLeft.right = cur
      prevLeft = cur

    self.head.left = prevLeft
    self.head.up = prevUp
    prevLeft.right = self.head
    prevUp.down = self.head
    prevUp = list(colList)

    for i in range(len(mat)): # create sparse table
      prevLeft = rowList[i]
      for j in range(len(mat[i])):
        if mat[i][j] == 1:
          cur = Node(left = prevLeft, right = rowList[i], up = prevUp[j], down = colList[j], col = colList[j], row = rowList[i])
          prevLeft.right = cur
          prevUp[j].down = cur
          cur.col.size += 1
          self.tl += [((prevLeft.row.name,prevLeft.col.name),(cur.row.name,cur.col.name)),((prevUp[j].row.name,prevUp[j].col.name),(cur.row.name,cur.col.name))]

          prevLeft = cur
          prevUp[j] = cur
      rowList[i].left = prevLeft
      self.tl += [((rowList[i].row.name,rowList[i].col.name),(prevLeft.row.name,prevLeft.col.name))]

    for i in range(len(mat[0])): # assign column up values
      colList[i].up = prevUp[i]
      self.tl += [((colList[i].row.name,colList[i].col.name),(prevUp[i].row.name,prevUp[i].col.name))]

    #print self.tl

  def danceOnce(self,  k=-1):
    if k == -1:
      k = self.startDance

    if self.noSols > 0:
      return self.solutions

    if self.head.right == self.head:
      self.solutions = self.outputSolution()
      return self.solutions

    c = self.chooseColumn()
    self.coverColumn(c)

    r = c.down
    while r != c:
      self.output[k] = r.row.name
      j = r.row.right
      while j != r.row:
        if j == r:
          j = j.right
          continue
        self.coverColumn(j.col)
        j = j.right
      self.danceOnce(k+1)
      if r.row.name != self.output[k] or c != r.col:
        raise Exception("WTF is going on here: " + str(r) + " " + str(self.output[k]) + " " + str(c) + " " + str(r.col))

      j = r.row.left
      while j != r.row:
        if j == r:
          j = j.left
          continue
        self.uncoverColumn(j.col)
        j = j.left
      r = r.down

    self.uncoverColumn(c)
    return self.solutions

  def dance(self, k=-1):
    #print k
    #print self
    if k == -1:
      k = self.startDance
    if self.head.right == self.head:
      return [self.outputSolution()]

    c = self.chooseColumn()
    #print c, c.name, c.size
    self.coverColumn(c)

    r = c.down
    while r != c:
      #print r, r.row.name
      self.output[k] = r.row.name
      j = r.row.right
      while j != r.row:
        if j == r:
          j = j.right
          continue
        #print j
        self.coverColumn(j.col)
        j = j.right
      map(self.solutions.add, self.dance(k+1))
      if r.row.name != self.output[k] or c != r.col:
        raise Exception("WTF is going on here: " + str(r) + " " + str(self.output[k]) + " " + str(c) + " " + str(r.col))

      j = r.row.left
      while j != r.row:
        if j == r:
          j = j.left
          continue
        self.uncoverColumn(j.col)
        j = j.left
      r = r.down

    self.uncoverColumn(c)
    return filter(lambda x: len(x) > 0, self.solutions)

  def makeMove(self,name):
    r = self.head.down
    while r != self.head:
      if name == r.name:
        break
      r = r.down

    if r == self.head:
      raise Exception("Tried to perform invalid move: " + str(name))

    self.output[self.startDance] = r.name
    self.startDance += 1
    j = r.right
    while j != r:
      self.coverColumn(j.col)
      j = j.right

  def chooseColumn(self):
    c = self.head.right
    s = float("inf")
    col = -1
    while c != self.head:
      #print c.name
      if c.size < s:
        s = c.size
        col = c
      c = c.right
    if col == -1:
      raise Exception("trying to choose column from empty table")
    return col

  def outputSolution(self):
    self.noSols += 1
    #print self.noSols
    #print tuple(sorted(self.output.values()))
    return tuple(sorted(self.output.values()))

  def toMatrix(self): # must be done from columns and transposed, otherwise coverColumn operation doesn't appear correctly since left/right row ops aren't removed
    mat = []
    ln = self.head.size[0]
    col = self.head.right
    while col != self.head:
      cell = col.down
      line = [] #[col.size]
      prevIndex = 0
      while cell != col:
        index = cell.row.name
        line += [0]*(index - prevIndex) + [1]
        prevIndex = index + 1
        cell = cell.down
      line += [0]*(ln - prevIndex)
      mat.append(line)
      col = col.right

    return zip(*mat)

  def __str__(self): 
    return '\n'.join(map(lambda line: ''.join(map(str,line)), filter(lambda line: any([c > 0 for c in line]), self.toMatrix())))

  def coverColumn(self, c):
    c.col.right.left = c.col.left
    c.col.left.right = c.col.right
    d = c.col.down
    while d != c.col:
      if d == c:
        d = d.down
        continue
      self.coverRow(d)
      d = d.down

  def coverRow(self, r):
    r.row.up.down = r.row.down
    r.row.down.up = r.row.up
    p = r.row.right
    while p != r.row:
      if p == r:
        p = p.right
        continue
      p.up.down = p.down
      p.down.up = p.up
      p.col.size -= 1
      p = p.right

  def uncoverColumn(self, c):
    u = c.col.up
    while u != c.col:
      if u == c:
        u = u.up
        continue
      self.uncoverRow(u)
      u = u.up
    c.col.right.left = c.col
    c.col.left.right = c.col

  def uncoverRow(self, r):
    l = r.row.left
    while l != r.row:
      if l == r:
        l = l.left
        continue
      l.col.size += 1
      l.up.down = l
      l.down.up = l
      l = l.left
    r.row.up.down = r.row
    r.row.down.up = r.row
      
      
if __name__ == '__main__':
  mat = []
  with open('test','r') as f:
    for line in f:
      mat.append(map(int, line.strip().split()))

  dl = DancingLinks(mat)
  print dl.dance()
