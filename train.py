from transformers import Trainer, TrainingArguments, default_data_collator
from model_utils import initialize_model, setup_fine_tuning
from dataset import create_nutrition_dataset

def main():
    print("Loading tokenizer and model...")
    tokenizer, model = initialize_model()
    print("Model loaded successfully!")

    print("Creating dataset...")
    dataset = create_nutrition_dataset()

    print("Setting up fine-tuning...")
    model = setup_fine_tuning(model, dataset)

    training_args = TrainingArguments(
        output_dir="./nutrition_model",
        num_train_epochs=3,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        gradient_checkpointing=True,
        fp16=True,
        learning_rate=2e-4,
        max_grad_norm=0.3,
        save_steps=100,
        save_total_limit=3,
        logging_steps=10,
        logging_first_step=True,
        remove_unused_columns=False,
        warmup_steps=100,
        optim="adamw_torch"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        tokenizer=tokenizer,
        data_collator=default_data_collator
    )

    print("Starting training...")
    trainer.train()

    print("Saving fine-tuned model...")
    model.save_pretrained("./nutrition_model")
    tokenizer.save_pretrained("./nutrition_model")
    print("Done!")

if __name__ == "__main__":
    main()
