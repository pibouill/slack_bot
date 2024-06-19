from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
from dotenv import load_dotenv

load_dotenv()

SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
SLACK_APP_TOKEN = os.environ['SLACK_APP_TOKEN']

app = App(token=SLACK_BOT_TOKEN)

@app.event("app_mention")
def mention_handler(body: dict, say: callable):
    sender_id = f"<@{body.get('event', {}).get('user')}>"
    say(f"What's up? {sender_id}")
    bot_id = body.get("event", {}).get("text").split()[0]
    # sender_submission = body.get("event", {}).get("text").split()[1]
    sender_submission = body.get("event", {}).get("text")
    sender_submission = sender_submission.replace(bot_id, "").strip()
    print(body)
    print("\nbot_id-->", bot_id)
    print("sender_id-->", sender_id)
    print("sender_submission-->", sender_submission)


    valid_input = "joe con - blabla"
    if valid_input in sender_submission.lower():
        print("Good")
        print(sender_submission)
        say("yep")
    else:
        print("Not Good")
        say("nope.")
	
    # say('Hello World!')

if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)

    handler.start()
