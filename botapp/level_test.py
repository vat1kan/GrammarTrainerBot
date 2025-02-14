import asyncio
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from botapp.keyboards import test_lvl

questions = [
    {"question": "[1 / 20] She ___ to the store yesterday.",  
     "options": ["go", "goes", "went", "going"],  
     "correct": 2, 
     "explanation": "'Went' is the correct past tense of 'go'."},
    
    {"question": "[2 / 20] I ___ coffee every morning.",  
     "options": ["drink", "drank", "drinks", "drinking"],  
     "correct": 0, 
     "explanation": "'Drink' is the correct present simple form for 'I'."},
    
    {"question": "[3 / 20] They ___ to the party if they had known.",  
     "options": ["go", "gone", "would have gone", "going"],  
     "correct": 2, 
     "explanation": "'Would have gone' is used for past hypothetical situations."},
    
    {"question": "[4 / 20] She ___ for a walk now.",  
     "options": ["goes", "is going", "going", "went"],  
     "correct": 1, 
     "explanation": "'Is going' is the correct present continuous form."},
    
    {"question": "[5 / 20] I ___ my homework before dinner.",  
     "options": ["did", "done", "do", "doing"],  
     "correct": 0, 
     "explanation": "'Did' is the correct past simple form of 'do'."},
    
    {"question": "[6 / 20] She has never ___ sushi before.",  
     "options": ["eaten", "ate", "eat", "eats"],  
     "correct": 0, 
     "explanation": "'Eaten' is the past participle needed after 'has never'."},
    
    {"question": "[7 / 20] If I ___ rich, I would travel the world.",  
     "options": ["was", "were", "am", "been"],  
     "correct": 1, 
     "explanation": "'Were' is used in second conditional sentences."},
    
    {"question": "[8 / 20] She ___ her keys and can’t find them.",  
     "options": ["lost", "has lost", "loses", "losing"],  
     "correct": 1, 
     "explanation": "'Has lost' is the correct present perfect form."},
    
    {"question": "[9 / 20] By this time next year, I ___ my degree.",  
     "options": ["will have finished", "finish", "finishes", "finished"],  
     "correct": 0, 
     "explanation": "'Will have finished' is the future perfect form."},
    
    {"question": "[10 / 20] I usually ___ to bed early.",  
     "options": ["go", "goes", "gone", "going"],  
     "correct": 0, 
     "explanation": "'Go' is the correct present simple form."},
    
    {"question": "[11 / 20] She ___ studying for the exam.",  
     "options": ["has finished", "finished", "finishing", "finishes"],  
     "correct": 0, 
     "explanation": "'Has finished' is present perfect for completed actions."},
    
    {"question": "[12 / 20] If he ___ harder, he would pass.",  
     "options": ["studied", "studies", "study", "studying"],  
     "correct": 0, 
     "explanation": "'Studied' fits second conditional sentences."},
    
    {"question": "[13 / 20] She ___ to Paris last summer.",  
     "options": ["went", "goes", "going", "gone"],  
     "correct": 0, 
     "explanation": "'Went' is past simple for completed actions."},
    
    {"question": "[14 / 20] We ___ here since 2010.",  
     "options": ["live", "lived", "have lived", "living"],  
     "correct": 2, 
     "explanation": "'Have lived' is correct for actions continuing from the past."},
    
    {"question": "[15 / 20] He ___ a book when I called him.",  
     "options": ["reads", "was reading", "read", "reading"],  
     "correct": 1, 
     "explanation": "'Was reading' is past continuous for interrupted actions."},
    
    {"question": "[16 / 20] This time tomorrow, we ___ on the beach.",  
     "options": ["lie", "lying", "will be lying", "lies"],  
     "correct": 2, 
     "explanation": "'Will be lying' is the future continuous form."},
    
    {"question": "[17 / 20] The book ___ by the author in 1995.",  
     "options": ["written", "was written", "wrote", "write"],  
     "correct": 1, 
     "explanation": "'Was written' is the correct past passive form."},
    
    {"question": "[18 / 20] She is ___ than her brother.",  
     "options": ["more tall", "taller", "most tall", "tallest"],  
     "correct": 1, 
     "explanation": "'Taller' is the correct comparative form."},
    
    {"question": "[19 / 20] I have never ___ such a big dog!",  
     "options": ["saw", "see", "seen", "seeing"],  
     "correct": 2, 
     "explanation": "'Seen' is the past participle needed after 'have never'."},
    
    {"question": "[20 / 20] She said she ___ come tomorrow.",  
     "options": ["will", "would", "can", "could"],  
     "correct": 1, 
     "explanation": "'Would' is the correct form in reported speech."}
]


user_data = {}

async def send_question(bot, chat_id, question_index):
    if chat_id not in user_data:
        user_data[chat_id] = {"score": 0, "question_index": 0, "current_poll_id": None}

    if question_index >= len(questions):
        await send_result(bot, chat_id)
        return
    
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Stop Test", callback_data=f"stop_test:{chat_id}")
    stop_button = keyboard.as_markup()

    question = questions[question_index]
    poll_message = await bot.send_poll(
        chat_id,
        question=question["question"],
        options=question["options"],
        type="quiz",
        correct_option_id=question["correct"],
        explanation=question["explanation"],
        open_period=60,
        is_anonymous=False,
        reply_markup=stop_button)
    
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