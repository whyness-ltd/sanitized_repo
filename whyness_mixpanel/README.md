# whyness_mixpanel

whyness_mixpanel integrates Mixpanel into Whyness

User activity creates many events, these are logged in the database. Mixpanel
integration sends these events to mixpanel for reporting and analysis.

Contents
- API
- Configuration
- Roadmap
- Links

## API

There are two models, a virtual one Event to package and send events to
Mixpanel, and a real one Log to capture errors when submission fails.

Events comprise:
- insert_id - to identify the event
- event - the name of the event as identified in whyness_django.TrackerItem
- user - identifies the user who performed the event
- ip - internet address of the user
- useragent - identify the mobile
- data - typically GET, PUT and POST
- time - moment the event happened

The event model has two functions, json() to return the event as a json
string and send() to send a single event to Mixpanel.

As there are two types of users, registered users (AuthUser) of the app and
prospects (whyness_crm.Contact), the Whyness django app stores events in a
number of tables,

- whyness_django.TrackerLog - app activity
- whyness_crm.AuthUserTrackerClick - app user communications
- whyness_crm.ContactTrackerClick - prospect communications

When events are logged, they are also sent to Mixpanel. After refactoring,
this will be replaced by a queue runner batch process, see Roadmap.

Mixpanel is referenced in whyness_django.tracker_log, and the whyness_crm.goto.

## Configuration

### MIXPANEL_PROJECT_ID
This is set to 2780485

### Service username and password
These are set via environment variables

- MIXPANEL_SERVICE_ACCOUNT
- MIXPANEL_SERVICE_PASSWORD

## Roadmap

As volume is currently low, it makes sense to maintain simplicity and send
events as they happen.

As volume increases, throughput would be higher with lower latency by
batching submissions to Mixpanel.

At very high volumes, send batches using 10-20 concurrent clients.

It may be useful to add a dictionary argument allowing for additional ad-hoc
data.

## Links

- https://REMOVED
- https://REMOVED
- https://REMOVED
