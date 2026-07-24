import requests

from config.settings import (
    AI_PROVIDER,
    AI_MODEL,
    OPENROUTER_API_KEY
)


class AIProvider:

    def __init__(self):
        self.provider = AI_PROVIDER
        self.model = AI_MODEL

    def generate(self, prompt):

        print("\n========== AI Provider ==========")
        print(f"Provider : {self.provider}")
        print(f"Model    : {self.model}")
        print("=================================\n")

        if not OPENROUTER_API_KEY:
            raise Exception("OpenRouter API Key not found.")

        print("Connecting to OpenRouter...\n")

        print("========== FINAL PROMPT ==========")
        print(prompt)
        print("==================================\n")

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "temperature": 0,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a professional crime documentary researcher. "
                        "Always follow the user's instructions exactly. "
                        "Return ONLY valid JSON. "
                        "Never use markdown. "
                        "Never use code blocks."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        try:

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )

            result = response.json()

            print("\n========== API Response ==========")
            print(result)
            print("==================================\n")

            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}: {result}")

            if "error" in result:
                raise Exception(result["error"]["message"])

            if "choices" not in result:
                raise Exception(f"Unexpected API response: {result}")

            return result["choices"][0]["message"]["content"]

        except requests.exceptions.RequestException as e:
            raise Exception(f"Network Error: {e}")

        except Exception as e:
            raise Exception(str(e))