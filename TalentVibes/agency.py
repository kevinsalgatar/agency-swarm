from agency_swarm import Agency
from JobDescriptionAgent import JobDescriptionAgent
from TalentVibesCEO import TalentVibesCEO

ceo = TalentVibesCEO()
job_desc = JobDescriptionAgent()

agency = Agency([ceo, job_desc, [ceo, job_desc],
                 ],
                shared_instructions='./agency_manifesto.md',  # shared instructions for all agents
                max_prompt_tokens=25000,  # default tokens in conversation for all agents
                temperature=0.3,  # default temperature for all agents
                )

if __name__ == '__main__':
    agency.demo_gradio()