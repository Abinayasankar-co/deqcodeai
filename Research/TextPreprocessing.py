import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from rake_nltk import Rake
from sklearn.feature_extraction.text import TfidfVectorizer

# Download necessary NLTK resources
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

class TextProcessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words("english"))
        self.rake = Rake()

    def preprocess(self, text:str):
        """Applies text preprocessing techniques."""
        text = text.lower()
        text = re.sub(r'\s+', ' ', text)  
        text = re.sub(r'[^\w\s]', '', text)  
        tokens = word_tokenize(text) 
        tokens = [word for word in tokens if word not in self.stop_words] 
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens]  
        return " ".join(tokens)

    def extract_keyphrases_rake(self, text):
        """Extracts key phrases using RAKE."""
        self.rake.extract_keywords_from_text(text)
        return self.rake.get_ranked_phrases()[:5] 

    def extract_keyphrases_tfidf(self, text, corpus):
        """Extracts key phrases using TF-IDF."""
        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform(corpus)
        feature_names = vectorizer.get_feature_names_out()
        scores = tfidf_matrix.toarray()[0]
        sorted_indices = scores.argsort()[::-1]
        top_keywords = [feature_names[i] for i in sorted_indices[:5]]
        return top_keywords

# Example Usage
if __name__ == "__main__":
    text = "Natural Language Processing is an exciting field of artificial intelligence."
    processor = TextProcessor()

    clean_text = processor.preprocess(text)
    print("Preprocessed Text:", clean_text)

    rake_keywords = processor.extract_keyphrases_rake(clean_text)
    print("RAKE Keyphrases:", rake_keywords)

    corpus = [text]  
    tfidf_keywords = processor.extract_keyphrases_tfidf(clean_text, corpus)
    print("TF-IDF Keyphrases:", tfidf_keywords)
