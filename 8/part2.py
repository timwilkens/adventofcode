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

  print(node_value(tree))

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

def node_value(node):
  if len(node.children) == 0:
    return sum(node.metadata)

  value = 0
  child_count = len(node.children)
  for meta in node.metadata:
    if meta == 0 or meta > child_count:
      continue

    value = value + node_value(node.children[meta-1])

  return value

if __name__ == '__main__':
  solve()
