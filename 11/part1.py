def solve():
  assert(calculuate_power_level(3, 5, 8) == 4)

  grid_serial_number = 8561

  # Build the grid with power levels for each cell
  grid = {}
  x = 1
  while x <= 300:
    y = 1
    while y <= 300:
      grid[str(x) + "," + str(y)] = calculuate_power_level(x, y, grid_serial_number)
      y = y + 1
    x = x + 1

  max_total_power = 0
  max_coords = ""

  x = 1
  while x <= 298:
    y = 1
    while y <= 298:
      total_power = 0
      x_off = 0
      while x_off < 3:
        y_off = 0
        while y_off < 3:
          total_power = total_power + grid[str(x+x_off) + "," + str(y+y_off)]
          y_off = y_off + 1
        x_off = x_off + 1
      if total_power > max_total_power:
        max_total_power = total_power
        max_coords = str(x) + "," + str(y)
      y = y + 1
    x = x + 1

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
