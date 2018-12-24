#include<iostream>
#include<fstream>
#include<vector>
#include<unordered_map>

struct plant_state {
  std::unordered_map<int64_t, char> pots;
  int64_t min_set;
  int64_t max_set;
};

plant_state parse_initial_state(std::string state_string) {
  plant_state state;
  std::unordered_map<int64_t, char> pots;
  int64_t i = 0;
  while (state_string[i] != ':') {
    i++;
  }
  i += 2;
  int64_t state_index = 0;
  while (i < state_string.size()) {
    pots.insert(std::make_pair<int64_t, char>(state_index++, state_string[i]));
    i++;
  } 

  // Pad with rule_length empty pots on each side. This ensures that we can safetly
  // start looking in 3 pots from each side and they will be set.
  int64_t min_set = 0;
  int64_t max_set = state_index-1;
  int rule_length = 5;

  for (int64_t i = min_set-1; i >= min_set - rule_length; i--) {
    pots.insert(std::make_pair<int64_t, char>(i, '.'));
  }
  for (int64_t i = max_set+1; i <= max_set + rule_length; i++) {
    pots.insert(std::make_pair<int64_t, char>(i, '.'));
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

std::string to_string(plant_state &state) {
  std::string s;
  for (int64_t i = state.min_set; i <= state.max_set; i++) {
    s += state.pots[i];
  }
  return s;
}

plant_state next_generation(plant_state &state, std::unordered_map<std::string, char> rules) {
  std::unordered_map<int64_t, char> next_gen_pots;

  // Init to opposite ends
  int64_t min_set = state.max_set;
  int64_t max_set = state.min_set;

  for (int64_t cur = state.min_set + 2; cur <= state.max_set - 2 ; cur++) {
    std::string pattern;
    for (int64_t offset = -2; offset <= 2; offset++) {
      pattern += state.pots[cur+offset];
    }

    char new_value = rules[pattern];
    next_gen_pots.insert(std::make_pair<int64_t, char>(cur, new_value));
    // Track the minimum and maximum set
    if (new_value == '#') {
      min_set = std::min(min_set, cur);
      max_set = std::max(max_set, cur);
    }
  }

  // Ensure invariant
  for (int64_t i = min_set-1; i >= min_set - 5; i--) {
    next_gen_pots.insert(std::make_pair<int64_t, char>(i, '.'));
  }
  for (int64_t i = max_set+1; i <= max_set + 5; i++) {
    next_gen_pots.insert(std::make_pair<int64_t, char>(i, '.'));
  }

  // Set pots
  plant_state new_state;
  new_state.pots = next_gen_pots;
  new_state.min_set = min_set - 5;
  new_state.max_set = max_set + 5;
  return new_state;
}

void compute_sum_with_offset(plant_state state, uint64_t offset) {
  uint64_t sum = 0;
  for (int i = state.min_set; i <= state.max_set; i++) {
    if (state.pots[i] == '#') {
      sum += ((uint64_t)i + offset);
    }
  }
  std::cout << sum << "\n";

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

  uint64_t generation = 0;
  uint64_t generations_to_run = 50000000000; 

  // The generation function has a fixed point.
  // Find it and exploit it.
  std::string prev_state_string = "";
  while (generation < generations_to_run) {
    state = next_generation(state, rules);
    generation++;
    std::string s = to_string(state);
    if (s == prev_state_string) {
        // Fixed point found. Determine how much the pots shift left or right
        // to compute the final sum.
        plant_state next = next_generation(state, rules); 
        uint64_t offset_per_gen = next.min_set - state.min_set;
        uint64_t gens_not_run = generations_to_run - generation;
        uint64_t offset = offset_per_gen * gens_not_run;
        compute_sum_with_offset(state, offset);
        break;
    }
    prev_state_string = s;
  }
  file.close();
}
