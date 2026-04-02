import json
import os

filename = "vocab.json"

def load_vocab():
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump({}, f)

    with open(filename, "r") as f:
        return json.load(f)

def save_vocab(vocab):
    with open(filename, "w") as f:
        json.dump(vocab, f, indent=4)

def add_words():
    vocab = load_vocab()
    print("\nAdd New Vocabulary")
    print("Type 'done' to return to menu.")

    while True:
        finnish = input("Finnish word: ")
        if finnish.lower() == "done":
            break

        english = input("English meaning: ")
        vocab[finnish] = english
        save_vocab(vocab)
        print("Saved!")

def show_all_words():
    vocab = load_vocab()
    if not vocab:
        print("No words saved yet.")
        return

    print("\n=== All Words ===")
    for fi, en in vocab.items():
        print(f"{fi} → {en}")

def review_words():
    import random
    vocab = load_vocab()

    if not vocab:
        print("No words to review.")
        return

    finnish = random.choice(list(vocab.keys()))
    answer = input(f"What does '{finnish}' mean? ")

    if answer.lower() == vocab[finnish].lower():
        print("Correct!")
    else:
        print(f"Wrong. It means: {vocab[finnish]}")
