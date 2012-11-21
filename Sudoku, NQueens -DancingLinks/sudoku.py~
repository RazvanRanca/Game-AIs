import dancingLinks as dl

def getMatrix(r=9,c=9,n=9,x=3,y=3):
  m1 = rowColConstrain(r,c,n)
  m2 = rowNumConstrain(r,c,n)
  m3 = colNumConstrain(r,c,n)
  m4 = boxNumConstrain(r,c,n,x,y)
  l = len(m1)

  return [m1[i] + m2[i] + m3[i] + m4[i] for i in range(l)]
  
def rowColConstrain(r=9,c=9,n=9):
  mat = []
  l = r*c
  for rc in range(r):
    for cc in range(c):
      for nc in range(n):
        b = rc*r + cc
        mat.append([0]*b + [1] + [0]*(l-b-1))
  return mat

def rowNumConstrain(r=9,c=9,n=9):
  mat = []
  l = r*c
  for rc in range(r):
    for cc in range(c):
      for nc in range(n):
        b = rc*r + nc
        mat.append([0]*b + [1] + [0]*(l-b-1))
  return mat

def colNumConstrain(r=9,c=9,n=9):
  mat = []
  l = r*c
  for rc in range(r):
    for cc in range(c):
      for nc in range(n):
        b = cc*r + nc
        mat.append([0]*b + [1] + [0]*(l-b-1))
  return mat

def boxNumConstrain(r=9,c=9,n=9,x=3,y=3):
  mat = []
  l = r*c
  for rc in range(r):
    for cc in range(c):
      for nc in range(n):
        b = (rc/y)*r*x + (cc/x)*c + nc
        mat.append([0]*b + [1] + [0]*(l-b-1))
  return mat

def getAllSolutions(mat): # 9x9x9 is too big for this
  dlx = dl.DancingLinks(mat)
  sols = dlx.dance()
  print sols

def getSolution(mat, moves):
  dlx = dl.DancingLinks(mat)
  map(lambda m: dlx.makeMove(m), moves)
  sol = dlx.danceOnce()
  return sol

def readMoves(fileName):
  moveMat = []
  moves = []
  with open(fileName,'r') as f:
    (r,c,n) = map(int,f.readline().strip().split())
    for line in f:
      moveMat.append(map(int, line.strip().split()))

    for i in range(len(moveMat)):
      for j in range(len(moveMat[0])):
        if moveMat[i][j] > 0:
          moves.append(i*c*n + j*n + moveMat[i][j] - 1)

  return moves

def prettyPrint(sol, r=9,c=9,n=9,x=3,y=3):
  mat = []
  ln = c + c/x - 1
  for rc in range(r):
    if rc % y == 0:
      mat.append('| ' + '- '*ln + '|')
    line = []
    for cc in range(c):
      if cc % x == 0:
        line.append('|')        
      cell = ' '
      for nc in range(n):
        rez = rc*c*n + cc*n + nc
        if rez in sol:
          cell = str(nc+1)
      line.append(cell)
    line.append('|')
    mat.append(' '.join(line))
  mat.append('| ' + '- '*ln + '|')
  print '\n'.join(mat)

def prettyPrintMat(mat):
  print '\n'.join(map(lambda x:''.join(map(str,x)), mat))

if __name__ == '__main__':

  #print '\n'.join(map(lambda x:''.join(map(str,x)), getMatrix(4,4,4,2,2)))
  s = 5
  prettyPrint(getSolution(getMatrix(s*s,s*s,s*s,s,s),[]),s*s,s*s,s*s,s,s)
  #prettyPrint(getSolution(getMatrix(),readMoves('sudokuTest')))
