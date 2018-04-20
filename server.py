from flask import Flask, request
import logging
from logging.handlers import RotatingFileHandler
import requests
import bot
import os

application = Flask(__name__)

#API_KEY = os.environ.get('RAAPIKEY')

# Sample Dates
YDate = '19-04-2018'
TDate = '20-04-2018'
TMDate = '21-04-2018'

def related_to_railway(response):
    response = response.lower()
    if 'pnr' in response:
        if response[0:4] != 'pnr/':
            PNR = ''
            for x in response.split():
                if x.isnumeric() and len(x) == 10:
                    PNR = x
                    break
        else:
            PNR = response[4:]
        if PNR:
            url = 'https://api.railwayapi.com/v2/pnr-status/pnr/{}/apikey/{}/'.format(PNR, API_KEY)
            response =  requests.get(url)
            if response.status_code != 200:
                return 'Cannot contact my guys in railway, please remind me later.'
            else:
                try:
                    response = response.json()
                    if response['response_code'] == 200:
                        details_to_return = []
                        passengers = response['passengers']
                        details_to_return.append("Here I have details of " + str(len(passengers)) + " passenger{}".format("s." if (len(passengers) - 1) else "."))
                        for x in passengers:
                            details_to_return.append("Passenger no "+ str(x["no"]) + "'s current status is "+ x['current_status'] + ", it was "+ x['booking_status'] + " at the time of booking.")
                        details_to_return.append("Train the PNR refers to is "+ response["train"]["name"] + ". It'll run from "+ response["from_station"]["name"] + " to " + response["to_station"]["name"])
                        details_to_return.append("Make sure you board on "+ response["boarding_point"]["name"] + " on " + response["doj"]+ ".")
                        return ' '.join(details_to_return)
                    else:
                        return 'Please provide a valid PNR also with your question.'
                except Exception as e:
                    application.logger.error(e)
                    return 'Please provide a valid PNR also with your question.'

        else:
            return 'Please provide a valid PNR also with your question.'
    elif 'cancelled' in response or response[0:2] == 'c/':
        if response[0:2] != 'c/':
            if 'yesterday' in response:
                DATE = YDate
            elif 'today' in response:
                DATE = TDate
            elif 'tomorrow' in response:
                DATE = TMDate
            else:
                return 'Please ask for either Yesterday, Today or Tommorow.'
        else:
            DATE = response[2:]
        url = 'https://api.railwayapi.com/v2/cancelled/date/{}/apikey/{}/'.format(DATE, API_KEY)
        response =  requests.get(url)
        if response.status_code != 200:
            return 'Cannot contact my guys in railway, please remind me later.'
        else:
            try:
                response = response.json()
                details_to_return = []
                details_to_return.append("On " + DATE + " a total of " + str(response["total"]) + " trains were cancelled.")
                if response["total"]:
                    details_to_return.append("They were.")
                    for x in response["trains"]:
                        details_to_return.append(x["name"] + ", " + x["type"]+ " train, going from " + x["source"]["name"] + " to " + x["dest"]["name"] + ".")
                    return ' '.join(details_to_return)
            except Exception as e:
                application.logger.error(e)
                return 'Railway guys are not listening to me, maybe they are busy somewhere. Please try after lunch.'
    elif 'rescheduled' in response or response[0:2] == 'r/':
        if response[0:2] != 'r/':
            if 'yesterday' in response:
                DATE = YDate
            elif 'today' in response:
                DATE = TDate
            elif 'tomorrow' in response:
                DATE = TMDate
            else:
                return 'Please ask for either Yesterday, Today or Tommorow.'
        else:
            DATE = response[2:]
        url = 'https://api.railwayapi.com/v2/rescheduled/date/{}/apikey/{}/'.format(DATE, API_KEY)
        response =  requests.get(url)
        if response.status_code != 200:
            return 'Cannot contact my guys in railway, please remind me later.'
        else:
            try:
                response = response.json()
                details_to_return = []
                details_to_return.append("On " + DATE + " these trains were rescheduled.")
                for x in response["trains"]:
                    details_to_return.append(x["name"] + " train, going from " + x["from_station"]["name"] + " to " + x["to_station"]["name"] + " is now rescheduled to " + x["rescheduled_date"] + " at " + x["rescheduled_time"] + ".")
                return ' '.join(details_to_return)
            except Exception as e:
                application.logger.error(e)
                return 'Railway guys are not listening to me, maybe they are busy somewhere. Please try after lunch.'
    elif ('live' in response and 'status' in response) or (response.count('/')==2):
        if response.count("/")!=2:
            if 'yesterday' in response:
                DATE = YDate
            elif 'today' in response:
                DATE = TDate
            elif 'tomorrow' in response:
                DATE = TMDate
            else:
                return 'Please ask for either Yesterday, Today or Tommorow.'
            TRAIN_NO = ''
            for x in response.split():
                if x.isnumeric() and len(x) == 5:
                    TRAIN_NO = x
                    break
        else:
            response = response.split('/')
            TRAIN_NO = response[0]
            DATE = response[2]
        url = 'https://api.railwayapi.com/v2/live/train/{}/date/{}/apikey/{}/'.format(TRAIN_NO, DATE, API_KEY)
        response =  requests.get(url)
        if response.status_code != 200:
            return 'Cannot contact my guys in railway, please remind me later.'
        else:
            try:
                response = response.json()
                details_to_return = []
                details_to_return.append(response["train"]["number"] + ", " + response["train"]["name"] + ".")
                details_to_return.append(response["position"])
                return ' '.join(details_to_return)
            except Exception as e:
                application.logger.error(e)
                return 'Railway guys are not listening to me, maybe they are busy somewhere. Please try after lunch.'

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
        try:
            return get_appropriate_response(response)
        except:
            return 'Damn it! Railway guys are not reachable!'
    else:
        return 'Cannot understand that, maybe I need more training'

if __name__ == "__main__":
    handler = RotatingFileHandler('flask.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    application.logger.addHandler(handler)
    application.run(host='0.0.0.0')
