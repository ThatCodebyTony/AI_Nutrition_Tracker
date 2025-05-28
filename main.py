from transformers import Trainer, TrainingArguments, default_data_collator
from model_utils import initialize_model, setup_fine_tuning  # Changed from main to model_utils
from dataset import create_nutrition_dataset

def main():
    # Initialize model and tokenizer
    tokenizer, model = initialize_model()

    # Prepare dataset
    dataset = create_nutrition_dataset()

    # Setup LoRA fine-tuning
    model = setup_fine_tuning(model, dataset)

    # Training arguments
    training_args = TrainingArguments(
        output_dir="./nutrition_model",
        num_train_epochs=3,
        per_device_train_batch_size=2,
        save_steps=100,
        logging_steps=10,
        learning_rate=2e-4,
        remove_unused_columns=False,
        max_grad_norm=0.3,
        gradient_checkpointing=True,
        gradient_accumulation_steps=4,
        fp16=True,
        optim="adamw_torch",
        warmup_steps=100,
        logging_first_step=True,
        save_total_limit=3
    )

    # Initialize trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        tokenizer=tokenizer,
        data_collator=default_data_collator,
    )

    # Train the model
    trainer.train()

    # Save the fine-tuned model and tokenizer
    model.save_pretrained("./nutrition_model")
    tokenizer.save_pretrained("./nutrition_model")

if __name__ == "__main__":
    main()
