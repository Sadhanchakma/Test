from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from config import TOKEN
from handlers import start, handle, handle_photo, addbalance  # ✅ addbalance add

app = ApplicationBuilder().token(TOKEN).build()

# ✅ COMMAND HANDLER FIRST
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("addbalance", addbalance))  # ✅ add this

# ✅ THEN MESSAGE HANDLER
app.add_handler(MessageHandler(filters.TEXT, handle))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

app.run_polling()
