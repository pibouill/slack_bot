##########################
##########################
##########################
##########################
##########################
##########################

import os
import json

LEADERBOARD_FILE = "leaderboard.json"

# Load leaderboard from JSON file

def load_leaderboard():
    # If the file doesn't exist, create an empty file
    if not os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, 'w') as f:
            json.dump({}, f)  # Write an empty JSON object to the file
        return {}  # Return an empty dictionary for the leaderboard

    with open(LEADERBOARD_FILE, 'r') as f:
        return json.load(f)

# Save leaderboard to JSON file
def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(leaderboard, f)

leaderboard = load_leaderboard()

#add users to the leaderboard
def add_user_to_leaderboard(user_id, points=1):
    if user_id in leaderboard:
        leaderboard[user_id] += points
    else:
        leaderboard[user_id] = points
    save_leaderboard(leaderboard)

#format the leaderboard for display
def format_leaderboard():
    if not leaderboard:
        return "The leaderboard is currently empty."

    sorted_leaderboard = sorted(leaderboard.items(), key=lambda item: item[1], reverse=True)
    formatted = "\n".join([f"<@{user_id}>: {points} points" for user_id, points in sorted_leaderboard])
    return f"*Leaderboard:*\n{formatted}"

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
