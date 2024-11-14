# Whyness CRM

Managing communications with Registered and prospective users.

The CRM dashboard is where you can monitor and create new activities.

The default view shows the first 200 prospective and current users.

## Workflow

First choose a dataset such as all active prospects or all active users.

If you wish to test/filter against a previous message choose a test message. Leave as "Choose message" to send to all recipients.

If you wish to test against the message "Thank you for downloading our app" you can choose to send your message to:

- Everyone;
- Only those who have received this message;
- Only those who have not received this message.

There is a similar test/filter for trackers, for example anyone who has, or has not clicked to see the "Whyness demo".

Then choose the message to send, for example "Thank you for taking the first steps in your self discovery journey".

It's essential to test emails before sending them to your target audience, and there is a "Send to me" button to send the email to your registered email address.

### Things to notice:

- When choosing a message, its description is displayed after the title;
- After choosing messages to test and send, the number of messages that will be sent is listed together with the first few emails.

After you have checked the test message sent to yourself, click "Send to all" button to send the message to everyone in the list.

## Users

Registered users are in the main Whyness_django module - Auth users.

Prospective users is in this CRM module - Contacts.

## Messages

Messages are the core purpose of this CRM module.

When you create a new message:

- Title will be used as the email subject;
- Description is a short paragraph to help you identify the email when you choose it in the dashboard;
- From user is the account the message will be sent from;
- Message is the message to be sent to users;
- Email should be clicked as this is currently the only message type supported.

### Links and names

To include a link to be tracked, use one of the following:

- To insert a clickable link {% crm_link "https://REMOVED %}
- To insert a clickable link with a title {% crm_link "https://REMOVED "title" %}

A clickable link {% crm_link "https://REMOVED %} will be rendered as a link with the url.

A clickable link with a title will use a more friendly form with the title instead of the url.

If the URL is new it will be saved in "Tracker destinations".

## Sending messages

When messages are sent, the event will be recorded for both current users and prospective contacts. Currently messages sent are only listed with prospective contacts.

If there are any trackers included in a message, each message will be personalised with a clickable link to check when a current users or prospective contact has clicked their link.

## Trackers

These are automatically created when a message includes a link as described above. You may wish to change the Title to better reflect the url.

## User SQLs - Datasets

User SQLs create datasets. Because Prospects and Registered users are separate you need to create a SQL query for one or the other.

The Query is divided into two parts, first the SELECT, this must use alias prefixes and be the id, name and email, for example:

```
SELECT c.id, c.name, c.email
```

Second is the FROM and WHERE part where tables and filters are included:

```
FROM whyness_crm_contact AS c
WHERE c.is_prospect = TRUE
AND c.status = 1
AND c.use_email = TRUE
```

## Reports

There are a number of bespoke reports:

- App aggregate
- User status
- User stories
- User stories/week
- User transcript readers per week
- User AI analysis
- Trackers

## Database views

A number of views have been created to facilitate querying the database:

- whyness_crm_contact_view
- whyness_crm_user_view
- whyness_crm_contact_tracker_view
- whyness_crm_user_tracker_view
