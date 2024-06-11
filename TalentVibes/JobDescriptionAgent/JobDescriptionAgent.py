from agency_swarm.agents import Agent


class JobDescriptionAgent(Agent):
    def __init__(self):
        super().__init__(
            name="JobDescriptionAgent",
            description="Create accurate and attractive job descriptions based on employer inputs.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[],
            tools_folder="./tools",
            temperature=0.3,
            max_prompt_tokens=25000,
        )
        
    def response_validator(self, message):
        return message
