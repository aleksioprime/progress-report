import torch
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model, prepare_model_for_int8_training
import bitsandbytes as bnb

# Загружаем LLaMA 2 (например, 7B)
MODEL_NAME = "meta-llama/Llama-2-7b-hf"

# Загружаем токенизатор
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Загружаем модель с int8-квантованием (экономия памяти)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    load_in_8bit=True,
    torch_dtype=torch.float16,
    device_map="auto"
)

# Конфигурация LoRA
lora_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM"
)

# Применяем LoRA к модели
model = get_peft_model(model, lora_config)
model = prepare_model_for_int8_training(model)
model.print_trainable_parameters()

# Загружаем датасет
dataset = load_dataset("json", data_files="data/reviews.jsonl", split="train")

# Токенизируем текст
def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=512)

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Настройки обучения
training_args = TrainingArguments(
    output_dir="./lora-finetuned-llama",
    per_device_train_batch_size=2,
    num_train_epochs=3,
    logging_steps=10,
    save_steps=500,
    save_total_limit=2,
    report_to="none"
)

# Создаём Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets
)

# Запуск обучения
trainer.train()

# Сохраняем обученную LoRA-модель
model.save_pretrained("lora-finetuned-llama")
