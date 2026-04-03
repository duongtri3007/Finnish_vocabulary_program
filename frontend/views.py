from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
import os
from django.conf import settings
# Create your views here.from django.shortcuts import render

def main_menu(request):
    # We define the options as a list so the HTML can loop through them
    options = [
        "Add new words",
        "Review all words",
        "Show all words",
        "Vocabulary sets",
        "Exit"
    ]
    return render(request, 'frontend/template_web.html', {'options': options})

def show_words(request):
    # This finds your vocab.json in your main project folder
    json_path = os.path.join(settings.BASE_DIR, 'vocab.json')

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            vocab_data = json.load(f)
    except FileNotFoundError:
        vocab_data = [] # If file doesn't exist yet, send empty list

    return render(request, 'frontend/words_list.html', {'vocabulary': vocab_data})

# This tells Django exactly where your vocab.json is located
VOCAB_FILE = os.path.join(settings.BASE_DIR, 'vocab.json')

def load_vocab():
    if not os.path.exists(VOCAB_FILE):
        return {}
    with open(VOCAB_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_vocab(vocab):
    with open(VOCAB_FILE, 'w', encoding='utf-8') as f:
        json.dump(vocab, f, indent=4)

# Your existing add_word function comes after these...
def add_word(request):
    if request.method == "POST":
        fi = request.POST.get('finnish_word')
        en = request.POST.get('english_word')
        
        if fi and en:
            vocab = load_vocab()  # Now it will find the function above!
            vocab[fi] = en
            save_vocab(vocab)
            return redirect('main_menu')
            
    return render(request, 'frontend/add_word.html')