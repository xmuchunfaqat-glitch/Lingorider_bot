"""
Botning barcha matnlari shu yerda — o'zgartirish kerak bo'lsa faqat shu faylga kirasiz.
"""

WELCOME = (
    "Salom! 👋 Men <b>Lingorider</b> — sizning shaxsiy til o'rganish yordamchingizman.\n\n"
    "Men sizga to'g'ri talaffuzni o'rgataman, kunlik mashqlar beraman va "
    "qaysi tilni o'rganish kerakligi bo'yicha maslahat beraman.\n\n"
    "Avval siz bilan tanishib olaylik. Bu atigi 1 daqiqa vaqt oladi 🙂"
)

ASK_NAME = "Ismingiz nima? ✍️"
ASK_AGE = "Necha yoshdasiz? (faqat raqam bilan yozing)"
ASK_AGE_INVALID = "Iltimos, yoshingizni raqam bilan yozing. Masalan: 19"
ASK_REGION = "Qaysi viloyatdansiz? Quyidagidan tanlang 👇"
ASK_DISTRICT = "Qaysi tuman/shahardansiz? (masalan: Chilonzor tumani)"
ASK_GOAL = "Tilni nima maqsadda o'rganmoqchisiz?"
GOAL_OPTIONS = [
    "💼 Ishga joylashish",
    "✈️ Sayohat qilish",
    "🎓 O'qish (talabalik)",
    "🌍 Chet elga ko'chish",
    "🤝 Do'stlar topish / muloqot",
    "📈 Shaxsiy rivojlanish",
]
ASK_LANGUAGE = "Qaysi tilni o'rganmoqchisiz?"
ASK_LANGUAGE_UNSURE = "🤔 Bilmayman, maslahat bering"
ASK_DAILY_ROUTINE = (
    "Kuningiz qanday o'tadi? (masalan: talabaman, ishlayman, uyda o'qiyman) — "
    "bu sizga mos mashq jadvalini tuzishga yordam beradi."
)
ASK_FOCUS_AREA = "Nimaga ko'proq e'tibor qaratishni xohlaysiz?"
FOCUS_OPTIONS = [
    "🗣 Talaffuz (Pronunciation)",
    "📚 Grammatika",
    "🧠 Lug'at boyligi",
    "💬 Erkin gapirish",
]

ONBOARDING_DONE = (
    "Ajoyib, {name}! 🎉 Profilingiz tayyor.\n\n"
    "Endi <b>{language}</b> tilini birga o'rganamiz. Har kuni sizga mashqlar yuboraman, "
    "talaffuzingizni tekshiraman va kerak bo'lganda AI maslahat beraman.\n\n"
    "Quyidagi tugmalardan birini tanlang 👇"
)

MAIN_MENU_BUTTONS = [
    "🎯 Kunlik mashq",
    "🤖 AI maslahat",
    "📊 Mening natijalarim",
    "⚙️ Sozlamalar",
]

SETTINGS_MENU_BUTTONS = ["🌐 Tilni o'zgartirish", "🔁 Profilni qayta to'ldirish", "⬅️ Orqaga"]

EXERCISE_INTRO = "🎧 Diqqat bilan tinglang va xuddi shunday talaffuz qiling:"
EXERCISE_PROMPT_TEXT = "Matn: <b>{text}</b>\n\nEndi ovozli xabar yuborib, shu so'z/jumlani talaffuz qiling 🎤"
EXERCISE_NO_VOICE = "Iltimos, matn emas, <b>ovozli xabar</b> yuboring 🎤"
EXERCISE_ANALYZING = "🔎 Talaffuzingiz tekshirilmoqda, bir necha soniya kuting..."

EXERCISE_RESULT_GREAT = (
    "✅ Ajoyib! Talaffuzingiz juda yaxshi ({score}%).\n"
    "Eshitilgan: <i>{heard}</i>\n\nDavom etamizmi?"
)
EXERCISE_RESULT_OK = (
    "🟡 Yaxshi, lekin yana mashq qiling ({score}%).\n"
    "Kerakli: <i>{target}</i>\nEshitilgan: <i>{heard}</i>\n\n"
    "Yana urinib ko'rasizmi yoki davom etamizmi?"
)
EXERCISE_RESULT_BAD = (
    "🔴 Talaffuzni yaxshilash kerak ({score}%).\n"
    "Kerakli: <i>{target}</i>\nEshitilgan: <i>{heard}</i>\n\n"
    "Yana bir bor urinib ko'ring — eshitgan ovozli xabarni qayta tinglang."
)
EXERCISE_RETRY_BUTTON = "🔁 Qayta urinish"
EXERCISE_NEXT_BUTTON = "➡️ Keyingisi"
EXERCISE_STOP_BUTTON = "⛔️ Mashqni tugatish"
EXERCISE_FINISHED = "Bugungi mashq yakunlandi! 👏 Natijangiz hisobotga yozildi."

AI_ADVICE_THINKING = "🤖 Sizga mos maslahat tayyorlanmoqda..."
AI_ADVICE_ERROR = "Hozircha AI maslahat xizmati band, birozdan keyin qayta urinib ko'ring."

PROFILE_STATS_TEMPLATE = (
    "📊 <b>Sizning natijalaringiz</b>\n\n"
    "Til: {language}\n"
    "Bajarilgan mashqlar: {total}\n"
    "O'rtacha to'g'rilik: {avg_score}%\n"
    "Oxirgi mashg'ulot: {last_date}"
)

NOT_ADMIN = "Bu buyruq faqat admin uchun mavjud."
ADMIN_MENU = "👨‍💻 Admin panel\n\nQuyidagi buyruqlardan foydalaning:\n/stats — umumiy statistika\n/users — foydalanuvchilar ro'yxati"

LANGUAGE_CHANGED = "Til muvaffaqiyatli o'zgartirildi: {language} ✅"
RESTART_PROFILE = "Profilni qaytadan to'ldiramiz. /start tugmasini bosing."
