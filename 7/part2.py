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

  num_workers = 5
  workers = []
  wid = 0
  while wid < num_workers:
    workers.append(None)
    wid = wid + 1

  current_second = 0
  num_completed = 0
  num_to_complete = len(dependency_graph)

  while True:
    # First, gather the possible steps that could be allocated to free elves
    available = with_no_dependencies(dependency_graph)
    available.sort()

    # Give available workers work
    wid = 0
    while wid < num_workers:
      if workers[wid] == None and len(available) > 0:
        work_item = available[0]
        available = available[1:]
        workers[wid] = [work_item, 61 + ord(work_item) - ord('A')]

        # Remove from the dependency_graph but leave the dependencies in place
        del dependency_graph[work_item]
      wid = wid + 1

    # Check for workers that have completed work
    wid = 0
    while wid < num_workers:
      if workers[wid] != None:
        workers[wid][1] = workers[wid][1] - 1
        # Work complete
        if workers[wid][1] == 0:
          num_completed = num_completed + 1
          remove_dependency(dependency_graph, workers[wid][0])
          workers[wid] = None
      wid = wid + 1

    # Check if we have completed all the work.
    # If we have the next second is the first where the work was done.
    if num_completed == num_to_complete:
      print(current_second+1)
      return

    current_second = current_second + 1
    
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
