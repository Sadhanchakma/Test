from telegram import ReplyKeyboardMarkup, KeyboardButton
try:
    from telegram.constants import KeyboardButtonStyle  # v21.4+
except ImportError:
    KeyboardButtonStyle = None  # OLD version fallback

from database import load_data, save_data
from config import ADMIN_ID

# ডাটাবেস থেকে ইউজার ডাটা লোড করা
users = load_data()
user_steps = {}
# সার্ভিসের তালিকা এবং মূল্য
services = {
    "Netflix": {
        "1 Month 1 Screen (Share) Price 350": 350, 
        "1 Month 2 Screen (Share) Price 680": 680
    },
    "Spotify": {
        "1 Month (Premium) Price 200": 200, 
        "3 Month (Premium) Price 580": 580
    },
    "YouTube Premium": {
        "1 Month (Premium) Price 120": 120, 
        "1 Year (Premium) Price 2899": 2899
    },
    "Amazon Prime": {
        "1 Month (Premium) Price 100": 100, 
        "3 Month (Premium) Price 300": 300
    },
    "Crunchyroll": {
        "1 Month (Premium) Price 180": 180, 
        "3 Month (Premium) Price 499": 499
    },
    "Hulu": {
        "1 Month (Premium) Price 230": 230, 
        "3 Month (Premium) Price 650": 650
    },
    "Disney+": {
        "1 Month (Premium) Price 350": 350, 
        "3 Month (Premium) Price 1050": 1050
    },
    "Disney+ Hotstar": {
        "1 Month (Premium) Price 180": 180, 
        "3 Month (Premium) Price 540": 540
    },
    "HBO Max": {
        "1 Month (Premium) Price 180": 180, 
        "3 Month (Premium) Price 540": 540
    },
    "Telegram Premium": {
        "1 Month (Premium) Price 600": 600, 
        "3 Month (Premium) Price 1800": 1800
    }
}

# ✅ BULLETPROOF BLUE KEYBOARD - Works on ALL hosting!
def get_blue_keyboard(buttons):
    """BLUE ReplyKeyboard - v21.4+ = BLUE, OLD = Regular (both look great!)"""
    if KeyboardButtonStyle:
        # NEW VERSION: TRUE BLUE BUTTONS! 🔵
        blue_keyboard = []
        for row in buttons:
            blue_row = [KeyboardButton(text, style=KeyboardButtonStyle.PRIMARY) for text in row]
            blue_keyboard.append(blue_row)
        return ReplyKeyboardMarkup(blue_keyboard, resize_keyboard=True)
    else:
        # OLD VERSION: Regular buttons (still professional)
        regular_keyboard = [[KeyboardButton(text) for text in row] for row in buttons]
        return ReplyKeyboardMarkup(regular_keyboard, resize_keyboard=True)

# ---------------- MAIN MENU ----------------
async def main_menu(update):
    keyboard = [["💰 Balance", "➕ Add Balance"], ["🛒 Buy Service", "🎁 Referral"], ["❓ Help"]]
    await update.message.reply_text(
        '<tg-emoji emoji-id="5416041192905265756">🏠</tg-emoji> <b>Main Menu</b>',
        reply_markup=get_blue_keyboard(keyboard),
        parse_mode="HTML"
    )


# ---------------- START COMMAND ----------------
async def start(update, context):
    user = update.message.from_user
    user_id = str(user.id)
    full_name = user.first_name 
    username = user.username or "No Username"

    # নতুন ইউজার রেজিস্ট্রেশন এবং রেফারেল চেক
    if user_id not in users:
        referrer_id = context.args[0] if context.args else None
        users[user_id] = {"balance": 0, "referred_by": referrer_id, "refer_count": 0}
        
        if referrer_id and referrer_id in users and referrer_id != user_id:
            users[referrer_id]["balance"] += 5 
            users[referrer_id]["refer_count"] = users[referrer_id].get("refer_count", 0) + 1
            try:
                await context.bot.send_message(
                    chat_id=int(referrer_id), 
                    text='<tg-emoji emoji-id="4958699241137505132">🎁</tg-emoji> <b>আপনার লিংকে নতুন একজন জয়েন করেছে! আপনি ৫ টাকা বোনাস পেয়েছেন।</b>',
                    parse_mode="HTML"
                )
            except: 
                pass
        save_data(users)

    keyboard = [
        ["💰 Balance", "➕ Add Balance"],
        ["🛒 Buy Service", "🎁 Referral"],
        ["❓ Help"]
    ]

    welcome_msg = (
        f'<tg-emoji emoji-id="5413694143601842851">👋</tg-emoji> <b>স্বাগতম! {full_name}</b>\n\n'
        f'<tg-emoji emoji-id="5373012449597335010">👤</tg-emoji> <b>Username:</b> @{username}\n'
        f'<tg-emoji emoji-id="5841276284155467413">🆔</tg-emoji> <b>User ID:</b> <code>{user_id}</code>\n\n'
        f'<tg-emoji emoji-id="4958926882994127612">💰</tg-emoji> <b>Balance:</b> {users[user_id]["balance"]} Tk\n'
        f'━━━━━━━━━━━━━━━━━━━━\n'
        f'<tg-emoji emoji-id="4958489311726011319">✨</tg-emoji> <b>আপনার অ্যাকাউন্ট সফলভাবে লোড হয়েছে</b>\n'
        f'━━━━━━━━━━━━━━━━━━━━'
    )

    await update.message.reply_text(
        welcome_msg,
        reply_markup=get_blue_keyboard(keyboard),  # CHANGED TO BLUE!
        parse_mode="HTML"
    )

# ---------------- HANDLE TEXT MESSAGES ----------------
async def handle(update, context):
    user_id = update.message.from_user.id
    text = update.message.text
    uid = str(user_id)
    bot_username = (await context.bot.get_me()).username

    # নেভিগেশন বাটন
    if text == "🔙 Back":
        user_steps.pop(user_id, None)
        return await main_menu(update)

    if text == "❌ Cancel":
        user_steps.pop(user_id, None)
        return await update.message.reply_text(
            '<tg-emoji emoji-id="4958526153955476488">❌</tg-emoji> <b>Process cancelled</b>', 
            reply_markup=get_blue_keyboard([["🔙 Back"]]),  # BLUE BACK BUTTON!
            parse_mode="HTML"
        )

    # ব্যালেন্স চেক
    if text == "💰 Balance":
        bal = users[uid]["balance"]
        return await update.message.reply_text(
            f'<tg-emoji emoji-id="4958926882994127612">💰</tg-emoji> <b>বর্তমান টাকার পরিমাণ:</b> {bal} Tk', 
            reply_markup=get_blue_keyboard([["🔙 Back"]]),  # BLUE BACK!
            parse_mode="HTML"
        )

    # রেফারেল তথ্য
    if text == "🎁 Referral":
        refer_link = f"https://t.me/{bot_username}?start={user_id}"
        count = users[uid].get("refer_count", 0)
        ref_msg = (
            f'<tg-emoji emoji-id="4958699241137505132">🎁</tg-emoji> <b>আপনার রেফারেল তথ্য</b>\n\n'
            f'<tg-emoji emoji-id="4958689671950369798">🔗</tg-emoji> <b>লিংক:</b> <code>{refer_link}</code>\n'
            f'<tg-emoji emoji-id="5372926953978341366">👥</tg-emoji> <b>মোট রেফার:</b> {count} জন'
        )
        return await update.message.reply_text(
            ref_msg, 
            reply_markup=get_blue_keyboard([["🔙 Back"]]),  # BLUE BACK!
            parse_mode="HTML"
        )

    # সাহায্য মেনু
    if text == "❓ Help":
        help_text = (
            f'<tg-emoji emoji-id="6210598417404534865">ℹ️</tg-emoji> '
            f'<tg-emoji emoji-id="6210868652451832759">❓</tg-emoji> '
            f'<tg-emoji emoji-id="6213057917541688006">🆘</tg-emoji> '
            f'@Sadhan_Chakma '
            f'<tg-emoji emoji-id="6212779255768554475">💠</tg-emoji>\n\n'
            f'<b>বটটি যেভাবে কাজ করে:</b>\n'
            f'১. প্রথমে <b>Add Balance</b> এ গিয়ে টাকা রিচার্জ করুন।\n'
            f'২. টাকা অ্যাড হলে <b>Buy Service</b> থেকে আপনার পছন্দের সার্ভিসটি বেছে নিন।'
        )
        return await update.message.reply_text(
            help_text, 
            reply_markup=get_blue_keyboard([["🔙 Back"]]),  # BLUE BACK!
            parse_mode="HTML"
        )

    # ব্যালেন্স অ্যাড করার ধাপ শুরু
    if text == "➕ Add Balance":
        user_steps[user_id] = {"step": "method"}
        keyboard = [["bKash", "Nagad"], ["Rocket", "Binance"], ["🔙 Back", "❌ Cancel"]]
        return await update.message.reply_text(
            '<tg-emoji emoji-id="6273684842668366415">💳</tg-emoji> <b>পেমেন্ট মেথড নির্বাচন করুন:</b>', 
            reply_markup=get_blue_keyboard(keyboard),  # BLUE PAYMENT BUTTONS!
            parse_mode="HTML"
        )

    # পেমেন্ট মেথড হ্যান্ডলার
    payment_methods = ["bKash", "Nagad", "Rocket", "Binance"]
    if text in payment_methods:
        numbers = {"bKash": "01537310053", "Nagad": "01533833020", "Rocket": "01537310053", "Binance": "989885533"}
        method_emojis = {
            "bKash": "6172387334617569402", 
            "Nagad": "6172505618016900525", 
            "Rocket": "6300809090150964522", 
            "Binance": "6172522041971842488"
        }
        user_steps[user_id] = {"step": "amount", "method": text}
        m_emoji = method_emojis.get(text)
        return await update.message.reply_text(
            f'<tg-emoji emoji-id="{m_emoji}">🏩</tg-emoji> <b>{text} Number:</b>\n\n'
            f'<code>{numbers[text]}</code>\n\n'
            f'<tg-emoji emoji-id="4956601935592424315">💲</tg-emoji> Minimum Amount : 100 Tk\n'
            f'<tg-emoji emoji-id="6158862632926319619">👉</tg-emoji> <b>আপনার টাকার পরিমাণ দেন:</b>', 
            reply_markup=get_blue_keyboard([["🔙 Back", "❌ Cancel"]]),  # BLUE BACK/CANCEL!
            parse_mode="HTML"
        )

    # সার্ভিস কেনা শুরু
    if text == "🛒 Buy Service":
        user_steps[user_id] = {"step": "service"}
        keyboard = [[s] for s in services.keys()] + [["🔙 Back"]]
        return await update.message.reply_text(
            '<tg-emoji emoji-id="5431499171045581032">🛒</tg-emoji> <b>Service select করুন:</b>', 
            reply_markup=get_blue_keyboard(keyboard),  # BLUE SERVICE BUTTONS!
            parse_mode="HTML"
        )

    # ইউজার স্টেপ অনুযায়ী ইনপুট হ্যান্ডলিং
    if user_id in user_steps:
        step = user_steps[user_id]["step"]

        if step == "amount":
            if not text.isdigit(): 
                return await update.message.reply_text(
                    "❌ সংখ্যা দিন", 
                    reply_markup=get_blue_keyboard([["🔙 Back"]])  # BLUE BACK!
                )
            user_steps[user_id].update({"step": "trx", "amount": int(text)})
            return await update.message.reply_text(
                '<tg-emoji emoji-id="5330115548900501467">🔑</tg-emoji> <b>ট্রানজ্যাকশন আইডি (TRX ID) দিন:</b>', 
                reply_markup=get_blue_keyboard([["🔙 Back", "❌ Cancel"]]),  # BLUE!
                parse_mode="HTML"
            )

        elif step == "trx":
            user_steps[user_id].update({"step": "ss", "trx": text})
            return await update.message.reply_text(
                '<tg-emoji emoji-id="5235837920081887219">📸</tg-emoji> <b>পেমেন্টের স্ক্রিনশটটি পাঠান:</b>', 
                reply_markup=get_blue_keyboard([["🔙 Back", "❌ Cancel"]]),  # BLUE!
                parse_mode="HTML"
            )

        elif step == "service":
            if text not in services: return
            user_steps[user_id].update({"step": "plan", "service": text})
            s_emojis = {
                "Netflix": "6212718494866218568", "Spotify": "6210917542064562518",
                "YouTube Premium": "6212927921766538445", "Amazon Prime": "6212752888964328143",
                "Telegram Premium": "6212844260098581451", "Disney+ Hotstar": "6210529324265643615",
                "HBO Max": "6210840035084738342", "Crunchyroll": "6195129886529559586"
            }
            s_id = s_emojis.get(text, "4956719506027185156")
            keyboard = [[p] for p in services[text].keys()] + [["🔙 Back"]]
            return await update.message.reply_text(
                f'<tg-emoji emoji-id="{s_id}">💎</tg-emoji> <b>{text} plan select করুন:</b>', 
                reply_markup=get_blue_keyboard(keyboard),  # BLUE PLAN BUTTONS!
                parse_mode="HTML"
            )

        elif step == "plan":
            service = user_steps[user_id]["service"]
            if text not in services[service]: return
            price = services[service][text]
            if users[uid]["balance"] >= price:
                users[uid]["balance"] -= price
                save_data(users)
                user_steps.pop(user_id)
                return await update.message.reply_text(
                    f'<tg-emoji emoji-id="4958610528588008305">✅</tg-emoji> <b>অর্ডার সফল হয়েছে!</b>\n\n'
                    f'📦 সার্ভিস: {service}\n💎 প্ল্যান: {text}\n💰 মূল্য: {price} Tk\n'
                    f'━━━━━━━━━━━━━━━━━━━━\n<tg-emoji emoji-id="5433614747381538714">📤</tg-emoji> @Sadhan_chakma',
                    reply_markup=get_blue_keyboard([["🔙 Back"]]),  # BLUE BACK!
                    parse_mode="HTML"
                )
            else:
                return await update.message.reply_text(
                    '<tg-emoji emoji-id="6215419994935660864">❗️</tg-emoji> <b>ব্যালেন্স পর্যাপ্ত নয়।</b>', 
                    reply_markup=get_blue_keyboard([["🔙 Back"]]),  # BLUE BACK!
                    parse_mode="HTML"
                )

# ---------------- PHOTO HANDLER ----------------
async def handle_photo(update, context):
    user_id = update.message.from_user.id
    if user_id in user_steps and user_steps[user_id]["step"] == "ss":
        data = user_steps[user_id]
        
        caption = (
            f'<tg-emoji emoji-id="4956480749147521743">💰</tg-emoji> <b>New Request</b>\n'
            f'<tg-emoji emoji-id="5373012449597335010">👤</tg-emoji> <b>ID:</b> <code>{user_id}</code>\n'
            f'<tg-emoji emoji-id="6273684842668366415">💳</tg-emoji> <b>Method:</b> {data["method"]}\n'
            f'<tg-emoji emoji-id="4958926882994127612">💵</tg-emoji> <b>Amount:</b> {data["amount"]} Tk\n'
            f'<tg-emoji emoji-id="5330115548900501467">🔑</tg-emoji> <b>TRX:</b> <code>{data["trx"]}</code>'
        )

        try:
            await context.bot.send_photo(
                chat_id=ADMIN_ID, 
                photo=update.message.photo[-1].file_id, 
                caption=caption, 
                parse_mode="HTML"
            )
        except:
            plain_caption = f"💰 New Request\n👤 ID: {user_id}\n💳 Method: {data['method']}\n💵 Amount: {data['amount']} Tk\n🔑 TRX: {data['trx']}"
            await context.bot.send_photo(
                chat_id=ADMIN_ID, 
                photo=update.message.photo[-1].file_id, 
                caption=plain_caption
            )
            
        await update.message.reply_text(
            '<tg-emoji emoji-id="4958587679361991667">🔎</tg-emoji> <b>রিকুয়েস্ট সফল! যাচাই শেষে ব্যালেন্স যোগ হবে।</b>', 
            reply_markup=get_blue_keyboard([["🔙 Back"]]),  # BLUE BACK!
            parse_mode="HTML"
        )
        user_steps.pop(user_id)

# ---------------- ADMIN ADD BALANCE COMMAND ----------------
async def addbalance(update, context):
    if update.message.from_user.id != ADMIN_ID: return
    try:
        u_id, amount = context.args[0], int(context.args[1])
        if u_id not in users: 
            users[u_id] = {"balance": 0}
        
        users[u_id]["balance"] += amount
        save_data(users)
        
        await update.message.reply_text(f"✅ Balance Added to {u_id}!")
        await context.bot.send_message(
            chat_id=int(u_id), 
            text=f'<tg-emoji emoji-id="4958926882994127612">💰</tg-emoji> <b>{amount} Tk added to your balance!</b>', 
            reply_markup=get_blue_keyboard([["🔙 Back"]]),  # BLUE BACK!
            parse_mode="HTML"
        )
    except:
        await update.message.reply_text("❌ Use: /addbalance user_id amount")
