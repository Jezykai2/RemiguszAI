#  Remigiusz AI: Fine-Tuned Polish Culinary LLM (Developer Diary)

---

##  Ekosystem Projektu (Hugging Face)
* ** [Model GGUF (Download)](https://huggingface.co/Jezyk43/Remigiusz-AI-Qwen2.5-7B-GGUF)** – gotowy, skompresowany plik 8-bitowy `Remigiusz.gguf` do odpalenia w LM Studio.
* ** [Dataset JSONL](https://huggingface.co/datasets/Jezyk43/remigiusz-culinary-dataset-pl)** – autorski zbiór danych (ChatML) użyty do nauki modelu twardej chemii kulinarnej.

---

##  Architektura i Tech Stack
* **Model bazowy:** `Qwen/Qwen2.5-7B-Instruct` (zaawansowane rozumienie języka polskiego).
* **Trening (Fine-Tuning):** `PyTorch (CUDA)`, `HuggingFace Transformers`, `PEFT (LoRA)`.
* **Optymalizacja pamięci:** `BitsAndBytes` (kwantyzacja QLoRA w 8-bitach w locie, omijająca limity VRAM).
* **Kompilacja i dystrybucja:** `Llama.cpp` (Konwersja HF -> GGUF, architektura `Q8_0`).

---

## Dziennik Dewelopera: Pokonywanie "Bossów" LLM

Ten projekt to nie jest gotowy skrypt z tutoriala. To proces inżynieryjny, w którym każdy krok wymagał debugowania niskopoziomowych bibliotek, zarządzania pamięcią na domowej karcie RTX 3060 oraz matematycznego dostrajania parametrów generowania.

### Krok 1: Data Engineering i Rola Systemowa
Zamiast korzystać ze "śmieciowych" baz z internetu, zbudowałem autorski zbiór danych (`dataset.jsonl`). Model dostał konkretną rolę: szorstki szef kuchni opierający przepisy na prawach fizyki i chemii (łańcuchy białkowe, koagulacja, ciśnienie osmotyczne). Każdy wpis w datasecie wymuszał rygorystyczny System Prompt i formatowanie (SKŁADNIKI / PRZYGOTOWANIE).

### Krok 2: QLoRA Training (Walka o VRAM)
Z powodu limitu 12 GB VRAM, pełny trening modelu 7B skutkowałby błędem OOM (Out of Memory). Rozwiązanie? Zamrożenie głównych wag Qwena w 8-bitach (`bitsandbytes`) i trening wyłącznie lekkich macierzy adapterów LoRA za pomocą biblioteki `TRL`. Optymalizator `paged_adamw_8bit` skutecznie przerzucał nadmiar pamięci do systemowego RAM-u.

### Krok 3: Inwazja "Solątek" i "Baraniny" (Debugowanie Halucynacji)
Podczas pierwszych testów, po zadaniu luźnego pytania o Ramen, model całkowicie stracił zmysły. Generował neologizmy (np. *"solątki"*), a na domiar złego proponował **ugotowanie ramenu z baraniny w mące triticum aestivum** (łac. pszenica zwyczajna). 

**Diagnoza i rozwiązanie (Dlaczego Ramen pokonał model?):**
1. **Klątwa gilotyny n-gramowej (`no_repeat_ngram_size=6`):** Ustawiłem sztywną blokadę zapętlania słów. W polskiej gramatyce i tekstach kulinarnych (np. "sos sojowy", "dodaj") model dostał "zakaz" używania poprawnych powtórzeń. Wpadł w matematyczną panikę i zaczął losować słowa ze słownika bazowego (stąd łacina). Usunąłem ten parametr, zastępując go płynnym "podatkiem" `repetition_penalty=1.18`.
2. **Out of Distribution & System Prompt:** Model zderzył się z potocznym pytaniem bez wstrzykniętej roli szefa kuchni. Próbował mapować luźny tekst na hiper-techniczne wagi LoRA. Rygorystyczne dodanie System Promptu przy inferencji w `czat.py` natychmiast ustabilizowało model.
3. **Tonkatsu vs Tonkotsu:** Kiedy zapytałem o "ramen tonkAtsu" zamiast "tonkOtsu", model posłusznie stworzył hybrydę ramenu z... japońskim kotletem schabowym w panierce. Dowód na to, że model podąża ślepo za poleceniami w tokenach.

### Krok 4: FP16 Merge & GGUF
Skompresowałem projekt do jednego, przośnego pliku.
1. **CPU Merge:** Używając 22 GB systemowej pamięci RAM, wtopiłem na stałe macierze LoRA w oryginalny szkielet Qwena (`merge_and_unload`).
2. **Poprawka Tokenizera:** `llama.cpp` wywalało krytyczny błąd konwersji ze względu na konflikt list w pliku konfiguracyjnym HF (`AttributeError: 'list' object has no attribute 'keys'`). Ręcznie naprawiłem strukturę JSON w `tokenizer_config.json`.
3. **Kwantyzacja:** Eksport modelu z 16-bitów do `Q8_0` (8-bit GGUF).

---

### Dla śmiechu:
W folderze z dowodami zostawiłem screeny z wczesnych faz testów, gdzie model proponował przyrządzenie 'mięsaka z kurczaka', poematy o soli oraz smażenie cebuli aż 'zacznie się roztrzaskać' -  wizualne studium przypadku halucynacji LLM."

---
*Stworzone jako dowód posiadania. Żaden ramen z baraniny nie ucierpiał podczas treningu.(raczje nie ucierpiał)*
