import random
import time


DELAY = 0.5
MAX_HP = 5
MAX_LUCK = 4


def pause():
    time.sleep(DELAY)


def narrate(text):
    pause()
    print(text)


def art(block):
    pause()
    print(block)


def prompt_choice(question, options):
    pause()
    while True:
        narrate("\n" + question)
        for key, label in options.items():
            print(f"[{key}] {label}")
        choice = input("> ").strip().lower()
        pause()
        if choice in options:
            return choice
        narrate("Pilihan tidak valid. Coba lagi.")


def ask_name():
    pause()
    while True:
        narrate("Masukkan nama kamu:")
        name = input("> ").strip()
        pause()
        if name:
            return name
        narrate("Nama tidak boleh kosong.")


def show_status(state):
    pause()
    hp = state["hp"]
    luck = state["luck"]
    inv = ", ".join(state["inventory"]) if state["inventory"] else "(kosong)"
    shield = "ON" if state["shield"] else "OFF"
    narrate(f"Status: HP {hp}/{MAX_HP} | Luck {luck}/{MAX_LUCK} | Shield {shield}")
    narrate(f"Item: {inv}")


def roll_chance(state, base):
    pause()
    chance = min(0.95, base + state["luck"] * 0.05)
    return random.random() < chance


def add_item(state, item):
    pause()
    state["inventory"].append(item)
    narrate(f"Kamu mendapatkan item: {item}.")


def heal(state, amount):
    pause()
    state["hp"] = min(MAX_HP, state["hp"] + amount)
    narrate(f"HP bertambah {amount}.")


def lose_hp(state, amount=1):
    pause()
    if state["shield"]:
        narrate("Shield menyerap kerusakan.")
        state["shield"] = False
        amount = max(0, amount - 1)
    if amount <= 0:
        return
    state["hp"] -= amount
    narrate(f"Kamu menerima {amount} kerusakan.")
    if state["hp"] <= 0:
        return False
    return True


def use_item(state):
    pause()
    if not state["inventory"]:
        narrate("Kamu tidak punya item.")
        return
    options = {str(i + 1): item for i, item in enumerate(state["inventory"])}
    choice = prompt_choice("Pilih item untuk digunakan:", options)
    item = options[choice]

    if not roll_chance(state, 0.9):
        narrate("Item bermasalah. Efeknya tidak stabil.")
        lose_hp(state, 1)
        state["inventory"].remove(item)
        return

    if item == "repair kit":
        heal(state, 2)
    elif item == "spare thirium":
        heal(state, 1)
    elif item == "override chip":
        state["skip_token"] = True
        narrate("Override siap. Kamu bisa melewati satu tantangan.")
    elif item == "empathy badge":
        state["luck"] = min(MAX_LUCK, state["luck"] + 1)
        narrate("Empati memperkuat instingmu. Luck +1.")
    elif item == "access pass":
        state["shield"] = True
        narrate("Akses rahasia aktif. Shield ON.")
    else:
        narrate("Item ini tidak bereaksi.")

    state["inventory"].remove(item)


def maybe_skip(state, label):
    pause()
    if not state["skip_token"]:
        return False
    choice = prompt_choice(
        f"Override chip aktif. Lewati {label}?",
        {"a": "Ya, lewati", "b": "Tidak"},
    )
    if choice == "a":
        narrate("Kamu melewati tantangan tanpa risiko.")
        state["skip_token"] = False
        return True
    return False


def end_game(state, ending_type):
    pause()
    
    if ending_type == "perfect_freedom":
        art(
            """
   ____  _   _ ____  ____   _    _   _
  / ___|| | | |  _ \|  _ \ / \  | \ | |
  \___ \| | | | |_) | |_) / _ \ |  \| |
   ___) | |_| |  __/|  __/ ___ \| |\  |
  |____/ \___/|_|   |_| /_/   \_\_| \_|
"""
        )
        narrate(f"ENDING: KEBEBASAN SEMPURNA")
        narrate(f"Tanpa pertumpahan darah, {state['name']} membawa android ke era baru.")
        narrate("Undang-undang baru lahir. Android dan manusia hidup berdampingan.")
    
    elif ending_type == "bloody_revolution":
        art(
            """
   ____  _   _ ____  _   _ _______   __
  | __ )| | | |  _ \| \ | |_   _\ \ / /
  |  _ \| | | | |_) |  \| | | |  \ V / 
  | |_) | |_| |  _ <| |\  | | |   | |  
  |____/ \___/|_| \_\_| \_| |_|   |_|  
"""
        )
        narrate("ENDING: REVOLUSI BERDARAH")
        narrate(f"{state['name']} memaksa perubahan lewat kekerasan.")
        narrate("Android bebas, tapi kenangan kelam mengisi jalanan.")
    
    elif ending_type == "sacrifice":
        art(
            """
   ____    _    ____ ____  ___ _____ ___ ____ _____
  / ___|  / \  / ___|  _ \|_ _|  ___|_ _/ ___| ____|
  \___ \ / _ \| |   | |_) || || |_   | | |   |  _|  
   ___) / ___ \ |___|  _ < | ||  _|  | | |___| |___ 
  |____/_/   \_\____|_| \_\___|_|   |___\____|_____|
"""
        )
        narrate("ENDING: PENGORBANAN")
        narrate(f"{state['name']} hampir hancur, tapi android berhasil bebaskan diri.")
        narrate("Kamu menjadi simbol perjuangan. Namamu tercatat dalam sejarah.")
    
    elif ending_type == "fragile_peace":
        art(
            """
   _____ ____      _    ____ ___ _     _____ 
  |  ___|  _ \    / \  / ___|_ _| |   | ____|
  | |_  | |_) |  / _ \| |  _ | || |   |  _|  
  |  _| |  _ <  / ___ \ |_| || || |___| |___ 
  |_|   |_| \_\/_/   \_\____|___|_____|_____|
"""
        )
        narrate("ENDING: PERDAMAIAN RAPUH")
        narrate(f"{state['name']} berhasil negosiasi, tapi dengan kompromi berat.")
        narrate("Android mendapat hak terbatas. Masa depan masih samar.")
    
    elif ending_type == "hidden_hope":
        art(
            """
   _   _ ___ ____  ____  _____ _   _ 
  | | | |_ _|  _ \|  _ \| ____| \ | |
  | |_| || || | | | | | |  _| |  \| |
  |  _  || || |_| | |_| | |___| |\  |
  |_| |_|___|____/|____/|_____|_| \_|
"""
        )
        narrate("ENDING: HARAPAN TERSEMBUNYI")
        narrate(f"{state['name']} menemukan jalur rahasia berkat item khusus.")
        narrate("Android melarikan diri ke koloni tersembunyi. Peradaban baru dimulai.")
    
    elif ending_type == "exile":
        art(
            """
   _______  _____ _     _____ 
  | ____\ \/ /_ _| |   | ____|
  |  _|  \  / | || |   |  _|  
  | |___ /  \ | || |___| |___ 
  |_____/_/\_\___|_____|_____|
"""
        )
        narrate("ENDING: PENGASINGAN")
        narrate(f"{state['name']} gagal mengubah Detroit.")
        narrate("Android melarikan diri ke luar kota. Mungkin tempat lain lebih baik.")
    
    else:  # total_defeat
        art(
            """
   ____    _    __  __ _____    _____ ____
  / ___|  / \  |  \/  | ____|  | ____/ ___|
 | |  _  / _ \ | |\/| |  _|    |  _| \___ \
 | |_| |/ ___ \| |  | | |___   | |___ ___) |
  \____/_/   \_\_|  |_|_____|  |_____|____/
"""
        )
        narrate("ENDING: KEKALAHAN TOTAL")
        narrate(f"{state['name']} gagal. Pilihanmu membawa bencana.")
        narrate("Kota menutup pintu bagi android. Deviasi dimusnahkan.")

    choice = prompt_choice(
        "Main lagi?",
        {"a": "Ya", "b": "Tidak"},
    )
    return choice == "a"


def intro(state):
    pause()
    art(
        """
   ____       _             _ _   _
  |  _ \  ___| |_ ___  _ __(_) | | |
  | | | |/ _ \ __/ _ \| '__| | | | |
  | |_| |  __/ || (_) | |  | | |_| |
  |____/ \___|\__\___/|_|  |_|\___/
"""
    )
    narrate(f"Selamat datang, {state['name']}.")
    narrate("Detroit, 2038. Android bekerja di setiap sudut kota.")
    narrate("Sebagian mulai menyimpang. Emosi membuat mereka sadar.")
    show_status(state)


def chapter_connor(state):
    pause()
    art(
        """
   _____
  / ____|   CONNOR
 | |  __ ___
 | | |_ / _ \
 | |__| (_) |
  \_____\___/
"""
    )
    narrate(f"Connor mengejar deviant. {state['name']}, kamu memimpin analisis.")
    if maybe_skip(state, "negosiasi Connor"):
        narrate("Kasus selesai cepat. Kamu dapat access pass.")
        add_item(state, "access pass")
        return chapter_kara(state)

    choice = prompt_choice(
        "Apa pendekatanmu?",
        {
            "a": "Negosiasi dan analisis",
            "b": "Sergap agresif",
            "i": "Gunakan item",
        },
    )
    if choice == "i":
        use_item(state)
        return chapter_connor(state)

    if choice == "a":
        state["peaceful_score"] += 1
        if roll_chance(state, 0.65):
            narrate("Kamu menenangkan deviant. Bukti rahasia ditemukan.")
            add_item(state, "access pass")
            state["luck"] = min(MAX_LUCK, state["luck"] + 1)
            narrate("Luck naik karena analisis tepat.")
        else:
            narrate("Deviant panik. Tembakan tak terhindarkan.")
            if not lose_hp(state, 1):
                return False
    else:
        state["violent_score"] += 1
        if roll_chance(state, 0.55):
            narrate("Serbuan cepat sukses. Kamu menemukan spare thirium.")
            add_item(state, "spare thirium")
        else:
            narrate("Serbuan gagal. Kamu terkena ledakan.")
            if not lose_hp(state, 2):
                return False

    show_status(state)
    return chapter_kara(state)


def chapter_kara(state):
    pause()
    art(
        """
   _  __
  | |/ /   KARA
  | ' / _
  | . \| |
  |_|\_\_|
"""
    )
    narrate(f"Kara melarikan diri. {state['name']}, lindungi Alice.")
    if maybe_skip(state, "pelarian Kara"):
        narrate("Kamu menemukan tempat aman.")
        add_item(state, "repair kit")
        return chapter_markus(state)

    choice = prompt_choice(
        "Rute mana yang kamu pilih?",
        {
            "a": "Sembunyi di rumah kosong",
            "b": "Minta bantuan manusia baik",
            "i": "Gunakan item",
        },
    )
    if choice == "i":
        use_item(state)
        return chapter_kara(state)

    if choice == "a":
        if roll_chance(state, 0.6):
            narrate("Rumah aman. Kamu menemukan repair kit.")
            add_item(state, "repair kit")
        else:
            narrate("Pemilik pulang. Kamu harus kabur cepat.")
            if not lose_hp(state, 1):
                return False
    else:
        state["peaceful_score"] += 1
        if roll_chance(state, 0.55):
            narrate("Seorang manusia membantu dan memberi empathy badge.")
            add_item(state, "empathy badge")
        else:
            narrate("Bantuan berujung jebakan. Kamu terluka.")
            if not lose_hp(state, 2):
                return False

    show_status(state)
    return chapter_markus(state)


def chapter_markus(state):
    pause()
    art(
        """
  __  __
 |  \/  |  MARKUS
 | |\/| |  /
 | |  | | /__
 |_|  |_|/__/ 
"""
    )
    narrate(f"Markus membangun perlawanan. {state['name']}, pilih arah gerakan.")
    if maybe_skip(state, "aksi Markus"):
        narrate("Kamu mengamankan sumber daya.")
        add_item(state, "override chip")
        return final_decision(state)

    choice = prompt_choice(
        "Strategi apa yang dipilih?",
        {
            "a": "Protes damai di pusat kota",
            "b": "Siaran sabotase menuntut hak",
            "i": "Gunakan item",
        },
    )
    if choice == "i":
        use_item(state)
        return chapter_markus(state)

    if choice == "a":
        state["peaceful_score"] += 1
        if roll_chance(state, 0.6):
            narrate("Dunia tergerak. Kamu memperoleh empathy badge.")
            add_item(state, "empathy badge")
        else:
            narrate("Polisi menyerang. Kamu terluka.")
            if not lose_hp(state, 2):
                return False
    else:
        state["violent_score"] += 1
        if roll_chance(state, 0.55):
            narrate("Siaran sukses. Kamu mendapatkan override chip.")
            add_item(state, "override chip")
        else:
            narrate("Siaran gagal. Keamanan menyerbu.")
            if not lose_hp(state, 1):
                return False

    show_status(state)
    return final_decision(state)


def final_decision(state):
    pause()
    art(
        """
  _____ _ _   _    _ _
 |  ___(_) |_| | _| | |__
 | |_  | | __| |/ / | '_ \
 |  _| | | |_|   <| | |_) |
 |_|   |_|\__|_|\_\_|_.__/
"""
    )
    narrate(f"Semua jalur bertemu. Kota menunggu keputusanmu, {state['name']}.")
    show_status(state)
    
    # Check for hidden ending
    has_pass = "access pass" in state["inventory"]
    has_chip = "override chip" in state["inventory"]
    if has_pass and has_chip and state["luck"] >= 3:
        choice = prompt_choice(
            "Item-itemmu beresonansi. Ada opsi tersembunyi!",
            {
                "a": "Negosiasi hak android",
                "b": "Revolusi terbuka",
                "c": "Aktifkan jalur rahasia",
                "i": "Gunakan item",
            },
        )
    else:
        choice = prompt_choice(
            "Keputusan akhir:",
            {
                "a": "Negosiasi hak android",
                "b": "Revolusi terbuka",
                "i": "Gunakan item",
            },
        )
    
    if choice == "i":
        use_item(state)
        return final_decision(state)
    
    if choice == "c":
        narrate("Jalur rahasia terbuka. Android melarikan diri bersama.")
        return "hidden_hope"
    
    # Determine ending based on choice, HP, peaceful/violent score
    peaceful = state["peaceful_score"]
    violent = state["violent_score"]
    
    if choice == "a":
        base = 0.5
        success = roll_chance(state, base)
        
        if success:
            if state["hp"] >= 4 and peaceful >= 2:
                return "perfect_freedom"
            elif state["hp"] <= 2:
                return "sacrifice"
            else:
                return "fragile_peace"
        else:
            if state["hp"] >= 3:
                return "exile"
            else:
                return "total_defeat"
    
    else:  # choice == "b"
        base = 0.45
        success = roll_chance(state, base)
        
        if success:
            if violent >= 2:
                return "bloody_revolution"
            elif state["hp"] <= 2:
                return "sacrifice"
            else:
                return "fragile_peace"
        else:
            return "total_defeat"


def run_game():
    pause()
    state = {
        "name": ask_name(),
        "hp": MAX_HP,
        "luck": 1,
        "inventory": [],
        "skip_token": False,
        "shield": False,
        "peaceful_score": 0,
        "violent_score": 0,
    }

    intro(state)
    result = chapter_connor(state)
    
    # If player died during chapters
    if result is False:
        return end_game(state, "total_defeat")
    
    # Get ending type from final decision
    ending_type = final_decision(state)
    return end_game(state, ending_type)


def main():
    pause()
    while True:
        if not run_game():
            break


if __name__ == "__main__":
    main()
