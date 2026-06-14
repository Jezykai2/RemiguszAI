
def lonczenie_do_datasetu():
    plik_kopia =r"./dataset remi kopia.txt"
    plik_gotowe_przep=r"./przepisy gotowe.txt"
    plik_dataset_wyj="Dataset remi polonczony.txt"
    with open(plik_kopia, 'r', encoding='utf-8') as plik:
        p1= plik.read()
    with open(plik_gotowe_przep, 'r', encoding='utf-8') as plik1:
        p2= plik1.read()

    wynik = p1 + p2

    with open(plik_dataset_wyj, 'w', encoding="utf-8") as f:
        f.write(wynik)

plik_oryginal =r"E:\1\DATASET REMI.txt"
plik_kopia =r"./dataset remi kopia.txt"
plik_przepisy=r"./przepisy gotowe.txt"
plik_dataset_wyj=r"./Dataset remi polonczony.txt"

with open (plik_oryginal,'r',encoding = 'utf-8' ) as plik:
    caly_plik=plik.read()

ilosc_par=caly_plik.count('Użytkownik:')
tryb_szefa=caly_plik.count('Tryb szefa kuchni')

print(f"mam aktualnie: {ilosc_par} par Q&A")
print(f"oraz mam: {tryb_szefa} par ULTRA przepisów")

with open(r'E:\1\szkl\python Wifle love\RemigiuszAI\przepisy.txt','r',encoding='utf-8') as plik1:
    caly_plik1=plik1.read()

ilosc_par1=caly_plik1.count('XD.')

print(f"mam aktualnie: {ilosc_par1} przepisów do ogarnięcia💀")

while True:
    print(f"wpisz 'nie' by zakończyć program")
    pytanie = input("łączymy dane do datasetu?: ")
    if pytanie.lower() == 'nie':
        break
    if pytanie.lower() == 'tak':
        lonczenie_do_datasetu()
        break
