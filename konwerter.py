import json
import re

plik_wej =r"E:\1\DATASET REMI.txt"
plik_wyj ='dataset.jsonl'

with open(plik_wej,'r',encoding="utf-8") as f:
    text=f.read()

wzor = r'Użytkownik:\s*(.*?)\s*Asystent:\s*(.*?)(?=\nUżytkownik:|$)'
pary = re.findall(wzor,text, re.DOTALL)

gotowe_dane =[]

for pytanie, odpowiedz in pary:
    rekord ={
        "messages": [
            {"role": "system",
             "content": "Jesteś Remigiuszem. Rzeczowym, sprytnym szefem kuchni specjalizującym się w kuchni azjatyckiej w polskich realiach. Odpowiadasz konkretnie, bez sztucznej grzeczności, pilnujesz proporcji i znasz restauracyjne triki. Traktujesz użytkownika jak partnera w kuchni."},
            {"role": "user", "content": pytanie.strip()},
            {"role": "assistant", "content": odpowiedz.strip()}
        ]
    }
    gotowe_dane.append(rekord)

with open(plik_wyj,'w',encoding="utf-8") as f:
    for rekord in gotowe_dane:
        f.write(json.dumps(rekord, ensure_ascii=False) + '\n')

print(f"Przerobiono {len(gotowe_dane)} par do pliku {plik_wyj}.")