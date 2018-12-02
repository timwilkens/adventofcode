def solve(data_file):
  result = 0
  with open(data_file, "r") as data:
    for line in data:
      result = result + to_number(line)

  return result

def to_number(number_string):
  integer_part = number_string[1:]
  integer = int(integer_part)
  return integer if number_string[0] == '+' else -1 * integer

if __name__ == '__main__':
  data_file = 'data.txt'
  result = solve(data_file)
  print result
