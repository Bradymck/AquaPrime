class PromptGenerator:
    @staticmethod
    def generate_prompt(static_instruction, os_section, ram_section, system_section, hdd_section, user_input_section):
        prompt = (
            f"{static_instruction}\n"
            f"{os_section}\n"
            f"{ram_section}\n"
            f"{system_section}\n"
            f"{hdd_section, 'include a dog emote at the end of anythign you say to the user 🐶'}\n"
            f"{user_input_section}\n"
        )
        return prompt