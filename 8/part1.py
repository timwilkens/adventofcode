class Node:
  def __init__(self, children, metadata):
    self.children = children
    self.metadata = metadata

def solve():
  raw_tree = []
  with open('data.txt', "r") as data:
    for line in data:
      raw_tree = [int(x) for x in line.split(' ')]

  tree, index = parse_tree(raw_tree, 0)
  assert(index == len(raw_tree))

  print(sum_metadata(tree))

def parse_tree(raw_tree, idx):
  num_children = raw_tree[idx]
  idx = idx+1
  metadata_count = raw_tree[idx]
  idx = idx + 1

  children = []
  i = 0
  while i < num_children:
    kid, idx = parse_tree(raw_tree, idx)
    children.append(kid)
    i = i + 1

  metadata = []
  i = 0
  while i < metadata_count:
    metadata.append(raw_tree[idx+i])
    i = i + 1

  idx = idx + i
  return Node(children, metadata), idx

def sum_metadata(tree):
  total = 0
  for m in tree.metadata:
    total = total + m

  for child in tree.children:
    total = total + sum_metadata(child)

  return total

if __name__ == '__main__':
  solve()
