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

machine_list = []
count_machine = 0
user_list = []

def create_new_machine():

    # Create a machine instance with the states configured.
    machine = TocMachine(
        states=["start_state", "state_for_menu", "state_for_homework_management", "state_for_exam_management", "state_for_reminder_management",
            "state_for_add_homework", "state_for_delete_homework", "state_for_examine_homework", "state_for_add_exam", "state_for_delete_exam", "state_for_examine_exam", 
            "state_for_add_reminder", "state_for_delete_reminder", "state_for_examine_reminder"],
        transitions=[
            {
                # "Initial state" to "selection state".
                "trigger": "go_to_menu",
                "source": "start_state",
                "dest": "state_for_menu",
            },
            {
                # "selection state" to "homework management state".
                "trigger": "go_to_homework_management",
                "source": "state_for_menu",
                "dest": "state_for_homework_management",
            },
            {
                # "selection state" to "exam management state".
                "trigger": "go_to_exam_management",
                "source": "state_for_menu",
                "dest": "state_for_exam_management",
            },
            {
                # "selection state" to "reminder management state".
                "trigger": "go_to_reminder_management",
                "source": "state_for_menu",
                "dest": "state_for_reminder_management",
            },
            {
                # "homework management state" to "add homework state".
                "trigger": "go_to_add_homework",
                "source": "state_for_homework_management",
                "dest": "state_for_add_homework",
            },
            {
                # "homework management state" to "examine homework state".
                "trigger": "go_to_examine_homework",
                "source": "state_for_homework_management",
                "dest": "state_for_examine_homework",
            },
            {
                # "homework management state" to "delete homework state".
                "trigger": "go_to_delete_homework",
                "source": "state_for_homework_management",
                "dest": "state_for_delete_homework",
            },
            {
                # "exam management state" to "add exam state".
                "trigger": "go_to_add_exam",
                "source": "state_for_exam_management",
                "dest": "state_for_add_exam",
            },
            {
                # "exam management state" to "examine exam state".
                "trigger": "go_to_examine_exam",
                "source": "state_for_exam_management",
                "dest": "state_for_examine_exam",
            },
            {
                # "exam management state" to "delete exam state".
                "trigger": "go_to_delete_exam",
                "source": "state_for_exam_management",
                "dest": "state_for_delete_exam",
            },
            {
                # "reminder management state" to "add reminder state".
                "trigger": "go_to_add_reminder",
                "source": "state_for_reminder_management",
                "dest": "state_for_add_reminder",
            },
            {
                # "reminder management state" to "examine reminder state".
                "trigger": "go_to_examine_reminder",
                "source": "state_for_reminder_management",
                "dest": "state_for_examine_reminder",
            },
            {
                # "reminder management state" to "delete reminder state".
                "trigger": "go_to_delete_reminder",
                "source": "state_for_reminder_management",
                "dest": "state_for_delete_reminder",
            },
            {
                # Back to "homework management state".
                "trigger": "go_back_to_homework_management",
                "source": ["state_for_add_homework", "state_for_examine_homework", "state_for_delete_homework"],
                "dest": "state_for_homework_management",
            },
            {
                # Back to "exam management state".
                "trigger": "go_back_to_exam_management",
                "source": ["state_for_add_exam", "state_for_examine_exam", "state_for_delete_exam"],
                "dest": "state_for_exam_management",
            },
            {
                # Back to "reminder management state".
                "trigger": "go_back_to_reminder_management",
                "source": ["state_for_add_reminder", "state_for_examine_reminder", "state_for_delete_reminder"],
                "dest": "state_for_reminder_management",
            },
            {
                # Back to "state_for_menu".
                "trigger": "go_back_to_menu", 
                "source": ["state_for_homework_management", "state_for_exam_management", "state_for_reminder_management", "state_for_add_homework",
                        "state_for_examine_homework", "state_for_delete_homework", "state_for_add_exam", "state_for_examine_exam", "state_for_delete_exam", 
                        "state_for_add_reminder", "state_for_examine_reminder", "state_for_delete_reminder"],
                "dest": "state_for_menu"
            },
            {
                # Back to "initial state".
                "trigger": "go_back", 
                "source": ["state_for_menu", "state_for_homework_management", "state_for_exam_management", "state_for_reminder_management", "state_for_add_homework",
                        "state_for_examine_homework", "state_for_delete_homework", "state_for_add_exam", "state_for_examine_exam", "state_for_delete_exam",
                        "state_for_add_reminder", "state_for_examine_reminder", "state_for_delete_reminder"],
                "dest": "start_state"
            },
        ],
        initial="start_state",
        auto_transitions=False,
        show_conditions=True,
    )
    
    # Add new machine to machine list.
    global machine_list
    machine_list.append(machine)
    global count_machine
    count_machine = count_machine + 1

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

        #print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        
        # Check whether the user is registered.
        global user_list
        is_user_found = False
        user_index = (-1)
        for index in range(len(user_list)):
            if user_list[index] == event.source.user_id:
                is_user_found = True
                user_index = index
        
        
        # Add a new machine or not.
        if is_user_found == False:
            user_list.append(event.source.user_id)
            create_new_machine();
        
        # Set index for this user.
        global count_machine
        if is_user_found == False:
            user_index = count_machine - 1;
        
        # Check whether the event results in state transition.
        if event.message.text.lower() == "reset":
            machine_list[user_index].reset_states(event)
        elif machine_list[user_index].state == "start_state":
            machine_list[user_index].check_user_start(event)
        elif machine_list[user_index].state == "state_for_menu":
            machine_list[user_index].check_state_for_operation_menu(event)
        elif machine_list[user_index].state == "state_for_homework_management":
            machine_list[user_index].check_state_for_homework_operation(event)
        elif machine_list[user_index].state == "state_for_exam_management":
            machine_list[user_index].check_state_for_exam_operation(event)
        elif machine_list[user_index].state == "state_for_reminder_management":
            machine_list[user_index].check_state_for_reminder_operation(event)   
        elif machine_list[user_index].state == "state_for_add_homework":
            machine_list[user_index].add_homework(event)
        elif machine_list[user_index].state == "state_for_add_exam":
            machine_list[user_index].add_exam(event)
        elif machine_list[user_index].state == "state_for_add_reminder":
            machine_list[user_index].add_reminder(event)
        elif machine_list[user_index].state == "state_for_examine_homework":
            machine_list[user_index].examine_homework(event)
        elif machine_list[user_index].state == "state_for_examine_exam":
            machine_list[user_index].examine_exam(event)
        elif machine_list[user_index].state == "state_for_examine_reminder":
            machine_list[user_index].examine_reminder(event)
        elif machine_list[user_index].state == "state_for_delete_homework":
            machine_list[user_index].delete_homework(event)
        elif machine_list[user_index].state == "state_for_delete_exam":
            machine_list[user_index].delete_exam(event)
        elif machine_list[user_index].state == "state_for_delete_reminder":
            machine_list[user_index].delete_reminder(event)
            

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
