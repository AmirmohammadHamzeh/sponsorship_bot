import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import sqlite  # Import the sqlite module

# Logging settings for detailed error observation
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Bot token and channels list
TOKEN = '7249726653:AAER3yUT6ezMe9ypfQOQyaCHh7FQ88LuCQQ'
CHANNELS = ['testhamzehproject1', 'testhamzehproject2', 'testhamzehproject3']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    bot = context.bot
    missing_channels = []

    # Add user to database
    new_user_added = sqlite.add_user(user.id)
    if new_user_added:
        logging.info(f"New user added: user_id={user.id}")
    else:
        logging.info(f"User already exists: user_id={user.id}")

    try:
        for channel in CHANNELS:
            member = await bot.get_chat_member(chat_id=f"@{channel}", user_id=user.id)
            if member.status not in ['member', 'administrator', 'creator']:
                missing_channels.append(channel)
    except Exception as e:
        logging.error(f"Error checking membership: {e}")
        await update.message.reply_text('There was an error. Please try again later.')
        return

    if not missing_channels:
        await update.message.reply_text('You are already a member of all channels.')
        sqlite.update_membership_status(user.id, True)  # Update membership status
    else:
        # Creating buttons for missing channels and membership check
        keyboard = [
            [InlineKeyboardButton(f"Join {channel}", url=f"https://t.me/{channel}") for channel in missing_channels],
            [InlineKeyboardButton("Check Membership", callback_data='check')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('Please join the following channels:', reply_markup=reply_markup)
        sqlite.update_membership_status(user.id, False)  # Update membership status

async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    bot = context.bot
    missing_channels = []

    try:
        for channel in CHANNELS:
            member = await bot.get_chat_member(chat_id=f"@{channel}", user_id=user.id)
            if member.status not in ['member', 'administrator', 'creator']:
                missing_channels.append(channel)
    except Exception as e:
        logging.error(f"Error checking membership: {e}")
        await query.edit_message_text('There was an error. Please try again later.')
        return

    if not missing_channels:
        await query.edit_message_text('You are a member of all channels.')
        sqlite.update_membership_status(user.id, True)  # Update membership status
    else:
        # Creating buttons for missing channels
        keyboard = [[InlineKeyboardButton(f"Join {channel}", url=f"https://t.me/{channel}")] for channel in missing_channels]
        keyboard.append([InlineKeyboardButton("Check Membership", callback_data='check')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text('Please join all the channels:', reply_markup=reply_markup)
        sqlite.update_membership_status(user.id, False)  # Update membership status

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(check_membership))

    application.run_polling()

if __name__ == '__main__':
    main()