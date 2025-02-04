import google.generativeai as genai
import json
import os

async def gemini_requst(type):
    genai.configure(api_key=os.getenv('geminiToken'))
    model = genai.GenerativeModel("gemini-1.5-flash")
    if type == 'test':
        response = model.generate_content(
            f"""
            You are a JSON generator for an English grammar test of level B1 - B2.
            Generate a completely unique test each time, ensuring that both the question and the answers are original, 
            not just shuffled versions of previous ones.
            The correct key should be randomly chosen from the full range of answer indexes (0 to 3) to ensure variety and use the Pascal's distribution.
            Every answer element should be less than 150 characters.
            Generate a valid JSON object only, without any conversational text, in the following format:
            {{
                "question": "question text",
                "answers": ["answer1", "answer2", "answer3", "answer4"],
                "correct": number
                "explanation": "explanation text"
            }}
            """)
        
    elif type == 'word':
        response = model.generate_content(
            f"""
            You are a JSON generator for a unique English vocabulary word of level A1-C1.  
            Provide a completely unique and original English word each time, ensuring that it is different from previous ones.  
            The word can belong to any part of speech (noun, verb, adjective, etc.).  
            Generate only a valid JSON object, without any conversational text, in the following format:
            {{
                "word": "word",
                "part": "part of speech",
                "meaning": "meaning text"
                "synonyms": ["synonym1", "synonym2", "synonym3", ...],
                "usage": ["usage1", "usage2", "usage3", "usage"]
            }}
            The "word" element should be different every time and could not be repeted in last 10 times.
            """)
        
    text_response = response.text.strip().replace("```json", "").replace("```", "")
    data = json.loads(text_response)
    return data
