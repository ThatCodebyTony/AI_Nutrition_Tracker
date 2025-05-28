from transformers import pipeline

# Load a smaller model to keep it fast and light
chatbot = pipeline("text-generation", model="gpt2")

while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        break
    response = chatbot(
        user_input,
        max_new_tokens=200,  # Increase for longer replies
        do_sample=True,
        truncation=True,     # Avoid length errors
        pad_token_id=50256   # Avoid warning about padding
    )
    print("AI:", response[0]['generated_text'])
