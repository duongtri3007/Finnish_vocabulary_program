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
    """Reads JSON file. Returns a LIST of objects."""
    if not os.path.exists(VOCAB_FILE):
        return []
    with open(VOCAB_FILE, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []

def save_vocab(vocab):
    """Writes list to JSON file."""
    with open(VOCAB_FILE, 'w', encoding='utf-8') as f:
        json.dump(vocab, f, indent=4, ensure_ascii=False)


# --- VOCABULARY SETS SERVICES ---

def get_vocabulary_sets_list():
    """Returns a list of IDs for the vocabulary sets."""
    if not os.path.exists(SETS_DIR):
        os.makedirs(SETS_DIR)
    return [str(i) for i in range(1, 21)]

def get_words_from_set(set_id):
    """Loads words from a specific numbered set file."""
    file_path = os.path.join(SETS_DIR, f"{set_id}.json")
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


# --- DATA SERVICES (Review & Games Logic) ---

def get_flashcards_data():
    """Shuffles the vocab list for randomized review sessions."""
    vocab_list = load_vocab()
    word_list = list(vocab_list) 
    random.shuffle(word_list)
    return word_list

def generate_quiz_data(limit=10):
    """Logic updated to include image and example data for each question."""
    all_words = load_vocab()
    
    if len(all_words) < 4:
        return None

    quiz_data = []
    # Pick random entries
    questions = random.sample(all_words, min(len(all_words), limit))

    for item in questions:
        fi = item['fi']
        en = item['en']
        # --- NEW: Extract image and example for the quiz UI ---
        img = item.get('image', '')
        ex = item.get('example', '')
        
        # Get 3 wrong answers from other words
        other_meanings = [w['en'] for w in all_words if w['en'] != en]
        wrong_options = random.sample(other_meanings, min(len(other_meanings), 3))
        
        options = wrong_options + [en]
        random.shuffle(options)
        
        quiz_data.append({
            'question': fi,
            'correct': en,
            'options': options,
            'image': img,      # Sent to quiz.html
            'example': ex      # Sent to quiz.html
        })
    return quiz_data

def backend_status(request):
    return HttpResponse("Backend Logic Engine is Running (List Format Active)")