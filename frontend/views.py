from django.shortcuts import render, redirect
from django.http import HttpResponse

# IMPORT the updated logic from your backend views
from backend.views import (
    load_vocab, 
    save_vocab, 
    get_flashcards_data, 
    generate_quiz_data,
    get_vocabulary_sets_list,  # New
    get_words_from_set         # New
)

def main_menu(request):
    # These options should match the links in your template_web.html
    options = ["Add new words", "Review all words", "Show all words", "Vocabulary sets", "Exit"]
    return render(request, 'frontend/template_web.html', {'options': options})

def show_words(request):
    # load_vocab now returns: [{"fi": "koira", "en": "dog"}, ...]
    word_list = load_vocab() 
    return render(request, 'frontend/words_list.html', {'vocabulary': word_list})

def add_word(request):
    if request.method == "POST":
        fi = request.POST.get('finnish_word')
        en = request.POST.get('english_word')
        
        if fi and en:
            # 1. Load the existing data (which will now be a list)
            vocab_list = load_vocab()
            
            # 2. Ensure it is a list (in case the file was empty or old format)
            if not isinstance(vocab_list, list):
                vocab_list = []
            
            # 3. Create the new word object
            new_entry = {
                "fi": fi,
                "en": en
            }
            
            # 4. Append to the list
            vocab_list.append(new_entry)
            
            # 5. Save the updated list back to vocab.json
            save_vocab(vocab_list)
            
            return redirect('main_menu')
            
    return render(request, 'frontend/add_word.html')

# --- NEW: Vocabulary Sets Views ---

def vocabulary_sets_menu(request):
    """Displays the grid of 20 numbered boxes."""
    sets = get_vocabulary_sets_list()
    return render(request, 'frontend/vocabulary_sets.html', {'sets': sets})

def view_set_detail(request, set_id):
    """Displays the list of words for a specific set ID (1-20)."""
    words = get_words_from_set(set_id)
    # We reuse words_list.html but pass a specific title
    return render(request, 'frontend/words_list.html', {
        'vocabulary': words,
        'set_title': f"Vocabulary Set {set_id}"
    })

# --- Review & Games ---

def review_options(request):
    return render(request, 'frontend/review_options.html')

def review_flashcards(request):
    # Ask backend for prepared flashcards
    words = get_flashcards_data()
    if not words:
        return HttpResponse("Your dictionary is empty!")
    return render(request, 'frontend/flashcards.html', {'words': words})

def review_quiz(request):
    # Ask backend to generate quiz logic
    quiz_data = generate_quiz_data()
    if quiz_data is None:
        return HttpResponse("Add at least 4 words to start the quiz!")
    return render(request, 'frontend/quiz.html', {'quiz_data': quiz_data})