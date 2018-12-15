from sets import Set

# Don't look in here.
# You don't want to write code like this.

class Cart:
  def __init__(self, cart_symbol, cartid):
    if not self.valid_cart(cart_symbol):
      raise Exception("Invalid cart: " + cart_symbol)
    self.cart_symbol = cart_symbol
    self.next_turn = 'LEFT'
    self.cartid = cartid

  def valid_cart(self, c):
    return c in ['>', '<', '^', 'v']

  # Turn in cycles of LEFT > STRAIGHT > RIGHT
  def turn_cart(self):
    if self.next_turn == 'LEFT':
      self.next_turn = 'STRAIGHT'
      self.cart_symbol = self.turn_symbol_left(self.cart_symbol)
    elif self.next_turn == 'RIGHT':
      self.next_turn = 'LEFT'
      self.cart_symbol = self.turn_symbol_right(self.cart_symbol)
    elif self.next_turn == 'STRAIGHT':
      self.next_turn = 'RIGHT'
    else:
      raise Exception("12")

  def turn_symbol_left(self, c):
    if c == '^':
      return '<'
    elif c == '>':
      return '^'
    elif c == '<':
      return 'v'
    elif c == 'v':
      return '>'
    else:
      raise Exception("10")

  def turn_symbol_right(self, c):
    if c == '^':
      return '>'
    elif c == '>':
      return 'v'
    elif c == '<':
      return '^'
    elif c == 'v':
      return '<'
    else:
      raise Exception("11")


class RoadSection:
  def __init__(self, road_symbol):
    if not self.valid_road(road_symbol):
     raise Exception("Invalid road: " + r)
    self.road_symbol = road_symbol
    self.road_type = self.get_road_type()
    self.carts = []

  def get_road_type(self):
    if self.road_symbol == '|':
      return 'UD'
    elif self.road_symbol == '-':
      return 'LR'
    elif self.road_symbol == '+':
      return 'INTERSECTION'
    elif self.road_symbol == '/':
      return 'RTURN'
    elif self.road_symbol == '\\':
      return 'LTURN'
    else:
      raise Exception("13")

  def valid_road(self, r):
    return r in ['-', '|', '+', '/', '\\']

  def add_cart(self, cart):
    self.carts.append(cart)

def solve():
  lines = []
  with open('data.txt', "r") as data:
    for line in data:
      line = line[:-1] # Remove new line
      lines.append(line)

  road = parse_lines_to_road(lines)
  row_len = len(road[0])
  for row in road:
    if row_len != len(row):
      raise Exception("Mismatch row length")

  carts = cart_locations(road)

  ticks = 0
  while True:
    if len(carts) <= 1:
      # Represented as row, col
      print(carts[0][1], carts[0][0])
      break
    carts = move_carts(road, carts)
    ticks = ticks + 1

# Return the new cart locations = [(row, col)]
def move_carts(road, cart_locations):
  sorted(cart_locations, key=lambda tup: (tup[0],tup[1]) )
  have_moved = set()
  new_carts = []
  for loc in cart_locations:
    row, col = loc
    section = road[row][col]
    if len(section.carts) == 0:
      continue
    # Assume we have a single cart
    remaining_carts = section.carts[:]
    for cart in section.carts:
      if cart.cartid in have_moved:
        continue
      # We are definitely moving the cart.
      remaining_carts.remove(cart)
      rs = section.road_symbol
      cs = cart.cart_symbol

      # Handle simple cases first (intersection most complicated)
      # Do as I say not as I do.
      # Can you say "technical debt"?
      new_row = None
      new_col = None
      if rs == '|':
        if cs == '^':
          new_row, new_col = row-1, col
        elif cs == 'v':
         new_row, new_col = row+1, col
        else:
          raise Exception("1")

      elif rs == '-':
        if cs == '<':
          new_row, new_col = row, col-1
        elif cs == '>':
          new_row, new_col = row, col+1
        else:
          raise Exception("2")
 
      elif rs == '/':
        if cs == '^':
          cart.cart_symbol = '>' 
          new_row, new_col = row, col+1
        elif cs == '<':
          cart.cart_symbol = 'v' 
          new_row, new_col = row+1, col
        elif cs == '>':
          cart.cart_symbol = '^' 
          new_row, new_col = row-1, col
        elif cs == 'v':
          cart.cart_symbol = '<' 
          new_row, new_col = row, col-1
        else:
          raise Exception("3")
 
      elif rs == '\\':
        if cs == '^':
          cart.cart_symbol = '<' 
          new_row, new_col = row, col-1
        elif cs == '>':
          cart.cart_symbol = 'v' 
          new_row, new_col = row+1, col
        elif cs == '<':
          cart.cart_symbol = '^' 
          new_row, new_col = row-1, col
        elif cs == 'v':
          cart.cart_symbol = '>' 
          new_row, new_col = row, col+1
        else:
          raise Exception("4")
 
      elif rs == '+':
        cart.turn_cart()
        cs = cart.cart_symbol
        if cs == '^':
          new_row, new_col = row-1, col
        elif cs == '>':
          new_row, new_col = row, col+1
        elif cs == '<':
          new_row, new_col = row, col-1
        elif cs == 'v':
          new_row, new_col = row+1, col
        else:
          raise Exception("5")
 
      else:
        raise Exception("6")

      
      road[new_row][new_col].add_cart(cart)
      have_moved.add(cart.cartid)
      # Remove the carts the minute a crash happens
      if len(road[new_row][new_col].carts) > 1:
        road[new_row][new_col].carts = []
      else:
        new_carts.append((new_row,new_col))

    # Update the carts on this cell to what remains
    road[row][col].carts = remaining_carts

  # Remove any crashing carts
  carts = []
  for loc in new_carts:
    row, col = loc
    section = road[row][col]
    if len(section.carts) > 1:
      section.carts = []
    elif len(section.carts) == 1:
      carts.append((row, col))

  return carts

def print_road(r):
  for row in r:
    row_string = ""
    for section in row:
      if section == None:
        row_string = row_string + " "
      else:
        if len(section.carts) > 0:
          row_string = row_string + section.carts[0].cart_symbol
        else:
          row_string = row_string + section.road_symbol
    print(row_string)

def cart_locations(road):
  locations = []
  num_cols = len(road[0])
  num_rows = len(road)
  for row in range(0, num_rows):
    for col in range(0, num_cols):
      section = road[row][col]
      if section != None and len(section.carts) > 0:
        locations.append((row, col))
  return locations

# We assume a square grid road here
def has_crash(r):
  num_cols = len(r[0])
  num_rows = len(r)
  for row in range(0, num_rows):
    for col in range(0, num_cols):
      if r[row][col] != None and len(r[row][col].carts) > 1:
        return (col, row)
  return None

def parse_lines_to_road(lines):
  row_length = 0
  for line in lines:
    if len(line) > row_length:
      row_length = len(line)

  cartid = 0
  road = []
  for line in lines:
    row = []
    for char in line:
      cell_type = classify_symbol(char)
      if cell_type == 'EMPTY':
        row.append(None)
      elif cell_type == 'ROAD':
        row.append(RoadSection(char))
      elif cell_type == 'CART':
        cart = Cart(char, cartid)
        cartid = cartid + 1
        roadChar = infer_road_from_cart(char)
        r = RoadSection(roadChar)
        r.add_cart(cart)
        row.append(r)
      else:
        raise Exception("8")
    while len(row) < row_length:
      row.append(None)
    road.append(row)
  return road

def infer_road_from_cart(cart):
  if cart == '<' or cart == '>':
    return '-'
  elif cart == '^' or cart == 'v':
    return '|'
  else:
    raise Exception("9")

def classify_symbol(s):
  if s == ' ':
    return 'EMPTY'
  elif s in ['>', '<', '^', 'v']:
    return 'CART'
  elif s in ['|', '-', '+', '/', '\\']:
    return 'ROAD'
  else:
    raise Exception("What is this?" + s)

if __name__ == '__main__':
  solve()
