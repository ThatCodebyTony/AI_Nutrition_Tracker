from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("./nutrition_model", trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained("./nutrition_model", trust_remote_code=True)

prompt = "What are the nutritional benefits of almonds?"
input_text = tokenizer.apply_chat_template(
    [{"role": "user", "content": prompt}],
    tokenize=False,
    add_generation_prompt=True
)

inputs = tokenizer(input_text, return_tensors="pt").to(model.device)
output = model.generate(**inputs, max_new_tokens=100)
print(tokenizer.decode(output[0], skip_special_tokens=True))
