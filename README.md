Here's an updated version of your README with proper credit:

---

# AI Nutrition Tracker

## Overview

The **AI Nutrition Tracker** is a Django-based web application that allows users to upload food images. The app utilizes a pre-trained object detection model (with 41.6M parameters) to identify food items in the image, then fetches detailed nutritional information for those items from the USDA API.

## Features

* **Image Upload**: Users can upload images of food items.
* **Food Detection**: The application uses a state-of-the-art object detection model to identify food in the image.
* **Nutritional Information**: The app fetches and displays nutritional information for the detected food items from the USDA API.

## Installation

1. Clone the repository.
2. Set up a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For macOS/Linux
   ```
3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Run the development server:

   ```bash
   python manage.py runserver
   ```

## Usage

1. Visit `http://127.0.0.1:8000/` in your browser.
2. Upload a food image.
3. View the detected food items and their nutritional information.

## Technologies Used

* Django (Python framework)
* Transformers (for object detection)
* USDA API (for nutritional data)

## Credits

This project uses the pre-trained **DETR (DEtection TRansformers) model** from Facebook for object detection.
Model available at: [facebook/detr-resnet-50](https://huggingface.co/facebook/detr-resnet-50)

---
