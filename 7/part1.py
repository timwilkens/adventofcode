from sets import Set

def solve():

  # Map each node to the set of dependencies which must complete before
  # the node can execute. When the set of dependencies is empty the node
  # is free to go (subject to the alphabetic constraints)
  dependency_graph = {}
  with open('data.txt', "r") as data:
    for line in data:
      # indep is free to complete independent of what happens with dep.
      # dep must wait for indep to complete.
      indep, dep = parse_line(line)
      if indep not in dependency_graph:
        dependency_graph[indep] = Set()
      if dep not in dependency_graph:
        dependency_graph[dep] = Set()

      dependency_graph[dep].add(indep)

  topo_order = []

  while len(dependency_graph) > 0:
    available = with_no_dependencies(dependency_graph)
    available.sort()
    to_process = available[0]
    topo_order.append(to_process)

    del dependency_graph[to_process]
    remove_dependency(dependency_graph, to_process)

  print("".join(topo_order))
    
def remove_dependency(graph, node):
  for v in graph.keys():
    if node in graph[v]:
      graph[v].remove(node)

def with_no_dependencies(g):
  no_dependents = []
  for node in g:
    if len(g[node]) == 0:
      no_dependents.append(node)

  return no_dependents

def parse_line(line):
  return line[5], line[36] 


if __name__ == '__main__':
  solve()
