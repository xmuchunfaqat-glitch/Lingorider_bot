# Railway (yoki boshqa Docker asosidagi xost) uchun.
# --no-install-recommends MUHIM: ffmpeg apt orqali o'rnatilganda yuzlab keraksiz
# paket (alsa, dbus, fontconfig, video-driver va h.k.) ham tortilib kelinadi va
# bu kichik build konteynerlarida xotira tugashiga (OOM, exit code 137) olib
# kelishi mumkin. --no-install-recommends faqat ffmpeg ishlashi uchun zarur
# bo'lgan kutubxonalarnigina o'rnatadi.

FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
