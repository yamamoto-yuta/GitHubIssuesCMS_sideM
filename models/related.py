import re
import json
import os

from sudachipy import tokenizer
from sudachipy import dictionary
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

from const import CONSTS_DIR 

class Related():
    def __init__(self, articles, k=4):
        self._compile_re()
        self.tokenizer = dictionary.Dictionary().create()
        self.texts = [self._make_text(article) for article in articles]
        self.slugs = np.array([article.slug for article in articles])
        self.vectorizer = TfidfVectorizer(tokenizer=self._tokenize)
        self.k = k
    
    def _make_text(self, article):
        title = article.title
        markdown = article.markdown
        description = article.description
        text = f'{title} {markdown} {description}'
        text = self._cleaning_text(text)
        return text

    def _compile_re(self):
        self.clean_pattern = []
        self.clean_pattern += [re.compile(r"!\[.*\]\(https?://[a-zA-Z\d!\?/\+\-_~=;\.,\*&@#\$%\(\)'\[\]]+\)")]
        self.clean_pattern += [re.compile(r"\[.*\]\(https?://[a-zA-Z\d!\?/\+\-_~=;\.,\*&@#\$%\(\)'\[\]]+\)")]
        self.clean_pattern += [re.compile(r"https?://[a-zA-Z\d!\?/\+\-_~=;\.,\*&@#\$%\(\)'\[\]]+")]

    def _cleaning_text(self, text):
        for pattern in self.clean_pattern:
            text = pattern.sub('', text)
        return text

    def _tokenize(self, text):
        mode = tokenizer.Tokenizer.SplitMode.B
        text = [m.normalized_form() for m in self.tokenizer.tokenize(text, mode) if not self._is_stopword(m.part_of_speech())]
        return text

    def _is_stopword(self, part_of_speech):
        stopwords_main =  ['助詞', '助動詞', '記号', '補助記号']
        stopwords_sub = ['非自立可能']
        is_stop = part_of_speech[0] in stopwords_main
        is_stop = is_stop or part_of_speech[1] in stopwords_sub
        return is_stop

    def _tfidf(self):
        X = self.vectorizer.fit_transform(self.texts)
        X = X.toarray()
        return X

    def _score(self, X):
        X = X.dot(X.T)
        """ 自身との類似度を無限大にし、スライスで確実に除去できるようにする """
        X[range(X.shape[0]), range(X.shape[1])] = np.inf
        return X
        
    def _sort_slugs_by_score(self, scores):
        sorted_index = np.argsort(scores, axis=0)[::-1].T
        slugs_dict = {}
        for i, index in enumerate(sorted_index):
            slug = self.slugs[i]
            slugs = self.slugs[index][1:self.k+1]
            slugs_dict[slug] = list(slugs)
        return slugs_dict

    def get_related(self):
        X = self._tfidf()
        scores = self._score(X)
        slugs = self._sort_slugs_by_score(scores)
        return slugs

    def save(self, slugs):
        if not os.path.exists(CONSTS_DIR):
            os.makedirs(CONSTS_DIR)
        with open(f'{CONSTS_DIR}/related.json', 'w', encoding="utf-8") as f:
            json.dump(slugs, f, indent=4, ensure_ascii=False)


