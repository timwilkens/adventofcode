def solve():
  desired_sequence = [9, 9, 0, 9, 4, 1]

  elf_to_recipe = [0, 1]
  recipes = [3, 7]

  while True:
    total = recipe_sum(elf_to_recipe, recipes)
    new_recipes = [int(c) for c in str(total)]
    for r in new_recipes:
      recipes.append(r)
      if len(recipes) < len(desired_sequence):
        continue
      if sequence_equals(desired_sequence, recipes[-len(desired_sequence):]):
        print(len(recipes)-len(desired_sequence))
        return

    for i in range(0, len(elf_to_recipe)):
      r_index = elf_to_recipe[i]
      steps = 1 + recipes[r_index]
      new_index = ((r_index + steps) % len(recipes))
      elf_to_recipe[i] = new_index


def sequence_equals(s1, s2):
  if len(s1) != len(s2):
    return False
  for i in range(0, len(s1)):
    if s1[i] != s2[i]:
      return False
  return True

def show(recipes, elf_to_recipe):
  outputs = []
  for i in range(0, len(recipes)):
    if i == elf_to_recipe[0]:
      outputs.append("("+str(recipes[i])+")")
    elif i == elf_to_recipe[1]:
      outputs.append("["+str(recipes[i])+"]")
    else:
      outputs.append(" "+str(recipes[i])+" ")

  return " ".join(outputs)

def recipe_sum(elf_to_recipe, recipes):
  sum = 0
  for recipe_idx in elf_to_recipe:
    sum = sum + recipes[recipe_idx]
  return sum


if __name__ == '__main__':
  solve()
