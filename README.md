# Solar Battery Health Monitor and Automated Messenger

An intelligent Edge-to-Cloud IoT system that monitors 18650 lithium-ion solar battery health, predicts remaining backup runtime using Machine Learning, calculates TNEB electricity bill savings, cross-references live satellite weather, and sends 5-bullet layman reports via Telegram using Google Gemini AI.

---

##  Quick Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/solar-battery-monitor.git
cd solar-battery-monitor
```

### 2. Install Required Python Libraries
```bash
pip install -r requirements.txt
```

---

##  Configuration (Open `live_monitor.py`)

Open `live_monitor.py` and set your credentials at the top (lines 28–39):

```python
# 1. Telegram Bot Credentials
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"  # Get from @BotFather on Telegram
TELEGRAM_CHAT_ID   = "YOUR_CHAT_ID"    # Get from @userinfobot on Telegram

# 2. Google Gemini API Key
GEMINI_API_KEY     = "YOUR_GEMINI_KEY" # Free from https://aistudio.google.com

# 3. Hardware COM Port & Location
COM_PORT           = "COM3"            # Port of Arduino Nano (e.g. COM3, COM4)
LATITUDE           = 13.0827           # Your city latitude (e.g., Chennai: 13.0827)
LONGITUDE          = 80.2707           # Your city longitude (e.g., Chennai: 80.2707)
```

---

##  How to Run

### Step 1: Train the Machine Learning Model
*(Only needs to be run once)*
```bash
python train_model.py
```
This loads the 18650 dataset, trains the Random Forest Regressors, and exports `battery_model.pkl`.

### Step 2: Upload Firmware to Arduino Nano
1. Open `arduino_sensor.ino` in Arduino IDE.
2. Select Board: **Arduino Nano**, Processor: **ATmega328P**.
3. Upload to your Nano.
4. **Close the Serial Monitor in Arduino IDE.**

### Step 3: Run the Live Monitor
```bash
python live_monitor.py
```

>  **No Hardware? No Problem!**  
> If an Arduino is not plugged in, the system automatically enters **Simulation Mode**, emulating your exact 18650 cell ($3.84\text{V}$) and 3W Rock Light solar panel ($5.85\text{V}$), so anyone can test it immediately on any laptop!

---

##  Sample 5-Bullet Report (Telegram & Console)

```markdown
🤖 Solar Battery Health Monitor & Messenger
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• 🔋 Battery Health: 94% (Healthy) • 6 Hours 40 Mins backup tonight
• ☀️ Solar Energy: 14.5 Watt-hours generated today
• 💰 TNEB Savings: 0.015 Units • Saved ₹1.20 today (₹36.00/month)
• ⛅ Weather Today: Sunny (31.5°C) • Cloud Cover 18%
• 💡 Smart Advice: Ample sun today! Full brightness backup assured all night.
```

---


