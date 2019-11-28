import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageAction

from fsm import TocMachine
from utils import send_text_message

# Let Flask set the environment variable depending on .env file.
load_dotenv()

# Create a machine instance with the states configured.
machine = TocMachine(
    states=["start_state", "state_for_selection", "state_for_homework_management", "state_for_exam_management", 
        "state_for_add_homework", "state_for_examine_homework", "state_for_add_exam", "state_for_examine_exam"],
    transitions=[
        {
            # "Initial state" to "selection state".
            "trigger": "prepare_for_user_start",
            "source": "start_state",
            "dest": "state_for_selection",
            "conditions": "is_going_to_state_for_selection",
        },
        {
            # "selection state" to "homework management state".
            "trigger": "wait_for_selection",
            "source": "state_for_selection",
            "dest": "state_for_homework_management",
            "conditions": "is_going_to_state_for_homework_management",
        },
        {
            # "selection state" to "exam management state".
            "trigger": "wait_for_selection",
            "source": "state_for_selection",
            "dest": "state_for_exam_management",
            "conditions": "is_going_to_state_for_exam_management",
        },
        {
            # "homework management state" to "add homework state".
            "trigger": "wait_for_selection_homework",
            "source": "state_for_homework_management",
            "dest": "state_for_add_homework",
            "conditions": "is_going_to_state_for_add_homework",
        },
        {
            # "homework management state" to "examine homework state".
            "trigger": "wait_for_selection_homework",
            "source": "state_for_homework_management",
            "dest": "state_for_examine_homework",
            "conditions": "is_going_to_state_for_examine_homework",
        },
        {
            # "homework management state" back to "selection state".
            "trigger": "is_back_to_selection",
            "source": "state_for_homework_management",
            "dest": "state_for_selection",
            "conditions": "is_going_back_to_state_for_selection",
        },
        {
            # "exam management state" to "add exam state".
            "trigger": "wait_for_selection_exam",
            "source": "state_for_exam_management",
            "dest": "state_for_add_exam",
            "conditions": "is_going_to_state_for_add_exam",
        },
        {
            # "exam management state" to "examine exam state".
            "trigger": "wait_for_selection_exam",
            "source": "state_for_exam_management",
            "dest": "state_for_examine_exam",
            "conditions": "is_going_to_state_for_examine_exam",
        },
        {
            # "exam management state" back to "selection state".
            "trigger": "is_back_to_selection",
            "source": "state_for_exam_management",
            "dest": "state_for_selection",
            "conditions": "is_going_back_to_state_for_selection",
        },
        {
            # Back to "state_for_selection".
            "trigger": "go_to_menu", 
            "source": ["state_for_homework_management", "state_for_exam_management", "state_for_add_homework",
                       "state_for_examine_homework", "state_for_add_exam", "state_for_examine_exam"],
            "dest": "state_for_selection"
        },
        {
            # Back to "initial state".
            "trigger": "go_back", 
            "source": ["state_for_selection", "state_for_homework_management", "state_for_exam_management", "state_for_add_homework",
                       "state_for_examine_homework", "state_for_add_exam", "state_for_examine_exam"],
            "dest": "start_state"
        },
    ],
    initial="start_state",
    auto_transitions=False,
    show_conditions=True,
)

# Use Flask to create a web application.
app = Flask(__name__, static_url_path="")

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

# Create a LineBotApi instance.
line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

#***************************************************************************************


# Bind url "webhook" to this function.
@app.route("/webhook", methods=["POST"])
def webhook_handler():
    # Get the signature.
    signature = request.headers["X-Line-Signature"]
    
    # Get request body as text.
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # Parse webhook body.
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # If event is MessageEvent and message is TextMessage, then echo text.
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue

        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        
        # Check whether the event results in state transition.
        if machine.state == "start_state":
            response = machine.prepare_for_user_start(event)
            if response == False:
                send_text_message(event.reply_token, "Enter \"go\" to get started.")
        elif machine.state == "state_for_selection":
            response = machine.wait_for_selection(event)
            if response == False:
                send_text_message(event.reply_token, "Fail to select one.")
        elif machine.state == "state_for_homework_management":
            response = machine.wait_for_selection_homework(event)
            if response == False:
                response2 = machine.is_back_to_selection(event)
                if response2 == False:
                    send_text_message(event.reply_token, "Homework fail.")
        elif machine.state == "state_for_exam_management":
            response = machine.wait_for_selection_exam(event)
            if response == False:
                response2 = machine.is_back_to_selection(event)
                if response2 == False:
                    send_text_message(event.reply_token, "Exam fail.") 
        elif machine.state == "state_for_add_homework":
            machine.add_homework(event)
            

    return "OK"

#***************************************************************************************

# Bind url "show-fsm" to this function.
@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


# If the script is executed positively instead of called by other script, run following code.
if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
