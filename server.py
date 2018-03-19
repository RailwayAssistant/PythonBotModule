from flask import Flask, request
import logging
from logging.handlers import RotatingFileHandler
import requests
import bot
import os

application = Flask(__name__)

API_KEY = os.environ.get('RAAPIKEY')

def related_to_railway(response):
    response = response.lower()
    if 'pnr' in response:
        PNR = ''
        for x in response.split():
            if x.isnumeric() and len(x) == 10:
                PNR = x
                break
        if PNR:
            url = 'https://api.railwayapi.com/v2/pnr-status/pnr/{}/apikey/{}/'.format(PNR, API_KEY)
            response =  requests.get(url)
            if response.status_code != 200:
                return 'Cannot contact my guys in railway, please remind me later.'
            else:
                try:
                    response = response.json()
                    details_to_return = []
                    passengers = response['passengers']
                    details_to_return.append("Here I have details of " + str(len(passengers)) + " passenger{}".format("s." if (len(passengers) - 1) else "."))
                    for x in passengers:
                        details_to_return.append("Passenger no "+ str(x["no"]) + "'s current status is "+ x['current_status'] + ", it was "+ x['booking_status'] + " at the time of booking.")
                    from_station = response["from_station"]["name"]
                    to_station = response["to_station"]["name"]
                    details_to_return.append("Train the PNR refers to is "+ response["train"]["name"] + ". It'll run from "+ response["from_station"]["name"] + " to " + response["to_station"]["name"])
                    details_to_return.append("Make sure you board on "+ response["boarding_point"]["name"] + " on " + response["doj"]+ ".")
                    return ' '.join(details_to_return)
                except Exception as e:
                    application.logger.error(e)
                    return 'Please provide a valid PNR also with your question.'

        else:
            return 'Please provide a valid PNR also with your question.'
    return False

def get_appropriate_response(response):
    railway_response = related_to_railway(response)
    if railway_response:
        return railway_response
    else:
        return bot.bot.get_response(response).serialize()['text']

@application.route("/", methods=['POST', 'GET'])
def hello():
    try:
        response = request.args.get('q')
    except:
        response = None
    if response:
        return get_appropriate_response(response)
    else:
        return 'Cannot understand that, maybe I need more training'

if __name__ == "__main__":
    handler = RotatingFileHandler('flask.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    application.logger.addHandler(handler)
    application.run(host='0.0.0.0')
