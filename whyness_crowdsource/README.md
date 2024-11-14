# whyness_crowdsource

whyness_crowdsource is a whyness_django module for managing crowdsourcing

Contents
- Purpose
- Provides
- Depends
- API

## Purpose

Helping users understand themselves by enabling their peers to offer feedback on their stories

This module is divided into two aspects, users who offer their stories and recieve feedback,
and users who review and offer feedback on others' stories.

## Provides

Users must grant access and this record is kept in StoryGrant

All reviews have a Review record with a status of REVIEW_*

When allocated, a reviewer is assigned to review a set of stories and these are maintained in:

- ReviewReviewer
- ReviewStories

When review is complete, feedback is recorded in:
- ReviewFeedback
- ReviewSweetSpot

## Depends
Dependencies are:

- whyness_django AuthUser
- whyness_userfeedback SweetSpotValue
- whyness_userfeedback SweetSpotStrength
- whyness_userfeedback SweetSpotImpact
- whyness_userfeedback SweetSpotConfidence

## API

The following crowdsource endpoints are available

* api/v1/crowdsource/
* api/v1/crowdsource/story/grant/
* api/v1/crowdsource/story/reviews/
* api/v1/crowdsource/story/status/
* api/v1/crowdsource/story/stories/
* api/v1/crowdsource/story/start/
* api/v1/crowdsource/review/status/
* api/v1/crowdsource/review/start/
* api/v1/crowdsource/review/stories/
* api/v1/crowdsource/review/reject/
* api/v1/crowdsource/review/close/

Note: These api's require Authorization: bearer [token] to read or update any data

### api/v1/crowdsource/

The crowdsource namespace is divided into
user stories and peer reviews

### api/v1/crowdsource/story/grant/

Users must grant access before any crowdsource is available

GET returns the most recent status or false

```
{
    "is_granted": bool,
    "create_date": date
}
```
POST updates the users grant status

```
{
    "is_granted": bool
}
```

### api/v1/crowdsource/story/reviews/

GET returns all available reviews

```
[
    {
        "review":
    },
]
Or HTTP_400_BAD_REQUEST
{
    "error": "CROWDSOURCE_NO_REVIEWS"
}
```

### api/v1/crowdsource/story/status/

GET returns the status of the current request for review

```

{
    "status": true,
    "updated_date": date,
    "create_date": date,
},

Or HTTP_400_BAD_REQUEST
{
    "error": "CROWDSOURCE_REVIEW_NOT_OPEN"
}
```

### api/v1/crowdsource/story/stories/

GET returns the list of a users stories for review

```
[
    {
        "review",
        "story",
        "create_date",
    },
]
Or HTTP_400_BAD_REQUEST
{
    "error": "CROWDSOURCE_REVIEW_NOT_OPEN"
}
```

### api/v1/crowdsource/story/start/

POST opens a review, and identifies all stories

Errors:

- CROWDSOURCE_NOT_GRANTED - Permission must be granted before reviewing stories
- CROWDSOURCE_REVIEW_OPEN - Only one review can be open at a time
- NOT_ENOUGH_STORIES - More stories must be recorded to meet the minimum threshold

Return will be something like the following:
```
{
    "status": "NOT_STARTED",
    "error": ""
}

{
    "status": "STARTED"
}
```

### api/v1/crowdsource/review/status/

GET Status of the current review if any

Returns one of the following:
```
{
    "status": true,
    "updated_date": date,
    "create_date": date
}
Or HTTP_400_BAD_REQUEST
{
    "error": "CROWDSOURCE_REVIEW_NOT_OPEN"
}

```

### api/v1/crowdsource/review/start/

POST finds the highest priority review and allocates it to a reviewer

Returns:
```
{
    "status": "STARTED"
}
Or HTTP_400_BAD_REQUEST
{
    "status": "NOT_STARTED",
    "error": "CROWDSOURCE_REVIEW_OPEN"
}
```

### api/v1/crowdsource/review/stories/

GET Peer stories to be reviewed

```
[
    {
        "review",
        "story",
        "create_date",
    },
]
Or HTTP_400_BAD_REQUEST
{
    "error": "CROWDSOURCE_REVIEW_NOT_OPEN"
}
```
### api/v1/crowdsource/review/reject/

POST Reject a review

```
{
    "status": "REJECTED",
}
Or HTTP_400_BAD_REQUEST
{
    "status": "NOT_REJECTED",
    "error": "CROWDSOURCE_REVIEW_NOT_OPEN"
}
```

### api/v1/crowdsource/review/close/

POST a sweetspot review with feedback, then closes the review

```
{
    "sweetspot":
        {
            "review": value,
            "value1": value,
            "value2": value,
            "value3": value,
            "valueother": value,
            "valueconfidence": value,
            "strength1": value,
            "strength2": value,
            "strength3": value,
            "strengthother": value,
            "strengthconfidence": value,
            "impact1": value,
            "impact2": value,
            "impact3": value,
            "impactother": value,
            "impactconfidence": value,
            "create_date": value
        },
    "feedback":
        {
            "feedback": value
        }
}
```
