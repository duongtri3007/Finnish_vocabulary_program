import json

sets_file = "sets.json"

def load_sets():
    try:
        with open(sets_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        with open(sets_file, "w") as f:
            json.dump({}, f)
        return {}

def save_sets(sets):
    with open(sets_file, "w") as f:
        json.dump(sets, f, indent=4)

def manage_sets():
    while True:
        print("\n=== Vocabulary Sets ===")
        print("1. Create new set")
        print("2. Add word to set")
        print("3. Show sets")
        print("4. Back to main menu")

        choice = input("Choose an option: ")

        if choice == "1":
            create_set()
        elif choice == "2":
            add_word_to_set()
        elif choice == "3":
            show_sets()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

def create_set():
    sets = load_sets()
    name = input("Set name: ")

    if name in sets:
        print("Set already exists.")
        return

    sets[name] = []
    save_sets(sets)
    print("Set created!")

def add_word_to_set():
    sets = load_sets()
    if not sets:
        print("No sets available.")
        return

    print("Available sets:")
    for s in sets:
        print("-", s)

    name = input("Choose a set: ")
    if name not in sets:
        print("Set not found.")
        return

    finnish = input("Finnish word: ")
    english = input("English meaning: ")

    sets[name].append({"fi": finnish, "en": english})
    save_sets(sets)
    print("Word added!")

def show_sets():
    sets = load_sets()
    if not sets:
        print("No sets created yet.")
        return

    for name, words in sets.items():
        print(f"\n{name}:")
        for w in words:
            print(f"  {w['fi']} → {w['en']}")