import pandas as pd
from flask import Flask, request, render_template
import joblib

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/resultado', methods=['GET'])
def predict(
    model_path = 'model.pkl',
):
    # Load the model
    #model = joblib.load(model_path)

    # Get the input from the user
    #input = request.form['input']

    # Make the prediction
    #prediction = model.predict(input)
    data = {}
    # Return the prediction to the user
    return render_template('index.html', ira=True, show_result=True, data=data)

if __name__ == "__main__":
    app.run(debug=True)