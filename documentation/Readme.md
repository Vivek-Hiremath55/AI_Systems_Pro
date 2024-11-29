<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/Vivek-Hiremath55/AI_Systems_Pro">
    <img src="images/gators.jpg" alt="Logo" width="150" height="150">
  </a>

  <h3 align="center">DermAI: AI Model for Early Skin Cancer Detection</h3>

  <p align="center">
    An AI-driven solution aimed at supporting early detection of skin cancer using low-quality images captured with smartphones.
    <br />
    <a href="https://github.com/Vivek-Hiremath55/AI_Systems_Pro/blob/main/README.md"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="#usage">View Demo</a>
    ·
    <a href="https://github.com/Vivek-Hiremath55/AI_Systems_Pro/issues">Report Bug</a>
    ·
    <a href="https://github.com/Vivek-Hiremath55/AI_Systems_Pro/issues">Request Feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#dependencies">Dependencies</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#authors">Authors</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

DermAI is an AI-driven solution aimed at supporting early detection of skin cancer using low-quality images captured with smartphones. The tool is designed to assist underserved populations with limited access to specialized dermatological care. By analyzing images and descriptions, DermAI can classify skin lesions as benign or malignant and provide insights to help triage patients who may need in-person consultations with dermatologists.

You can include tables or images to summarize your results when and if appropriate.

### Built With

* [Python](https://www.python.org/)
* [TensorFlow](https://www.tensorflow.org/)
* [Keras](https://keras.io/)
* [OpenCV](https://opencv.org/)
* [AWS SageMaker](https://aws.amazon.com/sagemaker/)

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running, follow these steps.

### Dependencies

* Python 3.8
* TensorFlow 2.5.0
  ```sh
  pip install tensorflow==2.5.0
* Keras 2.4.3
  ```sh
  pip install keras==2.4.3
* OpenCV 4.5.2
  ```sh
  pip install opencv-python==4.5.2
  
## Installation

This project is designed to be executed in **Google Colab**, which provides an easy-to-use environment with all the necessary packages pre-installed.

### Steps to Get Started on Google Colab

1. **Clone the Repository**  
   Open a new notebook in Google Colab and run the following command to clone the repository:  
   ```sh
   !git clone https://github.com/Vivek-Hiremath55/AI_Systems_Pro.git
2. **Navigate to Cloned Directory**
   ```sh
   %cd AI_Systems_Pro
3. **Install Additional Requirements**
   ```sh
   !pip install -r requirements.txt
   
<!-- USAGE EXAMPLES -->
## Usage
To use DermAI, follow these steps:

* Load the `ui_notebook.py` notebook. 
* Modify the paths to `pre-trained models` wherever necessary.
* Run the `ui_notebook.py` script in Colab with the paths to the uploaded files as arguments.
* Upload the image of affected area & fill up the requested information.
* 

<!-- AUTHORS -->
## Authors
Nikhil Reddy
Vivek Hiremath

<!--ACKNOWLEDGEMENT-->
## Acknowledgements
* Prof. Andrea Ramirez



