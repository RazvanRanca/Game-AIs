cid = 0
eow = '-'

class Node:
  def __init__(self, chd = {}, wd = False):
    global cid
    self.children = chd
    self.word = wd
    self.id = cid
    cid += 1

  def isWord(self):
    return self.word

  def hasEdge(self,e):
    return e in self.children

  def getChild(self,c):
    return self.children[c]

  def __str__(self):
    return str(self.id)

class Trie:
  def __init__(self, words = []):
    self.head = Node({})
    for word in words:
      self.add(word)

  def add(self, word):
    curNode = self.head
    commonPrefix = True
    for c in word:
      if commonPrefix and c in curNode.children:
        curNode = curNode.children[c]
      else:
        commonPrefix = False
        n = Node({})
        curNode.children[c] = n
        curNode = n
    curNode.word = True

  def find(self, string):
    curNode = self.head
    for c in string:
      if c in curNode.children:
        curNode = curNode.children[c]
      else:
        return None
      #print string, c, curNode
    return curNode

  def __str__(self):
    ret = ""
    nodes = [self.head]
    while len(nodes) > 0:
      node = nodes.pop(0)
      for k,v in node.children.iteritems():
        ret += str(node) + " " + str(k) + " " + str(v) + " " + str(v.word) +"\n"
        nodes.append(v)
    return ret

if __name__ == '__main__':
  with open('dictionary', 'r') as f:
    words = f.read().split()
    dc = Trie(words)
    print dc
