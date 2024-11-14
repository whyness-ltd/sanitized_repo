# whyness_joblisting

whyness_joblisting is a whyness_django module for managing job listings

Contents
- Purpose
- Provides
- Depends
- API

## Purpose

Provide and manage jobs

## Provides

A list of jobs for users

## Depends

Dependencies are:

- whyness_django AuthUser
- whyness_userfeedback SweetSpotValue
- whyness_userfeedback SweetSpotStrength
- whyness_userfeedback SweetSpotImpact

## API

Joblistings

* api/v1/joblist/
* api/v1/joblist/STATUS/
* api/v1/joblist/id/

Note: These api's require Authorization: bearer [token] to read or update any data

* api/v1/joblist/
* api/v1/joblist/STATUS/

GET returns a list of jobs available for a user

If filtering by status, use any of the following:

* UNSEEN
* SEEN
* LIKED
* REJECTED
* APPLIED

If an invalid filter is supplied, no filtering will apply and records will be
returned as normal.

```
[
{
    'id': number,
    'job_id': string,
    'company_id': string,
    'company': string,
    'company_website': string,
    'logo': string,
    'title': string,
    'country': string,
    'location': string,
    'job_type': string,
    'job_link': string,
    'status': string
}
]
```
An example
```
[
{
    'id': 1,
    'job_id': 'ax-z2',
    'company_id': 5,
    'company': 'Microsoft',
    'company_website': 'https://REMOVED
    'title': 'Software engineering',
    'logo': 'https://REMOVED
    'jobtype': 'Hybrid',
    'joblink': 'https://REMOVED
    'status': 'UNSEEN'
},
{
    'id': 2,
    'job_id': '',
    'company_id': 3,
    'company': 'GCHQ',
    'title': 'Data Science Researcher',
    'logo': 'https://REMOVED
    'jobtype': 'Hybrid',
    'joblink': 'https://REMOVED
    'status': 'UNSEEN'
}
]

```

* api/v1/joblist/2/

GET returns the job listing

```
{
    'id': number,
    'job_id': string,
    'company_id': number,
    'company': string,
    'company_website': string,
    'logo': string,
    'title': string,
    'industry': string,
    'location': string,
    'country': string,
    'job_type': string,
    'usp': string,
    'values1': string,
    'values2': string,
    'values3': string,
    'values4': string,
    'values5': string,
    'ssvalues1': string,
    'ssvalues2': string,
    'ssvalues3': string,
    'ssvalues4': string,
    'ssvalues5': string,
    'strength1': string,
    'strength2': string,
    'strength3': string,
    'impact1': string,
    'impact2': string,
    'impact3': string,
    'skills': string,
    'development': string,
    'culture': string,
    'edi_score': string,
    'glassdoor_rating': string,
    'job_link': string,
    'eligibility': string,
    'status': string,
    'create_date': string
    }
```

An example
```
{
    'id': 1,
    'job_id': '',
    'company_id': 3,
    'company': 'GCHQ',
    'company_website': 'https://REMOVED',
    'company_overview': 'We’re the Government Communications Headquarters – otherwise known as GCHQ. Tasked by UK government, we’re a world-leading intelligence, cyber and security agency. Our mission is to keep the UK and its citizens safe. We're really proud of our purpose - and our people.',
    'industry': 'Public Sector',
    'logo': 'https://REMOVED
    'title': 'Data Science Researcher',
    'country': 'UK',
    'location': 'Manchester',
    'job_type': 'Hybrid',
    'usp': 'Work alongside world class professionals to tackle complex, interesting, mission-critical real world problems that you just won’t find anywhere else.',
    'company_values1': 'Diversity',
    'company_values2': 'Collaboration',
    'company_values3': 'Innovation',
    'company_values4': 'Data-driven',
    'company_values5': 'Fairness',
    'ssvalues1': 'Togetherness',
    'ssvalues2': 'Futuristic',
    'ssvalues3': 'Belonging',
    'ssvalues4': 'Curiosity',
    'ssvalues5': 'Security',
    'strength1': 'Analytical',
    'strength2': 'Risk Management',
    'strength3': 'Attention-to-detail',
    'strength4': 'Research',
    'strength5': 'Positivity',
    'impact1': 'International Safety & Security',
    'impact2': 'Justice',
    'impact3': 'Public Service',
    'skills': '<ul><li>AI/ML or data science experience in a research capacity.</li>
<li>Proficiency with Python and common data science libraries, e.g. PyTorch</li></ul>',
    'development': '<p>We’ll invest in your skills and the way you like to learn, from books, study, courses, and conferences to stretching work with support of the team.</p>
<p>We’ll support and encourage you, helping you to master the art of software and become part of our world-class engineering team</p>',
    'culture': '<p>As part of our team, you’ll discover an inclusive workplace that’s welcoming, supportive and encouraging. You’ll be part of an organisation where people want to support one another and make a difference. Aside from fostering an open culture, we’ve got a range of growing affinity groups.</p>
<ul><li>Ethnic Minority and gender equality networks.</li>
<li>Groups supporting wellbeing, mental health, neurodiversity, and disability.</li>
<li>Faith/No Faith communities for staff to come together.</li>
<li>LGBTQ+ support networks.</li></ul>
<p>You’ll also find a variety of sports, activity, interest, and social groups to help you settle in and connect with people with similar interests.</p>
<p>Before You Apply to work at GCHQ, you need to be a British citizen. We do have a strict drugs policy, so once you start your application, you can’t take any recreational drugs and you’ll need to declare your previous drug usage at the relevant stage.</p>
<p>Honesty and integrity are really important if you want to work at GCHQ. Take some time to read about the vetting process and make sure you meet the criteria in the vetting pages of the ‘How to Apply’ section. The process can take some time, but this is just because it’s thorough. Giving misleading information and omitting or concealing information during the recruitment and vetting process is viewed very seriously.</p>
<p>The role is based in Cheltenham or Manchester, so you’ll need to live within a commutable distance of these locations. Please consider any financial implications and practicalities before applying.</p>
<p>Please note, you should only launch your application from within the UK. If you are based overseas, you should wait until you visit the UK to launch an application. Applying from outside the UK will impact on our ability to progress your application.</p>',
    'edi_score': '10',
    'glassdoor_rating': '3.4',
    'job_link': 'https://REMOVED
    'eligibility': '<p>To work in this role, you will need the highest security clearance, known as Developed Vetting (DV). It’s something everyone in the UK Intelligence Community must go through and it can take some time.</p>
<p>You must be a British Citizen. One of your parents must be a British Citizen or must have the nationality or citizenship from our approved list of countries here. If you hold dual nationality, of which one component is British, you will nonetheless be considered. (for more info link here). Candidates must normally have been resident in the UK for seven out of the last ten years. This is particularly important if you were born outside the UK. You can apply at the age of 17 years and 6 months, if successful you will not be offered a start date prior to your 18th birthday. Discretion is vital. You should not discuss your application, other than with your partner or a close family member. Please note, you should only launch your application from within the UK. If you are based overseas, you should wait until you visit the UK to launch an application. Applying from outside of the UK will impact on our ability to progress your application. Further information on our eligibility criteria can be found on the Applying section.</p>',
    'status': 'UNSEEN'
    'create_date': '2022-09-02 0:0:00'
    }
```

* api/v1/joblist/2/

PUT updates the job status for a user

Status can be one of the following:

* UNSEEN
* SEEN
* LIKED
* REJECTED
* APPLIED

```
{
    'status': string
}
```
An example
```
{
    'status': 'SEEN'
}
```
