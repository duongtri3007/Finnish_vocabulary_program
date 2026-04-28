from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import json
import os
import random

# --- PATH CONFIGURATION ---
VOCAB_FILE = os.path.join(settings.BASE_DIR, 'vocab.json')
# We look for the folder where your themed JSONs are
SETS_DIR = os.path.join(settings.BASE_DIR, 'src', 'vocab_sets')

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
    """UPDATED: Returns the actual filenames in the vocab_sets folder."""
    if not os.path.exists(SETS_DIR):
        os.makedirs(SETS_DIR)
        return []
    
    # Get all .json files and remove the extension for the ID/Title
    sets = [
        f.replace('.json', '') 
        for f in os.listdir(SETS_DIR) 
        if f.endswith('.json')
    ]
    return sorted(sets)

def get_words_from_set(set_id):
    """UPDATED: Loads words using the string ID (filename)."""
    file_path = os.path.join(SETS_DIR, f"{set_id}.json")
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


# --- DATA SERVICES (Review & Games Logic) ---

def get_flashcards_data(vocab_list):
    """Shuffles the provided list for randomized review sessions."""
    if not vocab_list:
        return []
    word_list = list(vocab_list) 
    random.shuffle(word_list)
    return word_list

def generate_quiz_data(vocab_list, limit=10):
    """Generates quiz data using the provided vocabulary list."""
    if not vocab_list or len(vocab_list) < 4:
        return None

    quiz_data = []
    questions = random.sample(vocab_list, min(len(vocab_list), limit))

    for item in questions:
        fi = item.get('fi')
        en = item.get('en')
        img = item.get('image', '')
        ex = item.get('example', '')
        
        other_meanings = [w['en'] for w in vocab_list if w['en'] != en]
        
        # Ensure we don't crash if user has exactly 4 words
        num_distractors = min(len(other_meanings), 3)
        wrong_options = random.sample(other_meanings, num_distractors)
        
        options = wrong_options + [en]
        random.shuffle(options)
        
        quiz_data.append({
            'question': fi,
            'correct': en,
            'options': options,
            'image': img,
            'example': ex
        })
    return quiz_data

def backend_status(request):
    return HttpResponse("Backend Logic Engine is Running (Themed JSON Support Active)")