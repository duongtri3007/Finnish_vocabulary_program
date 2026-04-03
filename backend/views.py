from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import json
import os
import random

# --- PATH CONFIGURATION ---
VOCAB_FILE = os.path.join(settings.BASE_DIR, 'vocab.json')
SETS_DIR = os.path.join(settings.BASE_DIR, 'vocab_sets')

# --- DATA ENGINE ---

def load_vocab():
    """Reads JSON file. Now returns a LIST of objects."""
    if not os.path.exists(VOCAB_FILE):
        return [] # Changed from {} to []
    with open(VOCAB_FILE, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return [] # Changed from {} to []

def save_vocab(vocab):
    """Writes list to JSON file."""
    with open(VOCAB_FILE, 'w', encoding='utf-8') as f:
        json.dump(vocab, f, indent=4, ensure_ascii=False)


# --- VOCABULARY SETS SERVICES ---

def get_vocabulary_sets_list():
    if not os.path.exists(SETS_DIR):
        os.makedirs(SETS_DIR)
    return [str(i) for i in range(1, 21)]

def get_words_from_set(set_id):
    file_path = os.path.join(SETS_DIR, f"{set_id}.json")
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


# --- DATA SERVICES (Updated for List Format) ---

def get_flashcards_data():
    """Since vocab is already a list, we just shuffle it."""
    vocab_list = load_vocab()
    # Create a copy so we don't shuffle the actual database file order
    word_list = list(vocab_list) 
    random.shuffle(word_list)
    return word_list

def generate_quiz_data(limit=10):
    """Logic updated to handle list of dictionaries."""
    all_words = load_vocab() # Now a list of {'fi':..., 'en':...}
    
    if len(all_words) < 4:
        return None

    quiz_data = []
    # Pick random entries from the list
    questions = random.sample(all_words, min(len(all_words), limit))

    for item in questions:
        fi = item['fi']
        en = item['en']
        
        # Get 3 wrong answers from the rest of the list
        other_meanings = [w['en'] for w in all_words if w['en'] != en]
        wrong_options = random.sample(other_meanings, min(len(other_meanings), 3))
        
        options = wrong_options + [en]
        random.shuffle(options)
        
        quiz_data.append({
            'question': fi,
            'correct': en,
            'options': options
        })
    return quiz_data

def backend_status(request):
    return HttpResponse("Backend Logic Engine is Running (List Format Active)")