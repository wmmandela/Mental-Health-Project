from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)
CORS(app)

# Reminder: Run this app.py from the backend directory to ensure model path resolves correctly
print("Starting app.py - ensure you run this from the backend directory")

# Load the trained model with error handling
try:
    model = joblib.load('model/mental_model.pkl')
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

feature_names = ['Gender', 'Country', 'Occupation', 'self_employed', 'family_history', 'treatment', 'Days_Indoors', 'Growing_Stress', 'Changes_Habits', 'Mental_Health_History', 'Mood_Swings', 'Coping_Struggles', 'Work_Interest', 'Social_Weakness', 'mental_health_interview', 'care_options']

# Define categorical features that need encoding
categorical_features = ['Gender', 'Country', 'Occupation', 'self_employed', 'family_history', 'treatment', 'Mental_Health_History', 'Mood_Swings', 'Coping_Struggles', 'Work_Interest', 'Social_Weakness', 'mental_health_interview', 'care_options']

# Initialize label encoders for each categorical feature
label_encoders = {feature: LabelEncoder() for feature in categorical_features}

# Fit label encoders with possible categories (you need to provide the categories)
# For demonstration, we will fit with example categories; replace with actual categories from your dataset
label_encoders['Gender'].fit(['Male', 'Female', 'Other'])
label_encoders['Country'].fit(['Kenya', 'USA', 'UK', 'Other'])
label_encoders['Occupation'].fit(['Teacher', 'Engineer', 'Doctor', 'Other'])
label_encoders['self_employed'].fit(['Yes', 'No'])
label_encoders['family_history'].fit(['Yes', 'No'])
label_encoders['treatment'].fit(['Yes', 'No'])
label_encoders['Mental_Health_History'].fit(['Yes', 'No'])
label_encoders['Mood_Swings'].fit(['Yes', 'No'])
label_encoders['Coping_Struggles'].fit(['Never', 'Sometimes', 'Often'])
label_encoders['Work_Interest'].fit(['Low', 'Medium', 'High'])
label_encoders['Social_Weakness'].fit(['Low', 'Medium', 'High'])
label_encoders['mental_health_interview'].fit(['Yes', 'No'])
label_encoders['care_options'].fit(['Yes', 'No'])

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    try:
        data = request.get_json()
        features = data['features']
        print("Received features:", features)  # Debug log
        # Convert features list to DataFrame with feature names
        df = pd.DataFrame([features], columns=feature_names)
        print("DataFrame before encoding:\n", df)  # Debug log

        # Encode categorical features with error handling for unknown categories
        for feature in categorical_features:
            if feature in df.columns:
                # For 'Country', map unknown inputs to 'Other'
                if feature == 'Country':
                    known_countries = set(label_encoders['Country'].classes_)
                    # Use .iloc to avoid SettingWithCopyWarning and ensure correct assignment
                    df.loc[:, 'Country'] = df['Country'].apply(lambda x: x if x in known_countries else 'Other')
                try:
                    df[feature] = label_encoders[feature].transform(df[feature])
                except ValueError as ve:
                    error_msg = f"Unknown category in feature '{feature}': {ve}"
                    print(error_msg)
                    return jsonify({'error': error_msg}), 400

        print("DataFrame after encoding:\n", df)  # Debug log

        prediction = model.predict(df)
        print("Prediction result:", prediction)  # Debug log
        return jsonify({'prediction': prediction.tolist()})
    except Exception as e:
        print("Error during prediction:", e)  # Debug log
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
