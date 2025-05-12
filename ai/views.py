import requests
import json
import os

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@csrf_exempt
def generate_text(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests are allowed."}, status=405)

    try:
        data = json.loads(request.body)
        prompt = data.get("prompt", "").strip()
        if not prompt:
            return JsonResponse({"error": "Missing prompt text."}, status=400)

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "llama3-8b-8192",  # or "mixtral-8x7b-32768"
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 256
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )

        if response.status_code != 200:
            return JsonResponse({
                "error": f"Groq API error: {response.status_code}",
                "details": response.text
            }, status=502)

        data = response.json()
        return JsonResponse({"output": data['choices'][0]['message']['content'].strip()})

    except requests.exceptions.Timeout:
        return JsonResponse({"error": "Groq API request timed out."}, status=504)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def home(request):
    return render(request, "index.html")