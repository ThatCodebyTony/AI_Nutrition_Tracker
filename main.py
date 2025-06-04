import os
from dotenv import load_dotenv
import requests
from transformers import DetrImageProcessor, DetrForObjectDetection
from PIL import Image
import torch


load_dotenv()
api_key = os.getenv('USDA_API_KEY')

# Function to get nutritional information
def get_nutritional_info(food_item, api_key):
    headers = {
        'X-Api-Key': api_key
    }

    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={food_item}"

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data['foods']:
            food_data = data['foods'][0]
            food_name = food_data['description']
            nutrients = food_data['foodNutrients']
            print(f"Food: {food_name}")
            for nutrient in nutrients:
                print(f"{nutrient['nutrientName']}: {nutrient['value']} {nutrient['unitName']}")
        else:
            print(f"No nutritional data found for {food_item}.")
    else:
        print(f"Error: {response.status_code} - {response.text}")


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
