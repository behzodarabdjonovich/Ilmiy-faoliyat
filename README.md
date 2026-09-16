# Rasmiy Xat Telegram Bot

O‘zbekiston tashkilotlari uchun AI yordamida rasmiy xat yaratish, tahrirlash va DOCX/PDF chiqarishga mo‘ljallangan aiogram 3.x loyihasi.

## Imkoniyatlar
- FSM orqali xat ma'lumotlarini yig‘ish
- OpenAI Responses API orqali o‘zbekcha rasmiy matn
- PostgreSQL + SQLAlchemy async
- Xat versiyalarini saqlash
- DOCX va PDF generatsiyasi
- Admin statistikasi
- Tashkilot va raqamlash uchun DB modellari
- Docker Compose

## Ishga tushirish
1. Python 3.12+ o‘rnating.
2. `.env.example` ni `.env` ga nusxalang va `BOT_TOKEN`, `OPENAI_API_KEY`, `DATABASE_URL`, `ADMIN_IDS` ni kiriting.
3. Lokal: `python -m venv .venv`, virtual muhitni faollashtiring, `pip install -r requirements.txt`.
4. PostgreSQL ishlayotganiga ishonch hosil qiling.
5. Tayyor migrationni qo‘llang: `alembic upgrade head`.
6. Botni ishga tushiring: `python -m app.main`.

## Docker
`.env` yarating, keyin:
```bash
docker compose up -d --build
docker compose exec bot alembic upgrade head
docker compose restart bot
```

## BotFather
Telegram ichida rasmiy BotFather orqali yangi bot yarating va tokenni `.env` dagi `BOT_TOKEN` ga yozing. Tokenni Git'ga yubormang.

## OpenAI
OpenAI API kalitini `.env` dagi `OPENAI_API_KEY` ga yozing. Model `OPENAI_MODEL` bilan boshqariladi. Default qiymat xarajatni nazorat qilish uchun `gpt-5.6-luna`.

## Production
- `.env` va tokenlarni secret managerda saqlang.
- PostgreSQL uchun backup va TLS qo‘llang.
- Botni reverse proxy talab qilmaydigan polling bilan yoki alohida webhook deployment bilan ishlating.
- Loglarda xat matni va API kalitlarini yozmang.
- Fayl storage'ni object storage'ga ko‘chirish mumkin.

## Eslatma
Repo asosiy ishlaydigan MVP va kengaytiriladigan arxitekturani beradi. Tashkilot profilini Telegram orqali to‘liq CRUD qilish, pagination UI, audit-log yozuvlari va yuklab olish statistikasi modelda ko‘zda tutilgan bo‘lsa-da, ularni deployment talablariga mos ravishda kengaytirish mumkin.


## Auditdan keyingi xavfsizlik tuzatishlari
- DOCX/PDF/revise callbacklari xat egasini tekshiradi (IDOR himoyasi).
- DB middleware xatoda rollback qiladi.
- PostgreSQL advisory lock bilan raqamlash race-conditiondan himoyalangan.
- PDF uchun Docker ichida DejaVu Unicode font o‘rnatiladi.
- Boshlang‘ich Alembic migration repoga qo‘shilgan.
- Input validator utility va real validator testlari qo‘shilgan.

## Hali MVP doirasida qolgan funksiyalar
Telegram orqali tashkilot CRUD/logotip yuklash, to‘liq pagination UI, audit-log yozish, download statistikasi va rate-limiter hali to‘liq implementatsiya qilinmagan. Ular original kengaytirilgan texnik topshiriqning keyingi bosqichi hisoblanadi.
