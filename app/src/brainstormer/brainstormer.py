"""
The generator of ideas given all the previous.
Given all the previous ideas, the generator of ideas will generate a new idea.
"""
from langchain.llms.openai import OpenAI
from langchain.chains import LLMChain
import os 
from langchain.prompts import PromptTemplate
from utils.utils import BRAINSTORM_LOGGER

IDEA_GENERATOR_TEMPLATE = """
Given all the previous ideas, the generator of ideas will generate a new idea.
{ideas}
"""

IDEA_CRITIQUE_PROMPT = """
Given the previous Ideas: {previous_ideas},

and the new idea: {new_idea},

Please judge the new idea compared to the previous ideas.
If the new idea is the same as a previous idea, please answer NO.
Otherwise, please answer YES.

"""



class Brainstomer():
    

    def __init__(self):
        llm = OpenAI()
        generator_prompt = PromptTemplate.from_template(IDEA_GENERATOR_TEMPLATE)
        self.idea_generator = LLMChain(prompt=generator_prompt, llm=llm)
        critique_prompt = PromptTemplate.from_template(IDEA_CRITIQUE_PROMPT)
        self.idea_critique = LLMChain(prompt = critique_prompt, llm=llm)


    
    def generate_idea(self, ideas):
        if len(ideas) == 0:
            BRAINSTORM_LOGGER.info("No previous ideas to generate from")
            return None
        candidate_idea = self.idea_generator.run(ideas)
        critique = self.idea_critique.run({"previous_ideas": ideas, "new_idea": candidate_idea})
        BRAINSTORM_LOGGER.info(f"Generated Idea: {candidate_idea}")
        BRAINSTORM_LOGGER.info(f"Critique: {critique}")
        if critique == "YES":
            return candidate_idea
        else:
            return None