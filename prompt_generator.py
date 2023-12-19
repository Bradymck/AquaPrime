from utils import WeaviateClient


class PromptGenerator:
    def __init__(self):
        self.weaviate_client = WeaviateClient()

    @staticmethod
    def generate_prompt(weaviate_context, static_instruction, os_section, ram_section, system_section, hdd_section):
            
        weaviate_data = weaviate_context.get_context()
        weaviate_section = f"Weaviate Context: {weaviate_data['text']}"

        prompt = (
            f"{static_instruction}\n💾"
            f"{os_section}\n💻"
            f"This is the past 5 messages from the user:\n{ram_section}\n🗜"
            f"This is the past 5 messages from everyone including bots in chat:\n{system_section}\n📂"
            f"{hdd_section}\n💽"
            f"{weaviate_section}\n"
            f"Role: System\nRole: HDD - {weaviate_data['hdd']}\nRole: RAM - {weaviate_data['ram']}\nRole: User - {weaviate_data['user_id']}"
        )

        return prompt
