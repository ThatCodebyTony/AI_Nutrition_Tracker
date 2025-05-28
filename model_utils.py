# model_utils.py

from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import prepare_model_for_kbit_training, get_peft_model, LoraConfig, TaskType

def initialize_model():
    model_name = "Qwen/Qwen3-0.6B"
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    print("Loading model...")
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype="auto",
        device_map="auto",
        load_in_4bit=True,
        trust_remote_code=True,
        use_cache=False
    )
    return tokenizer, model

def setup_fine_tuning(model, dataset):
    model = prepare_model_for_kbit_training(model)

    lora_config = LoraConfig(
        r=8,
        lora_alpha=32,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM
    )

    model = get_peft_model(model, lora_config)
    model.train()

    return model
