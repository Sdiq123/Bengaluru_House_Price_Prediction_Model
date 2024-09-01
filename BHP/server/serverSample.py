'''from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/hello')
def hello():
    return "Hi"

if __name__ == "__main__":
    print("starting prediction..........")
    app.run() '''


from flask import Flask, request, jsonify
from flask_cors import CORS
import util

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return "Welcome to the homepage!"

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    print("Endpoint /get_location_names called")
    try:
        locations = util.get_location_names()
        if locations is None:
            raise ValueError("No locations found.")
        return jsonify({'locations': locations})
    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

'''@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])

    response = jsonify({
        'estimated_price': util.get_estimated_price(location,total_sqft,bhk,bath)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response'''


@app.route('/predict_home_price', methods=['GET','POST'])
def predict_home_price():
    try:
        total_sqft = float(request.form['total_sqft'])
        location = request.form['location']
        bhk = int(request.form['bhk'])
        bath = int(request.form['bath'])
        
        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)
        
        response = jsonify({
            'estimated_price': estimated_price
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    
    except KeyError as e:
        return jsonify({'error': f'Missing parameter: {str(e)}'}), 400
    
    except ValueError as e:
        return jsonify({'error': f'Invalid value: {str(e)}'}), 400
    
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500



@app.route('/hello')
def hello():
    return "Hi"

if __name__ == "__main__":
    util.load_saved_artifacts()
    print("starting prediction..........")
    app.run(debug=True)  # debug=True for more verbose output
    #util.load_saved_artifacts()
    #app.run(debug=True)
