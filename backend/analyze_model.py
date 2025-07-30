import joblib

model_path = 'backend/model/mental_model.pkl'

def main():
    model = joblib.load(model_path)
    print("Model type:", type(model))
    # Try to print feature names if available
    if hasattr(model, 'feature_names_in_'):
        print("Feature names:", model.feature_names_in_)
    else:
        print("Model does not have feature_names_in_ attribute.")
    # Print expected input shape if possible
    if hasattr(model, 'n_features_in_'):
        print("Number of features expected:", model.n_features_in_)
    else:
        print("Model does not have n_features_in_ attribute.")

if __name__ == '__main__':
    main()
