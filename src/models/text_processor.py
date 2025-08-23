"""
Text processing utilities adapted from Streamlit version
"""

import re
import pandas as pd
from typing import List, Dict, Set, Optional
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

class TextProcessor:
    """Text processing utilities for analysis"""
    
    def __init__(self):
        self.stop_words = self._setup_nltk()
    
    def _setup_nltk(self) -> Set[str]:
        """Setup NLTK data and return stopwords"""
        try:
            try:
                nltk.data.find('tokenizers/punkt_tab')
            except LookupError:
                try:
                    nltk.data.find('tokenizers/punkt')
                except LookupError:
                    try:
                        nltk.download('punkt_tab', quiet=True)
                    except:
                        nltk.download('punkt', quiet=True)

            try:
                nltk.data.find('corpora/stopwords')
            except LookupError:
                nltk.download('stopwords', quiet=True)
                
            return set(stopwords.words('english'))
        except:
            # Fallback stopwords if NLTK fails
            return {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    
    def preprocess_text(self, text: str) -> str:
        """Basic text preprocessing"""
        text = text.replace("U.S.A.", "USA").replace("U.S.", "US")
        return text
    
    def tokenize_sentences(self, text: str) -> List[str]:
        """Tokenize text into sentences"""
        try:
            sentences = sent_tokenize(self.preprocess_text(text))
            return [s for s in sentences if s.strip()]
        except:
            # Fallback tokenization
            sentences = re.split(r'[.!?]+', self.preprocess_text(text))
            return [s.strip() for s in sentences if s.strip()]
    
    def clean_text(self, sentences: List[str]) -> List[Dict]:
        """Clean and process sentences"""
        cleaned_sentences = []
        for i, sentence in enumerate(sentences):
            try:
                text = sentence.lower()
                text = re.sub(r'[^\w\s]', '', text)
                words = text.split()
                words = [word for word in words if word and word not in self.stop_words and len(word) > 1]

                if words:
                    cleaned_sentences.append({
                        'sentence_id': i + 1,
                        'text': ' '.join(words),
                        'original': sentence
                    })
            except:
                continue

        return cleaned_sentences
    
    def generate_ngrams(self, cleaned_sentences: List[Dict], n: int) -> List[Dict]:
        """Generate n-grams from cleaned sentences"""
        ngrams = []
        for sentence in cleaned_sentences:
            words = sentence['text'].split()
            if len(words) >= n:
                for i in range(len(words) - n + 1):
                    ngram = ' '.join(words[i:i + n])
                    if ngram.strip():
                        ngrams.append({
                            'sentence_id': sentence['sentence_id'],
                            'ngram': ngram
                        })
        return ngrams
    
    def analyze_text(self, text_input: str, lexicon: pd.DataFrame) -> pd.DataFrame:
        """Analyze text against lexicon"""
        if not text_input or not text_input.strip():
            return pd.DataFrame({'Text': ['No text provided']})

        sentences = self.tokenize_sentences(text_input)
        if not sentences:
            return pd.DataFrame({'Text': ['No sentences found']})

        cleaned_sentences = self.clean_text(sentences)
        if not cleaned_sentences:
            return pd.DataFrame({'Text': sentences})

        # Generate n-grams
        all_ngrams = (self.generate_ngrams(cleaned_sentences, 1) + 
                     self.generate_ngrams(cleaned_sentences, 2) + 
                     self.generate_ngrams(cleaned_sentences, 3))

        if all_ngrams:
            ngrams_df = pd.DataFrame(all_ngrams)
        else:
            ngrams_df = pd.DataFrame(columns=['sentence_id', 'ngram'])

        results = {'Text': sentences}

        if lexicon.empty:
            return pd.DataFrame(results)

        # Process each entity
        for entity in lexicon['Entity'].unique():
            keywords = lexicon[lexicon['Entity'] == entity]['Keyword'].tolist()
            keywords = [str(k).lower() for k in keywords if pd.notna(k)]

            entity_matches = []

            for i, sentence in enumerate(sentences):
                sentence_id = i + 1

                if not ngrams_df.empty:
                    sentence_ngrams = ngrams_df[ngrams_df['sentence_id'] == sentence_id]['ngram'].tolist()
                else:
                    sentence_ngrams = []

                match = 1 if any(ngram in keywords for ngram in sentence_ngrams) else 0
                entity_matches.append(match)

            results[entity] = entity_matches

        return pd.DataFrame(results)