import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel

print("Ładowanie bazy i Remigiusza...")
nazwa_bazowa = "Qwen/Qwen2.5-7B-Instruct"
folder_modelu = "./Remigiusz-Model-Gotowy-v7"

bnb_config = BitsAndBytesConfig(
    load_in_8bit=True
    #load_in_4bit=True,
    #bnb_4bit_use_double_quant=True,
    #bnb_4bit_quant_type="nf4",
    #bnb_4bit_compute_dtype=torch.float16
)


tokenizer = AutoTokenizer.from_pretrained(nazwa_bazowa)
model_bazowy = AutoModelForCausalLM.from_pretrained(
    nazwa_bazowa,
    quantization_config=bnb_config,
    device_map={"": 0}
)

# NAKŁADANIE STYLU
model = PeftModel.from_pretrained(model_bazowy, folder_modelu)

print("\nGotowe! Wpisz 'wyjdz', aby zakończyć.")
print("-" * 50)

historia = [
    {"role": "system",
     "content": "Jesteś Remigiuszem. Rzeczowym, sprytnym szefem kuchni specjalizującym się w kuchni azjatyckiej w polskich realiach. Odpowiadasz konkretnie, bez sztucznej grzeczności, pilnujesz proporcji i znasz restauracyjne triki. Traktujesz użytkownika jak partnera w kuchni."}
]

# hamulec bezpieczeństwa
terminatory = [
    tokenizer.eos_token_id,
    tokenizer.convert_tokens_to_ids("<|im_end|>")
]

while True:
    pytanie = input("\nTy: ")

    if pytanie.lower() in ['wyjdz', 'wyjdź', 'exit', 'quit']:
        break

    if pytanie.startswith("/szef "):
        czyste_pytanie = pytanie.replace("/szef ", "")
        ukryte_zapytanie = '"Tryb szefa kuchni" podaj rozbudowany przepis. ' + czyste_pytanie
        print("(Remigiusz zakłada czapkę szefa kuchni)")
    else:
        ukryte_zapytanie = pytanie

    historia.append({"role": "user", "content": ukryte_zapytanie})

    tekst_wejsciowy = tokenizer.apply_chat_template(historia, tokenize=False, add_generation_prompt=True)
    tokeny = tokenizer(tekst_wejsciowy, return_tensors="pt").to("cuda")

    print("Remigiusz: ", end="", flush=True)

    #Test prompt 😭😭💀💀
    # /szef chce zrobić kurczaka z sosem bulgogi dla znajomych ale brak mi przepisu?
    # /szef dobra ale potrzebuje także zrobić zupe do obiadu bo bez zupy to taka pustka także mam ochote na ramen japoński.

    with torch.no_grad():
        wygenerowane = model.generate(
            **tokeny,
            max_new_tokens=1500,
            temperature=0.1,
            top_p=0.9,
            top_k=20,
            repetition_penalty=1.1,
            #no_repeat_ngram_size=6,
            do_sample=True,
            eos_token_id=terminatory,
            pad_token_id=tokenizer.eos_token_id
        )

    odpowiedz = tokenizer.decode(wygenerowane[0][tokeny.input_ids.shape[1]:], skip_special_tokens=True)
    print(f"{odpowiedz}")
    historia.append({"role": "assistant", "content": odpowiedz})