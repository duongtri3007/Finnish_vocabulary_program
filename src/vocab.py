import requests

while True:
    theme = input("Which theme do you want? ")
    word = input("Please type in a word: ")

    if word == 0:
        print("Goodbye!")
        break

    else:
        response = requests.post(f"http://127.0.0.1:8000/add-word/{theme}", params={"fin_word": word})