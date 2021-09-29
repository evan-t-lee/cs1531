# Iteration 2 Plan

Assuming iteration 2 starts Wednesday 9th and is due Sunday 27th of October.

## Phase 1: Essential Functionality
Aim to be done by **Sunday 13th October**

This portion of the interface functions are those deemed to be strictly necessary for the basic operation of the slackr application. At the end of this development phase the application should be able to work at a bare minimum (dependent on front end implementation of course).

The functions that will be completed in this phase make up the skeleton of the application, and the other functions won’t be able to work to the fullest extent, or at all, without this phase being completed.

### Core Authentication Functions
Time estimated: **1.5 days**

Includes:
- auth_register
- auth_login
- auth_logout

These functions will be the most important to implement first since ultimately these are the most important to the user. The user needs to be able to register and login to use slackr and would need to log out for security purposes. With regards to the code, the tokens return from the auth_register and auth_login functions are required as inputs for many of the other functions.

### Core Channel Functions
Time estimated: **2.5 days**

Includes:
- channels_create
- channel_invite
- channel_join
- channel_messages

The task that users will perform most on slackr are sending and reading messages, but this can’t be done without a channel. As such this category of core functions is the next most important to implement.

### Core Messages Functions
Time estimated: **1 day**

Includes:
- message_send
- message_remove

As mentioned, sending messages is likely to be the most used functionality on slackr so this is a necessary function to implement in the first phase. Removing messages may also be crucial in some instances and its implementation will be most similar to message_send.

## Phase 2: Important Features
Aim to be done by **Monday 21st October**

This phase is concerned with implementing the important functions and features which the clients want/need. Note that most of these functions depend on the ones in phase 1. By the end of this phase the bulk of the slackr application should be complete with most of the desired features implemented.

### Password Reset Functions
Time estimated: **1 day**

Includes:
- auth_passwordreset_request
- auth_passwordreset_reset

### Channel Functions
Time estimated: **3 days**

Includes:
- channel_details
- channel_leave
- channels_list
- channels_listall
- channel_addowner
- channel_removeowner

### Message Functions
Time estimated: **1.5 days**

Includes:
- message_edit
- message_pin
- message_unpin

### Miscellaneous Functions
Time estimated: **1.5 days**

Includes:
- admin_userpermission_change
- search

### User Profile Functions
Time estimated: **2 days**

Includes:
- user_profile
- user_profile_setname
- user_profile_setemail
- user_profile_sethandle
- user_profile_uploadphoto

## Phase 3: Nice Features
Aim to be done by **Thursday 24th October**

This phase is focused on implementing the remaining functions which are features that enhance the user experience but ultimately we have deemed to be a bit less important than the functions of the previous phases. Standup capabilities, delayed message sending and message reactions 

### Standup Functions
Time estimated: **1.5 days**

Includes:
- standup_start
- standup_send

### Message Functions
Time estimated: **1.5 days**

Includes:
- message_sendlater
- message_react
- message_unreact

## Phase 4: Reserve Time
The remainding of this iteration is reserved for further testing, documentation, bug fixing and just leaving spare time in case issues arise earlier in the iteration.

## Plan in Table Format
![alt text](https://doc-08-7c-docs.googleusercontent.com/docs/securesc/8lt20lj89i68rml3nk72jog8go7q41up/tqfcv4ornt8k91ol9v6gsk1vjt77q8g9/1570334400000/16558037282303276398/16558037282303276398/1ih3WHLQg56J8eifRm_87lHKbnQwjoQ2D?e=view "Iteration 2 Plan")