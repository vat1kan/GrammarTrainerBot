import google.generativeai as genai
import aiohttp
import json
import os

async def get_quiz(user_lvl):
    genai.configure(api_key=os.getenv('geminiToken'))
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        f"""
        You are a JSON generator for an English grammar test of level {user_lvl} or 1 level higher.
        Generate a completely unique test each time, ensuring that both the question and the answers are original, 
        not just shuffled versions of previous ones.
        The correct key should be randomly chosen from the full range of answer indexes (0 to 3) to ensure variety and use the Pascal's distribution.
        Every answer element should be less than 150 characters.
        Generate a valid JSON object only, without any conversational text, in the following format:
        {{
            "question": "question text (max 150 symbols)",
            "answers": ["answer1", "answer2", "answer3", "answer4"] (max 50 symbols for each),
            "correct": number
            "explanation": "explanation text (max 150 symbols)"
        }}
        """)

    text_response = response.text.strip().replace("```json", "").replace("```", "")
    data = json.loads(text_response)
    return data


async def get_word():
    genai.configure(api_key=os.getenv('geminiToken'))
    model = genai.GenerativeModel("gemini-1.5-flash")
    word = await fetch_random_word()
    response = model.generate_content(
            f"""
            You are a JSON generator for a unique English vocabulary word of level A1-A2.  
            Provide a completely unique and original English word each time, ensuring that it is different from previous ones.  
            The word can belong to any part of speech (noun, verb, adjective, etc.).
            The word must be frequently used by the speakers and common.
            Generate only a valid JSON object, without any conversational text, in the following format:
            {{
                "word": "word",
                "part": "part of speech",
                "meaning": "meaning text"
                "synonyms": ["synonym1", "synonym2", "synonym3", ...],
                "usage": ["usage1", "usage2", "usage3", "usage"]
            }}
            """ if word == None 
            else f"""You json dictionary and provide the following additional information for the specified word. 
            Generate only a valid JSON object, without any conversational text, in the following format:
            {{
                "word": "{word}",
                "part": "part of speech",
                "meaning": "meaning text"
                "synonyms": ["synonym1", "synonym2", "synonym3", ...],
                "usage": ["usage1", "usage2", "usage3", "usage"]
            }}
            """)
    text_response = response.text.strip().replace("```json", "").replace("```", "")
    data = json.loads(text_response)
    return data


async def fetch_random_word():
    url = "https://random-word-api.herokuapp.com/word"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data[0]
            else:
                print("Error to get ranond heroku word:", response.status)
                return None

