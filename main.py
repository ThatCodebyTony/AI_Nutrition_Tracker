from transformers import AutoModelForCausalLM, AutoTokenizer

def initialize_model():
    model_name = "Qwen/Qwen3-0.6B"
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    print("Loading model...")
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype="auto",
        device_map="auto"
    )
    print("Model loaded successfully!")
    return tokenizer, model

def generate_response(prompt, tokenizer, model, max_new_tokens=1024):
    messages = [{"role": "user", "content": prompt}]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    
    print("Generating response...")
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=0.7,
        top_p=0.9
    )
    output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()
    
    # Extract thinking and final content
    try:
        index = len(output_ids) - output_ids[::-1].index(151668)  # </think> token id
    except ValueError:
        index = 0
    
    thinking_content = tokenizer.decode(output_ids[:index], skip_special_tokens=True).strip()
    content = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip()
    
    return thinking_content, content

def main():
    tokenizer, model = initialize_model()
    
    print("\nChat with Qwen3 (type 'exit' or 'quit' to end)")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        
        thinking, response = generate_response(user_input, tokenizer, model)
        
        print("\n[Thinking]:", thinking)
        print("\n[Response]:", response)

