from django.shortcuts import render, redirect
from django.http import HttpResponse

# IMPORT the updated logic from your backend views
from backend.views import (
    load_vocab, 
    save_vocab, 
    get_flashcards_data, 
    generate_quiz_data,
    get_vocabulary_sets_list,
    get_words_from_set
)

def main_menu(request):
    """Displays the main dashboard options."""
    options = ["Add new words", "Review all words", "Show all words", "Vocabulary sets", "Exit"]
    return render(request, 'frontend/template_web.html', {'options': options})

def show_words(request):
    """Displays the full list of vocabulary stored in vocab.json."""
    word_list = load_vocab() 
    return render(request, 'frontend/words_list.html', {'vocabulary': word_list})

def add_word(request):
    """Handles adding new words, including AI-generated images and examples."""
    if request.method == "POST":
        fi = request.POST.get('finnish_word')
        en = request.POST.get('english_word')
        
        # --- NEW: Capture AI-generated data from hidden inputs ---
        img_url = request.POST.get('image_url')
        example = request.POST.get('example_text')
        
        if fi and en:
            vocab_list = load_vocab()
            
            # Ensure the data is a list (handles empty files or old formats)
            if not isinstance(vocab_list, list):
                vocab_list = []
            
            # --- UPDATED: Create a rich data object ---
            new_entry = {
                "fi": fi,
                "en": en,
                "image": img_url if img_url else "",
                "example": example if example else ""
            }
            
            vocab_list.append(new_entry)
            save_vocab(vocab_list)
            
            # Re-render the page with a success flag for the UI
            return render(request, 'frontend/add_word.html', {'saved': True})
            
    return render(request, 'frontend/add_word.html')

# --- Vocabulary Sets Views ---

def vocabulary_sets_menu(request):
    """Displays the grid of available vocabulary sets (1-20)."""
    sets = get_vocabulary_sets_list()
    return render(request, 'frontend/vocabulary_sets.html', {'sets': sets})

def view_set_detail(request, set_id):
    """Displays words from a specific JSON set file."""
    words = get_words_from_set(set_id)
    return render(request, 'frontend/words_list.html', {
        'vocabulary': words,
        'set_title': f"Vocabulary Set {set_id}"
    })

# --- Learning & Review Modes ---

def review_options(request):
    """Page to choose between Flashcards or Quiz."""
    return render(request, 'frontend/review_options.html')

def review_flashcards(request):
    """Logic for the Flashcards study mode."""
    words = get_flashcards_data()
    if not words:
        return HttpResponse("Your dictionary is empty! Add words to start.")
    return render(request, 'frontend/flashcards.html', {'words': words})

def review_quiz(request):
    """Logic for the Multiple Choice Quiz."""
    quiz_data = generate_quiz_data()
    if quiz_data is None:
        return HttpResponse("Please add at least 4 words to generate a quiz!")
    return render(request, 'frontend/quiz.html', {'quiz_data': quiz_data})