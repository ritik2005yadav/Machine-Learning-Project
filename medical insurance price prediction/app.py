from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd
import pickle

app = Flask(__name__)

# Load your trained insurance model
with open('insurancemodelf.pkl', 'rb') as f:
    model = pickle.load(f)

# Serve the HTML page
@app.route('/')
def home():
    return render_template('index.html')

# Prediction endpoint
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input from request
        data = request.json['features']

        # Log the received data to verify
        print("Received data:", data)

        # Create a DataFrame to preprocess the data
        new_data = pd.DataFrame({
            'age': [data[0]],
            'sex': ['male' if data[1] == 0 else 'female'],
            'bmi': [data[2]],
            'children': [data[3]],
            'smoker': ['yes' if data[4] == 1 else 'no'],
            'region': ['northeast' if data[5] == 0 else 'northwest' if data[5] == 1 else 'southeast' if data[5] == 2 else 'southwest']
        })

        # Log the created DataFrame
        print("Preprocessed data for prediction:", new_data)

        # Map smoker column to 0/1 and drop unused columns
        new_data['smoker'] = new_data['smoker'].map({'yes': 1, 'no': 0})
        new_data = new_data.drop(columns=['sex', 'region'])

        # Log final DataFrame before prediction
        print("Final data for prediction:", new_data)

        # Make prediction
        prediction = model.predict(new_data)

        # Convert the prediction to a standard Python float
        prediction_value = float(prediction[0])

        # Log prediction result
        print("Prediction result:", prediction_value)

        # Return prediction as JSON
        return jsonify({'prediction': round(prediction_value, 2)})
    except Exception as e:
        print("Error during prediction:", str(e))
        return jsonify({'error': 'An error occurred during prediction'}), 500

if __name__ == '__main__':
    app.run(debug=True)
