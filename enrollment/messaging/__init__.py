from os import getenv

account_sid = getenv('TWILIO_SID')
auth_token = getenv('TWILIO_TOKEN')
pin = getenv('SMS_PIN')
twilio_number = '+17472394729'  # TODO: get phone number from env
