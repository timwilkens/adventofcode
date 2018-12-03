from sets import Set

def solve(data_file):
  count_triples = 0
  count_doubles = 0
  with open(data_file, "r") as data:
    for line in data:
      if contains_double(line):
        count_doubles = count_doubles + 1
      if contains_triple(line):
        count_triples = count_triples + 1

  return count_doubles * count_triples

def contains_double(boxid):
  return contains_exactly_n_times(boxid, 2)

def contains_triple(boxid):
  return contains_exactly_n_times(boxid, 3)

def contains_exactly_n_times(word, n):
  counts = {}
  for letter in word:
    if letter in counts:
      counts[letter] = counts[letter] + 1
    else:
      counts[letter] = 1

  for letter, count in counts.iteritems():
    if count == n:
      return True

  return False

if __name__ == '__main__':
  data_file = 'data.txt'
  result = solve(data_file)
  print result
