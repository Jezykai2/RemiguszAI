import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

base_model_path = "Qwen/Qwen2.5-7B-Instruct"
adapter_path = "./Remigiusz-Model-Gotowy-v7"
save_path = "./Remigiusz-FINAL-16BIT"

print("Ładowanie modelu bazowego w 16-bitach...")
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_path,
    torch_dtype=torch.float16,
    device_map="cpu"
)

tokenizer = AutoTokenizer.from_pretrained(base_model_path)

print("Nakładanie Twojego treningu (LoRA)")
model = PeftModel.from_pretrained(base_model, adapter_path)

print("Scalanie wag (Merging).")
model = model.merge_and_unload()

print(f"Zapisywanie ostatecznego Remigiusza do {save_path}")
model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)

print("SUKCES! folder Remigiusz-FINAL-16BIT ")