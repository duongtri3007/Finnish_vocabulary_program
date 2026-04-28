import os
import json
import httpx
import random
from fastapi import FastAPI, HTTPException

# --- CONFIGURATION ---
UNSPLASH_KEY = 'BAzazffKq-eqECErlrhZhd1aKOiGmwSX_TKJjt5T20o'
FOLDER_NAME = 'vocab_sets'

app = FastAPI()

@app.post("/add-word/{theme_name}")
async def add_single_word(theme_name: str, fin_word: str):
    file_path = os.path.join(FOLDER_NAME, f"{theme_name}.json")
    
    async with httpx.AsyncClient() as client:
        # 1. Get Translation
        t_url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=fi&tl=en&dt=t&q={fin_word}"
        t_res = await client.get(t_url)
        if t_res.status_code != 200 or not t_res.content:
            raise HTTPException(status_code=502, detail=f"Translation API failed: {t_res.status_code}")
        eng_word = t_res.json()[0][0][0]

        # 2. Get Image
        u_url = f"https://api.unsplash.com/search/photos?query={eng_word}&client_id={UNSPLASH_KEY}&per_page=1"
        u_res = await client.get(u_url)
        
        img_url = "no_image"
        if u_res.status_code == 200 and u_res.content:
            u_data = u_res.json()
            img_url = u_data['results'][0]['urls']['small'] if u_data.get('results') else "no_image"
        else:
            print(f"Unsplash API failed: status={u_res.status_code}, body={u_res.text[:200]}")

        # 3. Sentence Search (Tatoeba)
        fin_sentence = f"Tässä on {fin_word}."
        eng_sentence = f"This is a {eng_word}."

        try:
            tato_url = f"https://tatoeba.org/en/api_v0/search/display?query={fin_word}&from=fin&to=eng"
            tato_res = await client.get(tato_url, timeout=5.0)
            
            if tato_res.status_code == 200:
                results = tato_res.json().get('results', [])
                if results:
                    choice = random.choice(results[:5])
                    fin_sentence = choice.get('text', fin_sentence)
                    
                    for trans_group in choice.get('translations', []):
                        for t in trans_group:
                            if t.get('lang') == 'eng':
                                eng_sentence = t.get('text', eng_sentence)
                                break
        except Exception as e:
            print(f"Sentence API Error: {e}")

    # --- SAVE LOGIC ---
    new_entry = {
        "fi": fin_word,
        "en": eng_word,
        "image": img_url,
        "sentence_fi": fin_sentence,
        "sentence_en": eng_sentence
    }

    os.makedirs(FOLDER_NAME, exist_ok=True)
    data_list = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data_list = json.load(f)
            except:
                data_list = []

    data_list.append(new_entry)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)
    
    return {"status": "success", "added": fin_word, "image": img_url, "sentence": fin_sentence}