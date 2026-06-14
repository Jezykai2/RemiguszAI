import torch
import os
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainingArguments
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer, SFTConfig

os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

print("Ładowanie ustawień")
nazwa_modelu = "Qwen/Qwen2.5-7B-Instruct"
plik_danych = "dataset.jsonl"
folder_wyjsciowy = "./Remigiusz-Model-Gotowy"

bnb_config = BitsAndBytesConfig(
    load_in_8bit=True
    #load_in_4bit=True,
    #bnb_4bit_use_double_quant=True,
    #bnb_4bit_quant_type="nf4",
    #bnb_4bit_compute_dtype=torch.bfloat16
)

print("Pobieranie i ładowanie modelu bazowego")
tokenizer = AutoTokenizer.from_pretrained(nazwa_modelu)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.model_max_length = 2048

model = AutoModelForCausalLM.from_pretrained(
    nazwa_modelu,
    quantization_config=bnb_config,
    device_map={"": 0}
)

lora_config = LoraConfig(
    r=16,
    lora_alpha=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, lora_config)

print("Ładowanie i dzielenie datasetu")
pelny_dataset = load_dataset("json", data_files=plik_danych, split="train")

def formatuj_rozmowe(przyklad):
    tekst = tokenizer.apply_chat_template(przyklad["messages"], tokenize=False, add_generation_prompt=False)
    return {"text": tekst}

pelny_dataset = pelny_dataset.map(formatuj_rozmowe)
dataset_podzielony = pelny_dataset.train_test_split(test_size=0.2)

zbior_treningowy = dataset_podzielony["train"]
zbior_testowy = dataset_podzielony["test"]

parametry_treningu = SFTConfig(
    output_dir="./wyniki",
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    gradient_accumulation_steps=4,
    lr_scheduler_type="cosine",
    warmup_ratio=0.05,
    weight_decay=0.01,
    learning_rate=1e-5,
    logging_steps=5,
    max_steps=-1,
    num_train_epochs=1,
    eval_strategy="steps",
    eval_steps=40,
    optim="paged_adamw_8bit",
    bf16=True,
    save_steps=100,
    dataset_text_field="text",
)

trainer = SFTTrainer(
    model=model,
    train_dataset=zbior_treningowy,
    eval_dataset=zbior_testowy,
    args=parametry_treningu,
)

print("TRENING SZCZURA ")
trainer.train()

print(f"Zapisywanie gotowego modelu do folderu: {folder_wyjsciowy}")
trainer.model.save_pretrained(folder_wyjsciowy)
tokenizer.save_pretrained(folder_wyjsciowy)
print("Możliwe że zrobione")