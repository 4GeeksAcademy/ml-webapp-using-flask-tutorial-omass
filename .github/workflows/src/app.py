from flask import Flask, request, render_template
from joblib import load

# Initialize the Flask application
app = Flask(__name__)

# Load the trained decision tree model
model = load('../models/decision_tree_model.joblib')

# Assume 'features' contains the list of features expected by the model after encoding
features = list(X.columns)

@app.route('/')
def index():
    # Render the input form page and pass the feature names to the template
    return render_template('index.html', features=features)

@app.route('/predict', methods=['POST'])
def predict():
    # Extract features from the form inputs
    input_features = [request.form.get(feature) for feature in features]
    
    # Convert features to float and reshape for the model
    input_features = list(map(float, input_features))
    
    # Prepare the feature vector for prediction
    features_vector = [input_features]
    
    # Predict the class
    prediction = model.predict(features_vector)
    class_label = 'Poisonous' if prediction[0] == 1 else 'Edible'
    
    # Return the prediction result and re-render the form
    return render_template('index.html', prediction_text=f'The mushroom is {class_label}', features=features)

if __name__ == '__main__':
    app.run(debug=True)

