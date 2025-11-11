main.py:

```python
import os
import requests
import time
from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler

# تنظیمات
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '253782041:AAFs4_s8euDNuzZkFAOYogJPjihBZf3xo0g')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '@bahala_gp')

bot = Bot(token=TELEGRAM_TOKEN)

def check_whales():
    """بررسی تراکنش‌های بزرگ"""
    try:
        print("🔍 در حال بررسی تراکنش‌ها...")
        response = requests.get('https://mempool.space/api/mempool', timeout=10)
        mempool = response.json()
        
        large_transactions = []
        for tx_id, tx_info in list(mempool.items())[:50]:  # فقط 50 تا اول
            if tx_info.get('fee', 0) > 50000:  # کارمزد بالا
                large_transactions.append(tx_info)
        
        if large_transactions:
            message = "🐋 **تراکنش بزرگ بیت‌کوین**\n\n"
            for tx in large_transactions[:3]:  # فقط 3 تا
                message += f"💸 کارمزد: {tx['fee']:,} ساتوشی\n"
                message += f"📦 سایز: {tx['size']} بایت\n\n"
            
            bot.send_message(chat_id=CHAT_ID, text=message)
            print("✅ پیام ارسال شد")
        else:
            print("✅ تراکنش بزرگی یافت نشد")
            
    except Exception as e:
        print(f"❌ خطا: {e}")

def main():
    """اجرای اصلی"""
    print("🚀 ربات نهنگ‌یاب شروع به کار کرد")
    
    # زمان‌بندی بررسی هر 20 دقیقه
    scheduler = BlockingScheduler()
    scheduler.add_job(check_whales, 'interval', minutes=20)
    
    # اولین اجرا
    check_whales()
    
    try:
        scheduler.start()
    except KeyboardInterrupt:
        print("⏹️ ربات متوقف شد")

if __name__ == "__main__":
    main()
```
