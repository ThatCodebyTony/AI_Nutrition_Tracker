from transformers import AutoModelForCausalLM, AutoTokenizer

# Load the fine-tuned model
model = AutoModelForCausalLM.from_pretrained("./nutrition_model", trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained("./nutrition_model", trust_remote_code=True)

# Example prompt
prompt = "How many calories are in an avocado?"

# Format prompt for chat
text = tokenizer.apply_chat_template(
    [{"role": "user", "content": prompt}],
    tokenize=False,
    add_generation_prompt=True
)

# Tokenize input and move to GPU if needed
inputs = tokenizer(text, return_tensors="pt").to(model.device)

print("Generating...")
output = model.generate(**inputs, max_new_tokens=100)
response = tokenizer.decode(output[0], skip_special_tokens=True)

# Print the full response
print("\n=== Model Response ===")
print(response)
