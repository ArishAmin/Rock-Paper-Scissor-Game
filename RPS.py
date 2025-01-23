# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.
import random

def player(prev_play, opponent_history=[]):
    opponent_history.append(prev_play)
    
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    
    # Initialize global variables for strategy switching
    global strategy_scores, current_strategy, random_chance, switch_threshold
    
    if "strategy_scores" not in globals():
        strategy_scores = {"quincy": 0, "mrugesh": 0, "kris": 0, "abbey": 0}
        current_strategy = "quincy"
        switch_threshold = 5
        random_chance = 0.1  # 10% chance to play randomly to avoid predictability

    # Switch strategies if current one underperforms
    if strategy_scores[current_strategy] < -switch_threshold:
        current_strategy = max(strategy_scores, key=strategy_scores.get)
    
    # Implement strategy behavior
    if current_strategy == "quincy":
        # Fixed pattern counter for Quincy
        if len(opponent_history) >= 5 and opponent_history[-5:] == ['R', 'R', 'P', 'P', 'S']:
            next_move = "P"
        else:
            next_move = ideal_response.get(opponent_history[-1], "R")
        strategy_scores["quincy"] += 1 if next_move == ideal_response.get(prev_play, "R") else -1
    
    elif current_strategy == "mrugesh":
        # Counter most common move in the last 10 rounds for Mrugesh
        if len(opponent_history) >= 10:
            last_ten = opponent_history[-10:]
            most_common = max(set(last_ten), key=last_ten.count)
            next_move = ideal_response[most_common]
        else:
            next_move = ideal_response.get(opponent_history[-1], "R")
        strategy_scores["mrugesh"] += 1 if next_move == ideal_response.get(prev_play, "R") else -1

    elif current_strategy == "kris":
        # For Kris: Predict the counter to Kris’s previous mirror
        if len(opponent_history) >= 2:
            last_move = opponent_history[-2]
            next_move = ideal_response.get(last_move, "R")
        else:
            next_move = "P"  # Start with a neutral choice
        strategy_scores["kris"] += 1 if next_move == ideal_response.get(prev_play, "R") else -1

    elif current_strategy == "abbey":
        # Abbey's counter by tracking sequence probabilities
        if len(opponent_history) >= 3:
            recent = ''.join(opponent_history[-3:])
            sequence_counts = {'RRP': 'S', 'PPS': 'R', 'SSR': 'P', 'RPS': 'P'}
            next_move = sequence_counts.get(recent, "R")
        else:
            next_move = "R"
        strategy_scores["abbey"] += 1 if next_move == ideal_response.get(prev_play, "R") else -1

    # Add randomness to disrupt pattern detection by bots
    if random.random() < random_chance:
        next_move = random.choice(['R', 'P', 'S'])
    
    return next_move

