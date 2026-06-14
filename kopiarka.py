import re

plik_wej =r"E:\1\DATASET REMI.txt"
plik_wyj ='dataset remi kopia.txt'

with open(plik_wej,'r',encoding="utf-8") as f:
    text=f.read()

wzor = r'Użytkownik: "Tryb szefa kuchni"\s*(.*?)\s*Asystent:\s*(.*?)(?=\nUżytkownik: "Tryb szefa kuchni"|$)'
szef_kuchni = list(re.finditer(wzor,text, re.DOTALL))

duplikaty = []

for i in szef_kuchni:
    fregment=i.group(0)
    duplikaty.append(fregment*4)

wynik = text + '\n' + '\n'.join(duplikaty)

with open(plik_wyj,'w',encoding="utf-8") as f:
    f.write(wynik)

print(f"Przerobiono {len(szef_kuchni)} wpisów szefa kuchni")