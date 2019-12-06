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
from utils import send_push_message

from threading import Thread
from time import sleep
from datetime import datetime

class TocMachine(GraphMachine):
    
    # Homework name list.
    homework_name = []
    # Homework deadline list.
    homework_deadline = []
    # Exam name list.
    exam_name = []
    # Exam date list.
    exam_date = []
    # Reminder list.
    reminder = []
    # Reminder time.
    reminder_time = []
    
    # Constructor.
    # GraphMachine is a light-weight state machine implementation.
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        
    # Timer.
    def timer(self, event, target_time):
        
        # Find the index for the reminder.
        target_index = (-1)
        for index in range(len(self.reminder_time)):
            if (self.reminder_time[index] == target_time):
                target_index = index
                break;
        
        # Calculate the delay time.
        info_list_2 = self.reminder_time[target_index].split("/")
        note_time = datetime(int(info_list_2[0]), int(info_list_2[1]), int(info_list_2[2]), int(info_list_2[3]), int(info_list_2[4]), int(info_list_2[5]), 0)
        timestamp = datetime.timestamp(note_time) - 8 * 60 * 60
        delay = timestamp - datetime.timestamp(datetime.now())
        
        # After countdown is complete, the reminder is sent.
        for i in range(int(delay)):
            sleep(1)
        
        # Find the index for the reminder again.
        target_index = (-1)
        for index in range(len(self.reminder_time)):
            if (self.reminder_time[index] == target_time):
                target_index = index
                break;
                
        if target_index != (-1):      
            send_push_message(event.source.user_id, self.reminder[target_index])
            # After sending, the reminder is deleted.
            del self.reminder[target_index]
            del self.reminder_time[target_index]

    # Check whether transition to state_for_menu.
    def check_user_start(self, event):
        text = event.message.text
        if text.lower() == "go":
            self.go_to_menu(event)
        else:
            # Create a Line button template for interaction.
            buttons_template_message = TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://cise-egypt.com/wp-content/uploads/2019/09/WELCOME-ST-IVES.jpg',
                    title='This is a task manager.',
                    text='Click \"GO\" to get started!',
                    actions=[
                        MessageAction(
                            label='GO',
                            text='GO'
                        ),
                    ]
                )
            )
        
            # Send the button template to the user.
            send_button_message(event.reply_token, buttons_template_message)
            


    # Check whether transition to state_for_homework_management or state_for_exam_management.
    def check_state_for_operation_menu(self, event):
        text = event.message.text
        if text.lower() == "homework management":
            self.go_to_homework_management(event)
        elif text.lower() == "exam management":
            self.go_to_exam_management(event)
        elif text.lower() == "reminder":
            self.go_to_reminder_management(event)
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
            
    # Check whether transition to one of reminder operations.
    def check_state_for_reminder_operation(self, event):
        text = event.message.text
        if text.lower() == "add":
            self.go_to_add_reminder(event)
        elif text.lower() == "examine":
            self.go_to_examine_reminder(event)
        elif text.lower() == "delete":
            self.go_to_delete_reminder(event)
        elif text.lower() == "back":
            self.go_back_to_menu(event)
        else:
            send_text_message(event.reply_token, "Reminder fail.")

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
                    MessageAction(
                        label='Reminder',
                        text='Reminder'
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
        
    # Enter state_for_reminder_management, show the reminder opearaion button template.
    def on_enter_state_for_reminder_management(self, event):
        # Create a Line button template for interaction.
        buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://www.vippng.com/png/detail/0-391_facebook-fb-globe-notification-icon-logo-png-push.png',
                title='Reminder Management',
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
        # Create a Line button template for interaction.
        buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://icon-library.net/images/homework-icon-png/homework-icon-png-5.jpg',
                title='Add a new homework.',
                text='Enter \"Homework, Deadline\" \nto add a new homework.',
                actions=[
                    MessageAction(
                        label='Back',
                        text='Back'
                    ),
                ]
            )
        )

        # Send the button template to the user.
        send_button_message(event.reply_token, buttons_template_message)
        
        
    # Enter state_for_examine_homework, call another member function.
    def on_enter_state_for_examine_homework(self, event):
        self.examine_homework(event)
        
    # Enter state_for_delete_homework, reply with notification.
    def on_enter_state_for_delete_homework(self, event):
        if len(self.homework_name) == 0:
            reply_message = "No traced homework for deletion."
        else:
            reply_message = "Select one homework for deletion."    
        # Create a Line button template for interaction.
        buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://icon-library.net/images/homework-icon-png/homework-icon-png-5.jpg',
                title='Delete a traced homework.',
                text=reply_message,
                actions=[
                    MessageAction(
                        label='Back',
                        text='Back'
                    ),
                ]
            )
        )
        # Send the button template to the user.
        send_button_message(event.reply_token, buttons_template_message)
        
        if (reply_message != "No traced homework for deletion."):
            reply_message_2 = ""
            for index in range(len(self.homework_name)):
                reply_message_2 += "Homework: "
                reply_message_2 += self.homework_name[index]
                reply_message_2 += "\nDeadline: "
                reply_message_2 += self.homework_deadline[index]
                if index != (len(self.homework_name) - 1):
                    reply_message_2 += "\n\n"
            
            send_push_message(event.source.user_id, reply_message_2)
    
    # Enter state_for_add_reminder, reply with notification.
    def on_enter_state_for_add_reminder(self, event):
        # Create a Line button template for interaction.
        buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://www.vippng.com/png/detail/0-391_facebook-fb-globe-notification-icon-logo-png-push.png',
                title='Add a new reminder.',
                text='Enter \"Reminder, Time(Y/M/D/H/M/S)\".',
                actions=[
                    MessageAction(
                        label='Back',
                        text='Back'
                    ),
                ]
            )
        )

        # Send the button template to the user.
        send_button_message(event.reply_token, buttons_template_message)
       
        
    # Enter state_for_examine_reminder, call another member function.
    def on_enter_state_for_examine_reminder(self, event):
        self.examine_reminder(event)
        
    # Enter state_for_delete_reminder, reply with notification.
    def on_enter_state_for_delete_reminder(self, event):
        if len(self.reminder) == 0:
            reply_message = "No scheduled reminder for deletion."
        else:
            reply_message = "Select one reminder for deletion."    
        # Create a Line button template for interaction.
        buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://www.vippng.com/png/detail/0-391_facebook-fb-globe-notification-icon-logo-png-push.png',
                title='Delete a scheduled reminder.',
                text=reply_message,
                actions=[
                    MessageAction(
                        label='Back',
                        text='Back'
                    ),
                ]
            )
        )
        # Send the button template to the user.
        send_button_message(event.reply_token, buttons_template_message)
        
        if (reply_message != "No scheduled reminder."):
                reply_message_2 = ""
                for index in range(len(self.reminder)):
                
                    reply_message_2 += "Reminder: "
                    reply_message_2 += self.reminder[index]
                    reply_message_2 += "\nTime: "
                
                    # Set the form of time.
                    info_list_2 = self.reminder_time[index].split("/")
                    for index_2 in range(len(info_list_2)):
                        if index_2 < 3:
                            reply_message_2 += info_list_2[index_2]
                            if index_2 != 2:
                                reply_message_2 += "/"
                            else:
                                reply_message_2 += " "
                        else:
                            reply_message_2 += info_list_2[index_2]
                            if index_2 != 5:
                                reply_message_2 += ":"
                    
                    # New line for next reminder.
                    if index != (len(self.reminder) - 1):
                        reply_message_2 += "\n\n"
            
                send_push_message(event.source.user_id, reply_message_2)
    
    # Enter state_for_add_exam, reply with notification.
    def on_enter_state_for_add_exam(self, event):
        # Create a Line button template for interaction.
        buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://cdn4.iconfinder.com/data/icons/school-and-education-1-1/128/7-512.png',
                title='Add a new exam.',
                text='Enter \"Exam, Date\"\nto add a new exam.',
                actions=[
                    MessageAction(
                        label='Back',
                        text='Back'
                    ),
                ]
            )
        )

        # Send the button template to the user.
        send_button_message(event.reply_token, buttons_template_message)
        
    # Enter state_for_examine_exam, call another member function.
    def on_enter_state_for_examine_exam(self, event):
        self.examine_exam(event)
        
    # Enter state_for_delete_exam, reply with notification.
    def on_enter_state_for_delete_exam(self, event):
        if len(self.exam_name) == 0:
            reply_message = "No traced exam for deletion."
        else:
            reply_message = "Select one exam for deletion."
        # Create a Line button template for interaction.
        buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://cdn4.iconfinder.com/data/icons/school-and-education-1-1/128/7-512.png',
                title='Delete a traced exam.',
                text=reply_message,
                actions=[
                    MessageAction(
                        label='Back',
                        text='Back'
                    ),
                ]
            )
        )
        # Send the button template to the user.
        send_button_message(event.reply_token, buttons_template_message)
        
        if (reply_message != "No traced exam for deletion."):
            reply_message_2 = ""
            for index in range(len(self.exam_name)):
                reply_message_2 += "Exam: "
                reply_message_2 += self.exam_name[index]
                reply_message_2 += "\nDate: "
                reply_message_2 += self.exam_date[index]
                if index != (len(self.exam_name) - 1):
                    reply_message_2 += "\n\n"
            
            send_push_message(event.source.user_id, reply_message_2)
        
    # If it's in state_for_add_homework, call this function to add new homework.
    def add_homework(self, event):
        text = event.message.text
        if text.lower() == "back":
            self.go_back_to_homework_management(event)
        else:
            info_list = text.split(",")
            if len(info_list) == 2:
                reply_message = "Save successfully!\nContinue to enter next homework."
            else:
                reply_message = "Please follow the format."
            
            # Create a Line button template for interaction.
            buttons_template_message = TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://icon-library.net/images/homework-icon-png/homework-icon-png-5.jpg',
                    title='Notification',
                    text=reply_message,
                    actions=[
                        MessageAction(
                            label='Back',
                            text='Back'
                        ),
                    ]
                )
            )

            # Send the button template to the user.
            send_button_message(event.reply_token, buttons_template_message)
        
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
                reply_message = "Save successfully!\nContinue to enter next exam."
            else:
                reply_message = "Please follow the format."
            
            # Create a Line button template for interaction.
            buttons_template_message = TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://cdn4.iconfinder.com/data/icons/school-and-education-1-1/128/7-512.png',
                    title='Notification',
                    text=reply_message,
                    actions=[
                        MessageAction(
                            label='Back',
                            text='Back'
                        ),
                    ]
                )
            )

            # Send the button template to the user.
            send_button_message(event.reply_token, buttons_template_message)
        
            self.exam_name.append(info_list[0])
            self.exam_date.append(info_list[1])
            
    # If it's in state_for_add_reminder, call this function to add new reminder.
    def add_reminder(self, event):
        text = event.message.text
        if text.lower() == "back":
            self.go_back_to_reminder_management(event)
        else:
            info_list = text.split(",")
            if len(info_list) == 2:
                info_list_2 = info_list[1].split("/")
                if len(info_list_2) == 6:
                    reply_message = "Save successfully!\nContinue to enter next reminder."
                else:
                    reply_message = "Please follow the format."
            else:
                reply_message = "Please follow the format."
            
            # Create a Line button template for interaction.
            buttons_template_message = TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://www.vippng.com/png/detail/0-391_facebook-fb-globe-notification-icon-logo-png-push.png',
                    title='Notification',
                    text=reply_message,
                    actions=[
                        MessageAction(
                            label='Back',
                            text='Back'
                        ),
                    ]
                )
            )

            # Send the button template to the user.
            send_button_message(event.reply_token, buttons_template_message)
        
            if reply_message == "Save successfully!\nContinue to enter next reminder.":
                
                # Append the new reminder to list.
                self.reminder.append(info_list[0])
                self.reminder_time.append(info_list[1])
            
                # Start timer countdown.
                thread = Thread(target=self.timer, args=(event, info_list[1]))
                thread.start()
            
    # If it's in state_for_examine_homework, call this function to examine tracked homework.
    def examine_homework(self, event):
        text = event.message.text
        if text.lower() == "back":
            self.go_back_to_homework_management(event)
        else:
            if len(self.homework_name) == 0:
                reply_message = "No traced homework."
            else:
                reply_message = "Your homework are in the following."    
            # Create a Line button template for interaction.
            buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://icon-library.net/images/homework-icon-png/homework-icon-png-5.jpg',
                    title='Traced Homework',
                    text=reply_message,
                    actions=[
                        MessageAction(
                            label='Back',
                            text='Back'
                        ),
                    ]
                )
            )
            # Send the button template to the user.
            send_button_message(event.reply_token, buttons_template_message)
        
            if (reply_message != "No traced homework."):
                reply_message_2 = ""
                for index in range(len(self.homework_name)):
                    reply_message_2 += "Homework: "
                    reply_message_2 += self.homework_name[index]
                    reply_message_2 += "\nDeadline: "
                    reply_message_2 += self.homework_deadline[index]
                    if index != (len(self.homework_name) - 1):
                        reply_message_2 += "\n\n"
            
                send_push_message(event.source.user_id, reply_message_2)
            
    # If it's in state_for_examine_exam, call this function to examine incoming exam.
    def examine_exam(self, event):
        text = event.message.text
        if text.lower() == "back":
            self.go_back_to_exam_management(event)
        else:
            if len(self.exam_name) == 0:
                reply_message = "No incoming exam."
            else:
                reply_message = "Your exam are in the following.."
            # Create a Line button template for interaction.
            buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://cdn4.iconfinder.com/data/icons/school-and-education-1-1/128/7-512.png',
                    title='Incoming Exam',
                    text=reply_message,
                    actions=[
                        MessageAction(
                            label='Back',
                            text='Back'
                        ),
                    ]
                )
            )
            # Send the button template to the user.
            send_button_message(event.reply_token, buttons_template_message)
        
            if (reply_message != "No incoming exam."):
                reply_message_2 = ""
                for index in range(len(self.exam_name)):
                    reply_message_2 += "Exam: "
                    reply_message_2 += self.exam_name[index]
                    reply_message_2 += "\nDate: "
                    reply_message_2 += self.exam_date[index]
                    if index != (len(self.exam_name) - 1):
                        reply_message_2 += "\n\n"
            
                send_push_message(event.source.user_id, reply_message_2)         

    # If it's in state_for_examine_reminder, call this function to examine tracked reminder.
    def examine_reminder(self, event):
        text = event.message.text
        if text.lower() == "back":
            self.go_back_to_reminder_management(event)
        else:
            if len(self.reminder) == 0:
                reply_message = "No scheduled reminder."
            else:
                reply_message = "Your reminders are in the following."    
            # Create a Line button template for interaction.
            buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://www.vippng.com/png/detail/0-391_facebook-fb-globe-notification-icon-logo-png-push.png',
                    title='Scheduled Reminder',
                    text=reply_message,
                    actions=[
                        MessageAction(
                            label='Back',
                            text='Back'
                        ),
                    ]
                )
            )
            # Send the button template to the user.
            send_button_message(event.reply_token, buttons_template_message)
        
            if (reply_message != "No scheduled reminder."):
                reply_message_2 = ""
                for index in range(len(self.reminder)):
                
                    reply_message_2 += "Reminder: "
                    reply_message_2 += self.reminder[index]
                    reply_message_2 += "\nTime: "
                
                    # Set the form of time.
                    info_list_2 = self.reminder_time[index].split("/")
                    for index_2 in range(len(info_list_2)):
                        if index_2 < 3:
                            reply_message_2 += info_list_2[index_2]
                            if index_2 != 2:
                                reply_message_2 += "/"
                            else:
                                reply_message_2 += " "
                        else:
                            reply_message_2 += info_list_2[index_2]
                            if index_2 != 5:
                                reply_message_2 += ":"
                    
                    # New line for next reminder.
                    if index != (len(self.reminder) - 1):
                        reply_message_2 += "\n\n"
            
                send_push_message(event.source.user_id, reply_message_2)
       
       
    # If it's in state_for_delete_homework, call this function to delete tracked homework.
    def delete_homework(self, event):
        text = event.message.text
        if text.lower() == "back":
            self.go_back_to_homework_management(event)
        else:
            if len(self.homework_name) == 0:
                reply_message = "No tracked homework for deletion."
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
                    reply_message = "Delete successfully!"
                else:
                    reply_message = "No such homework."
                    
                # Create a Line button template for interaction.
                buttons_template_message = TemplateSendMessage(
                    alt_text='Buttons template',
                    template=ButtonsTemplate(
                        thumbnail_image_url='https://icon-library.net/images/homework-icon-png/homework-icon-png-5.jpg',
                        title='Notification',
                        text=reply_message,
                        actions=[
                            MessageAction(
                                label='Back',
                                text='Back'
                            ),
                        ]
                    )
                )

                # Send the button template to the user.
                send_button_message(event.reply_token, buttons_template_message)
                
    # If it's in state_for_delete_exam, call this function to delete tracked exam.
    def delete_exam(self, event):
        text = event.message.text
        if text.lower() == "back":
            self.go_back_to_exam_management(event)
        else:
            if len(self.exam_name) == 0:
                reply_message = "No tracked exam for deletion."
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
                    reply_message = "Delete successfully!"
                else:
                    reply_message = "No such exam."
                    
                # Create a Line button template for interaction.
                buttons_template_message = TemplateSendMessage(
                    alt_text='Buttons template',
                    template=ButtonsTemplate(
                        thumbnail_image_url='https://cdn4.iconfinder.com/data/icons/school-and-education-1-1/128/7-512.png',
                        title='Notification',
                        text=reply_message,
                        actions=[
                            MessageAction(
                                label='Back',
                                text='Back'
                            ),
                        ]
                    )
                )

                # Send the button template to the user.
                send_button_message(event.reply_token, buttons_template_message)
                
                    
    # If it's in state_for_delete_reminder, call this function to delete tracked reminder.
    def delete_reminder(self, event):
        text = event.message.text
        if text.lower() == "back":
            self.go_back_to_reminder_management(event)
        else:
            if len(self.reminder) == 0:
                reply_message = "No scheduled reminder for deletion."
            else:  
                is_target_found = False
                target_index = 0
                for index in range(len(self.reminder)):
                    if text == self.reminder[index]:
                        is_target_found = True
                        target_index = index
                        break
        
                if is_target_found == True:
                    del self.reminder[target_index]
                    del self.reminder_time[target_index]
                    reply_message = "Delete successfully!"
                else:
                    reply_message = "No such reminder."
                    
                # Create a Line button template for interaction.
                buttons_template_message = TemplateSendMessage(
                    alt_text='Buttons template',
                    template=ButtonsTemplate(
                        thumbnail_image_url='https://www.vippng.com/png/detail/0-391_facebook-fb-globe-notification-icon-logo-png-push.png',
                        title='Notification',
                        text=reply_message,
                        actions=[
                            MessageAction(
                                label='Back',
                                text='Back'
                            ),
                        ]
                    )
                )

                # Send the button template to the user.
                send_button_message(event.reply_token, buttons_template_message)  