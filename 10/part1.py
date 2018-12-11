from sets import Set

def solve():
  vectors = []
  with open('data.txt', "r") as data:
    for line in data:
      vectors.append(parse_pos_and_vel(line))

  assert_input(vectors)

  round = 0

  while True:
    round = round + 1
    vectors = perform_round(vectors) 
    x_diff = x_spread(vectors)
    y_diff = y_spread(vectors)
    # Guess it happens at 10942 by looking at output
    # Could programmatically determine by looking at
    # the plot of light area over time and taking the min.
    # But really, why bother?
    if round == 10942:
      print(x_diff, y_diff)
      show(vectors)
      return

def show(vectors):
    x_diff = x_spread(vectors)
    x_min = min_x(vectors)
    x_max = max_x(vectors)
    y_diff = y_spread(vectors)
    y_min = min_y(vectors)
    y_max = max_y(vectors)

    lit_up = Set()
    for v in vectors:
      lit_up.add(to_vector_key(v))

    # Some hardcoded iteration order here.
    # Really it depends on what quadrant we ended up in.
    y = y_min - 1
    while y <= y_max + 1:
      row_s = ""
      x = x_min - 1
      while x <= x_max + 1:
        vec_s = to_vector_key([x, y])
        if vec_s in lit_up:
          row_s = row_s + "#"
        else:
          row_s = row_s + "."
        x = x + 1
      print(row_s)
      y = y + 1

def to_vector_key(vector):
  return str(vector[0]) + "-" + str(vector[1])

def parse_pos_and_vel(line):
  line = line.strip()
  line = line[9:] # Remove "position="
  vector_s = line[:17]
  vector_s = vector_s.strip() # Looks like < 11149,  32974>
  vector = parse_to_list(vector_s)
  line = line[17:] # Looks like velocity=< 3, -5>
  line = line[9:] # Remove "velocity="
  velocity_vector = parse_to_list(line)
  vector = vector + velocity_vector
  return vector

def parse_to_list(s):
  s = s[1:-1]
  return [int(x.strip()) for x in s.split(",")]

def perform_round(vectors):
  updated = []
  for v in vectors:
    updated.append([v[0] + v[2], v[1] + v[3], v[2], v[3]])
  return updated

def x_spread(vectors):
  return max_x(vectors) - min_x(vectors)

def min_x(vectors):
  return min([v[0] for v in vectors])

def max_x(vectors):
  return max([v[0] for v in vectors])

def y_spread(vectors):
  return max_y(vectors) - min_y(vectors)

def min_y(vectors):
  return min([v[1] for v in vectors])

def max_y(vectors):
  return max([v[1] for v in vectors])

# Confirm a few properties of our input to make sure we haven't
# messed something up when parsing
def assert_input(vectors):
  assert(len(vectors) == 350)
  for vec in vectors:
    assert(len(vec) == 4)
  assert(vectors[0][0] == 11153)
  assert(vectors[0][1] == 22033)
  assert(vectors[0][2] == -1)
  assert(vectors[0][3] == -2)
  assert(vectors[312][0] == 11133)
  assert(vectors[312][1] == -54563)
  assert(vectors[312][2] == -1)
  assert(vectors[312][3] == 5)

if __name__ == '__main__':
  result = solve()
  print result
