from flask import Flask, request
application = Flask(__name__)

@application.route("/", methods=['POST', 'GET'])
def hello():
    try:
        response = request.args.get('q')
    except:
        response = 'Cannot understand that, maybe I need more training'
    if response:
        return response
    else:
        return 'Cannot understand that, maybe I need more training'

if __name__ == "__main__":
    application.run(host='0.0.0.0')

