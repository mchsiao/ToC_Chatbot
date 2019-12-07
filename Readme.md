# Personal Assistant Chatbot
A Line bot based on finite state machine runs on heroku.<br>
Send messages to the bot for task management.<br>

## Setup
### Prerequisite
* Python 3.6
* Heroku(HTTPS Server)
* Line Application

## Usage
### Three functions provided
* Homework Management<br>
    * ___add___, ___delete___, or ___examine___ ongoing homework<br>


## Finite State Machine
![fsm](./fsm.png)

## State Transition
The initial state is set to be `start_state`.
The messages can be sent either by typing or using the buttons.

* `start_state`:<br>
    * Input: Go<br>
    * Destination: `state_for_menu`<br>
    
* `state_for_menu`:<br>
    * Input: Homework Management<br>
    * Destination: `state_for_homework_management`<br>
    
    * Input: Exam Management<br>
    * Destination: `state_for_exam_management`<br>
    
    * Input: Reminder Management<br>
    * Destination: `state_for_reminder_management`<br>

    * Input: Reset<br>
    * Destination: `start_state`<br>
    
* `state_for_homework_management`:<br>
    * Input: Add<br>
    * Destination: `state_for_add_homework`<br>
    
    * Input: Examine<br>
    * Destination: `state_for_examine_homework`<br>
    
    * Input: Delete<br>
    * Destination: `state_for_delete_homework`<br>
    
    * Input: Back<br>
    * Destination: `state_for_menu`<br>
    
    * Input: Reset<br>
    * Destination: `start_state`<br>
    
* `state_for_exam_management`:<br>
    * Input: Add<br>
    * Destination: `state_for_add_exam`<br>
    
    * Input: Examine<br>
    * Destination: `state_for_examine_exam`<br>
    
    * Input: Delete<br>
    * Destination: `state_for_delete_exam`<br>
    
    * Input: Back<br>
    * Destination: `state_for_menu`<br>
    
    * Input: Reset<br>
    * Destination: `start_state`<br>
    
* `state_for_reminder_management`:<br>
    * Input: Add<br>
    * Destination: `state_for_add_reminder`<br>
    
    * Input: Examine<br>
    * Destination: `state_for_examine_reminder`<br>
    
    * Input: Delete<br>
    * Destination: `state_for_delete_reminder`<br>
    
    * Input: Back<br>
    * Destination: `state_for_menu`<br>
    
    * Input: Reset<br>
    * Destination: `start_state`<br>    