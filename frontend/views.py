from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
import os
from django.conf import settings
import random
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
    
def review_options(request):
    """Displays the selection menu: Flashcard or Multiple Choice"""
    return render(request, 'frontend/review_options.html')

def review_flashcards(request):
    """Retrieves data from vocab.json for Flashcards"""
    vocab = load_vocab()  # Uses your existing load_vocab function
    # Convert dict {fi: vi} into a list of pairs for easy looping in HTML
    word_list = [{'fi': fi, 'vi': vi} for fi, vi in vocab.items()]
    random.shuffle(word_list) # Randomize word order
    
    return render(request, 'frontend/flashcards.html', {'words': word_list})

def review_quiz(request):
    """Logic to generate a multiple-choice quiz from vocab.json"""
    vocab = load_vocab()
    all_words = list(vocab.items()) # List of tuples (fi, vi)
    
    if len(all_words) < 4:
        return HttpResponse("You need at least 4 words in your dictionary to play the quiz!")

    quiz_data = []
    # Get a maximum of 10 random questions
    sample_size = min(len(all_words), 10)
    questions = random.sample(all_words, sample_size)

    for fi, vi in questions:
        # Get 3 wrong Vietnamese meanings (different from the current correct one)
        other_meanings = [v for f, v in all_words if v != vi]
        wrong_options = random.sample(other_meanings, 3)
        
        # Combine correct and wrong answers, then shuffle them
        options = wrong_options + [vi]
        random.shuffle(options)
        
        quiz_data.append({
            'question': fi,
            'correct': vi,
            'options': options
        })

    return render(request, 'frontend/quiz.html', {'quiz_data': quiz_data})