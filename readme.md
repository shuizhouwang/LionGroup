We aim to develop an interactive web application for Columbia students to group together for different types of events. The motivation of this project initially comes from our brainstorming meeting when one teammate mentioned the need to group together at night to walk back home together for safety.

Function reviews:

1. User Interface

– Register: Nickname, email address, profile picture, password, and a brief self-introduction are required when registering for a new account
 
– Login: Correct password and the unique user ID provided automatically after registering successfully are required.

– Update User Profile: Any items filled in when registering for the account can be modified and updated in profile.

2. User Activity

– Create event: After logging in successfully, the user can create event of type ”Eat”, ”Study” or ”Home” by filling in the event description, event time, event image and event type.

– Browse Event: The user can browse the available events created by other users either by clicking on certain category (one the the three), or by going through all the events without specifying a certain type limit.

– Join Event:   The user can join any event created by other users.

– Search Event: The user can search for events by typing a keyword or key phrase to find out events whose event description containing that keyword or key phrase.

3. Notification Service

– Confirmation Subscription email: An email notification would be sent out using SES and SNS to the newly registered user for subscription conformation.

– Learning based Reminder Message: An email reminder will be sent to the user if this user’s event (event description) history contains negative mood too often which might suggest that this user is under too much pressure.

4. Developer Perspective

– Error Detection:
   ∗ User Log in:When the combination of password and user ID does not fit in any record in database, an error page will show up and user has to type in password again.
   ∗ Event Time: When the end time is earlier than the start time, the event cannot be created (posted), and an error page will show up.

– Database Manipulation: The mongoDB has two collections for this web application. One is to store user item and the other is to store event item. To keep the browser page clean, the developer will refresh the event collection every few days so that the event history of user and the discover page for browsing events will not looks too lengthy thus interfering user’s efficiency of searching events.

Tools:
1. Web APP Framework - Flask
- Frontend: HTML, JavaScrpit in Frontend layer

- Backend: Python in Router Layer, Logic layer, and database layer 
2. Developer Tool
- Pycharm: This IDE was utilized so that teammates can code and commit the modification easily without actually siting together. The commit screenshot can be seen in Appendix.

- Github: Every modification was committed and pushed onto our mutual private repository during the development process.
3. AWS Service

- EC2 Mongo: MongoDB was used in this project due to its NoSQL feature, which makes it relatively easy to search, add, delete and modify item content.

- ElasticSearch: This service is used to store all the events created by users so that users can search events by keywords.

- SES, SNS: These services are used for sending email notification when necessary.

- AWS CLI: This terminal plugin was installed for monitor the mongoDB on EC2 as developer.
4. Machine Learning
- AWS Comprehend: This machine learning API is used to analyze the text composed by all the event description written by a user to detect the mood of this user.

