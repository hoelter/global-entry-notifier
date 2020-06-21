import datetime
import logging
import os
import azure.functions as func
import requests
from twilio.rest import Client

# LOCATION_CODE = '6840' # Minneapolis
LOCATION_CODE = '7740' # Milwaukee
GLOBAL_ENTRY_URL = f'https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&limit=3&locationId={LOCATION_CODE}&minimum=1'

def main(mytimer: func.TimerRequest) -> None:
    try:
        data = requests.get(GLOBAL_ENTRY_URL).json()

        if not data:
            logging.warning('No response found')
            return

        dates = []
        for o in data:
            if o['active']:
                dt = o['startTimestamp']
                dtp = datetime.datetime.strptime(dt, '%Y-%m-%dT%H:%M')
                dates.append(dtp.strftime('%A, %B %d @ %I:%M%p'))

        if not dates:
            logging.info('No active dates found')
            return

        message = f'{len(dates)} new Milwaukee global entry appointment available, the earliest on {dates[0]}'

        logging.info(f'Sending message: {message}')

        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        client = Client(account_sid, auth_token)
        sentMessage = client.messages.create(body=message, to=os.environ['TARGET_NUMBER'], from_=os.environ['TWILIO_NUMBER'])

        logging.info(f'Message sent: {sentMessage}')

    except:
        logging.error('Something went wrong.')
