from utils.file_manager import FileManager


class PromptManager:

    @staticmethod
    def research_prompt(topic):

        prompt = FileManager.read_text(
            "templates/research_template.txt"
        )

        return prompt.replace("{topic}", topic)