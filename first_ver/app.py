############
############
############
############
############
############

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
import datetime
from dotenv import load_dotenv

load_dotenv()

SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
SLACK_APP_TOKEN = os.environ['SLACK_APP_TOKEN']

app = App(token=SLACK_BOT_TOKEN)

@app.event("app_mention")
def mention_handler(body: dict, say):

    sender_id = f"<@{body.get('event', {}).get('user')}>"

    say(f"What's up? {sender_id}")

    bot_id = body.get("event", {}).get("text").split()[0]
    sender_submission = body.get("event", {}).get("text")
    sender_submission = sender_submission.replace(bot_id, "").strip()
    sending_time = body.get("event_time")
    if sending_time is not None:
       # sending_time = datetime.datetime.fromtimestamp(sending_time, tz=datetime.timezone.utc)
       sending_time = datetime.datetime.fromtimestamp(sending_time)
    else:
       sending_time = None

    # print()
    print("\n-------------------------------------------------\n")
    print("\nbot_id-->", bot_id)
    print("sender_id-->", sender_id)
    print("sender_submission-->", sender_submission)


    if valid_input.lower() in sender_submission.lower():
        print("Good")
        say("yep")
    else:
        print("Not Good")
        say("nope.")
	
    print("valid_input-->", valid_input)
    print("sending_time-->", sending_time)

@app.event("message")
def	handle_message_events(body, logger):
	logger.info("received message event: %s", body)

	# You can add more logic here to respond to general messages if needed
    # For example, you might want to filter by user_id or channel_id
    # and perform specific actions based on the message content.




if __name__ == "__main__":
    valid_input = input("Your input: ")
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)

    handler.start()
