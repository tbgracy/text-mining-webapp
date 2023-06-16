from typing import List
from collections import Counter as ctr

import spacy
import nltk


class Counter:
    def __init__(self, text: str):
        self.text_list = text
        self.raw_text_string = ' '.join(self.text_list)
        self.keywords = []
        self._load_stop_words()
        self.verbs = []

    def spaces(self) -> int:
        result = 0
        for line in self.text_list:
            result += line.count(' ')
        return result

    def is_word(string: str, word) -> bool:
        for char in word:
            if char.isalnum():
                return True
        return False

    def words(self) -> int:
        return len([
            word 
            for line in self.text_list 
            for word in line.split(' ')
            if self.is_word(word)
        ])

    def characters(self) -> int:
        return len([char for line in self.text_list for char in line])

    def get_keywords(self) -> List[str]:
        words = [
            word
            for line in self.text_list
            for word in line.split()
            if self.is_word(word) and word.lower() not in self.stopwords
        ]
        most_important_words = ctr(words)
        for i, keyword in enumerate(most_important_words.most_common(8)):
            keyword_value = keyword[0]
            keyword_frequency = (keyword[1] / self.words()) * 100
            self.keywords.append(
                (keyword_value, round(keyword_frequency, 3), keyword[1])
            )
        return self.keywords

    def _load_stop_words(self):
        # self.stopwords = set(nltk.corpus.stopwords.words('french'))
        with open('french_stopwords') as f:
            self.stopwords = [line.strip() for line in f]

    def count_frequency(self) -> int:
        pass

    def sentences(self) -> int:
        full_text = ' '.join(self.text_list)
        return len(full_text.split('.'))

    def paragraphs(self) -> int:
        pass

    def find_verbs(self)-> List[str]:
        nlp = spacy.load('fr_core_news_sm')
        tokens_from_spacy = nlp(self.raw_text_string)

        self.verbs = [
            str(word)
            for word in tokens_from_spacy
            if word.pos_ == 'VERB'
        ]

        return self.verbs

    def __repr__(self):
        return str({
            "spaces": self.spaces(),
            "words": self.words(),
            "characters": self.characters(),
        })


if __name__ == "__main__":
    filename = 'sample.txt'
    text_lines = [line.strip() for line in open(filename)]
    counter = Counter(text_lines)
    print(counter.is_word('..s.'))
    print(counter)
