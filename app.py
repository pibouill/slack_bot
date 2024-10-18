############
############
############
############
############
############

from logging import WARNING
from slack_bolt import App, Say
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
import datetime
from dotenv import load_dotenv
import leaderboard

class bcolors:
     HEADER = '\033[95m'
     OKBLUE = '\033[94m'
     OKCYAN = '\033[96m'
     OKGREEN = '\033[92m'
     WARNING = '\033[93m'
     FAIL = '\033[91m'
     ENDC = '\033[0m'
     BOLD = '\033[1m'
     UNDERLINE = '\033[4m'



load_dotenv()

SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
SLACK_APP_TOKEN = os.environ['SLACK_APP_TOKEN']

app = App(token=SLACK_BOT_TOKEN)

@app.event("app_mention")
def mention_handler(body: dict, say):

    user_id = f"<@{body.get('event', {}).get('user')}>"

    say(f"What's up? {user_id}\nGive me something")

#### Get info from user's message
    bot_id = body.get("event", {}).get("text").split()[0]

    user_submission = body.get("event", {}).get("text")

    user_submission = user_submission.replace(bot_id, "").strip()

    user_id_info = body.get('event', {}).get('user')

    sending_time = body.get("event_time")

    if sending_time is not None:
       sending_time = datetime.datetime.fromtimestamp(sending_time)
    else:
       sending_time = None

    u = app.client.users_info(user=user_id_info)
    user_name = u.get('user', {}).get('real_name')

########### Print infos
    # print(body)
    # print(u)
    print("\n-------------------------------------------------\n")
    print("\nbot_id-->", bot_id)
    print("user_id-->", user_id)
    print("user_name -->", user_name)
    print("user_submission-->", user_submission)
    print("sending_time-->", sending_time)
    print("valid_input-->", valid_input)


######### Bot output
    if valid_input.lower() in user_submission.lower():
        print("Good")
        leaderboard.add_user_to_leaderboard(user_id_info)
        say(f"YOU GOT IT\n:clap: :clap:\n You win 1 point, {user_id}!")
    else:
        print("Not Good")
        say("nope.")
	

@app.event("message")
def	handle_message_events(body, logger):
	logger.info("received message event: %s", body)

# @app.command("/addpoints")
# def add_points(ack, body, say):
#     ack()
#     leaderboard.add_points(ack, body, say)

@app.command("/leaderboard")
def show_leaderboard(ack, body, say):
    ack()
    leaderboard.show_leaderboard(ack, body, say)

@app.command("/get_rank")
def show_rank(ack, body, say):
    ack()
    user_mention = body.get('text', '').strip()

    if user_mention:
        user_id = user_mention.strip("<@>")
        rank_message = leaderboard.get_user_rank(user_id)
        say(rank_message)
    else:
        say("I need a valid user name, starting with '@'.")

def launch_message():
	channel_id = 'C078TS7TD26'
	message = (
        "yoyoyo <!channel> ready to do stuff???\n\n"
        "You can use the following commands to interact with me:\n\n"
        "`/leaderboard` -> Get the current top 5 rank\n"
        "`/get_rank <user_name>` -> Get the current rank of the specified user\n"
    )

	try:
		app.client.chat_postMessage(channel=channel_id, text=message)
		print(f"{bcolors.OKGREEN}Launch message correctly sent{bcolors.ENDC}")
	except Exception as e:
		print(f"{bcolors.WARNING}Error sending welcome message: {e}{bcolors.ENDC}")

if __name__ == "__main__":
    valid_input = input("input: ")
    launch_message()
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)

    handler.start()
