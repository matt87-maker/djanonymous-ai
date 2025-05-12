# ai/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from transformers import pipeline
import json

generator = pipeline("text-generation", model="distilgpt2")

@csrf_exempt
def generate_text(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            prompt = data.get("prompt", "")
            result = generator(
                prompt,
                max_length=100,
                num_return_sequences=1,
                truncation=True,                 # 🧼 cleans the warning
                pad_token_id=50256               # 🧼 sets correct padding
            )
            return JsonResponse({"output": result[0]['generated_text']})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Only POST allowed"}, status=405)