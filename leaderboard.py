# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    leaderboard.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: pibouill <pibouill@student.42prague.com>   +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/09/01 12:21:21 by pibouill          #+#    #+#              #
#    Updated: 2024/11/01 14:41:10 by pibouill         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from collections import UserDict
import os
import json
import app
from app import cls
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

LEADERBOARD_FILE = "leaderboard.json"
slack_token = os.getenv("SLACK_BOT_TOKEN")
client = WebClient(token=slack_token)

# Load leaderboard from JSON file
def load_leaderboard():
    # If the file doesn't exist, create an empty file
    if not os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, 'w') as f:
            json.dump({}, f)  # Write an empty JSON object to the file
        return {}  # Return an empty dictionary for the leaderboard

    with open(LEADERBOARD_FILE, 'r') as f:
        return json.load(f)

leaderboard = load_leaderboard()


# Save leaderboard to JSON file
def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(leaderboard, f)

#add users to the leaderboard
def add_user_to_leaderboard(user_id, points=1):
    if user_id in leaderboard:
        leaderboard[user_id] += points
    else:
        leaderboard[user_id] = points
    save_leaderboard(leaderboard)

def get_user_real_name(app, user_id):
    try:
        response = client.users_info(user=user_id)
        user_info = response['user']
        return user_info['real_name']
    except SlackApiError as e:
        print(f"{cls.WARNING}fetching user info: {e.response['error']}{cls.ENDC}")

user_cache = {}

def get_user_id_by_name(app, name):
    """Resolve a user by real name or mention, using a cache."""
    if name in user_cache:
        return user_cache[name]
    try:
        users_list = app.client.users_list()
        for user in users_list['members']:
            user_cache[user['real_name']] = user['id']
            user_cache[user['name']] = user['id']
            user_cache[user['id']] = user['id']

            if user.get('real_name') == name or user.get('name') == name:
             return user['id']

    except Exception as e:
        print(f"Error fetching user list: {e}")

    return None  # Return None if no matching user is found

#format the leaderboard for display
def format_leaderboard():
    if not leaderboard:
        return "The leaderboard is currently empty."

    sorted_leaderboard = sorted(leaderboard.items(), key=lambda item: item[1], reverse=True)
    formatted = []
    for user_id, points in sorted_leaderboard:
        real_name = get_user_real_name(app, user_id)
        print(real_name)
        formatted.append(f"{real_name}: {points} point(s)")
    return f"*LEADERBOARD:*\n\n" + "\n".join(formatted)

# Command to show the leaderboard
def show_leaderboard(ack, body, respond):
    ack()  # Acknowledge the command request
    respond(format_leaderboard().replace('@', ''))

def get_user_rank(user_id, app):
    user_id = get_user_id_by_name(app, user_id)
    real_name = get_user_real_name(app, user_id)
    if user_id is None:
        return f"Player not found on the leaderboard.\nCheck yo typing skillz"
    if user_id not in leaderboard:
        return f"@{real_name} is not on the leaderboard yet"
    if not leaderboard:
        return "The leaderboard is currently empty."
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda item: item[1], reverse=True)
    for rank, (uid, points) in enumerate(sorted_leaderboard, start=1):
        if uid == user_id:
            return f"@{real_name} is ranked #{rank} with {points} points"
    return f"@{user_id} is not on the leaderboard yet"

