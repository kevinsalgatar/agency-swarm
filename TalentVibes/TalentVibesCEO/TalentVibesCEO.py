from agency_swarm.agents import Agent


class TalentVibesCEO(Agent):
    def __init__(self):
        super().__init__(
            name="TalentVibesCEO",
            description="Oversee the entire operation, ensuring that the goals and mission of TalentVibes are met. Coordinate with other agents and manage the communication flow.",
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
