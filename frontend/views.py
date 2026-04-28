from django.shortcuts import render, redirect
from django.http import HttpResponse
import urllib.parse

# Importing backend logic
from backend.views import (
    save_vocab, 
    get_flashcards_data, 
    generate_quiz_data,
    get_vocabulary_sets_list,
    get_words_from_set
)

def main_menu(request):
    """Main landing page."""
    options = ["Add new words", "Review all words", "Show all words", "Vocabulary sets", "Exit"]
    return render(request, 'frontend/template_web.html', {'options': options})

def show_words(request):
    """Displays the personal list from session."""
    word_list = request.session.get('user_vocabulary', []) 
    return render(request, 'frontend/words_list.html', {'vocabulary': word_list})

def add_word(request):
    """Saves words to session."""
    if request.method == "POST":
        fi = request.POST.get('finnish_word')
        en = request.POST.get('english_word')
        img_url = request.POST.get('image_url')
        example = request.POST.get('example_text')
        
        if fi and en:
            vocab_list = request.session.get('user_vocabulary', [])
            new_entry = {
                "fi": fi, "en": en,
                "image": img_url if img_url else "",
                "example": example if example else ""
            }
            vocab_list.append(new_entry)
            request.session['user_vocabulary'] = vocab_list
            request.session.modified = True 
            return render(request, 'frontend/add_word.html', {'saved': True})
            
    return render(request, 'frontend/add_word.html')

# --- Learning & Review Modes (Persistence Logic) ---

def review_options(request):
    """
    Selection menu. It captures 'set_name' from the URL 
    and passes it to the template to build the next links.
    """
    set_name = request.GET.get('set_name')
    return render(request, 'frontend/review_options.html', {'set_name': set_name})

def review_flashcards(request):
    """Reviews words via Flashcards while maintaining set context."""
    set_name = request.GET.get('set_name')
    
    if set_name:
        data_source = get_words_from_set(set_name)
    else:
        data_source = request.session.get('user_vocabulary', [])
    
    if not data_source:
        return HttpResponse(f"No words found for: {set_name if set_name else 'Personal Words'}")
    
    words = get_flashcards_data(data_source)
    return render(request, 'frontend/flashcards.html', {
        'words': words, 
        'set_name': set_name # Sent to HTML for the 'Back' button
    })

def review_quiz(request):
    """Reviews words via Quiz while maintaining set context."""
    set_name = request.GET.get('set_name')
    
    if set_name:
        data_source = get_words_from_set(set_name)
    else:
        data_source = request.session.get('user_vocabulary', [])
    
    if not data_source or len(data_source) < 4:
        return HttpResponse("Need at least 4 words to start a quiz.")
    
    quiz_data = generate_quiz_data(data_source)
    return render(request, 'frontend/quiz.html', {
        'quiz_data': quiz_data, 
        'set_name': set_name # Sent to HTML for the 'Back' button
    })

# --- Vocabulary Sets ---

def vocabulary_sets_menu(request):
    sets = get_vocabulary_sets_list()
    return render(request, 'frontend/vocabulary_sets.html', {'sets': sets})

def view_set_detail(request, set_id):
    """Viewing specific set details."""
    words = get_words_from_set(set_id)
    return render(request, 'frontend/word_set.html', {
        'vocabulary': words,
        'set_title': set_id, 
        'set_id': set_id
    })