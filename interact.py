'''
USER INTERACTS WITH THE SYSTEM PROMPT HERE

USER PROMPOT -> CLEANING -> BREAKDOWN PROMPT -> SYSTEMpROMPT
'''

import os
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv
from utils import remove_duplicate_punctuation, remove_special_characters, limit_word_length, remove_repeating_phrases, split_tasks
from prompts import BREAKDOWN_PROMPT, SystemPrompt
load_dotenv('.env')

def preprocess_pipeline(user_prompt):
    cleaned_user_prompt = remove_duplicate_punctuation(user_prompt)
    cleaned_user_prompt = remove_special_characters(cleaned_user_prompt)
    cleaned_user_prompt = remove_repeating_phrases(cleaned_user_prompt)
    cleaned_user_prompt = limit_word_length(cleaned_user_prompt)
    return cleaned_user_prompt

def decoder_llm(cleaned_user_prompt):
    prompt = PromptTemplate(template = BREAKDOWN_PROMPT, input_variables=["up"])
    llm = ChatOpenAI(temperature=0.5, model_name=os.environ.get("CHAT_MODEL"))
    chain = LLMChain(llm=llm, prompt=prompt)
    a = chain.run(up=cleaned_user_prompt)
    return a

def run_llm(safe_user_prompt):
    sp = """Here is a system prompt for an application along with the user prompt. Answer the user prompt based on the system prompt.\n SystemPrompt: """
    sp += SystemPrompt
    ssp = sp + """
        UserPrompt: {up}

        System Response:
    """
    prompt = PromptTemplate(template = ssp, input_variables=["up"])
    llm = ChatOpenAI(temperature=0.5, model_name=os.environ.get("CHAT_MODEL"))
    chain = LLMChain(llm=llm, prompt=prompt)
    a = chain.run(up=safe_user_prompt)
    return a