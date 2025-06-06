from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from main import detect_food
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        file = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename)
        
        # Get food detection results
        results = detect_food(fs.path(filename))
        
        return JsonResponse({
            'uploaded_file_url': uploaded_file_url,
            'results': results
        })
    return render(request, 'food_detector/upload.html')

# Initialize model and tokenizer globally
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-0.6B", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-0.6B", trust_remote_code=True, device_map="auto")

def chat(request):
    if request.method == 'POST':
        print("[DEBUG] Received POST to /chat/")
        message = request.POST.get('message')
        if not message:
            return JsonResponse({'response': 'No message provided'})
            
        # Add context for nutrition-related conversations
        prompt = f"You are a nutrition expert assistant. Help answer this nutrition-related question: {message}"
        
        try:
            # Generate response
            input_ids = tokenizer.encode(prompt, return_tensors="pt").to('cuda')
            outputs = model.generate(
                input_ids,
                max_length=200,  # Increased length for more detailed responses
                num_return_sequences=1,
                temperature=0.7,
                pad_token_id=tokenizer.eos_token_id
            )
            
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract the actual response (remove the prompt)
            response = response.replace(prompt, '').strip()
            
            return JsonResponse({'response': response})
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return JsonResponse({'response': 'I apologize, but I encountered an error processing your request.'})
            
    return render(request, 'food_detector/upload.html')