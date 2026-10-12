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
LATITUDE           = 11.6643           # Salem Latitude
LONGITUDE          = 78.1460           # Salem Longitude

# 4. Tomorrow Weather & Demo Simulation
SIMULATE_RAINY_TOMORROW = True         # Set True to test 'Rainy & Cloudy - Use Wisely' alert!
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
1. Connect sensors to Arduino Nano:
   - **Pin A0**: 18650 Battery Voltage Divider (10k resistor)
   - **Pin A1**: Solar Panel Voltage Divider (10k:10k resistors)
   - **Pin A2**: ACS712-05A Current Sensor OUT
   - **Pin A3**: LM35 Temperature Sensor VOUT
2. Open `arduino_sensor.ino` in Arduino IDE.
3. Select Board: **Arduino Nano**, Processor: **ATmega328P**.
4. Upload to your Nano.
5. **Close the Serial Monitor in Arduino IDE.**

### Step 3: Run the Live Monitor
```bash
python live_monitor.py
```

> 💡 **No Hardware? No Problem!**  
> If an Arduino is not plugged in, the system automatically enters **Simulation Mode**, emulating your exact 18650 cell ($3.84\text{V}$), 3W Rock Light solar panel ($5.85\text{V}$), 480mA load current, and 30.5°C cell temperature!

---

## 📬 Sample Predictive Report (Telegram & Console)

```markdown
🤖 Solar Battery Health Monitor & Messenger
📍 Station: Salem, TN • 06:46 PM
────────────────────────────────
• 🔋 Battery Health: 94% (Healthy) • 6h 40m backup tonight
• ⚡ Real Load: 480 mA (1.85 W) • Cell Temp: 31.2°C (Safe)
• ☀️ Solar Energy: 14.5 Wh generated today
• 💰 TNEB Savings: 0.015 Units • Saved ₹1.20 today (₹36.00/mo)
• ⛅ Salem Weather: Today: Partly Cloudy (29.8°C) • Cloud Cover 65%
• 🔮 Tomorrow Forecast: Rainy & Cloudy 🌧️ • Rain Chance 85%
• 💡 Smart Advice: ⚠️ Tomorrow is forecast to be Rainy & Cloudy in Salem (85% rain chance). Solar charging will be minimal tomorrow—use battery power wisely tonight and switch off non-essential loads!
```
---

## 💬 Two-Way Interactive AI Battery Doctor (Chatbot)

Users can chat directly with the bot on Telegram (`@mysolar_battery_health_bot`) to get instant answers regarding appliances, battery health, and weather preparation in **English or Tamil**:

### 🗣️ Example Chat Interactions:
* **Load Estimation:**
  > **User:** *"Can I run a 10W fan tonight?"*  
  > **AI Doctor:** *"⚡ At current voltage (3.88V, ~6.1 Wh usable), a 10W load will run for approx 0h 36m. ⚠️ Warning: Tomorrow in Salem is forecast to be Rainy & Cloudy 🌧️ (85% rain). Solar recharging will be poor tomorrow, so we advise keeping loads under 2W tonight!"*

* **Thermal & Health Diagnostics:**
  > **User:** *"Why is cell temperature 31°C?"*  
  > **AI Doctor:** *"🌡️ Battery temperature is 31.2°C. The optimal range for 18650 Li-ion is 20°C–35°C. The cell is operating within safe thermal parameters with zero thermal degradation."*

* **Regional Language (Tamil / Tanglish):**
  > **User:** *"Nalaiki mazhai peyyuma, battery epdi iruku?"*  
  > **AI Doctor:** *"🔋 பேட்டரி நிலை: 3.88V (ஆரோக்கியம்: 94%, வெப்பம்: 30.5°C). ⏳ பேக்கப்: 6h 40m. 🌧️ நாளை சேலம் வானிலை: Rainy & Cloudy (85% மழை). சோலார் சார்ஜிங் குறைவாக இருக்கும், எனவே இன்றிரவு சிக்கனமாக பயன்படுத்தவும்!"*

---

## 👥 Authors
Developed for Engineering Mini-Project:  
**Solar Battery Health Monitor and Automated Messenger**
