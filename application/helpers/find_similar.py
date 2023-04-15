import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#read json file
with open('application/training.json') as f:
    data = json.load(f)


arrayofquestions = [None] * len(data)

for i in range(0, len(data)):
    arrayofquestions[i] = data[i]['question']

def find_similar(question):
    # Compute the TF-IDF vectors for the questions
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(arrayofquestions)
    # Compute the cosine similarity matrix between the questions
    similarity_matrix = cosine_similarity(tfidf_matrix)

    # Example usage: find questions that are similar to what user gave
    query = question
    query_vector = tfidf_vectorizer.transform([query])
    similarity_scores = cosine_similarity(query_vector, tfidf_matrix).flatten()

    # Get the top most similar questions
    similar_indices = similarity_scores.argsort()[::-1]
    similar_questions = [arrayofquestions[i] for i in similar_indices]

    return { 'index' : similar_indices[0], 'question' : similar_questions[0], 'context' : data[similar_indices[0]]['context'] }
