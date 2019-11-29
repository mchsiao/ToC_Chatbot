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

    # Check whether transition to state_for_menu.
    def check_user_start(self, event):
        text = event.message.text
        if text.lower() == "go":
            self.go_to_menu(event)
        else:
            send_text_message(event.reply_token, "Start with \"Go\".")

    # Check whether transition to state_for_homework_management or state_for_exam_management.
    def check_state_for_homework_and_exam_management(self, event):
        text = event.message.text
        if text.lower() == "homework management":
            self.go_to_homework_management(event)
        elif text.lower() == "exam management":
            self.go_to_exam_management(event)
        else:
            send_text_message(event.reply_token, "Please select a function.")
        
    # Check whether transition to one of homework operations.
    def check_state_for_homework_operation(self, event):
        text = event.message.text
        if text.lower() == "add":
            self.go_to_add_homework(event)
        elif text.lower() == "examine":
            self.go_to_examine_homework(event)
        elif text.lower() == "delete":
            self.go_to_delete_homework(event)
        elif text.lower() == "back":
            self.go_back_to_menu(event)
        else:
            send_text_message(event.reply_token, "Homework fail.")
    
    # Check whether transition to one of exam operations.
    def check_state_for_exam_operation(self, event):
        text = event.message.text
        if text.lower() == "add":
            self.go_to_add_exam(event)
        elif text.lower() == "examine":
            self.go_to_examine_exam(event)
        elif text.lower() == "delete":
            self.go_to_delete_exam(event)
        elif text.lower() == "back":
            self.go_back_to_menu(event)
        else:
            send_text_message(event.reply_token, "Exam fail.")
        

    # Enter state_for_menu, and show the menu button template.
    def on_enter_state_for_menu(self, event):
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
        send_button_message(event.reply_token, buttons_template_message)

    # Enter state_for_homework_management, show the homework opearaion button template.
    def on_enter_state_for_homework_management(self, event):
        # Create a Line button template for interaction.
        buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://icon-library.net/images/homework-icon-png/homework-icon-png-5.jpg',
                title='Homework Management',
                text='Please select',
                actions=[
                    MessageAction(
                        label='Add',
                        text='Add'
                    ),
                    MessageAction(
                        label='Delete',
                        text='Delete'
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
        send_button_message(event.reply_token, buttons_template_message)
        
        
    # Enter state_for_homework_management, show the exam opearaion button template.
    def on_enter_state_for_exam_management(self, event):
        # Create a Line button template for interaction.
        buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://cdn4.iconfinder.com/data/icons/school-and-education-1-1/128/7-512.png',
                title='Exam Management',
                text='Please select',
                actions=[
                    MessageAction(
                        label='Add',
                        text='Add'
                    ),
                    MessageAction(
                        label='Delete',
                        text='Delete'
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
        send_button_message(event.reply_token, buttons_template_message)
        

    # Enter state_for_add_homework, reply with notification.
    def on_enter_state_for_add_homework(self, event):
        send_text_message(event.reply_token, "Enter \"Homework, Deadline\" to add a new homework.\n\nEnter \"Back\" to show the menu.")
        
    # Enter state_for_examine_homework, call another member function.
    def on_enter_state_for_examine_homework(self, event):
        self.examine_homework(event)
        
    # Enter state_for_delete_homework, reply with notification.
    def on_enter_state_for_delete_homework(self, event):
        if len(self.homework_name) == 0:
            reply_message = "No tracked homework for deletion.\n\n"
        else:
            reply_message = "Tracked homework are:\n\n"
            for index in range(len(self.homework_name)):
                reply_message += "Homework: "
                reply_message += self.homework_name[index]
                reply_message += "\nDeadline: "
                reply_message += self.homework_deadline[index]
                reply_message += "\n\n"
            reply_message += "Enter the homework you want to untrack.\n\n"
            
        reply_message += "Enter \"Back\" to show the menu."
        send_text_message(event.reply_token, reply_message)
        
    # Enter state_for_add_exam, reply with notification.
    def on_enter_state_for_add_exam(self, event):
        send_text_message(event.reply_token, "Enter \"Exam, Date\" to add a new exam.\n\nEnter \"Back\" to show the menu.")
        
    # Enter state_for_examine_exam, call another member function.
    def on_enter_state_for_examine_exam(self, event):
        self.examine_exam(event)
        
    # Enter state_for_delete_exam, reply with notification.
    def on_enter_state_for_delete_exam(self, event):
        if len(self.exam_name) == 0:
            reply_message = "No tracked exam for deletion.\n\n"
        else:
            reply_message = "Tracked exam are:\n\n"
            for index in range(len(self.exam_name)):
                reply_message += "Exam: "
                reply_message += self.exam_name[index]
                reply_message += "\nDate: "
                reply_message += self.exam_date[index]
                reply_message += "\n\n"
            reply_message += "Enter the exam you want to untrack.\n\n"
            
        reply_message += "Enter \"Back\" to show the menu."
        send_text_message(event.reply_token, reply_message)
        
    # If it's in state_for_add_homework, call this function to add new homework.
    def add_homework(self, event):
        text = event.message.text
        if text.lower() == "back":
            self.go_back_to_homework_management(event)
        else:
            info_list = text.split(",")
            if len(info_list) == 2:
                send_text_message(event.reply_token, "Save successfully!\n\nEnter next homework or enter \"Back\".")
            else:
                send_text_message(event.reply_token, "Please follow the format.")
        
            self.homework_name.append(info_list[0])
            self.homework_deadline.append(info_list[1])
            
    # If it's in state_for_add_exam, call this function to add new exam.
    def add_exam(self, event):
        text = event.message.text
        if text.lower() == "back":
            self.go_back_to_exam_management(event)
        else:
            info_list = text.split(",")
            if len(info_list) == 2:
                send_text_message(event.reply_token, "Save successfully!\n\nEnter next exam or enter \"Back\".")
            else:
                send_text_message(event.reply_token, "Please follow the format.")
        
            self.exam_name.append(info_list[0])
            self.exam_date.append(info_list[1])
            
    # If it's in state_for_examine_homework, call this function to examine tracked homework.
    def examine_homework(self, event):
        text = event.message.text
        if text.lower() == "back":
            self.go_back_to_homework_management(event)
        else:
            if len(self.homework_name) == 0:
                reply_message = "No tracked homework.\n\n"
            else:
                reply_message = "Tracked homework are:\n\n"
                for index in range(len(self.homework_deadline)):
                    reply_message += "Homework: "
                    reply_message += self.homework_name[index]
                    reply_message += "\nDeadline: "
                    reply_message += self.homework_deadline[index]
                    reply_message += "\n\n"    
            
            reply_message += "Enter \"Back\" to show the menu."
            send_text_message(event.reply_token, reply_message)
            
    # If it's in state_for_examine_exam, call this function to examine incoming exam.
    def examine_exam(self, event):
        text = event.message.text
        if text.lower() == "back":
            self.go_back_to_exam_management(event)
        else:
            if len(self.exam_name) == 0:
                reply_message = "No incoming exam.\n\n" 
            else:
                reply_message = "Incoming exam are:\n\n"
                for index in range(len(self.exam_date)):
                    reply_message += "Exam: "
                    reply_message += self.exam_name[index]
                    reply_message += "\nDate: "
                    reply_message += self.exam_date[index]
                    reply_message += "\n\n"    
            
            reply_message += "Enter \"Back\" to show the menu."
            send_text_message(event.reply_token, reply_message)
            
    # If it's in state_for_delete_homework, call this function to delete tracked homework.
    def delete_homework(self, event):
        text = event.message.text
        if text.lower() == "back":
            self.go_back_to_homework_management(event)
        else:
            if len(self.homework_name) == 0:
                reply_message = "No tracked homework for deletion.\n\n"
            else:  
                is_target_found = False
                target_index = 0
                for index in range(len(self.homework_name)):
                    if text == self.homework_name[index]:
                        is_target_found = True
                        target_index = index
                        break
        
                if is_target_found == True:
                    del self.homework_name[target_index]
                    del self.homework_deadline[target_index]
                    reply_message = "Delete successfully!\n\n"
                else:
                    reply_message = "No such homework.\n\n"
                    
            reply_message += "Enter \"Back\" to show the menu."
            send_text_message(event.reply_token, reply_message)
                
    # If it's in state_for_delete_exam, call this function to delete tracked exam.
    def delete_exam(self, event):
        text = event.message.text
        if text.lower() == "back":
            self.go_back_to_exam_management(event)
        else:
            if len(self.exam_name) == 0:
                reply_message = "No tracked exam for deletion.\n\n"
            else:  
                is_target_found = False
                target_index = 0
                for index in range(len(self.exam_name)):
                    if text == self.exam_name[index]:
                        is_target_found = True
                        target_index = index
                        break
        
                if is_target_found == True:
                    del self.exam_name[target_index]
                    del self.exam_date[target_index]
                    reply_message = "Delete successfully!\n\n"
                else:
                    reply_message = "No such exam.\n\n"
                    
            reply_message += "Enter \"Back\" to show the menu."
            send_text_message(event.reply_token, reply_message)
        