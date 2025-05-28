from datasets import Dataset
from model_utils import initialize_model


def create_nutrition_dataset():
    # Initialize tokenizer only (ignore the model)
    tokenizer, _ = initialize_model()

    # Sample conversations
    conversations = [
        {
            "instruction": "What are the nutritional benefits of almonds?",
            "response": "Almonds are rich in vitamin E, providing 7.3mg per 28g serving. They also contain healthy fats, protein (6g per serving), and fiber (3.5g per serving). Additionally, they're a good source of magnesium and contain beneficial antioxidants."
        },
        {
            "instruction": "Compare the protein content of chicken and fish.",
            "response": "Chicken breast contains approximately 31g of protein per 100g, while most fish varieties contain 20-25g per 100g. Both are excellent lean protein sources, with fish having the added benefit of omega-3 fatty acids."
        },
        {
            "instruction": "What are the main nutrients in spinach?",
            "response": "Spinach is rich in iron (2.7mg per 100g), vitamin K (483mcg per 100g), vitamin A (9380 IU per 100g), and vitamin C (28.1mg per 100g). It also contains folate, potassium, and calcium, making it a nutrient-dense leafy green."
        },
        {
            "instruction": "How many calories are in an avocado?",
            "response": "A medium avocado contains about 234 calories, primarily from healthy monounsaturated fats. It also offers 3g protein, 12g carbohydrates (mostly fiber), and nearly 21g of fat."
        },
        {
            "instruction": "Is quinoa a good source of protein?",
            "response": "Yes, quinoa contains around 8g of protein per cooked cup (185g). It is one of the few plant-based foods that provide all nine essential amino acids."
        },
        {
            "instruction": "What is the fat content in whole milk?",
            "response": "Whole milk contains about 8g of fat per 1-cup (244g) serving, including 5g of saturated fat. It also provides 149 calories and 8g of protein."
        },
        {
            "instruction": "What nutrients are in sweet potatoes?",
            "response": "Sweet potatoes are rich in vitamin A (19,218 IU per 200g), vitamin C (39.2mg), fiber (6.6g), and potassium (950mg). They're also a good source of complex carbohydrates."
        },
        {
            "instruction": "How does brown rice compare to white rice nutritionally?",
            "response": "Brown rice contains more fiber (1.8g vs. 0.4g per 100g) and magnesium, while white rice is lower in nutrients due to processing. Both have similar calorie counts—around 110-130 per 100g cooked."
        },
        {
            "instruction": "What is the carbohydrate content in a slice of bread?",
            "response": "A typical slice of whole wheat bread has about 12-15g of carbohydrates, including around 2g of fiber. White bread may have slightly more net carbs due to less fiber."
        },
        {
            "instruction": "Are eggs high in cholesterol?",
            "response": "Yes, one large egg contains about 186mg of cholesterol, all in the yolk. However, research suggests dietary cholesterol has less impact on blood cholesterol than previously thought for most people."
        }
    ]

    data = {
        'input_ids': [],
        'labels': [],
        'attention_mask': []
    }

    for conv in conversations:
        # Format messages in chat format
        messages = [
            {"role": "user", "content": conv["instruction"]},
            {"role": "assistant", "content": conv["response"]}
        ]

        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        encoded = tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=512,
            return_tensors="pt"
        )

        # Convert tensors to lists for compatibility with Hugging Face Trainer
        data["input_ids"].append(encoded["input_ids"][0].tolist())
        data["attention_mask"].append(encoded["attention_mask"][0].tolist())
        data["labels"].append(encoded["input_ids"][0].tolist())

    return Dataset.from_dict(data)
