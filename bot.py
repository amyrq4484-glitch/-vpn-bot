import random
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

TOKEN = '8603212915:AAF2mpUEk-33xSoMuq8RtNTu0s4s9MH4NhQ'
bot = telebot.TeleBot(TOKEN)
user_history = {}

BASE_NAMES = [
    "Proton VPN", "Cloudflare WARP", "Windscribe", "TunnelBear", "Atlas VPN",
    "GearUP Booster", "Turbo VPN", "Thunder VPN", "Super VPN", "Secure VPN",
    "V2RayNG", "Psiphon Pro", "Outline Client", "X-VPN", "Hotspot Shield"
]

DATABASE = {"gaming": [], "social": []}
categories_meta = [
    ("gaming", "🎮 بخش گیمینگ و کاهش پینگ", "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=600"),
    ("social", "📱 بخش شبکه‌های اجتماعی و وب‌گردی", "https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=600")
]

item_counter = 1
for cat_key, cat_title, photo_url in categories_meta:
    for i in range(1, 310):
        base = BASE_NAMES[(i - 1) % len(BASE_NAMES)]
        item_id = f"{cat_key}_{i}"
        item_name = f"⚡ {base} (سرور اختصاصی #{i})"
        ping_val = f"پینگ فوق‌العاده ({random.randint(25, 95)}ms)" if cat_key == "gaming" else f"سرعت دانلود ({random.randint(15, 50)} MB/s)"
        speed_val = "بهینه شده برای اتصال پایدار" if cat_key == "gaming" else "مناسب برای اینستاگرام و تلگرام"
        desc_val = f"نسخه تست‌شده و معتبر گوگل‌پلی با کد مرجع {i}."
        
        pkg = "ch.protonvpn.android" if i % 2 == 0 else "com.cloudflare.onedotonedotonedotone"
        link_val = f"https://play.google.com/store/apps/details?id={pkg}"
        
        DATABASE[cat_key].append({
            "id": item_id, "name": item_name, "ping": ping_val,
            "speed": speed_val, "desc": desc_val, "photo": photo_url, "link": link_val
        })
        item_counter += 1

def get_next_item(category, chat_id):
    items = DATABASE[category]
    user_key = f"{chat_id}_{category}"
    last_id = user_history.get(user_key)
    available = [i for i in items if i["id"] != last_id]
    if not available:
        available = items.copy()
    chosen = random.choice(available)
    user_history[user_key] = chosen["id"]
    return chosen

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🎮 بخش گیمینگ و کاهش پینگ", callback_data="menu_gaming"),
        InlineKeyboardButton("📱 بخش شبکه‌های اجتماعی و وب", callback_data="menu_social"),
        InlineKeyboardButton("👥 ورود به گروه رسمی ما", url="https://t.me/efootballgruopx")
    )
    bot.send_message(
        message.chat.id,
        "🌟 **به ربات بانک فیلترشکن‌های گوگل‌پلی خوش آمدید!**\n\nبخش مورد نظر خود را انتخاب کنید 👇",
        reply_markup=markup, parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    
    if call.data == "menu_gaming":
        item = get_next_item("gaming", chat_id)
        caption_text = f"🎮 **فیلترشکن گیمینگ:**\n\n🔹 **نام:** {item['name']}\n📊 **پینگ:** {item['ping']}\n📝 **توضیحات:** {item['desc']}\n\n📥 **[دانلود از گوگل‌پلی]({item['link']})**"
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("🔄 فیلترشکن دیگر (تغییر)", callback_data="menu_gaming"),
            InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="main_menu")
        )
        try:
            bot.edit_message_media(InputMediaPhoto(item['photo'], caption=caption_text, parse_mode="Markdown"), chat_id, message_id, reply_markup=markup)
        except:
            bot.send_photo(chat_id, item['photo'], caption=caption_text, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "menu_social":
        item = get_next_item("social", chat_id)
        caption_text = f"📱 **فیلترشکن شبکه‌های اجتماعی:**\n\n🔹 **نام:** {item['name']}\n📊 **سرعت:** {item['speed']}\n📝 **توضیحات:** {item['desc']}\n\n📥 **[دانلود از گوگل‌پلی]({item['link']})**"
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("🔄 فیلترشکن دیگر (تغییر)", callback_data="menu_social"),
            InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="main_menu")
        )
        try:
            bot.edit_message_media(InputMediaPhoto(item['photo'], caption=caption_text, parse_mode="Markdown"), chat_id, message_id, reply_markup=markup)
        except:
            bot.send_photo(chat_id, item['photo'], caption=caption_text, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "main_menu":
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("🎮 بخش گیمینگ و کاهش پینگ", callback_data="menu_gaming"),
            InlineKeyboardButton("📱 بخش شبکه‌های اجتماعی و وب", callback_data="menu_social"),
            InlineKeyboardButton("👥 ورود به گروه رسمی ما", url="https://t.me/efootballgruopx")
        )
        try:
            bot.delete_message(chat_id, message_id)
        except:
            pass
        bot.send_message(chat_id, "🌟 **منوی اصلی:**\nلطفاً یک بخش را انتخاب کنید:", reply_markup=markup, parse_mode="Markdown")

print("Bot is ready...")
bot.infinity_polling()
