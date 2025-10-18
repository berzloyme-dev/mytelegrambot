# bot.py
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import (
    Message, CallbackQuery,
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.filters import Command
from deep_translator import GoogleTranslator
from langdetect import detect, LangDetectException

# === Sozlamalar ===
TOKEN = "8465969217:AAEsu7AYFnLLflg2XwURYFIrXdCucjOBNUo"
OWNER_ID = 958705445
SECRET_PASSWORD = "00"

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_waiting_password = set()
translator_active_users = set()


async def notify_owner(text: str):
    try:
        await bot.send_message(OWNER_ID, text, disable_notification=True)
    except Exception:
        pass


@dp.message(Command("start"))
async def start_cmd(message: Message):
    menyu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📌 Ijtimoiy tarmoq"), KeyboardButton(text="🔐 Maxfiy bo‘lim")],
            [KeyboardButton(text="📡 Obuna kanallar"), KeyboardButton(text="🌍 Tarjimon")],
        ],
        resize_keyboard=True,
    )
    await message.answer("👋 Xush kelibsiz!", reply_markup=menyu)
    await notify_owner(f"📥 /start — @{message.from_user.username} (id: {message.from_user.id})")


@dp.callback_query()
async def callback_handler(callback: CallbackQuery):
    data = callback.data

    if data == "telegram_menu":
        tg_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="👤 Profil", url="https://t.me/Muhammadmuso_Alijonov")],
                [InlineKeyboardButton(text="📢 Kanal", url="https://t.me/s/alijonov133")],
                [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_main")],
            ]
        )
        await callback.message.edit_text("📱 Telegram bo‘limi 👇", reply_markup=tg_keyboard)
        await notify_owner(f"📲 Telegram tugmasi — @{callback.from_user.username}")

    elif data == "back_main":
        main_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📱 Telegram", callback_data="telegram_menu")],
                [InlineKeyboardButton(text="📸 Instagram", url="https://instagram.com/1.alijonov_muhammadmuso")],
                [InlineKeyboardButton(text="📘 Facebook", url="https://facebook.com/sizning_username")],
            ]
        )
        await callback.message.edit_text("🌐 Mening sahifalarim 👇", reply_markup=main_keyboard)

    await callback.answer()


@dp.message()
async def messages_handler(message: Message):
    user_id = message.from_user.id
    text = (message.text or "").strip()

    # 📌 Menyu tugmalari
    if text == "📌 Ijtimoiy tarmoq":
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📱 Telegram", callback_data="telegram_menu")],
                [InlineKeyboardButton(text="📸 Instagram", url="https://instagram.com/1.alijonov_muhammadmuso")],
                [InlineKeyboardButton(text="📘 Facebook", url="https://facebook.com/sizning_username")],
            ]
        )
        await message.answer("🌐 Mening sahifalarim 👇", reply_markup=kb)
        return

    if text == "🔐 Maxfiy bo‘lim":
        user_waiting_password.add(user_id)
        await message.answer("🔑 Parolni kiriting:")
        return

    if text == "📡 Obuna kanallar":
        kanallar = ["@alijonov133", "@python_uz", "@aiogram_news"]
        javob = "📢 Ochiq kanallar ro‘yxati:\n\n" + "\n".join(kanallar)
        await message.answer(javob)
        return

    if text == "🌍 Tarjimon":
        translator_active_users.add(user_id)
        await message.answer("🌍 Tarjimon faollashdi. Matn kiriting (🇺🇸 Inglizcha bo‘lsa O‘zbekchaga, aks holda inglizchaga tarjima qilaman). To‘xtatish uchun /stop_trans yozing.")
        return

    if text == "/stop_trans":
        translator_active_users.discard(user_id)
        await message.answer("🛑 Tarjimon o‘chirildi.")
        return

    # 🔐 Maxfiy bo‘lim — parol
    if user_id in user_waiting_password:
        if text == SECRET_PASSWORD:
            user_waiting_password.remove(user_id)
            await message.answer(
                "🪪 *Shaxsiy ma'lumotlarim*\n"
                "━━━━━━━━━━━━━━━\n"
                "👤 Ism: Muhammadmuso Alijonov Faxriddin o‘g‘li\n"
                "🎓 Kasb: Talaba\n"
                "🏦 Orzusi: Dasturchi\n"
                "🚛 Yoqtirgan kasbi: Yuk mashina haydovchisi\n"
                "🏦 Ishlash orzusi: Bankda\n"
                "🎬 Yoqtirgan filmlar: Kulrang odam, Fokus, Kelajak urushi\n"
                "📱 Telegram: @Muhammadmuso_Alijonov\n"
                "📸 Instagram: @1.alijonov_muhammadmuso\n"
                "━━━━━━━━━━━━━━━\n"
                "🔒 *Bu maxfiy sahifa — faqat siz uchun!*",
                parse_mode="Markdown"
            )
        else:
            await message.answer("❌ Parol noto‘g‘ri! Qayta urinib ko‘ring.")
        return

    # 🌍 Tarjimon rejimi — inglizcha ↔ o‘zbekcha
    if user_id in translator_active_users and text:
        await message.answer("⌛ Tarjima qilinmoqda...")
        try:
            try:
                lang = detect(text)
            except LangDetectException:
                lang = "auto"

            # Inglizcha bo‘lsa o‘zbekchaga
            if lang.startswith("en"):
                translated = GoogleTranslator(source='en', target='uz').translate(text)
                await message.answer(f"🇺🇸 ➜ 🇺🇿\n{translated}")
            else:
                # Aks holda o‘zbekchadan inglizchaga
                translated = GoogleTranslator(source='auto', target='en').translate(text)
                await message.answer(f"🇺🇿 ➜ 🇺🇸\n{translated}")
        except Exception as e:
            await message.answer(f"⚠️ Tarjima xatoligi: {e}")
        return

    # 📨 Oddiy foydalanuvchi xabari — admin (OWNER_ID) ga yuboriladi
    if user_id != OWNER_ID:
        msg_to_owner = (
            f"📨 Yangi xabar!\n"
            f"👤 {message.from_user.full_name}\n"
            f"🆔 {user_id}\n"
            f"💬 {text}"
        )
        await bot.send_message(OWNER_ID, msg_to_owner)
        return

    # 👑 Admin reply qilib foydalanuvchiga javob beradi
    if message.reply_to_message and user_id == OWNER_ID:
        replied_text = message.reply_to_message.text or ""
        if "🆔" in replied_text:
            try:
                user_line = [line for line in replied_text.splitlines() if "🆔" in line][0]
                target_id = int(user_line.replace("🆔", "").strip())
                await bot.send_message(target_id, f"📩 Admin javobi:\n{message.text}")
                await message.answer("✅ Foydalanuvchiga yuborildi.")
            except Exception as e:
                await message.answer(f"❌ IDni topishda xato: {e}")
        return

    await message.answer("⚠️ Men bu xabarni tushunmadim. /start yozing.")


async def main():
    print("🤖 Bot ishga tushdi!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
