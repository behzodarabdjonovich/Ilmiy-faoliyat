from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
def main_menu(admin=False):
    rows=[[KeyboardButton(text="📝 Yangi xat yaratish"),KeyboardButton(text="📂 Mening xatlarim")],[KeyboardButton(text="🏢 Tashkilot ma'lumotlari"),KeyboardButton(text="ℹ️ Yordam")]]
    if admin: rows.append([KeyboardButton(text="👨‍💼 Admin panel")])
    return ReplyKeyboardMarkup(keyboard=rows,resize_keyboard=True)
def types_kb():
    names=["Rasmiy murojaat","So‘rov xati","Iltimos xati","Javob xati","Hamkorlik taklifi","Kafolat xati","Axborot xati","Bildirishnoma","Erkin shakl"]
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=x)] for x in names],resize_keyboard=True,one_time_keyboard=True)
def confirm_kb():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="✅ Xatni yaratish",callback_data="letter:generate")],[InlineKeyboardButton(text="❌ Bekor qilish",callback_data="letter:cancel")]])
def result_kb(letter_id:int):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="✏️ AI bilan tahrirlash",callback_data=f"letter:revise:{letter_id}")],[InlineKeyboardButton(text="📄 DOCX",callback_data=f"letter:docx:{letter_id}"),InlineKeyboardButton(text="📕 PDF",callback_data=f"letter:pdf:{letter_id}")]])
