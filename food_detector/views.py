from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from main import detect_food
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os
import re  # added for bold‐tag replacement

USE_MODEL = False  # Set to False to use keyword responses only

# Initialize model and tokenizer globally with cache dir
cache_dir = os.path.expanduser("~/.cache/huggingface")
print(f"[DEBUG] Loading model from cache directory: {cache_dir}")

tokenizer = AutoTokenizer.from_pretrained(
    "Qwen/Qwen3-0.6B",
    trust_remote_code=True,
    cache_dir=cache_dir
)

model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen3-0.6B",
    trust_remote_code=True,
    device_map="auto",
    cache_dir=cache_dir
)

print(f"[DEBUG] Model loaded successfully")


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


def chat(request):
    print("[DEBUG] Chat view called")
    if request.method == 'POST':
        print("[DEBUG] POST request received")
        message = request.POST.get('message')
        print(f"[DEBUG] Message: {message}")

        if not message:
            print("[DEBUG] No message provided")
            return JsonResponse({'response': 'No message provided'})

        try:
            # Build prompt for nutritional‐value question
            prompt = f"Provide the nutritional value of the food mentioned in the following question concisely: {message}"
            messages = [{"role": "user", "content": prompt}]

            # Use chat template without “thinking” tokens
            template_text = tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
                enable_thinking=False
            )

            print(f"[DEBUG] Template text: {template_text}")

            # Tokenize and move inputs to GPU if available
            model_inputs = tokenizer([template_text], return_tensors="pt")
            if torch.cuda.is_available():
                model_inputs = {k: v.cuda() for k, v in model_inputs.items()}
                print("[DEBUG] Using GPU for inference")
            else:
                print("[DEBUG] Using CPU for inference")

            # Generate a short answer
            generated_ids = model.generate(
                **model_inputs,
                max_new_tokens=150,
                do_sample=True,
                temperature=0.5,
                repetition_penalty=1.5,
                no_repeat_ngram_size=3,
                pad_token_id=tokenizer.eos_token_id
            )

            # Isolate only the newly generated token IDs
            output_ids = generated_ids[0][len(model_inputs["input_ids"][0]):].tolist()

            # Decode the final content (may contain **bold** markers)
            content = tokenizer.decode(output_ids, skip_special_tokens=True).strip()
            print(f"[DEBUG] Raw generated content: {content}")

            # Truncate to one sentence
            if "." in content:
                content = content.split(".")[0].strip()

            # Replace **bold** markers with <strong>...</strong>
            content_html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", content)

            # Return the HTML‐wrapped response
            return JsonResponse({'response': content_html})

        except Exception as e:
            print(f"[DEBUG] Error generating response: {e}")

            # Keyword‐based fallbacks (each one sentence, with **bold** allowed)
            message_lower = message.lower()

            if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
                response = "Hello! How can I help you today?"

            elif 'sugar' in message_lower and 'ice cream' in message_lower:
                # wrap the numeric range in bold tags
                response = "Ice cream has about <strong>12–24 g</strong> of sugar per half‐cup."

            elif 'sugar-free diet' in message_lower:
                response = "A sugar-free diet eliminates added sugars to help manage weight and blood sugar."

            elif any(word in message_lower for word in ['protein', 'proteins']):
                response = "Good protein sources include <strong>eggs, chicken, fish, beans, and nuts</strong>."

            elif any(word in message_lower for word in ['carb', 'carbs', 'carbohydrate']):
                response = "Healthy carbs come from <strong>whole grains, fruits, and vegetables</strong>."

            elif any(word in message_lower for word in ['fat', 'fats']):
                response = "Healthy fats come from <strong>avocados, nuts, olive oil, and fatty fish</strong>."

            else:
                response = "A teaspoon of ice cream contains about <strong>2–3 g</strong> of sugar."

            print(f"[DEBUG] Fallback response (HTML): {response}")
            return JsonResponse({'response': response})

    print("[DEBUG] GET request, rendering template")
    return render(request, 'food_detector/upload.html')
