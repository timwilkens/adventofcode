import sys

def solve():
  assert(calculuate_power_level(3, 5, 8) == 4)

  grid_serial_number = 8561
  total_power_cache = {}

  # Build the grid with power levels for each cell
  grid = {}
  x = 1
  while x <= 300:
    y = 1
    while y <= 300:
      grid[str(x) + "," + str(y)] = calculuate_power_level(x, y, grid_serial_number)
      total_power_cache[str(x) + "," + str(y) + ",1"] = calculuate_power_level(x, y, grid_serial_number)
      y = y + 1
    x = x + 1

  max_total_power = -90000 * 5
  max_coords = ""

  square_size = 2


  while square_size <= 300:
    x = 1
    while x <= (300 - square_size + 1):
      y = 1
      while y <= (300 - square_size + 1):
        total_power = total_power_cache[str(x) + "," + str(y) + "," + str(square_size-1)]

        x_off = 0
        while x_off < square_size:
          total_power = total_power + grid[str(x + x_off) + "," + str(y + square_size - 1)]
          x_off = x_off + 1

        y_off = 0
        while y_off < square_size:
          total_power = total_power + grid[str(x + square_size - 1) + "," + str(y + y_off)]
          y_off = y_off + 1

        loc_key = str(x) + "," + str(y) + "," + str(square_size)
        total_power_cache[loc_key] = total_power

        if total_power > max_total_power:
          max_total_power = total_power
          max_coords = loc_key
          print(max_coords, max_total_power)
        y = y + 1
      x = x + 1
    square_size = square_size + 1

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
