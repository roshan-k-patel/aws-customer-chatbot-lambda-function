import time
import os
import logging
import googlesearch
from googlesearch import search


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def get_slots(intent_request):
    return intent_request['currentIntent']['slots']

def close(session_attributes, fulfillment_state, message, response_card):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message,
          "responseCard": response_card,
        }
    }
    return response

def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }

def backup_phone(intent_request):
    back_up_location = get_slots(intent_request)["BackupLocation"]
    phone_os = get_slots(intent_request)["PhoneType"]

    try:
        from googlesearch import search
    except ImportError:
        print("No module named 'google' found")

    # to search
    query = "How to back up {} to {}".format(phone_os, back_up_location)

    result_list = []
    for j in search(query, tld="com", num=5, stop=5, pause=2):
        result_list.append(j)

    return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'test'},
                 {'version': 1,
                     'contentType': 'application/vnd.amazonaws.card.generic',
                     'genericAttachments': [
                         {
                             'title': "Please select one of the options",
                             'subTitle': "{}".format(query),
                             "imageUrl": "https://image.shutterstock.com/image-illustration/this-apple-260nw-1204855174.jpg",
                             "attachmentLinkUrl": "https://www.asurion.com/",
                             'buttons': [
                                 {
                                     "text": "test",
                                     "value": "test"
                                 },
                             ]
                         }
                     ]
                 }
                 )


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug(
        'dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'BackupPhoneData':
        return backup_phone(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')


""" --- Main handler --- """


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)

