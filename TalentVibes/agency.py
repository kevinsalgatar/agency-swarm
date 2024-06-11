from agency_swarm import Agency
from CommunicationAgent import CommunicationAgent
from AssessmentAgent import AssessmentAgent
from ScreeningAgent import ScreeningAgent
from JobDescriptionAgent import JobDescriptionAgent
from TalentVibesCEO import TalentVibesCEO

ceo = TalentVibesCEO()
job_desc = JobDescriptionAgent()
screening = ScreeningAgent()
assessment = AssessmentAgent()
communication = CommunicationAgent()

agency = Agency([ceo, job_desc, screening, assessment, communication, [ceo, job_desc],
                 [ceo, screening],
                 [ceo, assessment],
                 [ceo, communication],
                 [job_desc, screening],
                 [screening, assessment],
                 [assessment, communication]],
                shared_instructions='./agency_manifesto.md',  # shared instructions for all agents
                max_prompt_tokens=25000,  # default tokens in conversation for all agents
                temperature=0.3,  # default temperature for all agents
                )

if __name__ == '__main__':
    agency.demo_gradio()