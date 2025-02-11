import asyncio
import logging
from botapp.keyboards import test_lvl

questions = [
    {"question": "What is the past participle of 'go'?", 
     "options": ["goed", "went", "gone", "going"], 
     "correct": 2, 
     "explanation": "'Gone' is the correct past participle of 'go'."},

    {"question": "Which word is a synonym for 'big'?", 
     "options": ["tiny", "huge", "slow", "old"], 
     "correct": 0, 
     "explanation": "'Tiny' is the opposite of 'big', not a synonym."},

    {"question": "Choose the correct article: ___ apple", 
     "options": ["a", "an", "the", "no article"], 
     "correct": 3, 
     "explanation": "'No article' is incorrect; an article is required."},

    {"question": "What is the comparative form of 'good'?", 
     "options": ["gooder", "more good", "better", "best"], 
     "correct": 1, 
     "explanation": "'Better' is the correct comparative form of 'good'."},

    {"question": "Which of these is an irregular verb?", 
     "options": ["talk", "work", "run", "play"], 
     "correct": 3, 
     "explanation": "'Play' follows the regular past tense rule (played)."},

    {"question": "Choose the correct preposition: 'interested ___ science'", 
     "options": ["on", "about", "in", "for"], 
     "correct": 2, 
     "explanation": "We say 'interested in' something."},

    {"question": "Which sentence is correct?", 
     "options": ["She don't like coffee.", "She doesn't like coffee.", "She not likes coffee.", "She isn't like coffee."], 
     "correct": 1, 
     "explanation": "In present simple negative, use 'doesn't' + verb."},

    {"question": "What is the opposite of 'fast'?", 
     "options": ["quick", "rapid", "slow", "speedy"], 
     "correct": 0, 
     "explanation": "'Slow' is the opposite of 'fast'."},

    {"question": "Which sentence is in passive voice?", 
     "options": ["She wrote the letter.", "She will write a letter.", "She is writing a letter.", "The letter was written by her."], 
     "correct": 3, 
     "explanation": "'The letter was written by her' is in passive voice."},
    {"question": "What is the past participle of 'eat'?", 
     "options": ["ate", "eaten", "eated", "eats"], 
     "correct": 2, 
     "explanation": "'Eaten' is the past participle of 'eat'."},

    {"question": "Choose the correct form: 'She ___ a book now.'", 
     "options": ["reads", "is reading", "read", "reading"], 
     "correct": 0, 
     "explanation": "'Reads' is incorrect for present continuous."},

    {"question": "What is the plural of 'child'?", 
     "options": ["childs", "children", "childes", "childen"], 
     "correct": 1, 
     "explanation": "'Children' is the irregular plural of 'child'."},

    {"question": "Choose the correct phrasal verb: 'He ___ his shoes.'", 
     "options": ["put on", "put out", "put off", "put in"], 
     "correct": 2, 
     "explanation": "'Put off' means to delay, not to wear clothes."},

    {"question": "Which of these is a modal verb?", 
     "options": ["run", "jump", "can", "play"], 
     "correct": 3, 
     "explanation": "'Can' is a modal verb used for ability or permission."},

    {"question": "What is the past simple of 'buy'?", 
     "options": ["buyed", "bought", "buys", "buy"], 
     "correct": 1, 
     "explanation": "'Bought' is the correct past simple of 'buy'."},

    {"question": "What does 'ought to' express?", 
     "options": ["possibility", "ability", "obligation", "future intention"], 
     "correct": 3, 
     "explanation": "'Ought to' is used for obligation or advice."},

    {"question": "Choose the correct order of adjectives:", 
     "options": ["a wooden old table", "a table wooden old", "an old wooden table", "a wooden table old"], 
     "correct": 0, 
     "explanation": "The correct order is opinion, size, age, shape, color, material."},

    {"question": "Which sentence uses the correct conditional form?", 
     "options": ["If I will see him, I tell him.", "If I saw him, I tell him.", "If I see him, I'll tell him.", "If I would see him, I tell him."], 
     "correct": 2, 
     "explanation": "First conditional: 'If' + present simple, 'will' + verb."},

    {"question": "Choose the correct sentence.", 
     "options": ["She suggested me to go.", "She suggested that I go.", "She suggested me that I go.", "She suggested I to go."], 
     "correct": 1, 
     "explanation": "'Suggest' is followed by 'that' + base verb."}
]


user_data = {}

async def send_question(bot, chat_id, question_index):
    if chat_id not in user_data:
        user_data[chat_id] = {"score": 0, "question_index": 0, "current_poll_id": None}

    if question_index >= len(questions):
        await send_result(bot, chat_id)
        return
    
    question = questions[question_index]
    poll_message = await bot.send_poll(
        chat_id,
        question=question["question"],
        options=question["options"],
        type="quiz",
        correct_option_id=question["correct"],
        explanation=question["explanation"],
        open_period=60,
        is_anonymous=False)
    
    user_data[chat_id] = user_data.get(chat_id, {"score": 0, "question_index": 0, "current_poll_id": None})
    user_data[chat_id]["current_poll_id"] = poll_message.poll.id
    user_data[chat_id]["question_index"] = question_index
    
    await asyncio.sleep(60)
    if user_data[chat_id]["question_index"] == question_index:
        await send_question(bot, chat_id, question_index + 1)

async def send_result(bot, chat_id):
    score = user_data[chat_id]["score"]
    levels = [(5, "A1"), (10, "A2"), (15, "B1"), (18, "B2"), (19, "C1"), (20, "C2")]
    level = next((lvl for threshold, lvl in levels if score <= threshold), "C2")
    await bot.send_message(chat_id, f"Your English level: {level} ({score}/20 correct)\n"
                           f"\nDo you want to use this level for quiz tests?", 
                           parse_mode="HTML", reply_markup=test_lvl(str(level)))
    del user_data[chat_id]