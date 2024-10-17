# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    load_scores.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: pibouill <pibouill@student.42prague.c      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/20 17:15:31 by pibouill          #+#    #+#              #
#    Updated: 2024/06/20 17:20:35 by pibouill         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import leaderboard

score_file = r"./scores.json"

try:
    with open(scores.json, 'r') as f:
        scores = json.load(f)
except FileNotFoundError:
    scores = {}


scores[intra_name] = new_score

with open(score_file, 'w+') as f:
    json.dump(scores, f)

def print_scores(scores):
	scores_sorted = sorted([(p, s) for p, s in scores.items()], reverse=True, key=lambda x: x[1])
	for player, score in scores_sorted:
		print(player, score)
