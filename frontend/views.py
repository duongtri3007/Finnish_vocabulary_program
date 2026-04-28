from django.shortcuts import render, redirect
from django.http import HttpResponse

# These now expect a list to be passed to them
from backend.views import (
    save_vocab, # Keep if you still want to save to JSON locally
    get_flashcards_data, 
    generate_quiz_data,
    get_vocabulary_sets_list,
    get_words_from_set
)

def main_menu(request):
    options = ["Add new words", "Review all words", "Show all words", "Vocabulary sets", "Exit"]
    return render(request, 'frontend/template_web.html', {'options': options})

def show_words(request):
    """UPDATED: Gets list from SESSION instead of load_vocab()"""
    word_list = request.session.get('user_vocabulary', []) 
    return render(request, 'frontend/words_list.html', {'vocabulary': word_list})

def add_word(request):
    """UPDATED: Saves to SESSION to keep users isolated"""
    if request.method == "POST":
        fi = request.POST.get('finnish_word')
        en = request.POST.get('english_word')
        img_url = request.POST.get('image_url')
        example = request.POST.get('example_text')
        
        if fi and en:
            # Get current private list
            vocab_list = request.session.get('user_vocabulary', [])
            
            new_entry = {
                "fi": fi, "en": en,
                "image": img_url if img_url else "",
                "example": example if example else ""
            }
            
            vocab_list.append(new_entry)
            
            # Save back to private session
            request.session['user_vocabulary'] = vocab_list
            request.session.modified = True 
            
            return render(request, 'frontend/add_word.html', {'saved': True})
            
    return render(request, 'frontend/add_word.html')

# --- Learning & Review Modes (The Big Changes) ---

def review_flashcards(request):
    """UPDATED: Passes session data to the backend shuffle engine"""
    user_list = request.session.get('user_vocabulary', [])
    
    if not user_list:
        return HttpResponse("Your personal list is empty! Add words first.")
    
    # We pass the list HERE
    words = get_flashcards_data(user_list)
    return render(request, 'frontend/flashcards.html', {'words': words})

def review_quiz(request):
    """UPDATED: Passes session data to the backend quiz generator"""
    user_list = request.session.get('user_vocabulary', [])
    
    # We pass the list HERE
    quiz_data = generate_quiz_data(user_list)
    
    if quiz_data is None:
        return HttpResponse("Please add at least 4 words to your list to start a quiz!")
        
    return render(request, 'frontend/quiz.html', {'quiz_data': quiz_data})

# --- Vocabulary Sets (Stay the same because they are read-only) ---

def vocabulary_sets_menu(request):
    sets = get_vocabulary_sets_list()
    return render(request, 'frontend/vocabulary_sets.html', {'sets': sets})

def view_set_detail(request, set_id):
    words = get_words_from_set(set_id)
    return render(request, 'frontend/word_set.html', {
        'vocabulary': words,
        'set_title': f"Vocabulary Set {set_id}"
    })

def review_options(request):
    """Page to choose between Flashcards or Quiz."""
    # This view just shows the menu to choose Flashcards or Quiz
    return render(request, 'frontend/review_options.html')