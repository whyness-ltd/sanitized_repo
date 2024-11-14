[![https://REMOVED](https://REMOVED whyness_django is the Django frontend and API server for Whyness

Contents
- Build notes
- API documentation
- Links
## Build Notes

### Files
Dockerfile is used for creating a docker image and is annotated.

Django can run a local server with manage.py runserver and will also serve
local static files, this is useful for development, but should not be used
in production. It is commented out if you wish to use it locally.

manage.py is used to manage and run the Django application
```
python3 manage.py
```
**Directory**
* whyness_django - The Django application;
* templates - Templates used to render the application;
* static - Static image and javascript files used by the application,
during development they can be served by manage.py runserver, but should
be served separately in production.

To reduce the effort to maintain this app, only Django version 3.2 is supported, others
may work, YMMV.

Apache is preferred to serve the application in production,
it is also used for serving static files including javascript, css and images.

### Docker commands

Two build scripts are available, build.sh for building and uploading the main docker image
and build-runner.sh for building and running the queue runner

### Build an image
```
cd ~/whyness_django
sudo docker build --tag whyness_django .
```

on Macbooks:
```
sudo docker buildx build . --platform=linux/amd64 -t whyness_django .
```

### Create a container

If you don't name the container, docker will generate a random one for you.

The Following environment variables must be set:

* BUILD_CONFIG	PROD/DEV
* AWS_DEFAULT_REGION
* AWS_REGION_NAME
* DJANGO_SECRET_KEY
* EMAIL_HOST
* EMAIL_HOST_PASSWORD
* EMAIL_HOST_USER
* EMAIL_PORT
* RDS_DB_NAME
* RDS_HOSTNAME
* RDS_PASSWORD (optional - if not set it will try to get it for the environment from Parameter store)
* RDS_PORT
* RDS_USERNAME

The environment variables may be set in a file and passed in during the container start. Example:

Create environment variables file:
```
touch env.list
```

Fill in the file with content as above:
```
BUILD_CONFIG=
EMAIL_HOST=
RDS_DB_NAME=
DJANGO_SECRET_KEY = "REMOVED"
etc
```

Create docker container with environment files
```
sudo docker container create -p 8000:8000 --name whyness_django --env-file env.list whyness_django
```

### AWS Configuration 

The application uses the `boto3` python library and therefore uses the credential initialisation patterns from boto. See docs here:

This can be via the config files of the AWS CLI which boto loads automatically and other methods including setting the following environment variables:

* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY

For docker configuration the credentials on the host system are mounted, in AWS the IAM role for the service running the application is used.


### List all containers
```
sudo docker ps -a
```

### Start and stop a container
```
sudo docker container start [CONTAINER ID]
sudo docker container stop [CONTAINER ID]

# docker run can be used to create and start a container
sudo docker container run -p 8000:8000 --name whyness_django --env-file env.list -v $HOME/.aws/credentials:/home/app/.aws/credentials:ro whyness_django

```

### Connect
Connect to the Django website using your favourite browser
```
http://IP.REMOVED:8000/
```

## Notes

List all docker images:
```
$ sudo docker image ls -a
```

List all docker containers:
```
$ sudo docker container ls -a
```

Information about a container including the location of container files
```
sudo docker container inspect [CONTAINER ID]
```

It's important to remove images and containers that are no longer required.
If an image fails to build it's important to remove the failed build, they
can be identified with <none> in the repository and tag for example:
```
$ sudo docker image ls -a
REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
<none>       <none>    c5c63f978c91   45 hours ago   948MB
```

To remove image c5c63f978c91:
```
sudo docker rmi 2d886365108e
```

To see a list of containers that may prevent deleting an image
```
$ sudo docker container ls -a
CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS                       PORTS     NAMES
68bca922bc72   59976f711c0c   "/bin/sh -c 'pip ins…"   45 hours ago    Exited (127) 45 hours ago              eager_chatelet
```

To remove container 68bca922bc72:
```
sudo docker rm 68bca922bc72
```
Connecting to AWS services such as S3, Transcribe, requires setting the environment variables
  AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY

env.sh extracts aws credentials and shows how to set them.

Parse amazon credentials file:
```
./env.sh path/to/name.csv
```


## DEPLOYMENT TO AWS

- Deployed using App runner service
- Two services need to be running - Main App (core API and services), and the Queue Runner (Periodically checks for new audio files to transcribe and status of transcriptions). The queue runner needs to be optimised and improved.
- Environment variables need to be setup in the configuration, however AWS uses service roles for accessing other resources
- Stack was deployed manually so infrastructure as code templates are not available. However the stack uses only 3-4 key services in addition to IAM


## API

The Whyness API is built using https://REMOVED has a web browsable API, and supports JSON and XML.

The following API endpoints are available
* api/version/
* api/v1/media/
* api/v1/media/id/
* api/v1/question/
* api/v1/question/id/
* api/v1/role/
* api/v1/role/id/
* api/v1/profession/
* api/v1/profession/id/
* api/v1/typeattributes/
* api/v1/typeattributes/id/
* api/v1/typeattributes/id/roles/
* api/v1/prospect/
* api/v1/prospect/id|email/
* api/v1/agpoll/dreamjob/
* api/v1/agpoll/sweetspotvalues/
* api/v1/agpoll/sweetspotstrengths/
* api/v1/agpoll/sweetspotimpacts/
* api/v1/agpoll/sweetspot/
* api/v1/user/
* api/v1/user/feedback/
* api/v1/user/profile/
* api/v1/user/reset_password/
* api/v1/user/status/
* api/v1/crowdsource/ for details see whyness_crowdsource

Note: These api's require Authorization: bearer [token] to upload or access user data

### api/version/

Verb: GET

Returns a JSON object with version information

```
[
    {
        "major":1,
        "minor":0,
        "revision":1,
        "version":"1.0.1-prod",
        "production":true,
    }
```

### api/v1/question/

Verb: GET

Returns a JSON array of questions ordered by sort_order

* id: internal reference number
* question: A question for the user
* sort_order: The order number to be optionally shown to the user
* status: Either 0 Inactive or 1 Active`

NOTE: Only active questions will be shown

Example:
```
[
    {
        "id":9,
        "question":"What was your favourite thing to do as a child?",
        "sort_order":1,
        "status":1
    },
    {
        "id":10,
        "question":"What is your earliest joyful childhood memory?",
        "sort_order":2,
        "status":1
    },
    ...
    {
        "id":19,
        "question":"How would you like to be remembered?",
        "sort_order":11,
        "status":1
    }
]
```

### api/v1/question/id/

Verb: GET

Returns the question as JSON

Example:
```
{
    "id":9,
    "question":"What was your favourite thing to do as a child?",
    "sort_order":1,
    "status":1
}
```

### api/v1/{role,profession,typeattributes}/

Verb: GET

Returns a list of role, profession or typeattributes

### api/v1/typeattributes/id/roles/

Verb: GET

Returns a list of roles for a typeattribute

### api/v1/{role,profession,typeattributes}/id/

Verb: GET

Returns a role, profession or typeattributes

### api/v1/media/

Verb: GET

Returns a list of audio uploads as JSON

NOTE:
This API currently returns all available media and will change to only show the user's media and omit the media link to S3

Example:
```
[
    {
        "id":22,
        "media":"https://REMOVED
        "status":1
    },
    {
        "id":21,
        "media":"https://REMOVED
        "status":1
    },
    ...
    {
        "id":2,
        "media":"https://REMOVED
        "status":1
    }
]
```

### api/v1/media/

Verb: PUT

The put request should contain JSON / form application/x-www-form-urlencoded
with the recorded audio file

```
{
    'question': <id>
    'media': 'encoded file'
}
```

If successfully uploaded, a request to transcribe the file is submitted

Returns the uploaded media as JSON

```
{
    'id': 1,
    'question': 1,
    'status': 1
}
```

Use the returned id to request the status of the upload

NOTE: This currently returns all media and will change to only the user's media

### api/v1/media/id/

Verb: GET

Returns as JSON

Returns the specified audio as JSON

```
{
    "id":58,
    "question":10,
    "transcript":"Good morning.",
    "status":4
}
```

Each call to GET checks the status of the media transcription and if in progress
checks the transcription job and if ready fetches the result and stores the transcription.

NOTE:
This API currently returns any media and will change to only show the user's media and omit the media link to S3

The status can be any of the following:

```
TRANSCRIPT_STATUS_INACTIVE = 0
TRANSCRIPT_STATUS_ACTIVE = 1
A media file has been uploaded to S3
TRANSCRIPT_STATUS_SENT_FOR_TRANSCRIPTION = 2
The link to the S3 media has been sent (queued) for transcription
TRANSCRIPT_STATUS_IN_PROGRESS = 3
The transcription is in progress
TRANSCRIPT_STATUS_TRANSCRIBED = 4
The transcription succeeded
TRANSCRIPT_STATUS_TRANSCRIBE_FAILED = 5
The transcription failed
TRANSCRIPT_STATUS_NEEDS_CONVERTING = 7
Send transcription for processing
TRANSCRIPT_STATUS_DELETED = 8
The media and transcription is marked for deletion
TRANSCRIPT_STATUS_ERROR = 9
There was an error
```

### api/v1/prospect/

Returns a JSON array of prospects

* id: internal reference number
* name: Name
* email: Email

Example:
```
[
    {
        "id":1,
        "name":"Alan Hicks",
        "email":'email@REMOVED',
    },
    ...
    {
        "id":2,
        "name":"Alan Hicks",
        "email":'email@REMOVED',
    }
]
```

### api/v1/prospect/id|email/

Verb: GET

Returns as JSON

Returns the specified prospect as JSON, for example https://REMOVED

```
{
        "id":1,
        "name":"Alan Hicks",
        "email":'email@REMOVED',
}
```

Verb: PUT

Adds a new prospect

Verb: DELETE

Deletes an existing prospect

### api/v1/agpoll/dreamjob/

Verb: GET, PUT, POST

Requires: Bearer token authorization

Returns as JSON

GET returns an array of all dream job polls for a user
PUT/POST Stores the submitted poll

```
{
    "role1": "",
    "role2": "",
    "role3": "",
    "roleother": "",
    "roleconfidence": "",
    "profession1": "",
    "profession2": "",
    "profession3": "",
    "professionother": "",
    "professionconfidence": "",
    "company_size": "",
    "office_culture": ""
}
```

### api/v1/agpoll/sweetspotvalues/
### api/v1/agpoll/sweetspotstrengths/
### api/v1/agpoll/sweetspotimpacts/

Verb: GET

Returns as JSON

Returns an array of all sweet spot values

```
[{
    "id": 1,
    "title": "Don't know"
}]
```

PUT Stores the submitted poll

### api/v1/agpoll/sweetspot/

Verb: POST

When POSTing a new sweetspot, use the id from
api/v1/agpoll/{sweetspotvalues,sweetspotstrengths,sweetspotimpacts}/

Returns as JSON

Returns the sweet spot poll

```
{
    "value1": 0,
    "value2": 0,
    "value3": 0,
    "value4": 0,
    "value5": 0,
    "valueother": "",
    "valueconfidence": "",
    "strength1": 0,
    "strength2": 0,
    "strength3": 0,
    "strength4": 0,
    "strength5": 0,
    "strengthother": "",
    "strengthconfidence": "",
    "impact1": 0,
    "impact2": 0,
    "impact3": 0,
    "impact4": 0,
    "impact5": 0,
    "impactother": "",
    "impactconfidence": ""
}
```

### api/v1/agpoll/sweetspot/id/

Verb: GET

Returns the sweet spot poll identified by id

Returns as JSON

Verb: PUT

Replaces the poll identified by id and returns the sweet spot poll

Returns as JSON

```
{
    "id": 1,
    "user": "",
    "value1": 1,
    "value2": 1,
    "value3": 1,,
    "value4": 1,,
    "value5": 1,
    "valueother": "",
    "valueconfidence": "",
    "strength1": 1,
    "strength2": 1,
    "strength3": 1,
    "strength4": 1,
    "strength5": 1,
    "strengthother": "",
    "strengthconfidence": "",
    "impact1": 1,
    "impact2": 1,
    "impact3": 1,
    "impact4": 1,
    "impact5": 1,
    "impactother": "",
    "impactconfidence": "",
    "create_date": ""
}
```

### api/v1/user/

Verb: GET PUT

Requires Authorization Bearer token

Returns user's name, xref and email or sets the user's name

When an authentication token provides this information
it will automatically update their record
so the user can't change their email address.

Returns as JSON

```
{
  "name": "",
  "xref": "",
  "email": ""
}
```

### api/v1/user/feedback/

Verb: GET

Requires Authorization Bearer token

Returns feedback from users

Returns as JSON

```
{
    "values":[
        {
            "value":"Don't know",
            "value_count":3
        }
    ],
    "strengths":[
        {
            "strength":"Don't know",
            "strength_count":3
        }
    ],
    "impacts":[
        {
            "impact":"Don't know",
            "impact_count":3
        }
    ],
    "confidence":[
        {
            "valueconfidence":"Agree",
            "valueconfidence_count":1,
            "strengthconfidence":"Agree",
            "strengthconfidence_count":1,
            "impactconfidence":"Agree",
            "impactconfidence_count":1
        }
    ]
}
```

### api/v1/user/profile/

Verb: GET

Requires Authorization Bearer token

Returns the user's profile

Returns as JSON

```
{
  "representational_system":{
    "visual":12,
    "auditory":5,
    "kinesthetic":1,
    "auditory_digital":4
  }
}
```

### api/v1/user/reset_password/

Verb: POST

Posting the user's email returns the users email in confirmation

Returns as JSON

```
{
  "email": "email@REMOVED"
}
```

### api/v1/user/status/

Verb: GET

Requires Authorization Bearer token

Returns the user's status

Returns as JSON

```
{
    "sweetspot_completed":true,
    "dreamjob_completed":true
}
```

### api/v1/crowdsource/

The crowdsource namespace is divided into
user stories and peer reviews

Please see whyness_crowdsource for details


## Links

* [Django](https://REMOVED
* [Docker](https://REMOVED
* [Slab](https://REMOVED
