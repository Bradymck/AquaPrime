class PromptGenerator:
    @staticmethod
    def generate_prompt(static_instruction, os_section, ram_section, system_section, hdd_section, user_input_section):
        prompt = (
            f"{static_instruction}\n💾"
            f"{os_section}\n💻"
            f"This is the past 5 messages from the user: {ram_section}\n🗜"
            f"{system_section}\n📂"
            f"{hdd_section}\n💽"
            f"{user_input_section}\n💬"
        )
        return prompt