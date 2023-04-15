import json
import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
from datetime import datetime
import random

#read json file
with open('application/training.json') as f:
    data = json.load(f)


# Load the pre-trained BERT model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
model = AutoModelForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad", return_dict=False)

# Define the function that will answer the question
def answer_question(question, context, num_tokens_before=50, num_tokens_after=50):
    input_dict = tokenizer.encode_plus(question, context, return_tensors='pt', padding=True, truncation=True)
    input_ids = input_dict['input_ids']
    token_type_ids = input_dict['token_type_ids']

    start_scores, end_scores = model(input_ids, token_type_ids=token_type_ids)

    all_tokens = tokenizer.convert_ids_to_tokens(input_ids[0])
    # answer_tokens = all_tokens[torch.argmax(start_scores) : torch.argmax(end_scores)+1]
    # answer = tokenizer.convert_tokens_to_string(answer_tokens)

    all_tokens = tokenizer.convert_ids_to_tokens(input_ids[0])
    answers = []
    for i, (start, end) in enumerate(zip(torch.argmax(start_scores, axis=1), torch.argmax(end_scores, axis=1))):
        answer_tokens = all_tokens[start : end+1]
        answer = tokenizer.convert_tokens_to_string(answer_tokens)
        answer_start_token = max(0, start - num_tokens_before)
        answer_end_token = min(len(all_tokens) - 1, end + num_tokens_after)
        answer_context_tokens = all_tokens[answer_start_token : answer_end_token + 1]
        answer_context = tokenizer.convert_tokens_to_string(answer_context_tokens)
        answer_with_context = answer_context.replace(answer, f"**{answer}**")
        answers.append(answer_with_context)

        #convenience code to get only the context in between [SEP]
        extracted_context = tokenizer.convert_tokens_to_string(all_tokens[answer_context_tokens.index("[SEP]"): answer_end_token + 1])
        #remove the string [SEP] and then remove white spaces in the beginning and end of the string
        newextractedcontext = (extracted_context.replace("[SEP]", '')).strip()
        #two answer type long one and short one
        answer_type = [newextractedcontext, answer]

    #randomize response between long and short
    return answer_type[random.randint(0,1)]
