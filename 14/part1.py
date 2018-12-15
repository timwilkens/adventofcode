def solve():
  # Recipe nuimber 990941 is located at index 990940
  # So the next recipe after is 990941
  first_recipe_to_consider = 990941
  num_recipes_to_count = 10

  elf_to_recipe = [0, 1]
  recipes = [3, 7]

  while len(recipes) < first_recipe_to_consider + num_recipes_to_count:
    total = recipe_sum(elf_to_recipe, recipes)
    new_recipes = [int(c) for c in str(total)]
    for r in new_recipes:
      recipes.append(r)

    for i in range(0, len(elf_to_recipe)):
      r_index = elf_to_recipe[i]
      steps = 1 + recipes[r_index]
      new_index = ((r_index + steps) % len(recipes))
      elf_to_recipe[i] = new_index

    #print(show(recipes, elf_to_recipe))

  answer = "".join([str(x) for x in recipes[first_recipe_to_consider:first_recipe_to_consider+num_recipes_to_count]])
  print(answer)

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
