from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Загружаем оригинальную модель
MODEL_NAME = "meta-llama/Llama-2-7b-hf"
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Подгружаем дообученную LoRA-модель
model = PeftModel.from_pretrained(model, "lora-finetuned-llama")

# Функция генерации
def generate_review(prompt, max_length=150):
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    output = model.generate(**inputs, max_length=max_length)
    return tokenizer.decode(output[0], skip_special_tokens=True)

# Проверяем генерацию
prompt = "Напиши отзыв на студента, который отлично разбирается в математике и активно участвует в олимпиадах."
print(generate_review(prompt))
