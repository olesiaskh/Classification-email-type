# Email Classification

## What is it about?
This projects creates a multi-class classification of emails based on their metadata. 

## What data was used?
Two separate data files were used - one for training, one for testing. Each included the following information about emails:
* __date__ - unix style date format, date-time on which the email was received
* __org__ - organisation of the sender
* __tld__ - top level domain of the organisation
* __ccs__ - number of emails cced with this email
* __bcced__ - is the receiver bcc'd in the email; can take two values 0 or 1
* __mail_type__ - type of the mail body
* __images__ - number of images in the mail body
* __urls__ - number of urls in the mail body
* __salutations__ - is salutation used in the email; can take two values 0 or 1
* __designation__ - is designation of the sender mentioned in the email; can take two values 0 or 1
* __chars_in_subject__ - number of characters in the mail subject
* __chars_in_body__ - number of characters in the mail body
* __label__ (only in train data) - label of this email; eight classes are 'Updates', 'Personal', ‘Promotions’, 'Forums', 'Purchases', 'Travel', 'Spam', and ‘Social’ (class ids start from 0 to 7)

## What is included in the code?
The code consists of two parts. 
1. __Jupyter notebook__ - data exploratorion, aims to describe the data used (including data quality, attribute types and values).
2. __Python files__ - the model and support functions in separate files.

The code is designed to be flexible - steps can be included or omitted as needed in the master code.
