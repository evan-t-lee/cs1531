# Assurance

## Acceptance Criteria for User Stories
Software validation is the process of evaluating whether the product satisfies user requirements and is concerned with whether the right system has been built. This part of software evaluation is primarily concerned with black box testing.

Acceptance criteria plays a crucial role in the validation of the slackr software solution and in the assurance of our backend implementation. By designing acceptance criteria for user stories, we as developers gain a deeper understanding of the client’s needs for various aspects of the software service and how a client’s needs should be satisfied. By fulfilling these acceptance criteria, we gain an assurance that the software product meets the needs of the stakeholders and thus we have a greater assurance that the software is valid.

Unfortunately acceptance testing was almost impossible to perform during iteration 2 due to integration complication between the frontend and the backend. For example, the input parameters from HTTP GET requestion could not be attained from the frontend and thus the backend would get invalid data. Among other issues, this in itself prevented users from being able to create channels. As a result we were unable to effectively evaluate the user experience of the software, since the frontend was basically unusable. However, with our acceptance criteria ready we are assured that once the frontend integrates the backend we will have the capability to ensure software validation.

### Auth Stories

*As a user, I want to be able to register an account so that I can use the slackr service.*
- Login page has an option to register an account.
- User is redirected to registration page
- User can register by entering email, password, first name and last name
- User is assigned a handle name based on their first and last names
- First and last names must be between 1 and 50 characters
- Password must be at least 6 characters
- Email address must be valid

*As a user, I want to be able to login to my slackr account on any device using only username and password, so that I am always able to check for new messages and be able to respond to them.*
- Login page should request an email address and the user’s password
- If the entered credentials are correct, the user is taken to the slackr home page where they can view their channels and their new messages

*As a user, I want to be able to logout so that other users are unable to perform unauthorised actions from my account without me being present.*
- The logout button is in the top right corner of the slackr interface.
- Upon logging out, the user’s messages and channels can only be accessed by logging in with the email and password again

*As a user, I want to be able to reset my password so that I can continue to use the slackr service if I have forgotten my registered password.*
- Scenario: Forgot password
- Given: User is on the login page
- When: The user selects the forgot password option
- And: The user has entered a valid email that matches a slackr account
- Then: A reset code is sent to the specified email address
- Given: The user received the reset code via email
- When: The user enters the reset code correctly
- Then: The user can set a new password

*As a user, I want to be able to request for a password reset using my email address, so that no one else can reset my password without my knowing.*
- A password reset must require email validation and verification.
- Using first and last names for verification is unsafe.

### Channel Stories

*As a student, I want to be able to see a list of all the channels that I am a part of, so I can easily check which channel my message belongs in.*
- From the home screen there is a side bar to the left with lists of channels.
- Under the heading “My Channels” the student can see all the channels they are a part of.

*As a student, I want to be able to list all the channels so that I can find the channels that are applicable to me.*
- There is a heading “Other Channels” listed under “My Channels” in the side bar.
- Under this heading, the student should be able to see the channels which they are not a part of

*As a course convener, I want the students to be able to see all the channels available to them, but not join those that are private. This is to ensure that they are unable to join tutor-lecture channels where confidential matters are discussed.*
- The students should be able to see all the channels in the slackr, in the side bar to the left.
- Students that try to join private channels should be denied access.

*As a student, I want to be able to view all the members of the channel so that I can identify the students that are in my course.*
- Given: User is a part of the channel
- Then: User is able to see the details of the channel, including the list of members
- When: Viewing the list of members
- Then: User is able to see the members without any permissions or channel admin/owner authority

*As a student, I want to see who is the owner and the admin members of the channel so that when I have an issue I know who to address.*
- Given: User is a part of the channel
- Then: User is able to see the details of the channel, including the list of members
- When: Viewing the list of members
- Then: User is able to see the members with special permissions or channel admin/owner authority

*As a course convener, I want to be able to appoint and remove admins so that if tutors were to change, I can update the channel appropriately.*
- Given: That the course convenor has an owner of slackr permission_id
- When: Owner wishes to see the list of owners/admins of a channel
- Then: There is an indicator saying who has what permissions
- When: The owner wishes remove admins
- Then: The owner can take away the position without removing the admin from the channel

*As a course convener, I want to be able to invite students to a channel in order to ensure that all students are a part of the channel and are receiving my updates*
- Given: Course convenor (CC) is a member of a private channel
- When: CC wishes to add students to the channel
- Then: Only using their u_ids, the user is added to the channel immediately

*As a student who is leaving a course, I want to be able to leave all the relevant channels so that I dont get spammed by irrelevant channels.*
- Given: Student is a part of a channel
- When: The student wishes to leave the channel
- Then: The student is removed from the members list and noo longer recieves updates on the channel

*As a student who wants to get involved in his subjects, I want to be able to join public channels that are related to my course so that we can form study groups.*
- Given: The student is motivated
- When: The student lists all the channels
- Then: All public channels are shown
- When: The student finds something he wants to join
- Then: He is able to check the details of the channel, including the name
- When: The student requests to join the channel he likes
- Then: The student is added immediatly 

*As a course convener, I want to be able to change the permission of members in specific channels. This is so that I can appoint admins who can help manage the channel for me.*
- Given: The course convener is an owner of a channel
- When: The owner can view the members of the channel
- Then: The owner can also view their permissions
- When: The owner changes the permissions of a member
- Then: The member is immediately removed from the members list and added onto the owner list

*As a course convenor, I want to be able to create different channels, so that there can be a public general course channel but also private channels that belong to tutors and are accessible only by the student’s of their tutorial.*
- Given: There needs to be a channel which students cant access
- When: A channel is created to be private
- Then: The channel cannot be joined or viewed by people not invited
- When: A channel is created to be public
- Then: The channel can be seen and joined by anyone

*As a potential owner, I want to be able to see all the members in the channel and readily identify who is an admin and who is a normal member so that I can address individuals in the correct manner.*
- Given: The course convener is an owner of a channel
- When: The owner can view the members of the channel
- Then: The owner can also view their permissions

### Message Stories
*As a user who doesn’t check Slackr often, I would like to have a way to start reading the conversation from my last unread message.*
- The user will access the channel normally.
- They should be able to view the most recent messages first as soon as they click on the channel.

*As a student I want to be able to see all the messages that have been sent in the particular channel, so I can review any announcements made by the lecturers.*
- The user will access the channel normally.
- The user should be able to see not just the recent messages but also be able to choose to view messages further in the past.
- This capability should be implemented by a button that return the next most recent batch of messages (50 at a time).

*As a user, I would like to be able to search through the messages with specific words.*
- The user should be able to search for a string.
- In response the user should be presented with all messages that contain that string.
- This should be done for all of the channels which the user is a member of.

### Miscellaneous Stories

*As a project manager, I want to be able to make a channel collect all messages for a 15 minute standup period and then after the period be released as system message. Used similar to agile planning*
- For every channel there should be an option to start a standup on the top bar.
- A standup can only be started if there is no standup currently taking place.
- Messages should't be allowed to be sent through during the standup so as not to interrupt the presenter.
- These messages (accumulated by all users) should instead be sent to the channel when the standup finishes
- A standup must last 15 minutes.
- A standup can't be started by a user not in the channel.

*As an owner, I would like to be able to modify permissions for certain groups/users allowing them to have particular permissions.*
- The slackr owner must have precedence over every other slackr member.
- The owner cannot be removed as owner of the slackr or as an owner from any channel.
- The owner can designate administrator roles to particular users, granting power to manage the server (however these admins cannot change the owner's permissions)

### User Profile Stories

*As a user, I would like to be able to view another user's profile such as their name and profile picture*
- A user should be able to see a list of users for each channel.
- Users must be able to view the profile of any of these users in the list
- On the selected user's profile page it should display basic information such as the name, handle and profile picture

*As a user, I would like to be able to edit my own profile information, including: my first name and last name and email.*
- There is a “Profile” button on the side bar.
- Upon clicking the button the user will be prompted to their profile page.
- Here they can view their own profile information and change certain fields such as their first and last names as well as the email address.

*As a user, I would like to be able to upload a profile picture*
- Also on the users profile page, they should be able to upload a profile picture using a URL that maps to an image

## Verification Assurance: Testing & Code Style
Software verification is more of an internal process and is concerned with whether the product is being built correctly. Our means of verification was white box testing, primarily the development and usage of unit tests to ensure that each piece of the software functions correctly individually. 

### Testing & Code Coverage
Unit testing is crucial to assuring the verification of the software because in order for integration testing and system testing to succeed, the individual functions and modules must themselves be functioning correctly.

Unfortunately in quite a few scenarios we found difficulties in implementing unit testing for functions for the following reasons (notable examples):
- Some functions had complicated functionality that relied on external entities. An example of this is the auth_passwordreset_request function. Sending emails is not a type of functionality that can be adequately tested.
- Some functions implemented timer based functionalities and so were too difficult to test reliably. For example, testing the sending of messages during a standup would required the test to run for the duration of the Timer (15 minutes) which would make the tests run too long (and potentially cause issues with the 1531 submission system).
- The use of persistent data storage made it hard to separate the testing of functions. During iteration 1 it was easy to set up a testing environment for a function and then perform the tests, but now because all of the set up is actually serialised and saved, this tends to cause clashes between the expected data available between functions.

However, we definitely ensured that we could extensively test where possible and try to maximise our code coverage. That said for use code coverage was used primarily as an indicator of the quality of the code we were developing. Code coverage could not serve as a "be all end all" metric due to our aforementioned issues with some tests being not completely possible (and thus particular branches of the code not being covered by unit tests).

### Code Style & Pylint
Pylint is a Python bug and quality checker. For our purposes, we use Pylint to tell us whether there are major issues with our code, but for the most part Pylint will point out a lot of style issues and demand that pythonic conventions be used. However, for this project we were less concerned with these really pedantic style demands because we had developed our own style guide and conventions which everyone was familiar with, and to drastically change that now is relatively redundant.

As a result, while Pylint gives an indicator of our general style, we chose to follow some different standards that deviate from PEP 8 (which Pylint enforces) which unfortunately results in a much lower Pylint score. However, we can still be assured of our software verification since we do have our own enforced style guide.

In an attempt to make the most from the Pylint tool, we chose to filter out and disable some Pylint criteria:
- missing-module-docstring (C0114): We opted to not use docstrings and stick with general comments
- missing-function-docstring (C0116): As above, we don’t use docstrings
- protected-access (W0212): We are using the underscore prefix to indicate constants rather than too show protected members of a class which PEP8 assumes
- global-statement (W0603): While Pylint discourages the use of global variables, it is fine to use when done so with precaution like we have done. We decided on the use of global variables all stored in a single file for easy data manipulation.
- unused-wildcard-import (W0614): We chose to use wildcard imports for code clarity purpose

So for our purposes we run Pylint with the command `pylint --disable=C0114,C0116,W0212,W0603,W0614 server/*`.
