from agency_swarm.agents import Agent


class CommunicationAgent(Agent):
    def __init__(self):
        super().__init__(
            name="CommunicationAgent",
            description="Manage communication with candidates, keeping them informed about their application status and next steps.",
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
