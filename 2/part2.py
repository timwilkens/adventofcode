from sets import Set

def solve(data_file):
  boxids = []
  with open(data_file, "r") as data:
    for line in data:
      boxids.append(line)

  # Simple quadratic solution
  for boxid1 in boxids:
    for boxid2 in boxids:
      if boxid1 == boxid2:
        continue # Not technically necessary

      if differ_by_one(boxid1, boxid2):
        return extract_shared_parts(boxid1, boxid2)

def differ_by_one(s1, s2):
  i = 0
  num_diff = 0
  while i < len(s1):
    if s1[i] != s2[i]:
      num_diff = num_diff + 1
      if num_diff > 1:
        return False # Not necessary
    i = i + 1
  return num_diff == 1

def extract_shared_parts(s1, s2):
  shared = ''
  i = 0
  while i < len(s1):
    if s1[i] == s2[i]:
      shared = shared + s1[i]
    i = i + 1
  return shared

if __name__ == '__main__':
  data_file = 'data.txt'
  result = solve(data_file)
  print result
