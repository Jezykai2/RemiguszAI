import re

def lonczenie_przepisow():
    plik_skladniki = 'przepisy do ogarniecia.txt'
    plik_opisy = 'przepisy raw.txt'
    plik_wyjsciowy = 'przepisy gotowe.txt'

    with open(plik_skladniki, 'r', encoding="utf-8") as f:
        tekst_skladniki = f.read()

    with open(plik_opisy, 'r', encoding="utf-8") as f:
        tekst_opisy = f.read()

    wzor = r'(?=Użytkownik: "Tryb szefa kuchni")'

    bloki_skladniki = [b.strip() for b in re.split(wzor, tekst_skladniki) if b.strip()]
    bloki_opisy = [b.strip() for b in re.split(wzor, tekst_opisy) if b.strip()]

    wynik = []

    for opis, skladniki in zip(bloki_opisy, bloki_skladniki):
        idx = skladniki.find("SKŁADNIKI:")

        if idx != -1:
            czysty_przepis = skladniki[idx:].strip()
            polaczony_tekst = f"{opis}\n{czysty_przepis}"
            wynik.append(polaczony_tekst)
        else:
            wynik.append(opis)

    gotowy_tekst = '\n\n'.join(wynik)

    with open(plik_wyjsciowy, 'w', encoding="utf-8") as f:
        f.write(gotowy_tekst)

    print("Gotowe.")

plik_wej =r"./przepisy.txt"
plik_wyj ='przepisy do ogarniecia.txt'
plik_raw ='przepisy raw.txt'

with open(plik_wej,'r',encoding="utf-8") as f:
    text=f.read()

wzor = r'XD\.\s*(.*?)(SKŁADNIKI:.*?)(?=XD\.|\Z)'
przepisXD = list(re.finditer(wzor,text, re.DOTALL))

wynik = []
wynik_raw =[]

for i in przepisXD:
    tytul = i.group(1).strip()
    reszta = i.group(2).strip()
    new =f'Użytkownik: "Tryb szefa kuchni" {tytul}\nAsystent: \n{reszta}'
    new1= f'Użytkownik: "Tryb szefa kuchni" {tytul}\nAsystent: \n'
    wynik.append(new)
    wynik_raw.append(new1)

zrobiony_wzor ='\n\n'.join(wynik)
zrobiony_wzor_raw ='\n\n'.join(wynik_raw)

with open(plik_wyj,'w',encoding="utf-8") as f:
    f.write(zrobiony_wzor)

with open(plik_raw,'w',encoding="utf-8") as f:
    f.write(zrobiony_wzor_raw)

print(f"przeroobiono {len(wynik)} przepisów do wzoru.")

while True:
    print(f"wpisz 'nie' by zakończyć program")
    pytanie = input("łączymy dane?: ")
    if pytanie.lower() == 'nie':
        break
    if pytanie.lower() == 'tak':
        lonczenie_przepisow()
        break