from transitions.extensions import GraphMachine
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton
)

from utils import send_text_message
from utils import send_button_message


class TocMachine(GraphMachine):
    
    # Constructor.
    # GraphMachine is a light-weight state machine implementation.
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    # Check whether transition to state 1.
    def is_going_to_state_for_selection(self, event):
        text = event.message.text
        return text.lower() == "go"

    # Check whether transition to state 2.
    def is_going_to_state_for_homework_management(self, event):
        text = event.message.text
        return text.lower() == "homework management"

    # Code for just entering state 1.
    def on_enter_state_for_selection(self, event):
        print("I'm entering state1")
		
		# Create a Line button template for interaction.
        buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://freeiconshop.com/wp-content/uploads/edd/book-open-flat.png',
                title='May I help you?',
                text='Please select',
                actions=[
                    MessageAction(
                        label='Homework management',
                        text='Homework management'
                    ),
					MessageAction(
                        label='Exam management',
                        text='Exam management'
                    ),
                    URIAction(
                        label='uri',
                        uri='http://example.com/'
                    )
                ]
            )
        )
        
		# Send the button template to the user.
        reply_token = event.reply_token
        send_button_message(reply_token, buttons_template_message)
		
		# Go back to user state.
        # self.go_back()
	

    # Code for just exiting state 1.
    def on_exit_state1(self):
        print("Leaving state1")

    # Code for just entering state 2.
    def on_enter_state_for_homework_management(self, event):
        print("I'm entering state2")

        reply_token = event.reply_token
        send_text_message(reply_token, "OK, please enter the deadline of your homework.")
        self.go_back()

    # Code for just exiting state 2.
    def on_exit_state2(self):
        print("Leaving state2")
