from sets import Set

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

  ticks = 0
  while True:
    #print_road(road)
    if has_crash(road) != None:
      print(has_crash(road))
      break
    move_carts(road)
    ticks = ticks + 1

def move_carts(road):
  have_moved = set()
  num_cols = len(road[0])
  num_rows = len(road)
  for col in range(0, num_cols):
    for row in range(0, num_rows):
      #print(col, row)
      if road[row][col] == None:
        continue
      section = road[row][col]
      if len(section.carts) == 0:
        continue
      # Assume we have a single cart
      cart = section.carts[0]
      if cart.cartid in have_moved:
        continue
      rs = section.road_symbol
      cs = cart.cart_symbol

      # Handle simple cases first (intersection most complicated)
      if rs == '|':
        if cs == '^':
          road[row-1][col].add_cart(cart)
          road[row][col].carts = []
        elif cs == 'v':
          road[row+1][col].add_cart(cart)
          road[row][col].carts = []
        else:
          raise Exception("1")

      elif rs == '-':
        if cs == '<':
          road[row][col-1].add_cart(cart)
          road[row][col].carts = []
        elif cs == '>':
          road[row][col+1].add_cart(cart)
          road[row][col].carts = []
        else:
          raise Exception("2")

      elif rs == '/':
        if cs == '^':
          cart.cart_symbol = '>' 
          road[row][col+1].add_cart(cart)
          road[row][col].carts = []
        elif cs == '<':
          cart.cart_symbol = 'v' 
          road[row+1][col].add_cart(cart)
          road[row][col].carts = []
        elif cs == '>':
          cart.cart_symbol = '^' 
          road[row-1][col].add_cart(cart)
          road[row][col].carts = []
        elif cs == 'v':
          cart.cart_symbol = '<' 
          road[row][col-1].add_cart(cart)
          road[row][col].carts = []
        else:
          raise Exception("3")

      elif rs == '\\':
        if cs == '^':
          cart.cart_symbol = '<' 
          road[row][col-1].add_cart(cart)
          road[row][col].carts = []
        elif cs == '>':
          cart.cart_symbol = 'v' 
          road[row+1][col].add_cart(cart)
          road[row][col].carts = []
        elif cs == '<':
          cart.cart_symbol = '^' 
          road[row-1][col].add_cart(cart)
          road[row][col].carts = []
        elif cs == 'v':
          cart.cart_symbol = '>' 
          road[row][col+1].add_cart(cart)
          road[row][col].carts = []
        else:
          raise Exception("4")

      elif rs == '+':
        cart.turn_cart()
        cs = cart.cart_symbol
        if cs == '^':
          road[row-1][col].add_cart(cart)
          road[row][col].carts = []
        elif cs == '>':
          road[row][col+1].add_cart(cart)
          road[row][col].carts = []
        elif cs == '<':
          road[row][col-1].add_cart(cart)
          road[row][col].carts = []
        elif cs == 'v':
          road[row+1][col].add_cart(cart)
          road[row][col].carts = []
        else:
          raise Exception("5")

      else:
        raise Exception("6")


      have_moved.add(cart.cartid)

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
