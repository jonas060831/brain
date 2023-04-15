from flask import request, make_response
from application import app, db
from datetime import datetime
from pydictionary import Dictionary
import pytz
import json
import random

from application.helpers.find_similar import find_similar
from application.helpers.answer_question import answer_question

@app.route("/web/ask/aarlo", methods=["GET","POST"])
def aarlo():
    if request.method == 'POST':
        answer = ''
        #question from userk kkmn000
        user_question = request.json['question']
        user_timezone = request.json['timezone']

        #the closest match from the training data
        similar = find_similar(user_question)

        if similar['index'] == 0:
            # Get the current time in the user's time zone
            tz = pytz.timezone(user_timezone) # Replace with the user's time zone
            current_time = datetime.now(tz).strftime('%I:%M %p')
            answer = current_time

        elif similar['index'] == 1:

            list_word = user_question.split()
            list_len = len(list_word)
            word_query = list_word[list_len - 1]

            dict = Dictionary(word_query)

            #the list of meaning
            word_meaning = dict.meanings()

            word_synonyms = dict.synonyms()

            type_of_answer = [
            f"Meaning of the word.... {word_query}.......... {word_meaning}",
            f"{word_query}.......... {word_meaning}",
            f"one Meaning of the word.....{word_query}.......... {word_meaning[random.randint(0,len(dict.meanings()) - 1)]}",
            f"{word_synonyms}"
            ]

            answer = type_of_answer[random.randint(0,3)]

        else:
            answer = answer_question(similar['question'], similar['context'])

        response = make_response({ "answer" : answer }, 200)
        return response

    response = make_response({"message": "There is something wrong with the Request"}, 400)
    
    return response
