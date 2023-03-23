import os
import yaml
from django.http import JsonResponse, HttpResponseBadRequest

# Load the YAML data into a dictionary
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'immature_phase.yml')

with open(DATA_FILE, 'r') as f:
    data = yaml.safe_load(f)

# Define the chatbot view
def chatbot(request):
    # Get the message from the request
    query = request.GET.get('query')

    # Make sure the query parameter is present and not empty
    if not query:
        response = 'Missing or empty "query" parameter'
        return JsonResponse({'Status': 400, 'data': {'response': response}, 'message': 'Unsuccess'})

    # Search for a matching intent and generate a response
    response = 'Sorry, I do not understand.'
    for intent in data['intents']:
        for pattern in intent['patterns']:
            # Check if all words in the query are present in the pattern
            if all(word.lower() in pattern.lower() for word in query.split()):
                response = intent['responses'][0]
                break
        if response != 'Sorry, I do not understand.':
            break

    # Return the response as JSON
    if response == 'Sorry, I do not understand.':
        return JsonResponse({'Status': 404, 'data': {'response': response}, 'message': 'Unsuccess'})
    else:
        return JsonResponse({'Status': 201, 'data': {'response': response}, 'message': 'Success'})
