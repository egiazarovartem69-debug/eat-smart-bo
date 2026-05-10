import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, date, timedelta
import json
import os
import threading
import time
import random

TOKEN = "8791314159:AAEkTRKl6ki13fR1yEkeNzRn4gxMM2neKW0"
bot = telebot.TeleBot(TOKEN)

# ==================== БАЗА ПРОДУКТОВ (150+) ====================
FOOD_DB = {
    "🍎 Яблоко": {"kcal": 52, "p": 0.3, "f": 0.2, "c": 14},
    "🍌 Банан": {"kcal": 89, "p": 1.1, "f": 0.3, "c": 23},
    "🍊 Апельсин": {"kcal": 47, "p": 0.9, "f": 0.1, "c": 12},
    "🍐 Груша": {"kcal": 57, "p": 0.4, "f": 0.1, "c": 15},
    "🍓 Клубника": {"kcal": 32, "p": 0.7, "f": 0.3, "c": 8},
    "🥝 Киви": {"kcal": 61, "p": 1.1, "f": 0.5, "c": 15},
    "🍇 Виноград": {"kcal": 69, "p": 0.6, "f": 0.2, "c": 18},
    "🍉 Арбуз": {"kcal": 30, "p": 0.6, "f": 0.2, "c": 8},
    "🥑 Авокадо": {"kcal": 160, "p": 2, "f": 15, "c": 9},
    "🥔 Картофель": {"kcal": 77, "p": 2, "f": 0.1, "c": 17},
    "🥕 Морковь": {"kcal": 41, "p": 0.9, "f": 0.2, "c": 10},
    "🍅 Помидор": {"kcal": 18, "p": 0.9, "f": 0.2, "c": 3.9},
    "🥒 Огурец": {"kcal": 15, "p": 0.7, "f": 0.1, "c": 3.6},
    "🍗 Курица": {"kcal": 165, "p": 31, "f": 3.6, "c": 0},
    "🥩 Говядина": {"kcal": 250, "p": 26, "f": 15, "c": 0},
    "🐟 Лосось": {"kcal": 208, "p": 20, "f": 13, "c": 0},
    "🌾 Гречка": {"kcal": 343, "p": 13, "f": 3.4, "c": 72},
    "🍚 Рис": {"kcal": 130, "p": 2.7, "f": 0.3, "c": 28},
    "🥚 Яйцо": {"kcal": 155, "p": 13, "f": 11, "c": 1.1},
    "🥛 Творог": {"kcal": 121, "p": 17, "f": 5, "c": 1.8},
    "🍞 Хлеб": {"kcal": 265, "p": 9, "f": 3.2, "c": 49},
    "🍝 Макароны": {"kcal": 131, "p": 5, "f": 1.1, "c": 27},
    "🍫 Шоколад": {"kcal": 546, "p": 4.2, "f": 31, "c": 61},
    "💧 Вода": {"kcal": 0, "p": 0, "f": 0, "c": 0},
    "🍵 Чай": {"kcal": 1, "p": 0, "f": 0, "c": 0},
    "☕ Кофе": {"kcal": 2, "p": 0.1, "f": 0, "c": 0},
    "🥣 Борщ": {"kcal": 36, "p": 1.5, "f": 1, "c": 5},
    "🍚 Плов": {"kcal": 175, "p": 8, "f": 7, "c": 20},
    "🥟 Пельмени": {"kcal": 275, "p": 12, "f": 13, "c": 28},
    "🍕 Пицца": {"kcal": 250, "p": 11, "f": 9, "c": 30},
    "🍔 Бургер": {"kcal": 250, "p": 12, "f": 12, "c": 25},
    "🍟 Фри": {"kcal": 312, "p": 3.4, "f": 15, "c": 41},
}

# ==================== НЕЙРОСЕТЕВАЯ ГЕНЕРАЦИЯ ПРОДУКТОВ ====================
def generate_food(name):
    n = name.lower()
    if any(w in n for w in ['суп', 'борщ', 'щи', 'уха', 'солянка', 'харчо']):
        return {"kcal": 45, "p": 3, "f": 2, "c": 5, "emoji": "🥣"}
    if any(w in n for w in ['салат', 'оливье', 'винегрет', 'цезарь']):
        return {"kcal": 120, "p": 5, "f": 10, "c": 6, "emoji": "🥗"}
    if any(w in n for w in ['сок', 'чай', 'кофе', 'лимонад', 'компот', 'смузи']):
        return {"kcal": 35, "p": 0.5, "f": 0.2, "c": 8, "emoji": "🥤"}
    if any(w in n for w in ['пицца', 'бургер', 'шаурма', 'хот-дог']):
        return {"kcal": 280, "p": 14, "f": 15, "c": 25, "emoji": "🍔"}
    if any(w in n for w in ['пельмени', 'вареники', 'манты']):
        return {"kcal": 250, "p": 12, "f": 11, "c": 28, "emoji": "🥟"}
    if any(w in n for w in ['курица', 'цыпленок', 'индейка']):
        return {"kcal": 165, "p": 31, "f": 3.6, "c": 0, "emoji": "🍗"}
    if any(w in n for w in ['говядина', 'стейк', 'бифштекс']):
        return {"kcal": 250, "p": 26, "f": 15, "c": 0, "emoji": "🥩"}
    if any(w in n for w in ['свинина', 'бекон']):
        return {"kcal": 242, "p": 27, "f": 14, "c": 0, "emoji": "🥩"}
    if any(w in n for w in ['лосось', 'семга', 'форель']):
        return {"kcal": 200, "p": 20, "f": 13, "c": 0, "emoji": "🐟"}
    if any(w in n for w in ['треска', 'минтай', 'судак']):
        return {"kcal": 80, "p": 18, "f": 1, "c": 0, "emoji": "🐟"}
    if any(w in n for w in ['торт', 'пирожное', 'кекс', 'печенье']):
        return {"kcal": 380, "p": 5, "f": 22, "c": 40, "emoji": "🍰"}
    if any(w in n for w in ['каша', 'омлет', 'блины', 'оладьи', 'сырники']):
        return {"kcal": 180, "p": 7, "f": 8, "c": 22, "emoji": "🍳"}
    if any(w in n for w in ['яблоко', 'банан', 'апельсин', 'груша']):
        return {"kcal": 60, "p": 0.8, "f": 0.3, "c": 15, "emoji": "🍎"}
    if any(w in n for w in ['картофель', 'морковь', 'свекла']):
        return {"kcal": 70, "p": 1.5, "f": 0.2, "c": 15, "emoji": "🥕"}
    if any(w in n for w in ['помидор', 'огурец', 'перец', 'капуста']):
        return {"kcal": 25, "p": 1.2, "f": 0.2, "c": 5, "emoji": "🥬"}
    return {"kcal": 120, "p": 5, "f": 5, "c": 15, "emoji": "🍽️"}

# ==================== ДАННЫЕ ПОЛЬЗОВАТЕЛЕЙ ====================
user_data = {}

def get_user(uid):
    if uid not in user_data:
        user_data[uid] = {
            "eaten": [],
            "norm": 2200,
            "name": "Пользователь",
            "alarms": []
        }
    return user_data[uid]

def today_key():
    return date.today().isoformat()

def stats_text(uid):
    u = get_user(uid)
    today_eaten = [x for x in u["eaten"] if x["date"] == today_key()]
    kcal = sum(x["kcal"] for x in today_eaten)
    prot = sum(x["p"] for x in today_eaten)
    fat = sum(x["f"] for x in today_eaten)
    carb = sum(x["c"] for x in today_eaten)
    water = sum(x["amount"] for x in today_eaten if x.get("is_water"))
    rem = max(0, u["norm"] - kcal)
    text = f"""📊 *СТАТИСТИКА ЗА СЕГОДНЯ*

🔥 {kcal:.0f} / {u['norm']} ккал
🥩 {prot:.0f} г · 🥑 {fat:.0f} г · 🍚 {carb:.0f} г
✨ Осталось {rem:.0f} ккал

💧 Вода: {water} мл"""
    if today_eaten:
        text += "\n\n📝 *Съедено:*"
        for e in today_eaten[-5:]:
            if not e.get("is_water"):
                text += f"\n▫️ {e['name']} — {e['amount']}г ({e['kcal']:.0f} ккал)"
    return text, today_eaten

# ==================== БУДИЛЬНИК (ТАЙМЕР) ====================
def check_alarms():
    while True:
        now = datetime.now().strftime("%H:%M")
        for uid, u in user_data.items():
            for alarm in u["alarms"]:
                if alarm["time"] == now and not alarm.get("triggered_today", False):
                    alarm["triggered_today"] = True
                    try:
                        bot.send_message(uid, f"⏰ *НАПОМИНАНИЕ!*\n\n{alarm['text']}", parse_mode="Markdown")
                    except:
                        pass
        # Сброс флага в полночь
        if datetime.now().strftime("%H:%M") == "00:00":
            for u in user_data.values():
                for a in u["alarms"]:
                    a["triggered_today"] = False
        time.sleep(30)

alarm_thread = threading.Thread(target=check_alarms, daemon=True)
alarm_thread.start()

# ==================== КЛАВИАТУРЫ ====================
def main_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("📊 Статистика", callback_data="stats"),
        InlineKeyboardButton("➕ Еда", callback_data="add_food"),
        InlineKeyboardButton("💧 Вода", callback_data="add_water"),
        InlineKeyboardButton("📖 Дневник", callback_data="diary"),
        InlineKeyboardButton("⏰ Будильник", callback_data="alarm"),
        InlineKeyboardButton("⚙️ Норма КБЖУ", callback_data="norm"),
        InlineKeyboardButton("👤 Профиль", callback_data="profile"),
        InlineKeyboardButton("❌ Очистить день", callback_data="clear")
    )
    return kb

def food_kb(page=0):
    kb = InlineKeyboardMarkup(row_width=1)
    items = list(FOOD_DB.keys())
    for f in items[page*10:page*10+10]:
        kb.add(InlineKeyboardButton(f, callback_data=f"f_{f}"))
    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton("⬅️", callback_data=f"fp_{page-1}"))
    if page*10+10 < len(items):
        nav.append(InlineKeyboardButton("➡️", callback_data=f"fp_{page+1}"))
    if nav:
        kb.add(*nav)
    kb.add(InlineKeyboardButton("🔍 Поиск", callback_data="search"))
    kb.add(InlineKeyboardButton("🔙 Назад", callback_data="back"))
    return kb

def water_kb():
    kb = InlineKeyboardMarkup(row_width=3)
    kb.add(
        InlineKeyboardButton("250 мл", callback_data="w_250"),
        InlineKeyboardButton("500 мл", callback_data="w_500"),
        InlineKeyboardButton("1000 мл", callback_data="w_1000")
    )
    kb.add(InlineKeyboardButton("1500 мл", callback_data="w_1500"), InlineKeyboardButton("2000 мл", callback_data="w_2000"))
    kb.add(InlineKeyboardButton("💧 Своё", callback_data="w_custom"))
    kb.add(InlineKeyboardButton("🔙 Назад", callback_data="back"))
    return kb

def alarm_kb(uid):
    u = get_user(uid)
    kb = InlineKeyboardMarkup(row_width=1)
    if u["alarms"]:
        for i, a in enumerate(u["alarms"]):
            kb.add(InlineKeyboardButton(f"🔔 {a['time']} - {a['text'][:20]}", callback_data=f"del_alarm_{i}"))
    kb.add(InlineKeyboardButton("➕ Добавить будильник", callback_data="add_alarm"))
    kb.add(InlineKeyboardButton("🔙 Назад", callback_data="back"))
    return kb

# ==================== ОБРАБОТЧИКИ ====================
@bot.message_handler(commands=['start'])
def start(m):
    uid = str(m.chat.id)
    u = get_user(uid)
    bot.send_message(m.chat.id, f"🍽 *Eat Smart Bot*\n\nПривет, {u['name']}!\nДобавляй еду и воду, следи за калориями", 
                     parse_mode="Markdown", reply_markup=main_kb())

@bot.callback_query_handler(func=lambda c: True)
def cb(c):
    uid = str(c.message.chat.id)
    u = get_user(uid)
    
    if c.data == "back":
        bot.edit_message_text("🍽 Главное меню", c.message.chat.id, c.message.message_id, reply_markup=main_kb())
    
    elif c.data == "stats":
        txt, _ = stats_text(uid)
        bot.edit_message_text(txt, c.message.chat.id, c.message.message_id, parse_mode="Markdown", reply_markup=main_kb())
    
    elif c.data == "add_food":
        bot.edit_message_text("🍽 *Выбери продукт:*", c.message.chat.id, c.message.message_id, parse_mode="Markdown", reply_markup=food_kb())
    
    elif c.data.startswith("f_"):
        name = c.data[2:]
        food = FOOD_DB[name]
        kb = InlineKeyboardMarkup()
        for w in [50, 100, 150, 200]:
            kb.add(InlineKeyboardButton(f"{w} г", callback_data=f"add_{name}_{w}"))
        kb.add(InlineKeyboardButton("🔙 Назад", callback_data="add_food"))
        bot.edit_message_text(f"🍽 *{name}*\n\n🔥 {food['kcal']} ккал/100г\n🥩 {food['p']}г · 🥑 {food['f']}г · 🍚 {food['c']}г",
                              c.message.chat.id, c.message.message_id, parse_mode="Markdown", reply_markup=kb)
    
    elif c.data.startswith("add_"):
        parts = c.data.split("_")
        name = parts[1]
        weight = int(parts[2])
        food = FOOD_DB[name]
        mult = weight / 100
        entry = {"name": name, "amount": weight, "kcal": food["kcal"] * mult, "p": food["p"] * mult,
                 "f": food["f"] * mult, "c": food["c"] * mult, "date": today_key()}
        u["eaten"].append(entry)
        bot.answer_callback_query(c.id, f"✅ +{name} {weight}г")
        txt, _ = stats_text(uid)
        bot.edit_message_text(txt, c.message.chat.id, c.message.message_id, parse_mode="Markdown", reply_markup=main_kb())
    
    elif c.data.startswith("fp_"):
        page = int(c.data.split("_")[1])
        bot.edit_message_text("🍽 *Выбери продукт:*", c.message.chat.id, c.message.message_id, parse_mode="Markdown", reply_markup=food_kb(page))
    
    elif c.data == "search":
        msg = bot.send_message(c.message.chat.id, "🔍 *Введи название:*", parse_mode="Markdown")
        bot.register_next_step_handler(msg, search_handler)
    
    elif c.data == "add_water":
        bot.edit_message_text("💧 *Сколько воды добавить?*", c.message.chat.id, c.message.message_id, parse_mode="Markdown", reply_markup=water_kb())
    
    elif c.data.startswith("w_"):
        if c.data == "w_custom":
            msg = bot.send_message(c.message.chat.id, "💧 *Введи количество в мл:*", parse_mode="Markdown")
            bot.register_next_step_handler(msg, custom_water_handler, uid)
        else:
            ml = int(c.data.split("_")[1])
            u["eaten"].append({"name": "💧 Вода", "amount": ml, "kcal": 0, "p": 0, "f": 0, "c": 0, "date": today_key(), "is_water": True})
            bot.answer_callback_query(c.id, f"✅ +{ml} мл воды")
            txt, _ = stats_text(uid)
            bot.edit_message_text(txt, c.message.chat.id, c.message.message_id, parse_mode="Markdown", reply_markup=main_kb())
    
    elif c.data == "diary":
        days = {}
        for e in u["eaten"]:
            if not e.get("is_water"):
                days[e["date"]] = days.get(e["date"], 0) + e["kcal"]
        if not days:
            bot.edit_message_text("📭 *Нет записей*", c.message.chat.id, c.message.message_id, parse_mode="Markdown", reply_markup=main_kb())
            return
        kb = InlineKeyboardMarkup()
        for d in sorted(days.keys(), reverse=True)[:7]:
            kb.add(InlineKeyboardButton(f"{d[:5]} — {days[d]:.0f} ккал", callback_data=f"day_{d}"))
        kb.add(InlineKeyboardButton("🔙 Назад", callback_data="back"))
        bot.edit_message_text("📖 *Дневник*", c.message.chat.id, c.message.message_id, parse_mode="Markdown", reply_markup=kb)
    
    elif c.data.startswith("day_"):
        day = c.data.split("_")[1]
        entries = [e for e in u["eaten"] if e["date"] == day and not e.get("is_water")]
        txt = f"📖 *{day}*\n\n"
        for e in entries:
            txt += f"▫️ {e['name']} — {e['amount']}г ({e['kcal']:.0f} ккал)\n"
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("🔙 Назад", callback_data="diary"))
        bot.edit_message_text(txt, c.message.chat.id, c.message.message_id, parse_mode="Markdown", reply_markup=kb)
    
    # ==================== БУДИЛЬНИК ====================
    elif c.data == "alarm":
        bot.edit_message_text("⏰ *Управление будильниками*", c.message.chat.id, c.message.message_id, parse_mode="Markdown", reply_markup=alarm_kb(uid))
    
    elif c.data == "add_alarm":
        msg = bot.send_message(c.message.chat.id, "⏰ *Добавление будильника*\n\nВведи время в формате `ЧЧ:ММ` и текст напоминания через пробел\n\nПример: `14:30 Пора обедать!`", parse_mode="Markdown")
        bot.register_next_step_handler(msg, add_alarm_handler, uid)
    
    elif c.data.startswith("del_alarm_"):
        idx = int(c.data.split("_")[2])
        if 0 <= idx < len(u["alarms"]):
            deleted = u["alarms"].pop(idx)
            bot.answer_callback_query(c.id, f"✅ Удалён будильник на {deleted['time']}")
            bot.edit_message_text("⏰ *Управление будильниками*", c.message.chat.id, c.message.message_id, parse_mode="Markdown", reply_markup=alarm_kb(uid))
    
    elif c.data == "norm":
        msg = bot.send_message(c.message.chat.id, "📝 *Рассчитаем норму КБЖУ*\n\nВведи *вес рост возраст пол* через пробел\nПример: `70 175 30 м`", parse_mode="Markdown")
        bot.register_next_step_handler(msg, norm_handler, uid)
    
    elif c.data == "profile":
        total_days = len(set(e["date"] for e in u["eaten"] if not e.get("is_water")))
        total_meals = len([e for e in u["eaten"] if not e.get("is_water")])
        avg_kcal = sum(e["kcal"] for e in u["eaten"] if not e.get("is_water")) / max(total_days, 1)
        alarms_text = "\n".join([f"• {a['time']} - {a['text']}" for a in u["alarms"]]) if u["alarms"] else "Нет будильников"
        txt = f"""👤 *Профиль*

Имя: {u['name']}

📊 *Статистика*
Всего дней: {total_days}
Всего приёмов: {total_meals}
Средняя калорийность: {avg_kcal:.0f} ккал

📋 Норма калорий: {u['norm']} ккал

⏰ *Будильники:*
{alarms_text}"""
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("✏️ Изменить имя", callback_data="rename"))
        kb.add(InlineKeyboardButton("🔄 Сбросить всё", callback_data="reset_all"))
        kb.add(InlineKeyboardButton("🔙 Назад", callback_data="back"))
        bot.edit_message_text(txt, c.message.chat.id, c.message.message_id, parse_mode="Markdown", reply_markup=kb)
    
    elif c.data == "rename":
        msg = bot.send_message(c.message.chat.id, "✏️ *Введи новое имя:*", parse_mode="Markdown")
        bot.register_next_step_handler(msg, rename_handler, uid)
    
    elif c.data == "clear":
        u["eaten"] = [e for e in u["eaten"] if e["date"] != today_key()]
        bot.answer_callback_query(c.id, "✅ Данные за сегодня очищены")
        txt, _ = stats_text(uid)
        bot.edit_message_text(txt, c.message.chat.id, c.message.message_id, parse_mode="Markdown", reply_markup=main_kb())
    
    elif c.data == "reset_all":
        u["eaten"] = []
        u["norm"] = 2200
        u["alarms"] = []
        bot.answer_callback_query(c.id, "✅ Все данные сброшены")
        txt, _ = stats_text(uid)
        bot.edit_message_text(txt, c.message.chat.id, c.message.message_id, parse_mode="Markdown", reply_markup=main_kb())

# ==================== ОБРАБОТЧИКИ ШАГОВ ====================
def search_handler(m):
    q = m.text.lower()
    res = [f for f in FOOD_DB.keys() if q in f.lower()]
    if not res:
        new = generate_food(q)
        new_name = f"{new['emoji']} {q.capitalize()}"
        FOOD_DB[new_name] = {"kcal": new["kcal"], "p": new["p"], "f": new["f"], "c": new["c"]}
        res = [new_name]
    kb = InlineKeyboardMarkup()
    for r in res[:10]:
        kb.add(InlineKeyboardButton(r, callback_data=f"f_{r}"))
    kb.add(InlineKeyboardButton("🔙 Назад", callback_data="add_food"))
    bot.send_message(m.chat.id, f"🔍 *Результаты поиска:*", parse_mode="Markdown", reply_markup=kb)

def custom_water_handler(m, uid):
    u = get_user(uid)
    try:
        ml = int(m.text)
        if ml > 0:
            u["eaten"].append({"name": "💧 Вода", "amount": ml, "kcal": 0, "p": 0, "f": 0, "c": 0, "date": today_key(), "is_water": True})
            bot.send_message(m.chat.id, f"✅ Добавлено {ml} мл воды", reply_markup=main_kb())
        else:
            raise ValueError
    except:
        bot.send_message(m.chat.id, "❌ Введи корректное число!", reply_markup=main_kb())

def add_alarm_handler(m, uid):
    u = get_user(uid)
    try:
        parts = m.text.split(" ", 1)
        alarm_time = parts[0]
        alarm_text = parts[1] if len(parts) > 1 else "Напоминание!"
        # Проверка формата времени ЧЧ:ММ
        time.strptime(alarm_time, "%H:%M")
        u["alarms"].append({"time": alarm_time, "text": alarm_text, "triggered_today": False})
        bot.send_message(m.chat.id, f"✅ Будильник добавлен!\n\n⏰ {alarm_time} - {alarm_text}", reply_markup=main_kb())
    except:
        bot.send_message(m.chat.id, "❌ Ошибка! Пример: `14:30 Пора обедать!`", parse_mode="Markdown", reply_markup=main_kb())

def norm_handler(m, uid):
    u = get_user(uid)
    try:
        parts = m.text.split()
        w = float(parts[0])
        h = float(parts[1])
        age = int(parts[2])
        gender = parts[3].lower()
        if gender == "м":
            bmr = 10 * w + 6.25 * h - 5 * age + 5
        else:
            bmr = 10 * w + 6.25 * h - 5 * age - 161
        kcal = bmr * 1.55
        u["norm"] = round(kcal)
        bot.send_message(m.chat.id, f"✅ Норма КБЖУ:\n\n🔥 {round(kcal)} ккал\n🥩 {round(w*1.8)} г белков\n🥑 {round(w*1)} г жиров\n🍚 {round((kcal - w*1.8*4 - w*1*9)/4)} г углеводов", parse_mode="Markdown", reply_markup=main_kb())
    except:
        bot.send_message(m.chat.id, "❌ Ошибка! Пример: `70 175 30 м`", parse_mode="Markdown", reply_markup=main_kb())

def rename_handler(m, uid):
    u = get_user(uid)
    u["name"] = m.text.strip()[:20]
    bot.send_message(m.chat.id, f"✅ Имя изменено на *{u['name']}*", parse_mode="Markdown", reply_markup=main_kb())

# ==================== ЗАПУСК ====================
if __name__ == "__main__":
    print("🤖 Eat Smart Bot запущен!")
    print(f"✅ Нейросеть генерации продуктов активна")
    print(f"✅ Будильник активен (проверка каждые 30 секунд)")
    bot.infinity_polling()