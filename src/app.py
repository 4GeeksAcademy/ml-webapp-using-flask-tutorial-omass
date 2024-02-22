from flask import Flask, request, render_template
import pickle
import os

modelFolder = os.path.join('src', 'model')
print(modelFolder)

# Initialize the Flask application
app = Flask(__name__)

# Load the trained decision tree model
model = pickle.load(open('./models/decision_tree_model.pkl', 'rb'))


# Update 'features' with the min and max values obtained 
features_with_ranges = [
    ('cap-shape', 0, 5), ('cap-surface', 0, 3), ('cap-color', 0, 9), ('bruises', 0, 1), ('odor', 0, 8),
    ('gill-attachment', 0, 1), ('gill-spacing', 0, 1), ('gill-size', 0, 1), ('gill-color', 0, 11),
    ('stalk-shape', 0, 1), ('stalk-root', 0, 4), ('stalk-surface-above-ring', 0, 3), ('stalk-surface-below-ring', 0, 3),
    ('stalk-color-above-ring', 0, 8), ('stalk-color-below-ring', 0, 8), ('veil-type', 0, 0), ('veil-color', 0, 3),
    ('ring-number', 0, 2), ('ring-type', 0, 4), ('spore-print-color', 0, 8), ('population', 0, 5), ('habitat', 0, 6)
    
]

@app.route('/')
def index():
    # Render the input form page and pass the feature names and ranges to the template
    return render_template('index.html', features=features_with_ranges)

@app.route('/predict', methods=['POST'])
def predict():
    # Extract features from the form inputs
    input_features = [float(request.form.get(feature)) for feature, _, _ in features_with_ranges]
    
    # Prepare the feature vector for prediction
    features_vector = [input_features]
    
    # Predict the class
    prediction = model.predict(features_vector)
    class_label = 'Poisonous' if prediction[0] == 1 else 'Edible'
    
    # Return the prediction result and re-render the form
    return render_template('index.html', prediction_text=f'The mushroom is {class_label}', features=features_with_ranges)

if __name__ == '__main__':
    app.run(debug=True)


