def solve():

  # Parse the input data
  rectangle_details = []
  with open("data.txt", "r") as data:
    for line in data:
      rectangle_details.append(parse_input_line(line))
  validate_rectangle_details(rectangle_details)

  # Convert each rectangle to the set of squares it covers and count them
  squares_covered_by_rect = [to_covered_squares(rd) for rd in rectangle_details]
  covered = {}
  for rectangle_squares in squares_covered_by_rect:
    for square in rectangle_squares:
      str_desc = square_to_string(square)
      if str_desc in covered:
        covered[str_desc] = covered[str_desc] + 1
      else:
        covered[str_desc] = 1

  # Get the count of squares covered more than once
  count_covered_two_or_more = 0
  for square, count in covered.iteritems():
    if count > 1:
      count_covered_two_or_more = count_covered_two_or_more + 1

  return count_covered_two_or_more

def parse_input_line(line):
  line = line.strip()
  space_divided = line.split(' ')
  # Elements are
  # 0 - boxid (#123)
  # 1 - at symbol
  # 2 - comma seperated distances (919,119:)
  # 3 - x seperate dimensions (123x34)

  # Remove the trailing colon
  distance_parts = space_divided[2][:-1].split(',')
  dimension_parts = space_divided[3].split('x')

  return {
    'left_edge_distance' : int(distance_parts[0]),
    'top_edge_distance' : int(distance_parts[1]),
    'width': int(dimension_parts[0]),
    'height': int(dimension_parts[1])
  }

# Squares returned are represeted by their upper left corner.
# The square in the very upper left of the entire grid is represented
# by (0, 0)

def to_covered_squares(rectangle_details):

  # If the rect is n inches from the left side then the
  # smallest coordinate it can have is n.
  # Similarly for the distance from the top.

  squares = []
  x = rectangle_details['left_edge_distance']
  y = rectangle_details['top_edge_distance']
  x_offset = 0
  while x_offset < rectangle_details['width']:
    y_offset = 0
    while y_offset < rectangle_details['height']:
      squares.append((x+x_offset, y+y_offset))
      y_offset = y_offset+1
    x_offset = x_offset+1

  return squares

def square_to_string(square):
  return str(square[0]) + "-" + str(square[1])

def validate_rectangle_details(rectangle_details):
  assert rectangle_details[0]['left_edge_distance'] == 16
  assert rectangle_details[0]['top_edge_distance'] == 576
  assert rectangle_details[0]['width'] == 17
  assert rectangle_details[0]['height'] == 14

  assert rectangle_details[1280]['left_edge_distance'] == 915
  assert rectangle_details[1280]['top_edge_distance'] == 814
  assert rectangle_details[1280]['width'] == 11
  assert rectangle_details[1280]['height'] == 22

if __name__ == '__main__':
  result = solve()
  print result
