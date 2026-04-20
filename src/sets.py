import os
import json
import httpx
from fastapi import FastAPI

app = FastAPI()

# 1. Configuration
FOLDER_NAME = "vocab_sets"
UNSPLASH_KEY = "BAzazffKq-eqECErlrhZhd1aKOiGmwSX_TKJjt5T20o"

# Ensure the folder exists so the code doesn't crash
if not os.path.exists(FOLDER_NAME):
    os.makedirs(FOLDER_NAME)

@app.post("/add-word/{theme_name}")
async def add_single_word(theme_name: str, fin_word: str):
    # Determine the file path (e.g., vocab_sets/animals.json)
    file_path = os.path.join(FOLDER_NAME, f"{theme_name}.json")
    
    async with httpx.AsyncClient() as client:
        # --- PHASE 1: AI Data Retrieval ---
        
        # A. Get English Translation
        t_url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=fi&tl=en&dt=t&q={fin_word}"
        t_res = await client.get(t_url)
        eng_word = t_res.json()[0][0][0]

        # B. Get Unsplash Image
        u_url = f"https://api.unsplash.com/search/photos?query={eng_word}&client_id={UNSPLASH_KEY}&per_page=1"
        u_res = await client.get(u_url)
        u_data = u_res.json()
        img_url = u_data['results'][0]['urls']['small'] if u_data['results'] else "no_image_found"

        # C. Get Finnish Example Sentence (via English Context)
        scenario = f"The {eng_word} is very important here."
        s_url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=fi&dt=t&q={scenario}"
        s_res = await client.get(s_url)
        fin_sentence = s_res.json()[0][0][0]

    # --- PHASE 2: Packing and Storing ---

    # Create the new word object
    new_entry = {
        "fi": fin_word,
        "en": eng_word,
        "image": img_url,
        "sentence": fin_sentence
    }

    # Load existing words if the file exists
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                vocab_list = json.load(f)
            except json.JSONDecodeError:
                vocab_list = []
    else:
        vocab_list = []

    # Add the new word to the list
    vocab_list.append(new_entry)

    # Save everything back to the folder
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(vocab_list, f, indent=4, ensure_ascii=False)

    return {"status": "success", "added": fin_word, "set": theme_name}

@app.get("/sets/{theme_name}")
async def get_set_content(theme_name: str):
    """Returns the words inside a specific theme file."""
    file_path = os.path.join(FOLDER_NAME, f"{theme_name}.json")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Theme set not found")
        
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    return data