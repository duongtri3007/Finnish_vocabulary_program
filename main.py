from src.vocab import add_words, review_words, show_all_words
from src.sets import manage_sets


def main():
    while True:
        print("\n=== Finnish Vocabulary Program ===")
        print("1. Add new words")
        print("2. Review all words")
        print("3. Show all words")
        print("4. Vocabulary sets")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_words()
        elif choice == "2":
            review_words()
        elif choice == "3":
            show_all_words()
        elif choice == "4":
            manage_sets()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

main()
