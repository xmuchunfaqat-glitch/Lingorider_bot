# 🎓 Lingorider_bot

O'zbek yoshlari uchun til o'rganish va talaffuz mashqlari bo'yicha Telegram bot.
Bot to'liq o'zbek tilida ishlaydi, AI maslahat beradi, kunlik talaffuz mashqlari
o'tkazadi va foydalanuvchi yuborgan ovozli xabarni tekshirib, to'g'ri yoki
noto'g'ri ekanini aytadi.

**Narx:** Botning barcha asosiy qismlari **bepul** ishlaydi:
- 🗣 Talaffuz namunasi (TTS) — `gTTS` (Google Translate ovoz sintezi), API kalit kerak emas
- 👂 Nutqni matnga aylantirish (STT) — `faster-whisper`, lokal ishlaydi, API kalit kerak emas
- 🤖 AI maslahat — Google **Gemini bepul tarifi** (kuniga limit bilan, lekin shaxsiy bot uchun yetarli)

Faqat **bitta** bepul API kalit kerak bo'ladi — Gemini uchun.

> Barcha fayllar **bitta papkada, ichki papkalarsiz** — shuning uchun GitHub'ga
> to'g'ridan-to'g'ri "Add file → Upload files" orqali hammasini birga
> tashlashingiz mumkin.

---

## 1. Talab qilinadigan narsalar

- Python 3.10 yoki undan yuqori
- `ffmpeg` (ovozli xabarlarni o'qish uchun)
- Telegram bot tokeni
- Bepul Gemini API kaliti

```bash
# Ubuntu/Debian serverda ffmpeg o'rnatish:
sudo apt update && sudo apt install -y ffmpeg
```

## 2. Kalitlarni olish

1. **Bot tokeni**: Telegramda [@BotFather](https://t.me/BotFather) ga yozing →
   `/newbot` → nomini "Lingorider_bot" deb belgilang → tokenni nusxalang.
2. **Sizning Telegram ID raqamingiz (admin)**: [@userinfobot](https://t.me/userinfobot)
   ga `/start` yozing, u sizga ID raqamingizni yuboradi.
3. **Bepul Gemini API kaliti**: https://aistudio.google.com/apikey ga kiring,
   Google hisobingiz bilan kiring, "Create API key" tugmasini bosing.

## 3. O'rnatish

```bash
python3 -m venv venv
source venv/bin/activate          # Windowsda: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# .env faylini ochib, BOT_TOKEN va GEMINI_API_KEY ni to'ldiring
# (ADMIN_ID allaqachon to'ldirilgan)
```

> **Eslatma:** birinchi marta ishga tushganda `faster-whisper` tanlangan modelni
> (`WHISPER_MODEL_SIZE`, standart: `small`) avtomatik yuklab oladi — internet
> kerak, lekin keyinroq internetsiz (lokal) ishlay oladi.

## 4. Ishga tushirish

```bash
python3 bot.py
```

Konsolda "Lingorider_bot ishga tushdi" degan xabarni ko'rsangiz — tayyor!
Botni doimiy ishlatish uchun serverda `systemd`, `tmux`/`screen` yoki
`pm2`/`supervisor` orqali fon rejimida qoldirish tavsiya etiladi.

---

## 5. GitHub'ga yuklash

```bash
git init
git add .
git commit -m "Lingorider_bot - dastlabki versiya"
git branch -M main
git remote add origin https://github.com/SIZNING_USERNAME/lingorider_bot.git
git push -u origin main
```

`.gitignore` fayli `.env` ni (haqiqiy tokenlaringiz bo'lgan fayl) avtomatik
chiqarib tashlaydi — uni hech qachon repo'ga qo'shmang.

---

## 6. Railway'ga joylashtirish (ixtiyoriy)

> **Eslatma:** Railway 2026-yilda haqiqiy "bepul tarif"ni olib tashladi.
> Ro'yxatdan o'tganda bir martalik $5 bonus (30 kun) beradi, shundan keyin
> oyiga $1 lik juda kichik "Free plan"ga (0.5GB RAM) tushadi. Bot doimiy
> ishlashi va Whisper modelini xotirada saqlashi kerak bo'lgani uchun, bu
> chegaradan tezda chiqib ketishi mumkin — amalda **Hobby plan ($5/oy)**
> kerak bo'lishi mumkin. Agar byudjet umuman yo'q bo'lsa, botni o'z
> kompyuteringizda (`tmux`/`screen` orqali) ishlatish 100% bepul yo'l.

Loyihada Railway uchun ikkita fayl tayyor: `Dockerfile` (botni va `ffmpeg`ni
to'g'ri, xotirani tejagan holda o'rnatadi) va `railway.toml` (ishga tushirish
buyrug'ini belgilaydi). Qadamlar:

1. GitHub repo'ngizni Railway'da **"Deploy from GitHub repo"** orqali ulang.
   `Dockerfile` borligi sababli Railway avtomatik shu orqali quradi.
2. Loyiha **Settings → Variables** bo'limida quyidagilarni qo'shing:
   ```
   BOT_TOKEN=...
   ADMIN_ID=5816903954
   GEMINI_API_KEY=...
   WHISPER_MODEL_SIZE=base
   TIMEZONE=Asia/Tashkent
   ```
   (`WHISPER_MODEL_SIZE=base` — Railway'ning kichik RAM limitiga moslab,
   `small` o'rniga tavsiya etiladi.)
3. **Settings → Volumes → "+ New Volume"** orqali volume qo'shing, mount
   path sifatida aniq **`/app/data`** ni kiriting. *(Bu yagona qadam —
   afsuski, volume yaratish Railway tomonidan faqat dashboard/CLI orqali
   qilinadi, kodga yozib avtomatlashtirib bo'lmaydi.)* Bot kodi allaqachon
   barcha doimiy ma'lumotlarni (`data/` papkasiga — SQLite baza va audio
   keshi) aynan shu yo'lga moslab yozadi, shuning uchun boshqa hech narsa
   o'zgartirish kerak emas — volume avtomatik ishlaydi.
4. Deploy qiling.

> **Eslatma (build xatosi bo'lsa):** `ffmpeg`ni oddiy `apt-get install`
> orqali o'rnatish o'nlab keraksiz qo'shimcha paketni (alsa, dbus,
> fontconfig va h.k.) ham tortib keladi va kichik build konteynerlarida
> xotira tugashiga (`exit code: 137`) sabab bo'lishi mumkin. Shu sababli
> `Dockerfile` ichida `--no-install-recommends` flagi ishlatilgan — bu
> faqat zarur narsalarnigina o'rnatadi va muammoni hal qiladi.

---

## 7. Bot qanday ishlaydi

### Tanishuv (onboarding)
`/start` bosilganda bot ismi, yoshi, viloyati, tumani, til o'rganish maqsadi,
o'rganmoqchi bo'lgan til, kunlik mashg'uloti va e'tibor qaratmoqchi bo'lgan
sohasini so'raydi. Profil tugagach, **adminga darrov hisobot** yuboriladi.

### Talaffuz mashqi (ovozli)
"🎯 Talaffuz mashqi" tugmasi → bot tanlangan tilda jumla aytib beradi (ovozli) →
foydalanuvchi xuddi shunday talaffuz qilib (yoki erkin gapirib) ovozli xabar
yuboradi → Whisper orqali matnga aylantiriladi → maqsadli matn bilan
solishtirilib, foiz ko'rinishida natija va izoh beriladi. Mashq davomida
foydalanuvchi **⏸ Pauza** (keyinroq xuddi shu jumladan davom etadi) yoki
**⛔️ To'xtatish** tugmalaridan foydalanishi mumkin. Mashq tugagach, **adminga
hisobot** avtomatik yuboriladi.

### Grammatika va Lug'at boyligi (yozma)
Bu ikkisi ovozsiz, faqat o'qish uchun:
- **"📚 Grammatika"** — foydalanuvchi o'rganayotgan tilning asosiy grammatik
  mavzulari (zamonlar, kelishiklar, qo'shimchalar va h.k.) o'zbek tilida
  tushuntiriladi (`grammar.json`).
- **"🧠 Lug'at boyligi"** — so'zlar mavzular bo'yicha (Salomlashish, Oila,
  Ovqat-ichimlik) o'z tilida yozilgan holda, lotin harflarida qanday
  aytilishi va o'zbekcha ma'nosi bilan beriladi (`vocabulary.json`).

### AI maslahat
"🤖 AI maslahat" tugmasi foydalanuvchi profiliga (maqsad, kunlik tartib,
e'tibor sohasi) mos shaxsiy maslahat beradi (Gemini orqali, o'zbek tilida).

### Davriy hisobotlar
Har **30 daqiqada** (Toshkent vaqti bo'yicha), agar shu vaqt ichida faollik
bo'lsa (yangi foydalanuvchi yoki bajarilgan mashq), adminga umumiy statistika
yuboriladi. Faollik bo'lmasa — hisobot yuborilmaydi.

### Admin panel
Faqat `.env` faylidagi `ADMIN_ID` ga mos foydalanuvchi quyidagi buyruqlardan
foydalanishi mumkin:
- `/admin` — admin menyusi
- `/stats` — umumiy va so'nggi 30 daqiqalik statistika

---

## 8. Fayllar tuzilishi (barchasi bitta papkada)

| Fayl | Vazifasi |
|---|---|
| `bot.py` | Botni ishga tushiruvchi asosiy fayl |
| `config.py` | Sozlamalar, tillar, viloyatlar ro'yxati |
| `database.py` | Ma'lumotlar bazasi (User, ExerciseLog jadvallari + so'rovlar) |
| `texts.py` | Barcha o'zbek tilidagi matnlar |
| `keyboards.py` | Tugmalar (reply/inline) |
| `states.py` | FSM holatlari (onboarding, mashq, sozlamalar) |
| `handlers_start.py` | `/start` va tanishuv oqimi |
| `handlers_exercises.py` | Talaffuz mashqi oqimi (pauza/to'xtatish bilan) |
| `handlers_learn.py` | Grammatika va Lug'at boyligi (yozma bo'limlar) |
| `handlers_menu.py` | AI maslahat, natijalar, sozlamalar |
| `handlers_admin.py` | Admin buyruqlari (`/admin`, `/stats`) |
| `tts_service.py` | gTTS — talaffuz namunasi audiosi |
| `stt_service.py` | faster-whisper — nutqni matnga aylantirish |
| `pronunciation_checker.py` | Talaffuzni solishtirish va baholash |
| `gemini_service.py` | AI maslahat (Gemini, bepul tarif) |
| `report_service.py` | Adminga hisobotlar |
| `scheduler_service.py` | Har 30 daqiqalik fon vazifasi |
| `phrases.json` | Mashq uchun jumlalar bazasi (7 til) |
| `grammar.json` | Grammatika mavzulari (7 til, o'zbek tilida tushuntirilgan) |
| `vocabulary.json` | Lug'at — so'z, talaffuzi va o'zbekcha ma'nosi (7 til) |
| `requirements.txt` | Python kutubxonalari ro'yxati |
| `.env.example` | Muhit o'zgaruvchilari namunasi (token/kalitlar) |
| `.gitignore` | GitHub'ga yuklanmasligi kerak bo'lgan fayllar |
| `railway.toml` | Railway uchun ishga tushirish sozlamasi (ixtiyoriy) |
| `Dockerfile` | Railway/Docker uchun quruvchi fayl (ffmpeg'ni xavfsiz o'rnatadi) |
| `.dockerignore` | Docker build'ga kerak bo'lmagan fayllarni chiqarib tashlaydi |

`data/` papkasi (SQLite baza, audio kesh) bot birinchi marta ishga tushganda
avtomatik yaratiladi — uni qo'lda yaratish shart emas.

## 9. Kengaytirish bo'yicha tavsiyalar

- **Ko'proq jumlalar**: `phrases.json` ga istalgancha jumla qo'shing.
- **Ko'proq grammatika/lug'at**: `grammar.json` va `vocabulary.json` da hozir
  har bir til uchun boshlang'ich to'plam bor (4 grammatika mavzusi, 15 so'z).
  Xohlagancha mavzu/so'z qo'shishingiz mumkin — struktura JSON formatida,
  yangi til qo'shish ham mumkin (avval `config.py` dagi `LANGUAGES` ga
  qo'shing).
- **Ko'proq adminlar**: hozircha faqat 1 admin ishlaydi (talabga ko'ra).
  Ko'paytirish kerak bo'lsa, `config.py` dagi `ADMIN_ID` ni ro'yxatga aylantiring.
- **Whisper modeli**: `small` o'rtacha aniqlik/tezlik beradi. Kuchli server
  bo'lsa, `.env` dagi `WHISPER_MODEL_SIZE=medium` qilib aniqlikni oshiring.
- **Gemini modeli**: Google modellarni vaqti-vaqti bilan yangilab boradi.
  Xatolik chiqsa, https://ai.google.dev/gemini-api/docs/models dan joriy
  bepul model nomini tekshirib, `gemini_service.py` da almashtiring.
