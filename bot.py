import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

BOT_TOKEN = "8008901751:AAGoUKOr-bFgN8sNuEWVuxqUdRJdKFEyask"
ADMIN_ID = 123456789

bolimlar = {
    "oziq":      "🥦 Oziq-ovqat mahsulotlari",
    "quruq":     "🌾 Quruq mahsulotlar",
    "shirinlik": "🍫 Shirinlik va gazaklar",
    "ichimlik":  "🥤 Ichimliklar",
    "maishiy":   "🧴 Maishiy kimyo va gigiyena",
    "tayyor":    "🍱 Tayyor va yarim tayyor",
    "nooziq":    "📦 Nooziq-ovqat mahsulotlari",
}

kategoriyalar = {
    "sabzavot_meva":   {"nomi": "🥬 Sabzavot va mevalar",        "bolim": "oziq"},
    "gosht":           {"nomi": "🥩 Go'sht, tovuq, baliq",       "bolim": "oziq"},
    "sut":             {"nomi": "🥛 Sut mahsulotlari",           "bolim": "oziq"},
    "non":             {"nomi": "🍞 Non va pishiriqlar",          "bolim": "oziq"},
    "tuxum":           {"nomi": "🥚 Tuxum",                      "bolim": "oziq"},
    "un_guruch":       {"nomi": "🌾 Un, guruch, makaron",         "bolim": "quruq"},
    "shakar_tuz":      {"nomi": "🧂 Shakar, tuz, yog'",          "bolim": "quruq"},
    "dukkakli":        {"nomi": "🫘 Dukkaklilar",                "bolim": "quruq"},
    "konserva":        {"nomi": "🥫 Konserva mahsulotlari",       "bolim": "quruq"},
    "shokolad_konfet": {"nomi": "🍫 Shokolad va konfet",          "bolim": "shirinlik"},
    "pechenye_tort":   {"nomi": "🍪 Pechenye va tortlar",         "bolim": "shirinlik"},
    "chips":           {"nomi": "🍟 Chips va krakerlar",          "bolim": "shirinlik"},
    "muzqaymoq":       {"nomi": "🍦 Muzqaymoq",                  "bolim": "shirinlik"},
    "suv":             {"nomi": "💧 Suv",                        "bolim": "ichimlik"},
    "sharbat":         {"nomi": "🧃 Sharbatlar",                 "bolim": "ichimlik"},
    "gazli":           {"nomi": "🥤 Gazlangan ichimliklar",       "bolim": "ichimlik"},
    "energetik":       {"nomi": "⚡ Energetik ichimliklar",       "bolim": "ichimlik"},
    "choy_qahva":      {"nomi": "☕ Choy va qahva",              "bolim": "ichimlik"},
    "kir_yuvish":      {"nomi": "🧺 Kir yuvish vositalari",      "bolim": "maishiy"},
    "gigiyena":        {"nomi": "🪥 Gigiyena vositalari",         "bolim": "maishiy"},
    "tozalash":        {"nomi": "🧹 Uy tozalash vositalari",      "bolim": "maishiy"},
    "kolbasa_sosiska": {"nomi": "🌭 Kolbasa va sosiska",          "bolim": "tayyor"},
    "muzlatilgan":     {"nomi": "❄️ Muzlatilgan mahsulotlar",     "bolim": "tayyor"},
    "tayyor_ovqat":    {"nomi": "🍽 Tayyor ovqatlar",             "bolim": "tayyor"},
    "yarim_tayyor":    {"nomi": "🥘 Yarim tayyor mahsulotlar",    "bolim": "tayyor"},
    "kantselyariya":   {"nomi": "✏️ Kantselyariya",              "bolim": "nooziq"},
    "oyinchoq":        {"nomi": "🧸 O'yinchoqlar",               "bolim": "nooziq"},
    "idish":           {"nomi": "🍽 Idish-tovoq",                "bolim": "nooziq"},
    "texnika":         {"nomi": "🔋 Batareyalar va texnika",      "bolim": "nooziq"},
}

products = {

    "pomidor":        {"nomi": "🍅 Pomidor",         "narxi": 12000, "tavsif": "Toza pomidor (1kg)",           "kat": "sabzavot_meva"},
    "bodring":        {"nomi": "🥒 Bodring",         "narxi": 10000, "tavsif": "Toza bodring (1kg)",           "kat": "sabzavot_meva"},
    "kartoshka":      {"nomi": "🥔 Kartoshka",       "narxi": 10000, "tavsif": "Yangi kartoshka (1kg)",        "kat": "sabzavot_meva"},
    "sabzi":          {"nomi": "🥕 Sabzi",           "narxi": 8000,  "tavsif": "Toza sabzi (1kg)",             "kat": "sabzavot_meva"},
    "piyoz":          {"nomi": "🧅 Piyoz",           "narxi": 7000,  "tavsif": "Sariq piyoz (1kg)",            "kat": "sabzavot_meva"},
    "karam":          {"nomi": "🥬 Karam",           "narxi": 9000,  "tavsif": "Oq karam (1kg)",               "kat": "sabzavot_meva"},
    "olma":           {"nomi": "🍎 Olma",            "narxi": 15000, "tavsif": "Toza olma (1kg)",              "kat": "sabzavot_meva"},
    "banan":          {"nomi": "🍌 Banan",           "narxi": 20000, "tavsif": "Banan (1kg)",                  "kat": "sabzavot_meva"},
    "uzum":           {"nomi": "🍇 Uzum",            "narxi": 25000, "tavsif": "Toza uzum (1kg)",              "kat": "sabzavot_meva"},
    "limon":          {"nomi": "🍋 Limon",           "narxi": 18000, "tavsif": "Toza limon (1kg)",             "kat": "sabzavot_meva"},
    "tarvuz":         {"nomi": "🍉 Tarvuz",          "narxi": 18000, "tavsif": "Shirin tarvuz (1kg)",          "kat": "sabzavot_meva"},
    # Go'sht
    "tovuq":          {"nomi": "🍗 Tovuq",           "narxi": 55000, "tavsif": "Butun tovuq (1kg)",            "kat": "gosht"},
    "tovuq_filye":    {"nomi": "🍗 Tovuq filye",     "narxi": 65000, "tavsif": "Tovuq ko'kragi (1kg)",         "kat": "gosht"},
    "mol_gosht":      {"nomi": "🥩 Mol go'shti",     "narxi": 90000, "tavsif": "Toza mol go'shti (1kg)",       "kat": "gosht"},
    "qoy_gosht":      {"nomi": "🍖 Qo'y go'shti",   "narxi":100000, "tavsif": "Toza qo'y go'shti (1kg)",      "kat": "gosht"},
    "baliq":          {"nomi": "🐟 Baliq",           "narxi": 60000, "tavsif": "Toza baliq (1kg)",             "kat": "gosht"},
    "krevetka":       {"nomi": "🦐 Krevetka",        "narxi": 85000, "tavsif": "Muzlatilgan krevetka (500g)",  "kat": "gosht"},
    # Sut mahsulotlari
    "sut":            {"nomi": "🥛 Sut",             "narxi": 8000,  "tavsif": "Toza qishloq suti (1L)",       "kat": "sut"},
    "qatiq":          {"nomi": "🍶 Qatiq",           "narxi": 9000,  "tavsif": "Toza qatiq (1L)",              "kat": "sut"},
    "yogurt":         {"nomi": "🥛 Yogurt",          "narxi": 11000, "tavsif": "Tabiiy yogurt (400g)",         "kat": "sut"},
    "pishloq":        {"nomi": "🧀 Pishloq",         "narxi": 45000, "tavsif": "Rus pishlog'i (500g)",         "kat": "sut"},
    "smetana":        {"nomi": "🥄 Smetana",         "narxi": 12000, "tavsif": "Qaymoq smetana (400g)",        "kat": "sut"},
    "saryog":         {"nomi": "🧈 Sariyog'",        "narxi": 35000, "tavsif": "Toza sariyog' (200g)",         "kat": "sut"},
    # Non
    "non":            {"nomi": "🍞 Non",             "narxi": 3000,  "tavsif": "Yangi pishirilgan non",        "kat": "non"},
    "lavash":         {"nomi": "🫓 Lavash",          "narxi": 4000,  "tavsif": "Yumshoq lavash (5 dona)",      "kat": "non"},
    "bulochka":       {"nomi": "🥐 Bulochka",        "narxi": 5000,  "tavsif": "Yangi bulochka (4 dona)",      "kat": "non"},
    # Tuxum
    "tuxum":          {"nomi": "🥚 Tuxum",           "narxi": 15000, "tavsif": "Toza tuxum (10 dona)",         "kat": "tuxum"},
    "bedana":         {"nomi": "🥚 Bedana tuxumi",   "narxi": 12000, "tavsif": "Bedana tuxumi (20 dona)",      "kat": "tuxum"},
    # Un, guruch, makaron
    "guruch":         {"nomi": "🍚 Guruch",          "narxi": 25000, "tavsif": "Toshkent guruchi (1kg)",       "kat": "un_guruch"},
    "un":             {"nomi": "🌾 Un",              "narxi": 20000, "tavsif": "Bug'doy uni (2kg)",             "kat": "un_guruch"},
    "makaron":        {"nomi": "🍝 Makaron",         "narxi": 12000, "tavsif": "Italyan makaroni (500g)",      "kat": "un_guruch"},
    "grechixa":       {"nomi": "🌰 Grechixa",        "narxi": 18000, "tavsif": "Grechixa yarma (1kg)",         "kat": "un_guruch"},
    # Shakar, tuz, yog'
    "qand":           {"nomi": "🍬 Shakar",          "narxi": 18000, "tavsif": "Oq qand (1kg)",                "kat": "shakar_tuz"},
    "tuz":            {"nomi": "🧂 Tuz",             "narxi": 5000,  "tavsif": "Osh tuzi (1kg)",               "kat": "shakar_tuz"},
    "yog":            {"nomi": "🧈 O'simlik yog'i",  "narxi": 30000, "tavsif": "Tozalangan yog' (1L)",         "kat": "shakar_tuz"},
    "zaytun_yog":     {"nomi": "🫒 Zaytun yog'i",   "narxi": 65000, "tavsif": "Toza zaytun yog'i (500ml)",    "kat": "shakar_tuz"},
    # Dukkaklilar
    "loviya":         {"nomi": "🫘 Loviya",          "narxi": 15000, "tavsif": "Qizil loviya (1kg)",           "kat": "dukkakli"},
    "noxat":          {"nomi": "🫘 No'xat",          "narxi": 14000, "tavsif": "Sariq no'xat (1kg)",           "kat": "dukkakli"},
    "mosh":           {"nomi": "🟢 Mosh",            "narxi": 16000, "tavsif": "Toza mosh (1kg)",              "kat": "dukkakli"},
    # Konserva
    "tomat_pasta":    {"nomi": "🍅 Tomat pasta",     "narxi": 9000,  "tavsif": "Tomat pasta (200g)",           "kat": "konserva"},
    "kons_makkaj":    {"nomi": "🌽 Makkajo'xori",    "narxi": 11000, "tavsif": "Konserva makkajo'xori (400g)", "kat": "konserva"},
    "ketchup":        {"nomi": "🍅 Ketchup",         "narxi": 15000, "tavsif": "Pomidor ketchupi (500g)",      "kat": "konserva"},
    "mayyonez":       {"nomi": "🥣 Mayyonez",        "narxi": 14000, "tavsif": "Klassik mayyonez (400g)",      "kat": "konserva"},
    # Shokolad va konfet
    "shokolad":       {"nomi": "🍫 Shokolad",        "narxi": 20000, "tavsif": "Qora shokolad (100g)",         "kat": "shokolad_konfet"},
    "sut_shokolad":   {"nomi": "🍫 Sut shokoladi",   "narxi": 18000, "tavsif": "Sut shokoladi (100g)",         "kat": "shokolad_konfet"},
    "konfet":         {"nomi": "🍬 Konfet",          "narxi": 25000, "tavsif": "Aralash konfet (500g)",        "kat": "shokolad_konfet"},
    "asal":           {"nomi": "🍯 Asal",            "narxi": 50000, "tavsif": "Tabiiy asal (500g)",           "kat": "shokolad_konfet"},
    # Pechenye va tortlar
    "pechenye":       {"nomi": "🍪 Pechenye",        "narxi": 15000, "tavsif": "Yog'li pechenye (300g)",       "kat": "pechenye_tort"},
    "vafel":          {"nomi": "🧇 Vafel",           "narxi": 12000, "tavsif": "Shirinli vafel (200g)",        "kat": "pechenye_tort"},
    "murabbo":        {"nomi": "🍯 Murabbo",         "narxi": 22000, "tavsif": "Uy murrabbosi (500g)",         "kat": "pechenye_tort"},
    # Chips
    "chips":          {"nomi": "🍟 Chips",           "narxi": 12000, "tavsif": "Kartoshka chips (100g)",       "kat": "chips"},
    "kraker":         {"nomi": "🫙 Kraker",          "narxi": 10000, "tavsif": "Tuzli kraker (150g)",          "kat": "chips"},
    "popkorn":        {"nomi": "🍿 Popkorn",         "narxi": 8000,  "tavsif": "Shirin popkorn (100g)",        "kat": "chips"},
    # Muzqaymoq
    "eskimo":         {"nomi": "🍦 Eskimo",          "narxi": 8000,  "tavsif": "Shokoladli eskimo",            "kat": "muzqaymoq"},
    "plombir":        {"nomi": "🍨 Plombir",         "narxi": 10000, "tavsif": "Klassik plombir",              "kat": "muzqaymoq"},
    "muz_tort":       {"nomi": "🍰 Muz tort",        "narxi": 45000, "tavsif": "Muzli tort (500g)",            "kat": "muzqaymoq"},
    # Suv
    "suv_gazsiz":     {"nomi": "💧 Suv (gazsiz)",    "narxi": 6000,  "tavsif": "Toza ichimlik suvi (1.5L)",    "kat": "suv"},
    "suv_gazli":      {"nomi": "💦 Suv (gazlangan)", "narxi": 7000,  "tavsif": "Gazlangan suv (1.5L)",         "kat": "suv"},
    # Sharbat
    "sharbat_olma":   {"nomi": "🍎 Olma sharbati",   "narxi": 12000, "tavsif": "Tabiiy olma sharbati (1L)",   "kat": "sharbat"},
    "sharbat_uzum":   {"nomi": "🍇 Uzum sharbati",   "narxi": 13000, "tavsif": "Uzum sharbati (1L)",          "kat": "sharbat"},
    "sharbat_aral":   {"nomi": "🧃 Aralash sharbat", "narxi": 11000, "tavsif": "Aralash meva sharbati (1L)",  "kat": "sharbat"},
    # Gazlangan
    "kola":           {"nomi": "🥤 Kola",            "narxi": 9000,  "tavsif": "Kola ichimlik (0.5L)",         "kat": "gazli"},
    "limonad":        {"nomi": "🍋 Limonad",         "narxi": 8000,  "tavsif": "Limonad (0.5L)",               "kat": "gazli"},
    "sprite":         {"nomi": "🥤 Sprite",          "narxi": 9000,  "tavsif": "Sprite (0.5L)",                "kat": "gazli"},
    # Energetik
    "energetik":      {"nomi": "⚡ Energetik",       "narxi": 15000, "tavsif": "Energetik ichimlik (0.25L)",   "kat": "energetik"},
    # Choy va qahva
    "choy_yashil":    {"nomi": "🍵 Yashil choy",     "narxi": 25000, "tavsif": "Yashil choy (100g)",           "kat": "choy_qahva"},
    "choy_qora":      {"nomi": "🍵 Qora choy",       "narxi": 22000, "tavsif": "Qora choy (100g)",             "kat": "choy_qahva"},
    "kofe_eritma":    {"nomi": "☕ Eritma kofe",      "narxi": 45000, "tavsif": "Eritma kofe (100g)",           "kat": "choy_qahva"},
    "kofe_don":       {"nomi": "☕ Don kofe",         "narxi": 80000, "tavsif": "Don kofe (250g)",              "kat": "choy_qahva"},
    # Kir yuvish
    "kir_kukun":      {"nomi": "🧺 Kir kukuni",      "narxi": 35000, "tavsif": "Kir yuvish kukuni (3kg)",      "kat": "kir_yuvish"},
    "kir_gel":        {"nomi": "🫧 Kir geli",        "narxi": 40000, "tavsif": "Kir yuvish geli (1L)",         "kat": "kir_yuvish"},
    "yumshatgich":    {"nomi": "🌸 Yumshatgich",     "narxi": 25000, "tavsif": "Kiyim yumshatgich (1L)",       "kat": "kir_yuvish"},
    # Gigiyena
    "sovun":          {"nomi": "🧼 Sovun",           "narxi": 8000,  "tavsif": "Tuvalet sovuni (4 dona)",      "kat": "gigiyena"},
    "shampun":        {"nomi": "🧴 Shampun",         "narxi": 25000, "tavsif": "Soch uchun shampun (400ml)",   "kat": "gigiyena"},
    "tish_pastasi":   {"nomi": "🦷 Tish pastasi",    "narxi": 15000, "tavsif": "Tish pastasi (150ml)",         "kat": "gigiyena"},
    "dezodorant":     {"nomi": "🌺 Dezodorant",      "narxi": 20000, "tavsif": "Dezodorant (150ml)",           "kat": "gigiyena"},
    # Tozalash
    "supurgi":        {"nomi": "🧹 Supurgi",         "narxi": 25000, "tavsif": "Uy supurgisi",                 "kat": "tozalash"},
    "idish_yuvish":   {"nomi": "🫧 Idish yuvish",    "narxi": 12000, "tavsif": "Idish yuvish vositasi (500ml)","kat": "tozalash"},
    "hojatxona_gel":  {"nomi": "🚽 Hojatxona geli",  "narxi": 15000, "tavsif": "Hojatxona tozalash geli",     "kat": "tozalash"},
    # Kolbasa va sosiska
    "kolbasa":        {"nomi": "🌭 Kolbasa",         "narxi": 50000, "tavsif": "Pishirilgan kolbasa (500g)",   "kat": "kolbasa_sosiska"},
    "sosiska":        {"nomi": "🌭 Sosiska",         "narxi": 35000, "tavsif": "Tovuq sosiskasi (500g)",       "kat": "kolbasa_sosiska"},
    "vetchina":       {"nomi": "🥓 Vetchina",        "narxi": 55000, "tavsif": "Vetchina (300g)",              "kat": "kolbasa_sosiska"},
    # Muzlatilgan
    "muz_tovuq":      {"nomi": "❄️ Muzlatilgan tovuq","narxi":50000, "tavsif": "Muzlatilgan tovuq (1kg)",      "kat": "muzlatilgan"},
    "muz_baliq":      {"nomi": "❄️ Muzlatilgan baliq","narxi":55000, "tavsif": "Muzlatilgan baliq (1kg)",      "kat": "muzlatilgan"},
    "muz_sabzavot":   {"nomi": "❄️ Aralash sabzavot","narxi": 20000, "tavsif": "Muzlatilgan sabzavot (1kg)",   "kat": "muzlatilgan"},
    # Tayyor ovqatlar
    "plov":           {"nomi": "🍚 Plov",            "narxi": 35000, "tavsif": "Tayyor plov (500g)",           "kat": "tayyor_ovqat"},
    "lagmon":         {"nomi": "🍜 Lag'mon",         "narxi": 30000, "tavsif": "Tayyor lag'mon (500g)",        "kat": "tayyor_ovqat"},
    "salat":          {"nomi": "🥗 Salat",           "narxi": 25000, "tavsif": "Aralash salat (300g)",         "kat": "tayyor_ovqat"},
    # Yarim tayyor
    "kotlet":         {"nomi": "🥩 Kotlet",          "narxi": 40000, "tavsif": "Yarim tayyor kotlet (500g)",   "kat": "yarim_tayyor"},
    "samsa":          {"nomi": "🫓 Samsa",           "narxi": 25000, "tavsif": "Yarim tayyor samsa (6 dona)",  "kat": "yarim_tayyor"},
    "manti":          {"nomi": "🥟 Manti",           "narxi": 30000, "tavsif": "Yarim tayyor manti (20 dona)", "kat": "yarim_tayyor"},
    # Kantselyariya
    "daftar":         {"nomi": "📓 Daftar",          "narxi": 8000,  "tavsif": "96 varaq daftar",              "kat": "kantselyariya"},
    "ruchka":         {"nomi": "✒️ Ruchka",          "narxi": 3000,  "tavsif": "Ko'k ruchka (3 dona)",         "kat": "kantselyariya"},
    "qalam":          {"nomi": "✏️ Qalam",           "narxi": 4000,  "tavsif": "Oddiy qalam (5 dona)",         "kat": "kantselyariya"},
    # O'yinchoqlar
    "ayiqcha":        {"nomi": "🧸 Ayiqcha",         "narxi": 45000, "tavsif": "Yumshoq o'yinchoq ayiqcha",   "kat": "oyinchoq"},
    "kubik":          {"nomi": "🧊 Kubiklar",        "narxi": 25000, "tavsif": "Rangli kubiklar to'plami",     "kat": "oyinchoq"},
    # Idish-tovoq
    "piyola":         {"nomi": "🍵 Piyola",          "narxi": 15000, "tavsif": "Chinni piyola (6 dona)",       "kat": "idish"},
    "tarelka":        {"nomi": "🍽 Tarelka",         "narxi": 20000, "tavsif": "Chuqur tarelka (6 dona)",      "kat": "idish"},
    "kazan":          {"nomi": "🥘 Kazan",           "narxi":150000, "tavsif": "Alyuminiy kazan (5L)",         "kat": "idish"},
    # Texnika
    "batareya":       {"nomi": "🔋 Batareya",        "narxi": 10000, "tavsif": "AA batareya (4 dona)",         "kat": "texnika"},
    "lampochka":      {"nomi": "💡 Lampochka",       "narxi": 15000, "tavsif": "LED lampochka (9W)",           "kat": "texnika"},
    "rozetka":        {"nomi": "🔌 Rozetka",         "narxi": 20000, "tavsif": "Ikki teshikli rozetka",        "kat": "texnika"},
}

promo_kodlar = {"MARKET10": 10, "YANGI20": 20, "SALOM15": 15}

savat = {}
buyurtmalar = {}
buyurtma_raqam = [1]
kunlik_buyurtmalar = []

class BuyurtmaHolat(StatesGroup):
    ism = State()
    telefon = State()
    lokatsiya = State()  
    manzil = State()     
    promo = State()
    tolov = State()

class AdminHolat(StatesGroup):
    xabar = State()
    yangi_nomi = State()
    yangi_narxi = State()
    yangi_tavsif = State()
    yangi_kat = State()
    buyurtma_raqam = State()
    buyurtma_holat = State()
    kuryer_raqam = State()  

class QidiruvHolat(StatesGroup):
    qidiruv = State()

kuryerlar = {}

kuryer_buyurtma = {}

def asosiy_menu():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🛍 Mahsulotlar"), KeyboardButton(text="🔍 Qidirish")],
        [KeyboardButton(text="🛒 Savatcha"),    KeyboardButton(text="🎁 Promo kod")],
        [KeyboardButton(text="📦 Buyurtmalarim"), KeyboardButton(text="🚴 Kuryer holati")],
        [KeyboardButton(text="📞 Aloqa")],
    ], resize_keyboard=True)

def admin_menu():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📊 Statistika"),       KeyboardButton(text="📈 Kunlik hisobot")],
        [KeyboardButton(text="📦 Buyurtmalar"),      KeyboardButton(text="✅ Holat yangilash")],
        [KeyboardButton(text="🚴 Kuryer boshqaruv"), KeyboardButton(text="➕ Mahsulot qo'shish")],
        [KeyboardButton(text="📢 Xabar yuborish"),   KeyboardButton(text="🔙 Asosiy menu")]
    ], resize_keyboard=True)

def lokatsiya_kb():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📍 Lokatsiyani yuborish", request_location=True)],
    ], resize_keyboard=True)

def bolimlar_kb():
    items = list(bolimlar.items())
    tugmalar = []
    for i in range(0, len(items), 2):
        qator = [InlineKeyboardButton(text=bnom, callback_data=f"bolim_{bid}")
                 for bid, bnom in items[i:i+2]]
        tugmalar.append(qator)
    return InlineKeyboardMarkup(inline_keyboard=tugmalar)

def kategoriyalar_kb(bid):
    items = [(kid, k) for kid, k in kategoriyalar.items() if k['bolim'] == bid]
    tugmalar = []
    for i in range(0, len(items), 2):
        qator = [InlineKeyboardButton(text=k['nomi'], callback_data=f"kat_{kid}")
                 for kid, k in items[i:i+2]]
        tugmalar.append(qator)
    tugmalar.append([InlineKeyboardButton(text="🔙 Bo'limlar", callback_data="bolimlar")])
    return InlineKeyboardMarkup(inline_keyboard=tugmalar)

def mahsulotlar_kb(kid):
    tugmalar = [[InlineKeyboardButton(
        text=f"{p['nomi']} — {p['narxi']:,} so'm",
        callback_data=f"mahsulot_{pid}"
    )] for pid, p in products.items() if p.get('kat') == kid]
    bid = kategoriyalar[kid]['bolim']
    tugmalar.append([InlineKeyboardButton(text="🔙 Kategoriyalar", callback_data=f"bolim_{bid}")])
    return InlineKeyboardMarkup(inline_keyboard=tugmalar)

def mahsulot_kb(pid):
    kid = products[pid]['kat']
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="➖", callback_data=f"kam_{pid}"),
            InlineKeyboardButton(text="🛒 Savatga", callback_data=f"qosh_{pid}"),
            InlineKeyboardButton(text="➕", callback_data=f"kop_{pid}"),
        ],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"kat_{kid}")]
    ])

def tolov_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Payme", callback_data="tolov_payme")],
        [InlineKeyboardButton(text="💳 Click", callback_data="tolov_click")],
    ])

def promo_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➡️ Promosiz davom etish", callback_data="promo_skip")]
    ])

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(Command("start"))
async def start(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("👋 Admin paneli:", reply_markup=admin_menu())
    else:
        await message.answer(
            f"🌟 Assalomu alaykum, {message.from_user.first_name}!\n\n"
            f"🏪 <b>MARKET botiga xush kelibsiz!</b>\n\n"
            f"🛒 Qulay buyurtma | 🚚 Tez yetkazib berish | 🎁 Promo kodlar",
            parse_mode="HTML", reply_markup=asosiy_menu()
        )

@dp.message(F.text == "🛍 Mahsulotlar")
async def mahsulotlar(message: types.Message):
    await message.answer("🏪 <b>Bo'limni tanlang:</b>",
                         parse_mode="HTML", reply_markup=bolimlar_kb())

@dp.callback_query(F.data == "bolimlar")
async def bolimlar_cb(callback: types.CallbackQuery):
    await callback.message.edit_text("🏪 <b>Bo'limni tanlang:</b>",
                                     parse_mode="HTML", reply_markup=bolimlar_kb())

@dp.callback_query(F.data.startswith("bolim_"))
async def bolim_tanlash(callback: types.CallbackQuery):
    bid = callback.data[6:]
    bnom = bolimlar.get(bid, "")
    soni = sum(1 for k in kategoriyalar.values() if k['bolim'] == bid)
    await callback.message.edit_text(
        f"{bnom}\n\n📂 {soni} ta kategoriya:",
        parse_mode="HTML", reply_markup=kategoriyalar_kb(bid)
    )

@dp.callback_query(F.data.startswith("kat_"))
async def kategoriya_tanlash(callback: types.CallbackQuery):
    kid = callback.data[4:]
    k = kategoriyalar.get(kid)
    if not k: return
    soni = sum(1 for p in products.values() if p.get('kat') == kid)
    await callback.message.edit_text(
        f"{k['nomi']}\n\n🛍 {soni} ta mahsulot:",
        parse_mode="HTML", reply_markup=mahsulotlar_kb(kid)
    )

@dp.callback_query(F.data.startswith("mahsulot_"))
async def mahsulot_detail(callback: types.CallbackQuery):
    pid = callback.data[9:]
    p = products.get(pid)
    if not p: return
    uid = callback.from_user.id
    miqdor = savat.get(uid, {}).get(pid, 1)
    await callback.message.edit_text(
        f"{p['nomi']}\n\n📝 {p['tavsif']}\n"
        f"💰 Narxi: <b>{p['narxi']:,} so'm</b>\n\n"
        f"Miqdor: <b>{miqdor} dona</b>\n"
        f"Jami: <b>{p['narxi'] * miqdor:,} so'm</b>",
        parse_mode="HTML", reply_markup=mahsulot_kb(pid)
    )

@dp.callback_query(F.data.startswith("kop_"))
async def miqdor_kop(callback: types.CallbackQuery):
    pid = callback.data[4:]
    uid = callback.from_user.id
    if uid not in savat: savat[uid] = {}
    savat[uid][pid] = savat[uid].get(pid, 1) + 1
    await mahsulot_detail(callback)

@dp.callback_query(F.data.startswith("kam_"))
async def miqdor_kam(callback: types.CallbackQuery):
    pid = callback.data[4:]
    uid = callback.from_user.id
    if uid not in savat: savat[uid] = {}
    if savat[uid].get(pid, 1) > 1:
        savat[uid][pid] = savat[uid].get(pid, 1) - 1
    await mahsulot_detail(callback)

@dp.callback_query(F.data.startswith("qosh_"))
async def savatga_qosh(callback: types.CallbackQuery):
    pid = callback.data[5:]
    uid = callback.from_user.id
    p = products.get(pid)
    if uid not in savat: savat[uid] = {}
    savat[uid][pid] = savat[uid].get(pid, 1)
    await callback.answer(f"✅ {p['nomi']} savatga qo'shildi!", show_alert=True)

@dp.message(F.text == "🔍 Qidirish")
async def qidirish(message: types.Message, state: FSMContext):
    await state.set_state(QidiruvHolat.qidiruv)
    await message.answer("🔍 Mahsulot nomini yozing:")

@dp.message(QidiruvHolat.qidiruv)
async def qidirish_natija(message: types.Message, state: FSMContext):
    so_z = message.text.lower()
    natijalar = {pid: p for pid, p in products.items()
                 if so_z in p['nomi'].lower() or so_z in p['tavsif'].lower()}
    await state.clear()
    if not natijalar:
        await message.answer(f"❌ '<b>{message.text}</b>' topilmadi.", parse_mode="HTML")
        return
    tugmalar = [[InlineKeyboardButton(
        text=f"{p['nomi']} — {p['narxi']:,} so'm", callback_data=f"mahsulot_{pid}"
    )] for pid, p in natijalar.items()]
    await message.answer(f"🔍 <b>{len(natijalar)} ta natija:</b>",
                         parse_mode="HTML",
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=tugmalar))

@dp.message(F.text == "🛒 Savatcha")
async def savatcha(message: types.Message):
    uid = message.from_user.id
    if not savat.get(uid):
        await message.answer("🛒 Savatchingiz bo'sh!")
        return
    matn = "🛒 <b>Sizning savatchingiz:</b>\n\n"
    jami = 0
    tugmalar = []
    for pid, miqdor in savat[uid].items():
        if pid not in products: continue
        p = products[pid]
        narx = p['narxi'] * miqdor
        jami += narx
        matn += f"• {p['nomi']} x{miqdor} = <b>{narx:,} so'm</b>\n"
        tugmalar.append([InlineKeyboardButton(text=f"❌ {p['nomi']}", callback_data=f"ochir_{pid}")])
    matn += f"\n💰 <b>Jami: {jami:,} so'm</b>"
    tugmalar.append([InlineKeyboardButton(text="✅ Buyurtma berish", callback_data="buyurtma_ber")])
    tugmalar.append([InlineKeyboardButton(text="🗑 Tozalash", callback_data="savat_tozala")])
    await message.answer(matn, parse_mode="HTML",
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=tugmalar))

@dp.callback_query(F.data.startswith("ochir_"))
async def ochir(callback: types.CallbackQuery):
    pid = callback.data[6:]
    uid = callback.from_user.id
    if uid in savat and pid in savat[uid]:
        del savat[uid][pid]
    await callback.answer("❌ O'chirildi")
    await savatcha(callback.message)

@dp.callback_query(F.data == "savat_tozala")
async def savat_tozala(callback: types.CallbackQuery):
    savat[callback.from_user.id] = {}
    await callback.message.edit_text("🛒 Savatchingiz bo'sh!")

@dp.callback_query(F.data == "buyurtma_ber")
async def buyurtma_boshlash(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(BuyurtmaHolat.ism)
    await callback.message.answer("📝 Ismingizni kiriting:")

@dp.message(BuyurtmaHolat.ism)
async def ism_qabul(message: types.Message, state: FSMContext):
    await state.update_data(ism=message.text)
    await state.set_state(BuyurtmaHolat.telefon)
    await message.answer("📞 Telefon raqamingizni yuboring:",
        reply_markup=ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text="📱 Raqamni yuborish", request_contact=True)]
        ], resize_keyboard=True))

@dp.message(BuyurtmaHolat.telefon, F.contact)
async def telefon_contact(message: types.Message, state: FSMContext):
    await state.update_data(telefon=message.contact.phone_number)
    await lokatsiya_so_ra(message, state)

@dp.message(BuyurtmaHolat.telefon)
async def telefon_matn(message: types.Message, state: FSMContext):
    await state.update_data(telefon=message.text)
    await lokatsiya_so_ra(message, state)

async def lokatsiya_so_ra(message, state):
    await state.set_state(BuyurtmaHolat.lokatsiya)
    await message.answer(
        "📍 <b>Lokatsiyangizni yuboring!</b>\n\n"
        "Bu kuryer sizni topishi uchun kerak.\n"
        "Pastdagi tugmani bosing 👇",
        parse_mode="HTML",
        reply_markup=lokatsiya_kb()
    )

@dp.message(BuyurtmaHolat.lokatsiya, F.location)
async def lokatsiya_qabul(message: types.Message, state: FSMContext):
    lat = message.location.latitude
    lon = message.location.longitude
    await state.update_data(lat=lat, lon=lon,
                            manzil=f"📍 {lat:.5f}, {lon:.5f}")
    await state.set_state(BuyurtmaHolat.manzil)
    await message.answer(
        "✅ Lokatsiya qabul qilindi!\n\n"
        "🏠 Qo'shimcha manzil yozing (masalan: 3-qavat, 12-xonadon)\n"
        "yoki <b>O'tkazish</b> tugmasini bosing:",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text="➡️ O'tkazish")]
        ], resize_keyboard=True)
    )

@dp.message(BuyurtmaHolat.lokatsiya)
async def lokatsiya_eslatma(message: types.Message):
    await message.answer(
        "⚠️ Iltimos, <b>lokatsiyangizni yuboring!</b>\n\n"
        "Pastdagi 📍 tugmani bosing:",
        parse_mode="HTML",
        reply_markup=lokatsiya_kb()
    )

@dp.message(BuyurtmaHolat.manzil)
async def manzil_matn(message: types.Message, state: FSMContext):
    if message.text != "➡️ O'tkazish":
        data = await state.get_data()
        manzil = data.get('manzil', '') + f"\n🏠 {message.text}"
        await state.update_data(manzil=manzil)
    await promo_so_ra(message, state)

async def promo_so_ra(message, state):
    await state.set_state(BuyurtmaHolat.promo)
    await message.answer("🎁 Promo kodingiz bormi?", reply_markup=promo_kb())

@dp.message(F.text == "🎁 Promo kod")
async def promo_info(message: types.Message):
    await message.answer(
        "🎁 <b>Promo kodlar:</b>\n\nBuyurtma berishda kod kiriting — chegirma oling!\n\n"
        "📢 Yangi kodlar uchun kanalimizni kuzating.", parse_mode="HTML")

@dp.message(BuyurtmaHolat.promo)
async def promo_qabul(message: types.Message, state: FSMContext):
    kod = message.text.upper().strip()
    if kod in promo_kodlar:
        chegirma = promo_kodlar[kod]
        await state.update_data(promo=kod, chegirma=chegirma)
        await message.answer(f"✅ <b>{chegirma}% chegirma</b> qo'llanildi! 🎉", parse_mode="HTML")
    else:
        await state.update_data(promo=None, chegirma=0)
        await message.answer("❌ Promo kod noto'g'ri.")
    await state.set_state(BuyurtmaHolat.tolov)
    await message.answer("💳 To'lov usulini tanlang:", reply_markup=tolov_kb())

@dp.callback_query(F.data == "promo_skip")
async def promo_skip(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(promo=None, chegirma=0)
    await state.set_state(BuyurtmaHolat.tolov)
    await callback.message.answer("💳 To'lov usulini tanlang:", reply_markup=tolov_kb())

@dp.callback_query(F.data.startswith("tolov_"))
async def tolov_qabul(callback: types.CallbackQuery, state: FSMContext):
    tolov_turi = "Payme" if "payme" in callback.data else "Click"
    data = await state.get_data()
    uid = callback.from_user.id
    uid_savat = {pid: m for pid, m in savat.get(uid, {}).items() if pid in products}
    jami = sum(products[pid]['narxi'] * m for pid, m in uid_savat.items())
    chegirma_foiz = data.get('chegirma', 0)
    chegirma_summa = int(jami * chegirma_foiz / 100)
    yakuniy = jami - chegirma_summa
    raqam = buyurtma_raqam[0]
    buyurtma_raqam[0] += 1
    buyurtmalar[raqam] = {
        "user_id": uid, "ism": data.get('ism', ''), "telefon": data.get('telefon', ''),
        "manzil": data.get('manzil', ''), "lat": data.get('lat'), "lon": data.get('lon'),
        "tolov": tolov_turi, "mahsulotlar": dict(uid_savat),
        "jami": jami, "chegirma": chegirma_summa, "yakuniy": yakuniy,
        "holat": "🕐 Kutilmoqda", "sana": datetime.now().strftime("%d.%m.%Y %H:%M")
    }
    kunlik_buyurtmalar.append(raqam)
    mahsulot_matn = "\n".join([f"• {products[pid]['nomi']} x{m}" for pid, m in uid_savat.items()])
    chegirma_matn = f"\n🎁 Chegirma ({chegirma_foiz}%): -{chegirma_summa:,} so'm" if chegirma_summa else ""
    tolov_info = {"Payme": "8600 1234 5678 9012", "Click": "8600 9876 5432 1098"}
    await callback.message.answer(
        f"✅ <b>Buyurtma #{raqam} qabul qilindi!</b>\n\n"
        f"👤 {data.get('ism', '')} | 📞 {data.get('telefon', '')}\n"
        f"🏠 {data.get('manzil', '')}\n\n"
        f"🛍 {mahsulot_matn}\n\n"
        f"💰 {jami:,} so'm{chegirma_matn}\n"
        f"💵 <b>To'lov: {yakuniy:,} so'm</b>\n\n"
        f"💳 {tolov_turi}: {tolov_info[tolov_turi]}\n"
        f"⏳ To'lovdan so'ng chekni yuboring.",
        parse_mode="HTML", reply_markup=asosiy_menu()
    )
    xarita = f"\n🗺 https://maps.google.com/?q={data['lat']},{data['lon']}" if data.get('lat') else ""
    await bot.send_message(ADMIN_ID,
        f"🆕 <b>Yangi buyurtma #{raqam}!</b>\n\n"
        f"👤 {data.get('ism', '')} | 📞 {data.get('telefon', '')}\n"
        f"🏠 {data.get('manzil', '')}{xarita}\n\n"
        f"🛍 {mahsulot_matn}\n💵 <b>{yakuniy:,} so'm</b> | {tolov_turi}",
        parse_mode="HTML")
    savat[uid] = {}
    await state.clear()

@dp.message(F.text == "📦 Buyurtmalarim")
async def mening_buyurtmalarim(message: types.Message):
    uid = message.from_user.id
    mening = {r: b for r, b in buyurtmalar.items() if b['user_id'] == uid}
    if not mening:
        await message.answer("📦 Siz hali buyurtma bermagansiz.")
        return
    matn = "📦 <b>Sizning buyurtmalaringiz:</b>\n\n"
    for r, b in list(mening.items())[-5:]:
        matn += f"🔢 #{r} — {b['holat']}\n💰 {b['yakuniy']:,} so'm | {b['sana']}\n\n"
    await message.answer(matn, parse_mode="HTML")

@dp.message(F.text == "📞 Aloqa")
async def aloqa(message: types.Message):
    await message.answer(
        "📞 <b>Biz bilan bog'laning:</b>\n\n"
        "📱 +998 90 123 45 67\n📲 @market_support\n🕐 9:00 - 21:00",
        parse_mode="HTML")

@dp.message(F.text == "📊 Statistika")
async def statistika(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    jami_summa = sum(b['yakuniy'] for b in buyurtmalar.values())
    await message.answer(
        f"📊 <b>Statistika:</b>\n\n"
        f"📦 Jami: {len(buyurtmalar)}\n"
        f"🕐 Kutilmoqda: {sum(1 for b in buyurtmalar.values() if 'Kutilmoqda' in b['holat'])}\n"
        f"💰 Daromad: {jami_summa:,} so'm\n"
        f"👥 Mijozlar: {len(set(b['user_id'] for b in buyurtmalar.values()))}",
        parse_mode="HTML")

@dp.message(F.text == "📈 Kunlik hisobot")
async def kunlik_hisobot(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    bugun = datetime.now().strftime("%d.%m.%Y")
    bugungi = {r: buyurtmalar[r] for r in kunlik_buyurtmalar if r in buyurtmalar}
    if not bugungi:
        await message.answer(f"📈 <b>{bugun}:</b>\n\nBugun buyurtma yo'q.", parse_mode="HTML")
        return
    jami = sum(b['yakuniy'] for b in bugungi.values())
    ms = {}
    for b in bugungi.values():
        for pid, m in b['mahsulotlar'].items():
            ms[pid] = ms.get(pid, 0) + m
    top = sorted(ms.items(), key=lambda x: x[1], reverse=True)[:3]
    top_matn = "\n".join([f"• {products[p]['nomi']} — {m} dona" for p, m in top if p in products])
    await message.answer(
        f"📈 <b>{bugun}:</b>\n\n📦 {len(bugungi)} ta | 💰 {jami:,} so'm\n\n🏆 Top:\n{top_matn}",
        parse_mode="HTML")

@dp.message(F.text == "📦 Buyurtmalar")
async def admin_buyurtmalar(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    if not buyurtmalar:
        await message.answer("📦 Hali buyurtma yo'q.")
        return
    matn = "📦 <b>So'nggi buyurtmalar:</b>\n\n"
    for r, b in list(buyurtmalar.items())[-10:]:
        matn += f"#{r} | {b['ism']} | {b['yakuniy']:,} so'm | {b['holat']}\n"
    await message.answer(matn, parse_mode="HTML")

@dp.message(F.text == "✅ Holat yangilash")
async def holat_yangilash(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID: return
    await state.set_state(AdminHolat.buyurtma_raqam)
    await message.answer("🔢 Buyurtma raqamini kiriting:")

@dp.message(AdminHolat.buyurtma_raqam)
async def holat_raqam(message: types.Message, state: FSMContext):
    try:
        raqam = int(message.text)
        if raqam not in buyurtmalar:
            await message.answer("❌ Topilmadi.")
            await state.clear()
            return
        await state.update_data(buyurtma_raqam=raqam)
        await state.set_state(AdminHolat.buyurtma_holat)
        await message.answer("Holatni tanlang:", reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🕐 Kutilmoqda",    callback_data="h_k")],
            [InlineKeyboardButton(text="🚚 Yetkazilmoqda", callback_data="h_y")],
            [InlineKeyboardButton(text="✅ Yetkazildi",    callback_data="h_t")],
            [InlineKeyboardButton(text="❌ Bekor",         callback_data="h_b")],
        ]))
    except ValueError:
        await message.answer("❌ Faqat raqam!")
        await state.clear()

@dp.callback_query(F.data.in_({"h_k", "h_y", "h_t", "h_b"}))
async def holat_ozgartir(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID: return
    holat_map = {"h_k": "🕐 Kutilmoqda", "h_y": "🚚 Yetkazilmoqda",
                 "h_t": "✅ Yetkazildi",  "h_b": "❌ Bekor qilindi"}
    yangi = holat_map[callback.data]
    data = await state.get_data()
    raqam = data.get('buyurtma_raqam')
    if raqam and raqam in buyurtmalar:
        buyurtmalar[raqam]['holat'] = yangi
        if callback.data in ("h_t", "h_b") and raqam in kuryer_buyurtma:
            kid = kuryer_buyurtma[raqam]
            if kid in kuryerlar:
                kuryerlar[kid]['holat'] = "bo'sh"
                kuryerlar[kid]['joriy_buyurtma'] = None
            del kuryer_buyurtma[raqam]
        try:
            await bot.send_message(buyurtmalar[raqam]['user_id'],
                f"📦 <b>Buyurtma #{raqam}:</b> {yangi}", parse_mode="HTML")
        except: pass
        await callback.message.answer(f"✅ #{raqam}: {yangi}")
    await state.clear()

@dp.message(F.text == "➕ Mahsulot qo'shish")
async def mahsulot_qoshish(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID: return
    await state.set_state(AdminHolat.yangi_nomi)
    await message.answer("🛍 Mahsulot nomini kiriting:")

@dp.message(AdminHolat.yangi_nomi)
async def yangi_nomi(message: types.Message, state: FSMContext):
    await state.update_data(nomi=message.text)
    await state.set_state(AdminHolat.yangi_narxi)
    await message.answer("💰 Narxini kiriting (so'mda):")

@dp.message(AdminHolat.yangi_narxi)
async def yangi_narxi(message: types.Message, state: FSMContext):
    try:
        await state.update_data(narxi=int(message.text.replace(" ", "")))
        await state.set_state(AdminHolat.yangi_tavsif)
        await message.answer("📝 Tavsifini kiriting:")
    except ValueError:
        await message.answer("❌ Faqat raqam!")

@dp.message(AdminHolat.yangi_tavsif)
async def yangi_tavsif(message: types.Message, state: FSMContext):
    await state.update_data(tavsif=message.text)
    await state.set_state(AdminHolat.yangi_kat)
    items = list(kategoriyalar.items())
    tugmalar = []
    for i in range(0, len(items), 2):
        qator = [InlineKeyboardButton(text=k['nomi'], callback_data=f"nk_{kid}")
                 for kid, k in items[i:i+2]]
        tugmalar.append(qator)
    await message.answer("📂 Kategoriyani tanlang:",
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=tugmalar))

@dp.callback_query(F.data.startswith("nk_"))
async def yangi_kat(callback: types.CallbackQuery, state: FSMContext):
    kid = callback.data[3:]
    data = await state.get_data()
    pid = f"yangi_{len(products)+1}"
    products[pid] = {"nomi": data['nomi'], "narxi": data['narxi'],
                     "tavsif": data['tavsif'], "kat": kid}
    await callback.message.answer(f"✅ Qo'shildi!\n{data['nomi']} — {data['narxi']:,} so'm")
    await state.clear()

@dp.message(F.text == "📢 Xabar yuborish")
async def xabar_yuborish(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID: return
    await state.set_state(AdminHolat.xabar)
    await message.answer("✍️ Xabarni yozing:")

@dp.message(AdminHolat.xabar)
async def xabar_tarqatish(message: types.Message, state: FSMContext):
    foydalanuvchilar = set(b['user_id'] for b in buyurtmalar.values())
    yuborildi = 0
    for uid in foydalanuvchilar:
        try:
            await bot.send_message(uid, f"📢 <b>Marketdan xabar:</b>\n\n{message.text}", parse_mode="HTML")
            yuborildi += 1
        except: pass
    await message.answer(f"✅ {yuborildi} ta foydalanuvchiga yuborildi!")
    await state.clear()

@dp.message(F.text == "🔙 Asosiy menu")
async def asosiy(message: types.Message):
    await message.answer("Asosiy menu:", reply_markup=asosiy_menu())

class KuryerHolat(StatesGroup):
    ism = State()
    telefon = State()
    tayinla_raqam = State()

@dp.message(F.text == "🚴 Kuryer holati")
async def kuryer_holati(message: types.Message):
    uid = message.from_user.id
    faol = {r: b for r, b in buyurtmalar.items()
            if b['user_id'] == uid and b['holat'] in (
                "🕐 Kutilmoqda", "🚴 Kuryer yo'lda", "✅ Yetkazildi")}
    if not faol:
        await message.answer(
            "🚴 <b>Kuryer holati:</b>\n\n"
            "Hozircha faol buyurtmangiz yo'q.\n"
            "Yangi buyurtma bering! 🛒",
            parse_mode="HTML"
        )
        return
    matn = "🚴 <b>Kuryer holati:</b>\n\n"
    for r, b in list(faol.items())[-3:]:
        kid = kuryer_buyurtma.get(r)
        kuryer_info = ""
        if kid and kid in kuryerlar:
            k = kuryerlar[kid]
            kuryer_info = f"\n👤 Kuryer: {k['ism']}\n📞 Tel: {k['telefon']}"
        matn += f"🔢 Buyurtma #{r}\n📦 Holat: <b>{b['holat']}</b>{kuryer_info}\n\n"
    await message.answer(matn, parse_mode="HTML")

@dp.message(F.text == "🚴 Kuryer boshqaruv")
async def kuryer_boshqaruv(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    if kuryerlar:
        k_matn = "\n".join([
            f"{'🟢' if k['holat'] == 'bo`sh' else '🔴'} {k['ism']} | {k['telefon']} | {k['holat']}"
            for kid, k in kuryerlar.items()
        ])
    else:
        k_matn = "Hali kuryer qo'shilmagan"
    await message.answer(
        f"🚴 <b>Kuryer boshqaruv:</b>\n\n{k_matn}",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="➕ Kuryer qo'shish",    callback_data="kuryer_qosh")],
            [InlineKeyboardButton(text="📋 Buyurtma tayinlash", callback_data="kuryer_tayinla")],
            [InlineKeyboardButton(text="📍 Mijoz lokatsiyalari",callback_data="kuryer_lok")],
        ])
    )

@dp.callback_query(F.data == "kuryer_qosh")
async def kuryer_qosh_cb(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID: return
    await state.set_state(KuryerHolat.ism)
    await callback.message.answer("👤 Kuryer ismini kiriting:")

@dp.message(KuryerHolat.ism)
async def kuryer_ism(message: types.Message, state: FSMContext):
    await state.update_data(ism=message.text)
    await state.set_state(KuryerHolat.telefon)
    await message.answer("📞 Kuryer telefon raqamini kiriting:")

@dp.message(KuryerHolat.telefon)
async def kuryer_telefon(message: types.Message, state: FSMContext):
    data = await state.get_data()
    kid = f"kuryer_{len(kuryerlar)+1}"
    kuryerlar[kid] = {
        "ism": data['ism'],
        "telefon": message.text,
        "holat": "bo'sh",
        "joriy_buyurtma": None
    }
    await message.answer(
        f"✅ Kuryer qo'shildi!\n\n👤 {data['ism']}\n📞 {message.text}\n🟢 Holat: Bo'sh"
    )
    await state.clear()

@dp.callback_query(F.data == "kuryer_tayinla")
async def kuryer_tayinla_cb(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID: return
    tayinlanmagan = {r: b for r, b in buyurtmalar.items()
                     if b['holat'] == "🕐 Kutilmoqda" and r not in kuryer_buyurtma}
    if not tayinlanmagan:
        await callback.message.answer("📋 Tayinlanishi kerak bo'lgan buyurtma yo'q.")
        return
    tugmalar = [[InlineKeyboardButton(
        text=f"#{r} — {b['ism']} — {b['yakuniy']:,} so'm",
        callback_data=f"kt_b_{r}"
    )] for r, b in list(tayinlanmagan.items())[-10:]]
    await callback.message.answer("📋 Qaysi buyurtmaga kuryer tayinlaysiz?",
                                  reply_markup=InlineKeyboardMarkup(inline_keyboard=tugmalar))

@dp.callback_query(F.data.startswith("kt_b_"))
async def kt_buyurtma(callback: types.CallbackQuery, state: FSMContext):
    raqam = int(callback.data.split("_")[-1])
    await state.update_data(tayinla_raqam=raqam)
    bosh = {kid: k for kid, k in kuryerlar.items() if k['holat'] == "bo'sh"}
    if not bosh:
        await callback.message.answer("❌ Hozir bo'sh kuryer yo'q!")
        return
    tugmalar = [[InlineKeyboardButton(
        text=f"🚴 {k['ism']} | {k['telefon']}",
        callback_data=f"kt_k_{kid}"
    )] for kid, k in bosh.items()]
    await callback.message.answer(f"🚴 #{raqam} uchun kuryer tanlang:",
                                  reply_markup=InlineKeyboardMarkup(inline_keyboard=tugmalar))

@dp.callback_query(F.data.startswith("kt_k_"))
async def kt_kuryer(callback: types.CallbackQuery, state: FSMContext):
    kid = callback.data[5:]
    data = await state.get_data()
    raqam = data.get('tayinla_raqam')
    if raqam and raqam in buyurtmalar and kid in kuryerlar:
        kuryer_buyurtma[raqam] = kid
        kuryerlar[kid]['holat'] = "band"
        kuryerlar[kid]['joriy_buyurtma'] = raqam
        buyurtmalar[raqam]['holat'] = "🚴 Kuryer yo'lda"
        b = buyurtmalar[raqam]
        k = kuryerlar[kid]
        xarita = f"\n🗺 https://maps.google.com/?q={b['lat']},{b['lon']}" if b.get('lat') else ""
        try:
            await bot.send_message(
                b['user_id'],
                f"🚴 <b>Kuryeringiz yo'lda!</b>\n\n"
                f"👤 Kuryer: {k['ism']}\n"
                f"📞 Tel: {k['telefon']}\n\n"
                f"📦 Buyurtma #{raqam} tez orada yetkaziladi!",
                parse_mode="HTML"
            )
        except: pass
        await callback.message.answer(
            f"✅ Tayinlandi!\n📦 #{raqam} → 🚴 {k['ism']}{xarita}",
            parse_mode="HTML"
        )
    await state.clear()

@dp.callback_query(F.data == "kuryer_lok")
async def kuryer_lok_cb(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID: return
    band = {kid: k for kid, k in kuryerlar.items() if k['holat'] == "band"}
    if not band:
        await callback.message.answer("🚴 Hozir band kuryer yo'q.")
        return
    matn = "📍 <b>Mijoz lokatsiyalari:</b>\n\n"
    for kid, k in band.items():
        r = k.get('joriy_buyurtma')
        b = buyurtmalar.get(r, {})
        if b.get('lat'):
            matn += (f"🚴 {k['ism']} → Buyurtma #{r}\n"
                     f"🏠 Mijoz: https://maps.google.com/?q={b['lat']},{b['lon']}\n\n")
        else:
            matn += f"🚴 {k['ism']} → Buyurtma #{r}\n🏠 Manzil: {b.get('manzil','')}\n\n"
    await callback.message.answer(matn, parse_mode="HTML")

@dp.callback_query(F.data.in_({"h_t", "h_b"}))
async def kuryer_ozod(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    raqam = data.get('buyurtma_raqam')
    if raqam and raqam in kuryer_buyurtma:
        kid = kuryer_buyurtma[raqam]
        if kid in kuryerlar:
            kuryerlar[kid]['holat'] = "bo'sh"
            kuryerlar[kid]['joriy_buyurtma'] = None
        del kuryer_buyurtma[raqam]

async def main():
    logging.basicConfig(level=logging.INFO)
    print("🏪 Market bot ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
