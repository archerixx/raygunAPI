from flask import Flask, request
import couchdb

app = Flask(__name__)


connection_string = "https://admin:IoTparking2020uat!@couchdb-iot-uat.apps.openshift.iot.bhtelecom.ba"
couch = couchdb.Server(connection_string)
db = couch['raygun_errors']

@app.route('/', defaults={'path': 'api'})
@app.route('/api/EventsFromRaygunToDatabase', methods=['POST', 'GET'])
def webhook_events():
    response = request.json
    print(response)
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)