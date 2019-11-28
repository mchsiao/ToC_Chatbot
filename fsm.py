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
    
    # Homework name list.
    homework_name = []
    # Homework deadline list.
    homework_deadline = []
    # Exam name list.
    exam_name = []
    # Exam date list.
    exam_date = []
    
    # Constructor.
    # GraphMachine is a light-weight state machine implementation.
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    # Check whether transition to state 1.
    def check_user_start(self, event):
        text = event.message.text
        if text.lower() == "go":
            self.go_to_menu(event)
        else:
            send_text_message(event.reply_token, "Enter \"go\" to get started.")

    # Check whether transition to state 2.
    def check_state_for_homework_and_exam_management(self, event):
        text = event.message.text
        if text.lower() == "homework management":
            self.go_to_homework_management(event)
        elif text.lower() == "exam management":
            self.go_to_exam_management(event)
        else:
            send_text_message(event.reply_token, "Fail to select neither homework nor exam.")
        
    # Check whether transition to state 2.
    def check_state_for_homework_operation(self, event):
        text = event.message.text
        if text.lower() == "add":
            self.go_to_add_homework(event)
        elif text.lower() == "examine":
            self.go_to_examine_homework(event)
        elif text.lower() == "back":
            self.go_back_to_menu_from_homework(event)
        else:
            send_text_message(event.reply_token, "Homework fail.")
    
    # Check whether transition to state 2.
    def check_state_for_exam_operation(self, event):
        text = event.message.text
        if text.lower() == "add":
            self.go_to_add_exam(event)
        elif text.lower() == "examine":
            self.go_to_examine_exam(event)
        elif text.lower() == "back":
            self.go_back_to_menu_from_exam(event)
        else:
            send_text_message(event.reply_token, "Exam fail.")
        

    # Code for just entering state 1.
    def on_enter_state_for_menu(self, event):
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
                        label='Homework Management',
                        text='Homework Management'
                    ),
					MessageAction(
                        label='Exam Management',
                        text='Exam Management'
                    ),
                ]
            )
        )
        
        # Send the button template to the user.
        reply_token = event.reply_token
        send_button_message(reply_token, buttons_template_message)
		
        # Go back to user state.
        # self.go_back()
    

    # Code for just entering state 2.
    def on_enter_state_for_homework_management(self, event):
        print("I'm entering state homework management.")

        # Create a Line button template for interaction.
        buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://freeiconshop.com/wp-content/uploads/edd/book-open-flat.png',
                title='Homework Management',
                text='Please select',
                actions=[
                    MessageAction(
                        label='Add',
                        text='Add'
                    ),
					MessageAction(
                        label='Examine',
                        text='Examine'
                    ),
                    MessageAction(
                        label='Back',
                        text='Back'
                    ),
                ]
            )
        )

        # Send the button template to the user.
        reply_token = event.reply_token
        send_button_message(reply_token, buttons_template_message)
        
        
    # Code for just entering state 2.
    def on_enter_state_for_exam_management(self, event):
        print("I'm entering state exam management.")

        # Create a Line button template for interaction.
        buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://freeiconshop.com/wp-content/uploads/edd/book-open-flat.png',
                title='Exam Management',
                text='Please select',
                actions=[
                    MessageAction(
                        label='Add',
                        text='Add'
                    ),
					MessageAction(
                        label='Examine',
                        text='Examine'
                    ),
                    MessageAction(
                        label='Back',
                        text='Back'
                    ),
                ]
            )
        )

        # Send the button template to the user.
        reply_token = event.reply_token
        send_button_message(reply_token, buttons_template_message)
        

    # Code for just entering state 2.
    def on_enter_state_for_add_homework(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "Enter \"name, deadline\" to add a new homework or enter \"Back\" to show the menu.")
        
        #self.go_back()
        
    # Code for just entering state 2.
    def on_enter_state_for_examine_homework(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "you can examine homework")
        self.go_back()
        
    # Code for just entering state 2.
    def on_enter_state_for_add_exam(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "you can add exam")
        self.go_back()
        
    # Code for just entering state 2.
    def on_enter_state_for_examine_exam(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "you can examine exam")
        self.go_back()
        
    # To add a new homework.
    def add_homework(self, event):
        text = event.message.text
        if text.lower() == "back":
            self.go_back_to_menu(event);
        else:
            info_list = text.split(",")
            if len(info_list) == 2:
                reply_token = event.reply_token
                send_text_message(reply_token, "Save successfully!, you can enter next one or type \"Back\" to show the menu.")
            else:
                reply_token = event.reply_token
                send_text_message(reply_token, "Please follow the format.")
        
            self.homework_name.append(info_list[0])
            self.homework_deadline.append(info_list[1])
        
        
        
        
        