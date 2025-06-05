import os
from dotenv import load_dotenv
import requests
from transformers import DetrImageProcessor, DetrForObjectDetection
from PIL import Image
import torch


load_dotenv()
api_key = os.getenv('USDA_API_KEY')

def detect_food(image_path):
    """Detect food items in image and return their nutritional information"""
    # Load image
    image = Image.open(image_path)
    
    # Process image
    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    
    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]
    
    detected_items = []
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        food_label = model.config.id2label[label.item()]
        confidence = score.item()
        detected_items.append({
            'label': food_label,
            'confidence': confidence,
            'nutrition': get_nutritional_info(food_label, api_key)
        })
    
    return detected_items

# Function to get nutritional information
def get_nutritional_info(food_item, api_key):
    """Get nutritional information for a food item using the USDA API"""
    base_url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {
        "api_key": api_key,
        "query": food_item,
        "pageSize": 1
    }
    
    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get('foods'):
                return {
                    'name': data['foods'][0]['description'],
                    'nutrients': data['foods'][0]['foodNutrients']
                }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching nutritional info: {e}")
    
    return None


processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")

# Load an image
image = Image.open("burger.jpg")

inputs = processor(images=image, return_tensors="pt")
outputs = model(**inputs)

target_sizes = torch.tensor([image.size[::-1]])  # Height, Width
results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

# Process each detected item and fetch nutritional information
for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    food_label = model.config.id2label[label.item()]
    print(f"Detected label: {food_label} with score: {score.item()}")
    
    # Fetch nutritional info using the USDA API
    get_nutritional_info(food_label, api_key)
