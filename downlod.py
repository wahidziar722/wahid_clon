#!/usr/bin/env python3
"""
د Telegram وډیو ډاونلوډ بوټ - د python-telegram-bot v20.7 سره
"""

import os
import logging
import asyncio
from datetime import datetime

# د python-telegram-bot v20.x سره سم imports
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext
)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import yt_dlp
import re

# ==================== د لوګینګ تنظیم ====================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==================== د بوټ توکن ====================
BOT_TOKEN = "8397436161:AAGZxrg2cBvsiso5hQXUPKtLBmvSEKIwkz8"

# ==================== د بوټ فعالیتونه ====================
async def start_command(update: Update, context: CallbackContext):
    """د /start کمانډ"""
    user = update.effective_user
    
    welcome_text = f"""
    🎬 **د وډیو ډاونلوډ بوټ** ته ښه راغلې {user.first_name}!

    👨‍💻 **جوړونکی:** @Itxwahid
    📢 **چینل:** https://t.me/acg_group_cyber

    📌 **لارښود:**
    1. لومړی چینل سره یوځای شئ
    2. هر وډیو لینک راولیږئ
    3. وډیو به ډاونلوډ شي

    🌐 **مشتري پلیټفارمونه:**
    • TikTok, Instagram, YouTube
    • Facebook, Twitter/X
    • نور ډیری...

    🔗 **نمونه لینکونه:**
    https://www.tiktok.com/@user/video/123
    https://www.instagram.com/reel/ABC123/
    https://youtu.be/dQw4w9WgXcQ
    """
    
    keyboard = [
        [InlineKeyboardButton("📢 چینل سره یوځای شئ", url="https://t.me/acg_group_cyber")],
        [InlineKeyboardButton("✅ چینل سره یوځای شوم", callback_data="check_joined")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_video_link(update: Update, context: CallbackContext):
    """د وډیو لینک پروسس کول"""
    url = update.message.text.strip()
    
    # د لینک اعتبار چک
    url_pattern = r'https?://(?:www\.)?(?:tiktok\.com|instagram\.com|youtube\.com|youtu\.be)/\S+'
    
    if re.match(url_pattern, url):
        await update.message.reply_text("🔄 وډیو پروسس کیږي...")
        
        try:
            # د وډیو ډاونلوډ
            await download_video(url, update, context)
        except Exception as e:
            await update.message.reply_text(f"❌ تېروتنه: {e}")
    else:
        await update.message.reply_text("❌ مهرباني وکړئ یو معتبر وډیو لینک ولیکئ.")

async def download_video(url, update: Update, context: CallbackContext):
    """د وډیو ډاونلوډ او لیږل"""
    try:
        # د downloads فولدر جوړول
        if not os.path.exists('downloads'):
            os.makedirs('downloads')
        
        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'format': 'best',
            'quiet': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # د وډیو لیږل
            with open(filename, 'rb') as video_file:
                await update.message.reply_video(
                    video=video_file,
                    caption=f"✅ وډیو بریالۍ ډاونلوډ شوه!\n\n🙏 **مننه چی زموړ بوټ کاروئ!**\n👨‍💻 **بوټ جوړونکی:** @Itxwahid"
                )
            
            # د فایل پاکول
            os.remove(filename)
            
    except Exception as e:
        logger.error(f"د ډاونلوډ تېروتنه: {e}")
        await update.message.reply_text("❌ د وډیو ډاونلوډ کې ستونزه رامنځته شوه.")

async def error_handler(update: Update, context: CallbackContext):
    """د تېروتنو مدیریت"""
    logger.error(f"❌ تېروتنه: {context.error}")
    if update and update.effective_chat:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⚠️ د بوټ ستونزې رامنځته شوې. لطفاً بیا هڅه وکړئ."
        )

# ==================== د بوټ پیلول ====================
def main():
    """د بوټ اصلي فنکشن"""
    print("=" * 50)
    print("🤖 Telegram Video Download Bot")
    print("📦 د python-telegram-bot v20.7 سره")
    print("👨‍💻 جوړونکی: @Itxwahid")
    print("=" * 50)
    
    # د Application جوړول
    application = Application.builder().token(BOT_TOKEN).build()
    
    # د handlers اضافه کول
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_video_link))
    
    # د تېروتنو handler
    application.add_error_handler(error_handler)
    
    # د بوټ پیلول
    application.run_polling(
        drop_pending_updates=True,
        allowed_updates=Update.ALL_TYPES
    )

if __name__ == "__main__":
    # د بوټ پیلول
    asyncio.run(main())