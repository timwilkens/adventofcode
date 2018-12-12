import sys

def solve():
  assert(calculuate_power_level(3, 5, 8) == 4)

  grid_serial_number = 8561
  total_power_cache = {}

  # Build the grid with power levels for each cell
  # Base case: square of size 1
  grid = {}
  for x in range (1, 301):
    total_power_cache[x] = {}
    grid[x] = {}
    for y in range(1, 301):
      total_power_cache[x][y] = {}
      grid[x][y] = calculuate_power_level(x, y, grid_serial_number)
      total_power_cache[x][y][1] = calculuate_power_level(x, y, grid_serial_number)

  # Base case: square of side length 2
  for x in range (1, 300):
    for y in range(1, 300):
      power = grid[x][y] + grid[x+1][y] + grid[x][y+1] + grid[x+1][y+1]
      total_power_cache[x][y][2] = power 

  max_total_power = -90000 * 5
  max_coords = ""

  for square_size in range(3, 301):
    for x in range(1, 300 - square_size + 2):
      for y in range(1, 300 - square_size + 2):

        # Recursive case:
        # This square is the sum of overlapping squares of size n - 1 minus a square of n - 2
        # plus the two non-included corners

 
        # Example:
        # A square of side length 3 can be found by adding the square of size 2 with the same upper left corner
        # with the square of side length 2 and upper left corner shifted diagonally right and down by 1 each.
        # This captures everything but the lower left and upper right corners so we also add them in explicitly.
        # But, the two squares of size n-1 overlap in the center so we subtract the overlap
        # square of size n-2 to prevent double counting.

        total_power = total_power_cache[x][y][square_size-1] \
                    + total_power_cache[x+1][y+1][square_size-1] \
                    - total_power_cache[x+1][y+1][square_size-2] \
                    + total_power_cache[x][y+square_size-1][1] \
                    + total_power_cache[x+square_size-1][y][1]

        total_power_cache[x][y][square_size] = total_power

        if total_power > max_total_power:
          max_total_power = total_power
          max_coords = ",".join([str(x), str(y), str(square_size)])

  print(max_coords)

def calculuate_power_level(x, y, grid_serial):
  rack_id = x + 10
  power_level = rack_id * y
  power_level = power_level + grid_serial
  power_level = power_level * rack_id
  if power_level < 100:
    power_level = 0
  else:
    power_level = int(str(power_level)[-3])

  return power_level - 5


if __name__ == '__main__':
  solve()
