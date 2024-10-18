##########################
##########################
##########################
##########################
##########################
##########################

from collections import UserDict
import os
import json
import app
from app import app
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

def get_user_rank(user_id):
    if user_id not in leaderboard:
        return f"@{user_id} is not on the leaderboard yet"
    if not leaderboard:
        return "The leaderboard is currently empty."
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda item: item[1], reverse=True)

    for rank, (uid, points) in enumerate(sorted_leaderboard, start=1):
        if uid == user_id:
            return f"@{user_id} is ranked #{rank} with {points} points"
    return f"@{user_id} is not on the leaderboard yet"


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
        user_info = app.client.users_info(user=user_id)
        return user_info['user']['real_name']
    except Exception as e:
        print(f"{app.bcolors.WARNING}Error fetching user info: {e}")
        return f"<@{user_id}>"

    # try:
    #     response = client.users_info(user=user_id)
    #     user_info = response['user']
    #     return user_info['real_name']
    # except SlackApiError as e:
    #     print(f"{app.bcolors.WARNING}fetching user info: {e.response['error']}{app.bcolors.ENDC}")


#format the leaderboard for display
def format_leaderboard():
    if not leaderboard:
        return "The leaderboard is currently empty."

    sorted_leaderboard = sorted(leaderboard.items(), key=lambda item: item[1], reverse=True)
    formatted = []
    for user_id, points in sorted_leaderboard:
        real_name = get_user_real_name(app, user_id)
        formatted.append(f"{real_name}: {points} points")
    return f"*Leaderboard:*\n\n" + "\n".join(formatted)

#add points to a user (including the sender)
def add_points(ack, body, say):
    ack()  # Acknowledge the command request

    user_id = body['user_id']
    text = body.get('text', '').strip()

    # If text is empty, add points to the sender
    if not text:
        add_user_to_leaderboard(user_id)
        say(f"<@{user_id}> has been added to the leaderboard with 1 point!")
    else:
        try:
            # Allow tagging users and specifying points (optional)
            target_user = text.split()[0].strip("<@>")
            points = int(text.split()[1]) if len(text.split()) > 1 else 1

            add_user_to_leaderboard(target_user, points)
            say(f"<@{target_user}> has been awarded {points} point(s)!")
        except (IndexError, ValueError):
            say("Invalid input! Use the format `/addpoints @user [points]`")

# Command to show the leaderboard
def show_leaderboard(ack, body, say):
    ack()  # Acknowledge the command request
    say(format_leaderboard())

