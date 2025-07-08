from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot token
# ADMINS ni ro'yxat sifatida o'qish va agar bitta str bo'lsa, uni listga aylantirish
ADMINS = env.list("ADMINS", subcast=int) if isinstance(env.list("ADMINS"), list) else [int(env.str("ADMINS"))]
IP = env.str("ip")  # Xosting ip manzili


# data/config.py
PAYMENT_AMOUNT = 14.09
PAYMENT_CARD = "9860 1234 5678 9012"
PAYMENT_OWNER = "FATTOYEV ABDUFATTOH"