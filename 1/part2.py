from sets import Set

def solve(data_file):
  changes = []
  with open(data_file, "r") as data:
    for line in data:
      changes.append(to_number(line))

  seen_frequencies = Set([0])
  current_frequency = 0
  change_index = 0

  while True:
    next_change = changes[change_index]
    current_frequency = current_frequency + next_change
    if current_frequency in seen_frequencies:
      return current_frequency
    seen_frequencies.add(current_frequency)
    change_index = (change_index + 1) % len(changes)

def to_number(number_string):
  integer_part = number_string[1:]
  integer = int(integer_part)
  return integer if number_string[0] == '+' else -1 * integer

if __name__ == '__main__':
  data_file = 'data.txt'
  result = solve(data_file)
  print result
