from flask import Flask, render_template, request, redirect, flash
import spacy

from functions import Counter

app = Flask(__name__)
app.secret_key = 'text mining'

nlp = spacy.load('fr_core_news_sm')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        raw_text = request.files['doc']
        
        if not 'text' in raw_text.mimetype:
            flash('Veuillez choisir un fichier texte')
            return render_template('index.html')

        text_lines = [line.decode() for line in raw_text]
        
        if len(text_lines) == 0:
            flash('Veuillez choisir un fichier')
            return render_template('index.html')
        
        counter = Counter(text_lines, nlp)
        return render_template(
            'index.html',
            text=text_lines,
            filename=raw_text.filename,
            keywords_only=[tuple_[0] for tuple_ in counter.get_keywords()],
            results={
                "nombre d'espaces": counter.spaces(),
                "nombre de mots": counter.words(),
                "nombre de charactères": counter.characters(),
                "keywords": counter.get_keywords(),
                "nombres de phrases": counter.sentences(),
                "verbs": counter.find_verbs(),
            })