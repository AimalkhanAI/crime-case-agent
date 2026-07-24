import json

from models.video import Video
from services.ai_provider import AIProvider
from services.prompt_manager import PromptManager


class ResearchAgent:

    def __init__(self):
        self.ai = AIProvider()

    def research(self, topic):

        print(f"Researching topic: {topic}")

        prompt = PromptManager.research_prompt(topic)

        ai_response = self.ai.generate(prompt)
        ai_response = ai_response.replace("```json", "")
        ai_response = ai_response.replace("```", "")
        ai_response = ai_response.strip()

        try:
            data = json.loads(ai_response)
        except json.JSONDecodeError:
            raise Exception(
                "AI did not return valid JSON.\n\n"
                f"Response was:\n{ai_response}"
            )

        video = Video()

        video.title = topic
        video.topic = topic

        video.summary = data["summary"]
        video.timeline = data["timeline"]
        video.interesting_facts = data["interesting_facts"]

        return video