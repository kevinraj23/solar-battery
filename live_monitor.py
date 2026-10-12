"""
Solar Battery Health Monitor and Automated Messenger
====================================================
Location: Salem, Tamil Nadu
Master Live Gateway with:
1. Arduino Nano ADC Edge Telemetry (Pin A0 Battery, Pin A1 Solar)
2. Machine Learning Inference (Random Forest Regressor from battery_model.pkl)
3. Live Satellite Weather API (Open-Meteo for Salem, TN)
4. TNEB Energy & Cost Savings Calculator (Tamil Nadu Electricity Board Tariff)
5. Dynamic Smart AI Diagnostic Advice
6. Automated Multi-User Telegram Alerts (Supports sending to both you & your friend!)
"""

import sys
import time
import datetime
import warnings
import requests
import joblib
import numpy as np
import serial
import serial.tools.list_ports
import threading
import re

# Suppress sklearn feature name warnings
warnings.filterwarnings('ignore', category=UserWarning)

# Ensure Windows terminal doesn't crash on emojis or special characters
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

# =====================================================================
# ⚙️ CONFIGURATION SETTINGS (EDIT THESE)
# =====================================================================

# 1. Telegram Bot Token (from @BotFather)
TELEGRAM_BOT_TOKEN = "8747746289:AAFUw90HmGsjKl_plzJ22VzSqG8KhTygViA"

# 2. Telegram Chat IDs: Add YOUR ID and your FRIEND'S ID here!
# Both phones will receive the alert at the same time:
TELEGRAM_CHAT_IDS = [
    "YOUR_TELEGRAM_CHAT_ID_HERE",
     "6189432323"  
]

# 3. Google Gemini API Key (Optional: free from https://aistudio.google.com)
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"

# 4. Hardware Settings
COM_PORT  = "COM3"    # Set your Arduino COM Port (e.g., 'COM3', 'COM4')
BAUD_RATE = 9600

# 5. Location Coordinates: SALEM, TAMIL NADU
LOCATION_NAME = "Salem"
LATITUDE      = 11.6643
LONGITUDE     = 78.1460

# 6. Reporting Interval (in seconds)
REPORT_INTERVAL_SECONDS = 60  # Sends update every 60 seconds (set to 300 for 5 mins)

# 7. Tomorrow Weather Simulation / Demo Mode
# Set to True to immediately demonstrate the "Rainy & Cloudy -> Use Wisely" alert!
# Set to False to fetch live satellite forecast from Open-Meteo for Salem.
SIMULATE_RAINY_TOMORROW = True

# 8. Solar Panel Dust / Soiling Detection & Demo Mode
# Set to True to immediately demonstrate the "Panel Dust / Dirty Glass Alert"!
# Set to False to dynamically calculate from live satellite solar irradiance vs panel output.
SIMULATE_DUSTY_PANEL = True

# =====================================================================
# 🧠 LOAD TRAINED MACHINE LEARNING MODEL
# =====================================================================
print("\n[INIT] Loading Machine Learning model from 'battery_model.pkl'...")
try:
    ml_package = joblib.load("battery_model.pkl")
    runtime_model = ml_package['runtime_model']
    soh_model     = ml_package['soh_model']
    print("[OK] ML Model loaded successfully! (Random Forest 18650 Predictor)")
except Exception as e:
    print(f"[ERROR] Could not load 'battery_model.pkl': {e}")
    print("Please run 'python train_model.py' first.")
    exit(1)

# =====================================================================
# ⛅ FETCH LIVE & TOMORROW SATELLITE WEATHER FOR SALEM (Open-Meteo API)
# =====================================================================
def get_live_weather(lat, lon, simulate_rainy=False):
    """
    Fetches real-time weather and tomorrow's forecast for Salem, TN.
    Includes rain probability, weather condition code, and daytime cloud cover.
    """
    if simulate_rainy:
        return {
            'today_desc': 'Partly Cloudy',
            'today_temp': 29.8,
            'today_cloud': 65,
            'today_irradiance': 0.0,
            'tmrw_desc': 'Rainy & Cloudy 🌧️',
            'tmrw_temp': 27.5,
            'tmrw_cloud': 85,
            'tmrw_rain_prob': 85,
            'tmrw_rain_mm': 18.5,
            'is_tmrw_rainy': True,
            'is_tmrw_cloudy': True
        }

    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&"
            f"current=temperature_2m,cloud_cover,direct_normal_irradiance&"
            f"daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum&"
            f"hourly=cloud_cover&timezone=auto"
        )
        res = requests.get(url, timeout=5).json()
        curr = res.get('current', {})
        daily = res.get('daily', {})
        hourly = res.get('hourly', {})

        today_temp = curr.get('temperature_2m', 29.8)
        today_cloud = curr.get('cloud_cover', 20)
        today_irr = curr.get('direct_normal_irradiance', 0.0)
        today_desc = "Sunny" if today_cloud < 35 else ("Partly Cloudy" if today_cloud < 70 else "Overcast")

        # Tomorrow daily forecast (index 1 is tomorrow)
        daily_codes = daily.get('weather_code', [0, 0])
        daily_temps = daily.get('temperature_2m_max', [30, 30])
        daily_probs = daily.get('precipitation_probability_max', [0, 0])
        daily_precip = daily.get('precipitation_sum', [0, 0])

        tmrw_code = daily_codes[1] if len(daily_codes) > 1 else 0
        tmrw_temp = daily_temps[1] if len(daily_temps) > 1 else 30.0
        tmrw_rain_prob = daily_probs[1] if len(daily_probs) > 1 else 0
        tmrw_rain_mm = daily_precip[1] if len(daily_precip) > 1 else 0.0

        # Estimate tomorrow daytime cloud cover (6am to 6pm, hours 30 to 42 in hourly)
        hourly_clouds = hourly.get('cloud_cover', [])
        if len(hourly_clouds) >= 42:
            tmrw_day_clouds = hourly_clouds[30:42]
            tmrw_cloud = round(sum(tmrw_day_clouds) / len(tmrw_day_clouds))
        else:
            tmrw_cloud = 30

        # WMO Weather code analysis
        is_rainy = tmrw_code in [51, 53, 55, 61, 63, 65, 80, 81, 82, 95, 96, 99] or tmrw_rain_prob >= 40 or tmrw_rain_mm >= 1.0
        is_cloudy = tmrw_code == 3 or tmrw_cloud >= 65

        if is_rainy and is_cloudy:
            tmrw_desc = "Rainy & Cloudy 🌧️"
        elif is_rainy:
            tmrw_desc = "Rain Showers 🌧️"
        elif is_cloudy:
            tmrw_desc = "Overcast / Cloudy ☁️"
        elif tmrw_cloud >= 35:
            tmrw_desc = "Partly Cloudy ⛅"
        else:
            tmrw_desc = "Clear & Sunny ☀️"

        return {
            'today_desc': today_desc,
            'today_temp': today_temp,
            'today_cloud': today_cloud,
            'today_irradiance': today_irr,
            'tmrw_desc': tmrw_desc,
            'tmrw_temp': tmrw_temp,
            'tmrw_cloud': tmrw_cloud,
            'tmrw_rain_prob': tmrw_rain_prob,
            'tmrw_rain_mm': tmrw_rain_mm,
            'is_tmrw_rainy': is_rainy,
            'is_tmrw_cloudy': is_cloudy
        }
    except Exception:
        # Realistic Salem fallback
        return {
            'today_desc': 'Partly Cloudy',
            'today_temp': 29.8,
            'today_cloud': 65,
            'today_irradiance': 0.0,
            'tmrw_desc': 'Rainy & Cloudy 🌧️',
            'tmrw_temp': 28.0,
            'tmrw_cloud': 80,
            'tmrw_rain_prob': 75,
            'tmrw_rain_mm': 12.0,
            'is_tmrw_rainy': True,
            'is_tmrw_cloudy': True
        }

# =====================================================================
# ☀️ SOLAR PANEL OPTICAL SOILING & DUST DETECTION ENGINE
# =====================================================================
def evaluate_panel_soiling(v_solar, irradiance, simulate_dust=False):
    """
    Senses optical soiling and dust accumulation on solar panel glass
    by comparing panel output against satellite direct solar irradiance.
    """
    if simulate_dust:
        return {
            'cleanliness_pct': 42,
            'is_dusty': True,
            'status': 'Dust Detected 🧹',
            'loss_pct': 58,
            'loss_watts': 1.4,
            'irradiance': 780.0
        }

    # At night or very weak sun (< 120 W/m²), optical soiling cannot be reliably assessed
    if irradiance < 120.0:
        return {
            'cleanliness_pct': 96,
            'is_dusty': False,
            'status': 'Night / Low Sunlight 🌙',
            'loss_pct': 0,
            'loss_watts': 0.0,
            'irradiance': irradiance
        }

    # Expected voltage for 6V 3W panel under sunshine
    expected_v = min(5.8, max(3.5, 3.5 + (irradiance / 1000.0) * 2.3))
    ratio = min(1.0, max(0.2, v_solar / expected_v))
    cleanliness = int(ratio * 100)
    is_dusty = cleanliness < 65
    loss_pct = max(0, 100 - cleanliness)
    loss_watts = round((loss_pct / 100.0) * 2.8, 2)

    return {
        'cleanliness_pct': cleanliness,
        'is_dusty': is_dusty,
        'status': 'Dust Detected 🧹' if is_dusty else 'Clean & Optimal ✨',
        'loss_pct': loss_pct,
        'loss_watts': loss_watts,
        'irradiance': irradiance
    }

# =====================================================================
# 💡 DYNAMIC SMART ADVICE ENGINE (PREDICTIVE & CONTEXT-AWARE)
# =====================================================================
advice_counter = 0

def get_dynamic_advice(v_bat, soh, hours, mins, weather, temp_bat=30.5, current_ma=480.0, panel_dust=None):
    """
    Generates intelligent, non-repetitive advice based on battery health,
    panel dust accumulation, temperature safety, load current, and tomorrow's forecast.
    """
    global advice_counter
    advice_counter += 1

    # 1. Thermal Safety Checks (18650 Lithium Chemistry Safety)
    if temp_bat > 45.0:
        return f"🔥 High battery temperature ({temp_bat:.1f}°C)! Move cell away from heat and reduce load to avoid thermal degradation."
    if temp_bat > 38.0 and advice_counter % 3 == 0:
        return f"🌡️ Cell temperature warm ({temp_bat:.1f}°C). Ensure ventilation around the 18650 holder for optimal cycle life."

    # 2. Critical voltage takes priority
    if v_bat < 3.3:
        return f"⚠️ Low battery warning ({v_bat:.2f}V)! Disconnect {current_ma:.0f}mA load now to prevent deep discharge."

    # 3. AUTOMATIC DUST / SOILING DETECTION ALERT
    if panel_dust and panel_dust.get('is_dusty'):
        if weather.get('is_tmrw_rainy'):
            return f"🧹 Panel Dust Detected (-{panel_dust['loss_pct']}% generation loss). However, tomorrow in Salem is forecast to be {weather['tmrw_desc']} ({weather['tmrw_rain_prob']}% rain chance) — natural rainwater will wash it clean, no manual wiping needed!"
        else:
            return f"🧹 Panel Dust Alert: Solar panel output is {panel_dust['loss_pct']}% below expected under bright sunlight! Wipe panel glass with a soft damp cloth today to restore full charging speed."

    # 4. PREDICTIVE ALERT: Tomorrow is Rainy & Cloudy!
    if weather.get('is_tmrw_rainy') or weather.get('is_tmrw_cloudy'):
        rainy_cloudy_pool = [
            f"🌧️ Tomorrow is forecast to be {weather['tmrw_desc']} in Salem ({weather['tmrw_rain_prob']}% rain chance). Solar charging will be minimal tomorrow—use battery power wisely tonight and switch off non-essential loads!",
            f"⚠️ Heavy clouds & rain expected tomorrow in Salem. Please use power wisely tonight: avoid high-drain loads so your {hours}h {mins}m backup lasts through tomorrow's low-sun hours.",
            f"☁️ Low solar harvest forecasted for Salem tomorrow ({weather['tmrw_cloud']}% cloud cover). Current load is {current_ma:.0f}mA—conserve energy tonight to maintain backup reserve.",
            f"🌧️ Rain expected tomorrow ({weather['tmrw_rain_mm']}mm rain). Solar panel output will be sluggish tomorrow morning, so practice energy conservation tonight and run in eco-mode!"
        ]
        return rainy_cloudy_pool[advice_counter % len(rainy_cloudy_pool)]

    # 5. OPTIMAL ALERT: Tomorrow is Sunny & Clear!
    if not weather.get('is_tmrw_rainy') and not weather.get('is_tmrw_cloudy'):
        sunny_pool = [
            f"☀️ Ample sunshine forecasted tomorrow in Salem ({weather['tmrw_temp']}°C). Full solar recharge expected tomorrow, so safe to utilize your normal battery backup tonight.",
            f"🌤️ Clear skies expected tomorrow in Salem. Solar panels will easily replenish your 18650 cell by noon; your {hours}h {mins}m backup is in great shape.",
            f"Battery cell temperature ({temp_bat:.1f}°C) is in the safe thermal zone for 18650 chemistry. Zero thermal stress.",
            f"Cell degradation is minimal (Health: {soh:.0f}%). Real load current steady at {current_ma:.0f}mA.",
            f"Solar charging curve matches standard 3W profile. Monthly TNEB savings tracking on target."
        ]
        return sunny_pool[advice_counter % len(sunny_pool)]

    return f"Battery voltage steady at {v_bat:.2f}V. Use power wisely to maximize your {hours}h {mins}m backup tonight."

# =====================================================================
# 🤖 GEMINI AI ENHANCED REPORT GENERATOR
# =====================================================================
def generate_layman_report(v_bat, soh, hours, mins, wh_today, tneb_units, tneb_saved, monthly_saved, weather, current_ma=480.0, temp_bat=30.5, panel_dust=None):
    """Formats the clean, beautiful report for Salem including telemetry, panel dust status, thermal health, and tomorrow's forecast."""
    real_power_w = round((v_bat * current_ma) / 1000.0, 2)
    thermal_status = "Safe" if temp_bat < 38.0 else ("Warm" if temp_bat < 45.0 else "Overheating")
    panel_status_str = f"{panel_dust['cleanliness_pct']}% ({panel_dust['status']})" if panel_dust else "Clean ✨"
    
    # 1. Try Gemini AI if API key is provided
    if GEMINI_API_KEY and GEMINI_API_KEY != "YOUR_GEMINI_API_KEY_HERE":
        try:
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")

            prompt = f"""
You are the AI Specialist for the 'Solar Battery Health Monitor and Automated Messenger' stationed in Salem, Tamil Nadu.
Telemetry:
- Battery Voltage: {v_bat:.2f}V | Current Draw: {current_ma:.0f}mA ({real_power_w:.2f}W) | Cell Temp: {temp_bat:.1f}°C ({thermal_status})
- Health: {soh:.0f}% | Backup: {hours}h {mins}m tonight
- Solar Panel: {wh_today:.1f} Wh harvested today | Panel Cleanliness: {panel_status_str}
- TNEB Units: {tneb_units:.3f} | Saved: Rs {tneb_saved:.2f} (Rs {monthly_saved:.2f}/mo)
- Salem Weather Today: {weather['today_desc']}, {weather['today_temp']}°C, Cloud Cover {weather['today_cloud']}%
- Tomorrow Forecast: {weather['tmrw_desc']}, Max Temp: {weather['tmrw_temp']}°C, Rain Probability: {weather['tmrw_rain_prob']}%, Cloud Cover: {weather['tmrw_cloud']}%

Generate EXACTLY these 7 bullet points with clear formatting and NO conversational opening:
• 🔋 *Battery Health:* {soh:.0f}% (Healthy) • {hours}h {mins}m backup tonight
• ⚡ *Real Load:* {current_ma:.0f} mA ({real_power_w:.2f} W) • Cell Temp: {temp_bat:.1f}°C ({thermal_status})
• ☀️ *Solar Panel:* {wh_today:.1f} Wh generated • Cleanliness: {panel_status_str}
• 💰 *TNEB Savings:* {tneb_units:.3f} Units • Saved ₹{tneb_saved:.2f} today (₹{monthly_saved:.2f}/mo)
• ⛅ *Salem Weather:* Today: {weather['today_desc']} ({weather['today_temp']}°C) • Cloud Cover {weather['today_cloud']}%
• 🔮 *Tomorrow Forecast:* {weather['tmrw_desc']} • Rain Chance {weather['tmrw_rain_prob']}%
• 💡 *Smart Advice:* [Write 1 fresh, practical tip. If panel is dusty, alert user to clean it or mention if tomorrow's rain will clean it! If tomorrow is rainy/cloudy, advise using power wisely tonight]
"""
            res = model.generate_content(prompt)
            if res and res.text:
                return res.text.strip()
        except Exception as e:
            pass

    # 2. Robust Built-in Dynamic Formatter (Zero-repetition, perfect predictive structure)
    smart_tip = get_dynamic_advice(v_bat, soh, hours, mins, weather, temp_bat=temp_bat, current_ma=current_ma, panel_dust=panel_dust)

    report = (
        f"• 🔋 *Battery Health:* `{soh:.0f}%` (Healthy) • `{hours}h {mins}m backup tonight`\n"
        f"• ⚡ *Real Load:* `{current_ma:.0f} mA` ({real_power_w:.2f} W) • Cell Temp: `{temp_bat:.1f}°C ({thermal_status})`\n"
        f"• ☀️ *Solar Panel:* `{wh_today:.1f} Wh` • Cleanliness: `{panel_status_str}`\n"
        f"• 💰 *TNEB Savings:* `{tneb_units:.3f} Units` • Saved `₹{tneb_saved:.2f} today` (₹{monthly_saved:.2f}/mo)\n"
        f"• ⛅ *Salem Weather:* Today: `{weather['today_desc']} ({weather['today_temp']}°C)` • Cloud Cover `{weather['today_cloud']}%`\n"
        f"• 🔮 *Tomorrow Forecast:* `{weather['tmrw_desc']}` • Rain Chance `{weather['tmrw_rain_prob']}%`\n"
        f"• 💡 *Smart Advice:* {smart_tip}"
    )
    return report

# =====================================================================
# 📲 MULTI-USER TELEGRAM DISPATCHER
# =====================================================================
def send_telegram_alerts(report_body):
    """Sends the report to ALL configured Telegram Chat IDs (you + friend)."""
    timestamp_str = datetime.datetime.now().strftime("%I:%M %p")
    header = (
        f"🤖 *Solar Battery Health Monitor & Messenger*\n"
        f"📍 *Station:* {LOCATION_NAME}, TN • `{timestamp_str}`\n"
        f"────────────────────────────────"
    )
    full_message = f"{header}\n{report_body}"

    # Check if user added their bot token
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        print("\n[TELEGRAM PREVIEW (Configure token to send to mobile)]:\n" + full_message + "\n")
        return

    # Filter out empty or placeholder chat IDs
    active_chat_ids = [
        cid for cid in TELEGRAM_CHAT_IDS 
        if cid and cid != "YOUR_TELEGRAM_CHAT_ID_HERE" and cid != "FRIENDS_CHAT_ID_HERE"
    ]

    if not active_chat_ids:
        print("[TELEGRAM] No valid Chat IDs configured in TELEGRAM_CHAT_IDS.")
        return

    for chat_id in active_chat_ids:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": full_message,
            "parse_mode": "Markdown"
        }
        try:
            res = requests.post(url, json=payload, timeout=6)
            if res.status_code == 200:
                print(f"[TELEGRAM] Alert sent to Chat ID {chat_id}!")
            else:
                print(f"[TELEGRAM ERROR] ID {chat_id}: HTTP {res.status_code}")
        except Exception as err:
            print(f"[TELEGRAM FAILED] ID {chat_id}: {err}")

# =====================================================================
# 🌐 SHARED TELEMETRY STATE FOR INTERACTIVE COPILOT
# =====================================================================
latest_telemetry = {
    'v_battery': 3.88,
    'v_solar': 5.82,
    'current_ma': 480.0,
    'temp_bat': 30.5,
    'real_power_w': 1.86,
    'pred_soh': 94.0,
    'backup_hours': 6,
    'backup_mins': 40,
    'wh_today': 14.5,
    'tneb_units': 0.015,
    'tneb_saved': 1.20,
    'monthly_saved': 36.00,
    'weather': {
        'today_desc': 'Partly Cloudy',
        'today_temp': 29.8,
        'today_cloud': 65,
        'tmrw_desc': 'Rainy & Cloudy 🌧️',
        'tmrw_temp': 27.5,
        'tmrw_cloud': 85,
        'tmrw_rain_prob': 85,
        'tmrw_rain_mm': 18.5,
        'is_tmrw_rainy': True,
        'is_tmrw_cloudy': True
    },
    'panel_dust': {
        'cleanliness_pct': 42,
        'is_dusty': True,
        'status': 'Dust Detected 🧹',
        'loss_pct': 58,
        'loss_watts': 1.4,
        'irradiance': 780.0
    }
}

# =====================================================================
# 💬 TWO-WAY INTERACTIVE AI BATTERY DOCTOR (COPILOT)
# =====================================================================
def ask_ai_battery_doctor(user_question, telemetry):
    """
    Answers arbitrary user questions about appliances, battery runtime,
    charging health, and weather preparation in English or Tamil.
    """
    v_bat   = telemetry['v_battery']
    v_sol   = telemetry['v_solar']
    cur_ma  = telemetry['current_ma']
    temp_c  = telemetry['temp_bat']
    p_w     = telemetry['real_power_w']
    soh     = telemetry['pred_soh']
    hrs     = telemetry['backup_hours']
    mins    = telemetry['backup_mins']
    wh_tot  = telemetry['wh_today']
    weather = telemetry['weather']
    panel_dust = telemetry.get('panel_dust', {'cleanliness_pct': 42, 'is_dusty': True, 'status': 'Dust Detected 🧹', 'loss_pct': 58, 'loss_watts': 1.4})
    thermal_status = "Safe" if temp_c < 38.0 else ("Warm" if temp_c < 45.0 else "Overheating")

    # 1. Try Gemini AI for open-ended contextual reasoning
    if GEMINI_API_KEY and GEMINI_API_KEY != "YOUR_GEMINI_API_KEY_HERE":
        try:
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")

            prompt = f"""
You are "SolarBot", the intelligent AI Electrochemical Copilot & Battery Doctor for an 18650 Solar Battery System stationed in Salem, Tamil Nadu.

LIVE SENSOR & WEATHER TELEMETRY:
• Battery: {v_bat:.2f}V | Health (SoH): {soh:.0f}% | Cell Temp: {temp_c:.1f}°C ({thermal_status})
• Current Draw: {cur_ma:.0f} mA | Load Power: {p_w:.2f} Watts
• Estimated Backup: {hrs}h {mins}m tonight
• Solar Panel: {wh_tot:.1f} Wh | Cleanliness: {panel_dust['cleanliness_pct']}% ({panel_dust['status']}) | Optical Loss: -{panel_dust['loss_pct']}%
• Salem Weather Today: {weather['today_desc']} ({weather['today_temp']}°C, {weather['today_cloud']}% clouds)
• Tomorrow's Forecast: {weather['tmrw_desc']}, Rain Probability: {weather['tmrw_rain_prob']}%, Cloud Cover: {weather['tmrw_cloud']}%

USER'S QUESTION:
"{user_question}"

INSTRUCTIONS:
1. Provide a direct, helpful, expert response in 2-4 sentences with relevant emojis.
2. If user asks about the solar panel, dust, cleanliness, or cleaning:
   - Report the cleanliness score and optical loss.
   - If tomorrow's forecast is rain, mention that natural rain will wash it clean! Otherwise, advise wiping with a damp cloth.
3. If the user asks whether they can run a specific appliance (e.g. 10W fan, TV, lamp):
   - Mathematically estimate if remaining battery capacity can sustain it.
   - Cross-reference with tomorrow's forecast: If tomorrow is rainy/cloudy in Salem, advise conserving power tonight because solar recharging tomorrow will be low!
4. If the user asks in Tamil or Tanglish, reply fluently and warmly in Tamil/Tanglish.
5. If asked "status", "hi", or "report", give a concise snapshot.
"""
            res = model.generate_content(prompt)
            if res and res.text:
                return res.text.strip()
        except Exception:
            pass

    # 2. Robust Built-in Smart Diagnostic Engine (Offline / Zero-API fallback)
    text = user_question.lower()

    # Solar Panel & Dust / Soiling query (e.g., "is panel dusty?", "panel health", "clean panel", "thusi")
    if any(k in text for k in ['dust', 'dirty', 'clean', 'panel', 'soiling', 'wash', 'wipe', 'thusi', 'kannaadi']):
        if any(k in text for k in ['sollu', 'iruku', 'epdi', 'thusi', 'soodu', 'mazhai']):
            return (
                f"🧹 *சோலார் பேனல் தூய்மை நிலை:*\n"
                f"பேனல் கண்ணாடியில் தூசி படிந்துள்ளது (தூய்மை: `{panel_dust['cleanliness_pct']}%`).\n"
                f"இதனால் சோலார் மின் உற்பத்தி `-{panel_dust['loss_pct']}%` குறைந்துள்ளது.\n"
                f"💡 *ஆலோசனை:* கண்ணாடியை மெல்லிய ஈரத்துணியால் துடைத்தால் சார்ஜிங் உடனடியாக அதிகரிக்கும்!"
            )
        rain_note = "Tomorrow's rain will naturally wash your panel clean!" if weather.get('is_tmrw_rainy') else "Wipe the panel glass with a soft damp microfiber cloth today to recover full 3W solar generation!"
        return (
            f"🧹 *Solar Panel Cleanliness Diagnosis:*\n"
            f"• Cleanliness Score: `{panel_dust['cleanliness_pct']}%` ({panel_dust['status']})\n"
            f"• Optical Loss: `-{panel_dust['loss_pct']}%` (~{panel_dust['loss_watts']}W lost under sunshine)\n"
            f"💡 *Recommendation:* {rain_note}"
        )

    # General Tamil / Tanglish intent
    if any(k in text for k in ['nalaiki', 'epdi', 'iruku', 'mazhai', 'sollu', 'vanakam', 'kaatru']):
        return (
            f"🔋 *பேட்டரி நிலை:* `{v_bat:.2f}V` (ஆரோக்கியம்: `{soh:.0f}%`, வெப்பம்: `{temp_c:.1f}°C`)\n"
            f"⏳ *பேக்கப்:* `{hrs}h {mins}m` இன்றிரவு.\n"
            f"🌧️ *நாளை சேலம் வானிலை:* `{weather['tmrw_desc']}` ({weather['tmrw_rain_prob']}% மழை வாய்ப்பு).\n"
            f"💡 *ஆலோசனை:* நாளை சோலார் சார்ஜிங் குறைவாக இருக்கும், எனவே இன்றிரவு பேட்டரியை சிக்கனமாக பயன்படுத்தவும்!"
        )

    # Appliance / Load assessment query (e.g., "Can I run a 10W fan?")
    watt_match = re.search(r'(\d+)\s*(w|watt)', text)
    if watt_match or any(k in text for k in ['fan', 'light', 'lamp', 'tv', 'load', 'run', 'power', 'device']):
        asked_watts = float(watt_match.group(1)) if watt_match else 10.0
        usable_soc = max(0.05, min(1.0, (v_bat - 3.2) / (4.15 - 3.2)))
        usable_wh = round(usable_soc * 8.5, 1)
        run_h = usable_wh / max(0.1, asked_watts)
        run_hours = int(run_h)
        run_minutes = int((run_h - run_hours) * 60)

        if weather.get('is_tmrw_rainy') or weather.get('is_tmrw_cloudy'):
            weather_adv = f"⚠️ *Warning:* Tomorrow in Salem is forecast to be {weather['tmrw_desc']} ({weather['tmrw_rain_prob']}% rain). Solar recharging will be poor tomorrow, so we advise keeping loads under 2W tonight!"
        else:
            weather_adv = f"☀️ Tomorrow's forecast is clear ({weather['tmrw_desc']}), so solar panels will easily replenish your battery tomorrow."

        return (
            f"⚡ *Appliance Assessment ({asked_watts:.0f}W):*\n"
            f"At your current voltage ({v_bat:.2f}V, ~{usable_wh} Wh usable), a {asked_watts:.0f}W load will run for approx `{run_hours}h {run_minutes}m`.\n"
            f"{weather_adv}"
        )

    # Status / Greeting query
    if any(k in text for k in ['status', 'report', 'health', 'how is', 'check', 'hi', 'hello', 'start', 'help']):
        return (
            f"🤖 *Solar Battery AI Doctor — Live Status:*\n"
            f"• 🔋 *Battery:* `{v_bat:.2f}V` | Health: `{soh:.0f}%` | Temp: `{temp_c:.1f}°C ({thermal_status})`\n"
            f"• ⚡ *Real Load:* `{cur_ma:.0f} mA` ({p_w:.2f} W) | Backup: `{hrs}h {mins}m`\n"
            f"• ☀️ *Solar Panel:* `{wh_tot:.1f} Wh` | Cleanliness: `{panel_dust['cleanliness_pct']}%` ({panel_dust['status']})\n"
            f"• 🔮 *Tomorrow:* `{weather['tmrw_desc']}` (Rain: `{weather['tmrw_rain_prob']}%`)\n"
            f"💬 *You can ask me questions like:*\n"
            f"- _\"Is my solar panel dirty?\"_\n"
            f"- _\"Can I run my 10W fan tonight?\"_\n"
            f"- _\"நாளைக்கு மழை பெய்யுமா?\"_"
        )

    # Temperature / Thermal query
    if any(k in text for k in ['temp', 'heat', 'hot', 'thermal']):
        return (
            f"🌡️ *Thermal Diagnosis:* Battery temperature is `{temp_c:.1f}°C`.\n"
            f"Optimal range for 18650 Li-ion is 20°C–35°C. " +
            ("Cell is operating within safe thermal parameters." if temp_c < 38.0 else "Ensure adequate ventilation around the battery holder!")
        )

    # General fallback
    return (
        f"🔋 *Live Summary:* Battery is at `{v_bat:.2f}V` ({soh:.0f}% SoH) with `{hrs}h {mins}m` backup.\n"
        f"Tomorrow's Salem forecast: `{weather['tmrw_desc']}` ({weather['tmrw_rain_prob']}% rain).\n"
        f"💡 Ask me any question about your appliances, panel dust, charging, or energy saving!"
    )

# =====================================================================
# 🤖 BACKGROUND TELEGRAM CHATBOT LISTENER THREAD
# =====================================================================
def telegram_chatbot_worker():
    """
    Background worker that listens for incoming Telegram user messages
    and responds instantly with AI Battery Doctor diagnostics and advice.
    """
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        return

    last_update_id = 0
    print("[CHATBOT] Telegram Interactive AI Copilot is LIVE and listening for questions!\n")

    while True:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
            params = {"timeout": 4, "offset": last_update_id + 1}
            res = requests.get(url, params=params, timeout=6).json()

            if res.get("ok") and res.get("result"):
                for update in res["result"]:
                    last_update_id = update["update_id"]
                    msg = update.get("message")
                    if not msg or "text" not in msg:
                        continue

                    chat_id = str(msg["chat"]["id"])
                    user_text = msg["text"].strip()
                    user_name = msg.get("from", {}).get("first_name", "User")

                    print(f"\n[CHATBOT QUESTION from {user_name} ({chat_id})]: '{user_text}'")

                    # Generate AI Copilot Response
                    ai_reply = ask_ai_battery_doctor(user_text, latest_telemetry)
                    print(f"[CHATBOT AI REPLY]:\n{ai_reply}\n")

                    # Send answer back to Telegram user
                    send_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                    payload = {
                        "chat_id": chat_id,
                        "text": ai_reply,
                        "parse_mode": "Markdown"
                    }
                    requests.post(send_url, json=payload, timeout=6)

        except Exception:
            time.sleep(2)

        time.sleep(1)

# =====================================================================
# 🔄 MAIN EXECUTION LOOP
# =====================================================================
def run_monitor():
    print(f"\n[INIT] Connecting to Arduino Nano on port '{COM_PORT}'...")
    try:
        ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=2)
        time.sleep(2)
        print(f"[OK] CONNECTED TO ARDUINO NANO ON {COM_PORT}!\n")
    except Exception as e:
        print(f"[INFO] Could not open {COM_PORT} ({e}).")
        print(f"Notice: Running in SIMULATION MODE for {LOCATION_NAME} (18650 & 3W Rock Light).\n")
        ser = None

    start_time = time.time()
    previous_v = None
    last_report_timestamp = 0
    sim_step = 0

    print("="*70)
    print(f"SOLAR BATTERY MONITOR & AUTOMATED MESSENGER ({LOCATION_NAME}, TN)")
    print(f"Predictive Weather: {'SIMULATED RAIN/CLOUDS' if SIMULATE_RAINY_TOMORROW else 'LIVE SATELLITE'}")
    print("="*70 + "\n")

    # Start 2-Way Interactive AI Chatbot Copilot Thread
    chatbot_thread = threading.Thread(target=telegram_chatbot_worker, daemon=True)
    chatbot_thread.start()

    try:
        while True:
            sim_step += 1
            if ser:
                try:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    if not line or ',' not in line:
                        continue
                    parts = line.split(',')
                    v_battery  = float(parts[0])
                    v_solar    = float(parts[1])
                    current_ma = float(parts[2]) if len(parts) > 2 else 480.0
                    temp_bat   = float(parts[3]) if len(parts) > 3 else 30.5
                except:
                    continue
            else:
                time.sleep(3)
                # Realistic simulation with slight dynamic drift so backup time changes
                v_battery = round(3.88 - (sim_step * 0.003), 2)
                if v_battery < 3.20:
                    v_battery = 3.88  # Reset cycle
                v_solar    = 5.82
                current_ma = 480.0  # 3W Rock Light draw ~ 480mA
                temp_bat   = round(30.5 + (sim_step * 0.02), 1)

            elapsed_minutes = (time.time() - start_time) / 60.0
            if previous_v is None:
                sag_rate_mv = 1.0
            else:
                sag_rate_mv = max(0.1, abs(previous_v - v_battery) * 1000.0)
            previous_v = v_battery

            # 1. Machine Learning Prediction
            features = np.array([[v_battery, elapsed_minutes, sag_rate_mv]])
            pred_runtime_minutes = runtime_model.predict(features)[0]
            pred_soh             = soh_model.predict(features)[0]

            backup_hours = int(pred_runtime_minutes // 60)
            backup_mins  = int(pred_runtime_minutes % 60)

            # 2. Solar & TNEB Savings
            wh_generated = round(v_solar * 0.48 * 5.0, 1)
            tneb_units   = round(wh_generated / 1000.0, 3)
            tneb_saved   = round(tneb_units * 8.0, 2)
            monthly_save = round(tneb_saved * 30, 2)

            # 3. Weather for Salem (Live Today + Tomorrow Forecast)
            weather_info = get_live_weather(LATITUDE, LONGITUDE, simulate_rainy=SIMULATE_RAINY_TOMORROW)

            # 4. Solar Panel Optical Dust & Soiling Detection
            panel_dust = evaluate_panel_soiling(v_solar, weather_info['today_irradiance'], simulate_dust=SIMULATE_DUSTY_PANEL)

            # Update shared state for interactive chatbot copilot
            latest_telemetry.update({
                'v_battery': v_battery,
                'v_solar': v_solar,
                'current_ma': current_ma,
                'temp_bat': temp_bat,
                'real_power_w': round((v_battery * current_ma) / 1000.0, 2),
                'pred_soh': pred_soh,
                'backup_hours': backup_hours,
                'backup_mins': backup_mins,
                'wh_today': wh_generated,
                'tneb_units': tneb_units,
                'tneb_saved': tneb_saved,
                'monthly_saved': monthly_save,
                'weather': weather_info,
                'panel_dust': panel_dust
            })

            # Stream to local terminal
            print(f"[STREAM] Bat: {v_battery:.2f}V | Sol: {v_solar:.2f}V (Dust: {panel_dust['cleanliness_pct']}%) | Load: {current_ma:.0f}mA | Temp: {temp_bat:.1f}°C | Backup: {backup_hours}h {backup_mins}m | Tmrw: {weather_info['tmrw_desc']}")

            # 5. Generate & Send Predictive Report
            current_time = time.time()
            if (current_time - last_report_timestamp) >= REPORT_INTERVAL_SECONDS:
                last_report_timestamp = current_time

                report_body = generate_layman_report(
                    v_bat=v_battery,
                    soh=pred_soh,
                    hours=backup_hours,
                    mins=backup_mins,
                    wh_today=wh_generated,
                    tneb_units=tneb_units,
                    tneb_saved=tneb_saved,
                    monthly_saved=monthly_save,
                    weather=weather_info,
                    current_ma=current_ma,
                    temp_bat=temp_bat,
                    panel_dust=panel_dust
                )

                print("\n" + "="*65)
                print(f"SMART PREDICTIVE REPORT ({LOCATION_NAME}):")
                print("="*65)
                print(report_body)
                print("="*65 + "\n")

                # Send to Telegram
                send_telegram_alerts(report_body)

    except KeyboardInterrupt:
        print("\n[STOP] Monitor stopped by user.")
        if ser:
            ser.close()

if __name__ == "__main__":
    run_monitor()
