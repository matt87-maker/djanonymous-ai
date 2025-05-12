import requests
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

@csrf_exempt
def generate_text(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)
        prompt = data.get("prompt", "")
        if not prompt:
            return JsonResponse({"error": "Missing prompt"}, status=400)

        headers = {
            "Authorization": f"Bearer {HF_API_TOKEN}",
            "Content-Type": "application/json",
        }

        hf_response = requests.post(
            "https://api-inference.huggingface.co/models/distilgpt2",
            headers=headers,
            json={"inputs": prompt}
        )

        response_data = hf_response.json()
        if isinstance(response_data, list) and "generated_text" in response_data[0]:
            return JsonResponse({"output": response_data[0]["generated_text"]})
        else:
            return JsonResponse({"error": response_data.get("error", "Unexpected response")}, status=500)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)