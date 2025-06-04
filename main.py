import torch
from transformers import DetrImageProcessor, DetrForObjectDetection
from PIL import Image
import requests

processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")


image = Image.open("burger.jpg")


# Preprocess the image and make predictions
inputs = processor(images=image, return_tensors="pt")
outputs = model(**inputs)

# Post-process the outputs to get bounding boxes and labels
target_sizes = torch.tensor([image.size[::-1]])  # Height, Width
results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

# Print the results (boxes and labels)
for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    box = [round(i, 2) for i in box.tolist()]
    print(f"Detected label: {model.config.id2label[label.item()]} with score: {score.item()}")
    print(f"Bounding box: {box}")
