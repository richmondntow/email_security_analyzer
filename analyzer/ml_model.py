import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

class EmailClassifier:
    def __init__(self, model_path="./models/nb_model.joblib"):
        self.model_path = model_path
        self.pipeline = None
        if os.path.exists(self.model_path):
            self.pipeline = joblib.load(self.model_path)

    def train_from_csv(self, csv_path, save=True):
        df = pd.read_csv(csv_path)
        df = df.fillna('')
        X = (df['subject'] + ' ' + df['body']).values
        y = df['label'].apply(lambda s: 1 if str(s).lower().strip() in ('phish','phishing','spam','malicious') else 0).values
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1,2))),
            ('clf', MultinomialNB())
        ])
        pipeline.fit(X_train, y_train)
        preds = pipeline.predict(X_test)
        acc = accuracy_score(y_test, preds)
        if save:
            os.makedirs(os.path.dirname(self.model_path) or '.', exist_ok=True)
            joblib.dump(pipeline, self.model_path)
        self.pipeline = pipeline
        return {'accuracy': float(acc)}

    def classify(self, text):
        if not self.pipeline:
            return ('unknown', 0.0)
        prob = self.pipeline.predict_proba([text])[0]
        pred = self.pipeline.predict([text])[0]
        confidence = max(prob)
        label = 'phish' if int(pred) == 1 else 'ham'
        return (label, float(confidence))