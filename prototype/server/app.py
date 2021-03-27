from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"/endpoint": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/", methods=["GET"])
def index(): 
    return "HELLO"

@app.route("/postAPI", methods=["POST"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def postAPI():
    apiCall = request.form.get("APICall")
    print(apiCall)
    #  POST TO SPOTIFY, RETURN TO BAD DJ
    return "test"

if __name__ == "__main__":
    app.run(port=4000, debug=True)