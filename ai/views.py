import requests
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

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
            "Authorization": f"Bearer {HF_API_TOKEN}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            "https://api-inference.huggingface.co/models/distilgpt2",
            headers=headers,
            json={"inputs": prompt},
            timeout=10
        )

        try:
            output = response.json()
        except ValueError:
            return JsonResponse({"error": "Invalid response from Hugging Face (not JSON)."}, status=502)

        # Hugging Face rate limit, model offline, etc.
        if response.status_code != 200:
            return JsonResponse({
                "error": output.get("error", f"Hugging Face API error: {response.status_code}")
            }, status=502)

        if isinstance(output, list) and "generated_text" in output[0]:
            return JsonResponse({"output": output[0]["generated_text"]})
        else:
            return JsonResponse({"error": "Unexpected response from Hugging Face API."}, status=500)

    except requests.exceptions.Timeout:
        return JsonResponse({"error": "Hugging Face API request timed out."}, status=504)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)