import streamlit as st
import pandas as pd
import pickle

# Set page configuration
st.set_page_config(
    page_title="India Crop Production Predictor",
    page_icon="🌾",
    layout="centered"
)

# App Header
st.title("🌾 Agriculture Crop Production Predictor")
st.markdown("This application predicts crop production metrics based on regional, structural, and cost metrics across India.")
st.write("---")

@st.cache_resource
def load_artifacts():
    """
    Cache artifacts to avoid re-loading model binaries on every user interaction clicks.
    """
    try:
        with open('crop_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('dropdown_options.pkl', 'rb') as f:
            dropdowns = pickle.load(f)
        return model, dropdowns
    except FileNotFoundError:
        return None, None

model, dropdowns = load_artifacts()

if model is None or dropdowns is None:
    st.error("⚠️ Model files (`crop_model.pkl` / `dropdown_options.pkl`) not found!")
    st.info("Please run `python train_model.py` first to generate the model files using your dataset.")
else:
    st.subheader("Enter Crop Details for Prediction")
    
    # Construct form layouts using columns
    col1, col2 = st.columns(2)
    
    with col1:
        # Dynamic drop downs matching dataset strings
        crop = st.selectbox("Select Crop", options=dropdowns.get('crop', ['Unknown']))
        variety = st.selectbox("Select Variety", options=dropdowns.get('variety', ['Unknown']))
        state = st.selectbox("Select State", options=dropdowns.get('state', ['Unknown']))
        
    with col2:
        season = st.selectbox("Select Season", options=dropdowns.get('season', ['Unknown']))
        zone = st.selectbox("Recommended Zone", options=dropdowns.get('recommended zone', ['Unknown']))
        cost = st.number_input("Cost of Cultivation/Production", min_value=0, value=5000, step=250)

    st.markdown("###")
    
    # Single prediction execution to guarantee output doesn't repeat or double-render
    if st.button("Predict Production Output", type="primary"):
        csv='C:/Users/S.Marok/Desktop/Project.4/crop_production.csv'
        # Build DataFrame with identical key names matching model training layout
        input_data = pd.DataFrame([{
            'crop': crop,
            'variety': variety,
            'state': state,
            'season': season,
            'recommended zone': zone,
            'cost': cost
        }])
        
        # Make a single prediction call
        try:
            prediction = model.predict(input_data)[0]
            
            # Display results once inside a clean UI container block
            st.success("🎉 Prediction Completed Successfully!")
            
            col_metric1, col_metric2 = st.columns(2)
            with col_metric1:
                st.metric(
                    label="Estimated Production Output", 
                    value=f"{prediction:.2f} Quintals/Hectares"
                )
            with col_metric2:
                st.metric(label="Input Cost Evaluated", value=f"₹ {cost:,}")
                
        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")