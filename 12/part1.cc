#include<iostream>
#include<fstream>
#include<vector>
#include<unordered_map>

struct plant_state {
  std::unordered_map<int, char> pots;
  int min_set;
  int max_set;
};

plant_state parse_initial_state(std::string state_string) {
  plant_state state;
  std::unordered_map<int, char> pots;
  int i = 0;
  while (state_string[i] != ':') {
    i++;
  }
  i += 2;
  int state_index = 0;
  while (i < state_string.size()) {
    pots.insert(std::make_pair<int, char>(state_index++, state_string[i]));
    i++;
  } 

  // Pad with rule_length empty pots on each side. This ensures that we can safetly
  // start looking in 3 pots from each side and they will be set.
  int min_set = 0;
  int max_set = state_index-1;
  int rule_length = 5;

  for (int i = min_set-1; i >= min_set - rule_length; i--) {
    pots.insert(std::make_pair<int, char>(i, '.'));
  }
  for (int i = max_set+1; i <= max_set + rule_length; i++) {
    pots.insert(std::make_pair<int, char>(i, '.'));
  }

  state.pots = pots;
  state.min_set = min_set - rule_length;
  state.max_set = max_set + rule_length; 
  return state;
}

void parse_and_add_rule(std::unordered_map<std::string, char> &rules, std::string rule_string) {
  std::string key = rule_string.substr(0, 5);
  char value = rule_string[9];
  rules.insert(std::make_pair<std::string, char>(key, value)); 
}

void output_state(plant_state &state) {
  for (int i = state.min_set; i <= state.max_set; i++) {
    std::cout << state.pots[i];
  }
  std::cout << std::endl;
}

void next_generation(plant_state &state, std::unordered_map<std::string, char> rules) {
  std::unordered_map<int, char> next_gen_pots;

  // Init to opposite ends
  int min_set = state.max_set;
  int max_set = state.min_set;

  for (int cur = state.min_set + 2; cur <= state.max_set - 2 ; cur++) {
    std::string pattern;
    for (int offset = -2; offset <= 2; offset++) {
      pattern += state.pots[cur+offset];
    }

    char new_value = rules[pattern];
    next_gen_pots.insert(std::make_pair<int, char>(cur, new_value));
    // Track the minimum and maximum set
    if (new_value == '#') {
      min_set = std::min(min_set, cur);
      max_set = std::max(max_set, cur);
    }
  }

  // Ensure invariant
  for (int i = min_set-1; i >= min_set - 5; i--) {
    next_gen_pots.insert(std::make_pair<int, char>(i, '.'));
  }
  for (int i = max_set+1; i <= max_set + 5; i++) {
    next_gen_pots.insert(std::make_pair<int, char>(i, '.'));
  }

  // Set pots
  state.pots = next_gen_pots;
  state.min_set = min_set - 5;
  state.max_set = max_set + 5;
}

int main() {
  std::ifstream file("data.txt");
  if (!file.is_open()) {
    std::cout << "Could not open data file\n";
    return 1;
  }

  plant_state state;
  std::unordered_map<std::string, char> rules;
  std::string line;
  int line_number = 0;
  while (getline(file, line)) {
    if (line_number == 0) {
      // Initial state
      state = parse_initial_state(line);
    } else if (line_number > 1) {
      // Rules
      parse_and_add_rule(rules, line);
    }
    line_number++;
  }

  int generation = 0;
  std::cout << generation << " ";
  output_state(state);
  while (generation < 20) {
    next_generation(state, rules);
    generation++;
    std::cout << generation << " ";
    output_state(state);
  }

  int sum = 0;
  for (int i = state.min_set; i <= state.max_set; i++) {
    if (state.pots[i] == '#') {
      sum += i;
    }
  }
  std::cout << sum << "\n";

  file.close();
}
