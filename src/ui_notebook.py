#!/usr/bin/env python
# coding: utf-8

# Importing Libraries and Models
import pandas as pd
import joblib
import gradio as gr
import torch
import numpy as np
from torchvision import transforms
from PIL import Image
from datetime import datetime
from prometheus_client import start_http_server, Summary, Counter, Gauge
import threading
import time

# Prometheus Metrics
REQUEST_LATENCY = Summary('Model_Response_Time', 'Latency of requests in seconds', ['endpoint'])  
REQUEST_COUNT = Counter('Number_of_Requests', 'Total number of requests', ['endpoint', 'status'])
APP_UPTIME = Gauge('Up_Time', 'Time since the application started in seconds') 
PERIODIC_LATENCY = Gauge('Show', 'Simulated latency calculated periodically')

# Start Prometheus HTTP server for metrics
start_http_server(8000)

# Initializing Models (.pkl files)
image_model = joblib.load("image_classifier.pkl")
model = joblib.load("best_rf_model_ADASYN.pkl")
comb_model = joblib.load("combining_dt_model.pkl")

# Building transformer for the input image
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Image prediction function
#@REQUEST_LATENCY.labels(endpoint='predict_image').time()
def predict_image(image):
    #REQUEST_COUNT.labels(endpoint='predict_image', status='success').inc()
    try:
        image = Image.fromarray(image.astype('uint8'), 'RGB') if isinstance(image, np.ndarray) else image
        transformed_image = transform(image).unsqueeze(0)

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        image_model.to(device)
        transformed_image = transformed_image.to(device)

        with torch.no_grad():
            output = image_model(transformed_image)
            probabilities = torch.softmax(output, dim=1)
            class_1_prob = probabilities[0][1].item()

        return class_1_prob
    except Exception as e:
        REQUEST_COUNT.labels(endpoint='predict_image', status='error').inc()
        return f"Error: {str(e)}"

# Feature prediction function
#@REQUEST_LATENCY.labels(endpoint='predict_from_features').time()
def predict_from_features(age, clin_size, area_perim_ratio, color_std_mean, eccentricity, x, y, z, sex, location):
    #REQUEST_COUNT.labels(endpoint='predict_from_features', status='success').inc()
    try:
        sex_encoded = 1 if sex == "Male" else 0

        location_categories = [
            'Left Arm', 'Left Arm - Lower', 'Left Arm - Upper', 'Left Leg',
            'Left Leg - Lower', 'Left Leg - Upper', 'Right Arm',
            'Right Arm - Lower', 'Right Arm - Upper', 'Right Leg',
            'Right Leg - Lower', 'Right Leg - Upper', 'Torso Back',
            'Torso Back Bottom Third', 'Torso Back Middle Third',
            'Torso Back Top Third', 'Torso Front', 'Torso Front Bottom Half',
            'Torso Front Top Half'
        ]
        location_encoded = [1 if loc == location else 0 for loc in location_categories]

        features = [age, clin_size, area_perim_ratio, color_std_mean, eccentricity, x, y, z, sex_encoded] + location_encoded
        features = np.array([features])
        feature_prob = model.predict_proba(features)[0][1]

        return feature_prob
    except Exception as e:
        REQUEST_COUNT.labels(endpoint='predict_from_features', status='error').inc()
        return f"Error: {str(e)}"

# Ensemble prediction function
@REQUEST_LATENCY.labels(endpoint='ensemble_predict').time()
def ensemble_predict(image, age, clin_size, area_perim_ratio, color_std_mean, eccentricity, x, y, z, sex, location):
    REQUEST_COUNT.labels(endpoint='ensemble_predict', status='success').inc()
    try:
        image_prob = predict_image(image)
        feature_prob = predict_from_features(age, clin_size, area_perim_ratio, color_std_mean, eccentricity, x, y, z, sex, location)

        final_input = np.array([[feature_prob, image_prob]])
        final_prediction = comb_model.predict(final_input)[0]

        return f"Final Prediction: {'Lesion is Malignant' if final_prediction else 'Lesion is Benign'}"
    except Exception as e:
        REQUEST_COUNT.labels(endpoint='ensemble_predict', status='error').inc()
        return f"Error: {str(e)}"

# Feedback handler
#@REQUEST_LATENCY.labels(endpoint='handle_feedback').time()
def handle_feedback(user_friendly, system_rating, additional_feedback):
    #REQUEST_COUNT.labels(endpoint='handle_feedback', status='success').inc()
    try:
        feedback_data = {
            "timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "user_friendly": [user_friendly],
            "system_rating": [system_rating],
            "additional_feedback": [additional_feedback]
        }
        feedback_df = pd.DataFrame(feedback_data)
        feedback_df.to_csv("feedback.csv", mode="a", header=False, index=False)
        return "Thank you for your feedback!"
    except Exception as e:
        REQUEST_COUNT.labels(endpoint='handle_feedback', status='error').inc()
        return f"Error: {str(e)}"

# Gradio Setup
age_approx_slider = gr.Slider(minimum=0, maximum=100, value=60, step=1, label="Approximate Age")
clin_size_slider = gr.Slider(minimum=1, maximum=30, value=3.04, step=0.1, label="Clinical Size Long Diameter (mm)")
area_perim_ratio_slider = gr.Slider(minimum=10, maximum=90, value=27.47, step=0.1, label="Area-Perimeter Ratio")
color_std_mean_slider = gr.Slider(minimum=0, maximum=10, value=0, step=0.1, label="Color Standard Mean")
eccentricity_slider = gr.Slider(minimum=0, maximum=1, value=0.9, step=0.01, label="Eccentricity")
x_slider = gr.Slider(minimum=-630, maximum=620, value=-182.70, step=0.1, label="X Coordinate")
y_slider = gr.Slider(minimum=-1100, maximum=1900, value=613.49, step=0.1, label="Y Coordinate")
z_slider = gr.Slider(minimum=-300, maximum=320, value=-42.42, step=0.1, label="Z Coordinate")
sex_dropdown = gr.Dropdown(choices=["Male", "Female"], label="Sex")
location_dropdown = gr.Dropdown(choices=[
    'Left Arm', 'Left Arm - Lower', 'Left Arm - Upper', 'Left Leg',
    'Left Leg - Lower', 'Left Leg - Upper', 'Right Arm',
    'Right Arm - Lower', 'Right Arm - Upper', 'Right Leg',
    'Right Leg - Lower', 'Right Leg - Upper', 'Torso Back',
    'Torso Back Bottom Third', 'Torso Back Middle Third',
    'Torso Back Top Third', 'Torso Front', 'Torso Front Bottom Half',
    'Torso Front Top Half'
], label="Location")

# Gradio interfaces
combined_interface = gr.Interface(
    fn=ensemble_predict,
    inputs=[
        gr.Image(type="pil", label="Upload Image"),
        age_approx_slider, clin_size_slider, area_perim_ratio_slider, color_std_mean_slider,
        eccentricity_slider, x_slider, y_slider, z_slider, sex_dropdown, location_dropdown
    ],
    outputs="text",
    title="DermAI",
    description="Upload an image and input features to get a final class prediction."
)

feedback_interface = gr.Interface(
    fn=handle_feedback,
    inputs=[
        gr.Radio(["Yes", "No"], label="Was the system user friendly?"),
        gr.Radio(["Good", "Better", "Best"], label="How would you rate the system?"),
        gr.Textbox(lines=2, placeholder="Enter additional feedback here", label="Additional Feedback")
    ],
    outputs="text",
    title="Feedback Form",
    description="Let us know your thoughts about the system!"
)

def monitor_aoo():
    start_time = time.time()
    while True:
        APP_UPTIME.set(time.time() - start_time)
        simulated_latency = np.random.uniform(0.1, 0.5)
        PERIODIC_LATENCY.set(simulated_latency)
        time.sleep(1)

threading.Thread(target = monitor_aoo, daemon = True).start()

# Launch Gradio
gr.TabbedInterface(
    interface_list=[combined_interface, feedback_interface],
    tab_names=["Prediction", "Feedback"]
).launch(server_name="0.0.0.0", server_port=7860, share=True)

