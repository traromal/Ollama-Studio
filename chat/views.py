import json
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

OLLAMA_API = "http://localhost:11434/api"

def chat_view(request):
    return render(request, 'chat/chat.html')

def get_models(request):
    response = requests.get(f"{OLLAMA_API}/tags")
    if response.status_code == 200:
        models = [model['name'] for model in response.json()['models']]
        return JsonResponse({'models': models})
    return JsonResponse({'error': 'Unable to fetch models'}, status=500)

@csrf_exempt
def generate_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        model = data.get('model')
        prompt = data.get('prompt')
        temperature = float(data.get('temperature', 0.7))

        ollama_data = {
            "model": model,
            "prompt": prompt,
            "temperature": temperature
        }
        
        response = requests.post(f"{OLLAMA_API}/generate", json=ollama_data, stream=True)
        
        full_response = ""
        for line in response.iter_lines():
            if line:
                json_response = json.loads(line)
                full_response += json_response['response']
                if json_response['done']:
                    break
        
        return JsonResponse({'response': full_response})
    return JsonResponse({'error': 'Invalid request method'}, status=400)