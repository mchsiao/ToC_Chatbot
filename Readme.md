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
* Exam Management<br>
    * ___add___, ___delete___, or ___examine___ incoming homework<br>
* Reminder<br>
    * ___add___, ___delete___, or ___examine___ reserved reminder<br>
    * Given the specific moment, the Line bot will send reminders to the user automatically.<br>


## Finite State Machine
![fsm](./fsm.png)

## State Transition
The initial state is set to be `start_state`.<br>
The messages can be entered either by typing or pushing the buttons.<br>

* `start_state`:<br>
    * Input: ___Go___<br>
    * Destination: `state_for_menu`<br>
    
* `state_for_menu`:<br>
    * Input: ___Homework___ ___Management___<br>
    * Destination: `state_for_homework_management`<br>
    
    * Input: ___Exam___ ___Management___<br>
    * Destination: `state_for_exam_management`<br>
    
    * Input: ___Reminder___ ___Management___<br>
    * Destination: `state_for_reminder_management`<br>

    * Input: ___Reset___<br>
    * Destination: `start_state`<br>
    
* `state_for_homework_management`:<br>
    * Input: ___Add___<br>
    * Destination: `state_for_add_homework`<br>
    
    * Input: ___Examine___<br>
    * Destination: `state_for_examine_homework`<br>
    
    * Input: ___Delete___<br>
    * Destination: `state_for_delete_homework`<br>
    
    * Input: ___Back___<br>
    * Destination: `state_for_menu`<br>
    
    * Input: ___Reset___<br>
    * Destination: `start_state`<br>
    
* `state_for_exam_management`:<br>
    * Input: ___Add___<br>
    * Destination: `state_for_add_exam`<br>
    
    * Input: ___Examine___<br>
    * Destination: `state_for_examine_exam`<br>
    
    * Input: ___Delete___<br>
    * Destination: `state_for_delete_exam`<br>
    
    * Input: ___Back___<br>
    * Destination: `state_for_menu`<br>
    
    * Input: ___Reset___<br>
    * Destination: `start_state`<br>
    
* `state_for_reminder_management`:<br>
    * Input: ___Add___<br>
    * Destination: `state_for_add_reminder`<br>
    
    * Input: ___Examine___<br>
    * Destination: `state_for_examine_reminder`<br>
    
    * Input: ___Delete___<br>
    * Destination: `state_for_delete_reminder`<br>
    
    * Input: ___Back___<br>
    * Destination: `state_for_menu`<br>
    
    * Input: ___Reset___<br>
    * Destination: `start_state`<br>   

* `state_for_add_homework`:<br>
    * Input: Enter ___Homework___, ___Deadline(Month/Day)___ to add the homework into traced tasks.
    * Destination: `state_for_add_homework`<br>
    
    * Input: ___Back___<br>
    * Destination: `state_for_homework_management`<br>
    
    * Input: ___Reset___<br>
    * Destination: `start_state`<br> 
    
* `state_for_add_exam`:<br>
    * Input: Enter ___Exam___, ___Date(Month/Day)___ to add the exam into traced tasks.
    * Destination: `state_for_add_exam`<br>
    
    * Input: ___Back___<br>
    * Destination: `state_for_exam_management`<br>
    
    * Input: ___Reset___<br>
    * Destination: `start_state`<br> 
    
* `state_for_add_reminder`:<br>
    * Input: Enter ___Reminder___, ___Informing___ ___Time(Y/M/D/H/M/S)___ to add the reminder.
    * Destination: `state_for_add_reminder`<br>
    
    * Input: ___Back___<br>
    * Destination: `state_for_reminder_management`<br>
    
    * Input: ___Reset___<br>
    * Destination: `start_state`<br> 
    
* `state_for_delete_homework`:<br>
    * Input: Enter traced ___Homework___ to delete the homework in traced tasks, if it exists.
    * Destination: `state_for_delete_homework`<br>
    
    * Input: ___Back___<br>
    * Destination: `state_for_homework_management`<br>
    
    * Input: ___Reset___<br>
    * Destination: `start_state`<br> 
    
* `state_for_delete_exam`:<br>
    * Input: Enter traced ___Exam___ to delete the exam in traced tasks, if it exists.
    * Destination: `state_for_delete_exam`<br>
    
    * Input: ___Back___<br>
    * Destination: `state_for_exam_management`<br>
    
    * Input: ___Reset___<br>
    * Destination: `start_state`<br>

* `state_for_delete_reminder`:<br>
    * Input: Enter traced ___Reminder___ to delete the reminder if it exists.
    * Destination: `state_for_delete_reminder`<br>
    
    * Input: ___Back___<br>
    * Destination: `state_for_reminder_management`<br>
    
    * Input: ___Reset___<br>
    * Destination: `start_state`<br>   

* `state_for_examine_homework`:<br>
    * Input: ___Back___<br>
    * Destination: `state_for_homework_management`<br>
    
    * Input: ___Reset___<br>
    * Destination: `start_state`<br>

* `state_for_examine_exam`:<br>
    * Input: ___Back___<br>
    * Destination: `state_for_exam_management`<br>
    
    * Input: ___Reset___<br>
    * Destination: `start_state`<br>

* `state_for_examine_reminder`:<br>
    * Input: ___Back___<br>
    * Destination: `state_for_reminder_management`<br>
    
    * Input: ___Reset___<br>
    * Destination: `start_state`<br>    
    