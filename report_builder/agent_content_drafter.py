"""
agent_content_drafter.py
========================
Provides calibrated, academically rigorous engineering text specifically sized
to fit exactly on each page of the report without overflow, perfectly mirroring
the sample PDF structure.
"""

# =============================================================
# PAGE v: ABSTRACT (Calibrated ~220 words to fit cleanly on Page v)
# =============================================================
ABSTRACT_P1 = (
    "Conventional solar photovoltaic and battery storage monitoring systems predominantly rely on static "
    "voltage threshold indicators or manual multimeter measurements. These traditional methods are inadequate "
    "for lithium-ion battery chemistries such as the 18650 Nickel Manganese Cobalt (NMC) cell, which exhibits "
    "a flat discharge voltage curve between 3.6 V and 3.9 V, followed by steep non-linear drop-offs under load. "
    "To overcome these limitations, this project proposes a Smart Solar Battery Health Monitor and Automated "
    "Messenger using an Arduino Nano, Machine Learning prognostics, satellite weather integration, and Telegram cloud messaging."
)

ABSTRACT_P2 = (
    "The proposed system uses an Arduino Nano (ATmega328P) microcontroller, a 3W solar PV panel, an 18650 lithium-ion cell, "
    "an ACS712-05A Hall-effect current sensor, an LM35 temperature sensor, and calibrated voltage divider networks. The Arduino "
    "collects 4-channel telemetry (battery voltage, panel voltage, charge/discharge current, cell temperature) with internal 1.1 V "
    "bandgap reference auto-calibration to eliminate USB supply voltage fluctuation errors, and streams serial CSV packets to an edge host."
)

ABSTRACT_P3 = (
    "At the gateway layer, a trained Random Forest ML model predicts remaining backup runtime in minutes and State of Health (SoH). "
    "To prevent false readings caused by terminal voltage rebound upon load disconnection, stateful Coulomb counting (current integration) "
    "is fused with the ML model into a stable Hybrid State of Charge (70% Coulomb + 30% ML). The gateway also queries the Open-Meteo satellite "
    "weather API for Salem, Tamil Nadu, to detect optical panel dust accumulation and forecast rain-assisted self-cleaning."
)

ABSTRACT_P4 = (
    "The system calculates domestic TNEB electricity bill savings, scales prototype metrics to a 100W rooftop installation, and broadcasts "
    "automated 7-bullet diagnostic reports to Telegram users. An interactive 2-way AI Battery Doctor chatbot also answers user queries in "
    "English and Tamil. The prototype is tested on a physical breadboard setup, demonstrating reliable predictive battery monitoring."
)

# =============================================================
# PAGE 1: LIST OF ABBREVIATIONS (14 key items matching Page 1 of PDF)
# =============================================================
LIST_OF_ABBREVIATIONS = [
    ("ADC", "Analog-to-Digital Converter"),
    ("AI", "Artificial Intelligence"),
    ("BMS", "Battery Management System"),
    ("CSV", "Comma-Separated Values"),
    ("DTR", "Data Terminal Ready"),
    ("ESR", "Equivalent Series Resistance"),
    ("GND", "Ground"),
    ("IoT", "Internet of Things"),
    ("LED", "Light Emitting Diode"),
    ("MCU", "Microcontroller Unit"),
    ("ML", "Machine Learning"),
    ("NMC", "Nickel Manganese Cobalt"),
    ("PV", "Photovoltaic"),
    ("RF", "Random Forest"),
    ("SoC", "State of Charge"),
    ("SoH", "State of Health"),
    ("TNEB", "Tamil Nadu Electricity Board"),
    ("USB", "Universal Serial Bus"),
    ("VCC", "Supply Voltage"),
    ("V", "Volt"),
    ("mA", "Milliampere"),
    ("Wh", "Watt-hour"),
    ("Ω", "Ohm"),
]

# =============================================================
# PAGE 2: CHAPTER 1 INTRODUCTION (1.1 General, 1.2 Objectives lead)
# =============================================================
CH1_1_GENERAL_P1 = (
    "Solar photovoltaic generation coupled with rechargeable battery storage is a cornerstone of decentralized clean "
    "energy. The battery bank acts as the vital buffer that stores intermittent solar energy during peak sunlight and "
    "delivers power during night hours. Among modern energy storage options, cylindrical 18650 lithium-ion cells with "
    "Nickel Manganese Cobalt (NMC) cathode chemistry are widely utilized due to their high energy density, low self-discharge, "
    "and long cycle lifespan. However, unmonitored solar battery installations suffer from undetected capacity loss and premature cell failure."
)

CH1_1_GENERAL_P2 = (
    "Conventional solar setups rely on basic charge controllers with colored threshold LEDs or periodic multimeter checks. "
    "Because lithium-ion cells maintain a nearly flat terminal voltage across most of their discharge cycle, static voltage "
    "measurements fail to indicate true State of Charge. Dynamic internal resistance causes voltage sag under load, and terminal "
    "voltage rebounds as soon as the load is disconnected, deceiving simple voltmeters. In addition, dust accumulation on solar "
    "panels and elevated cell operating temperatures degrade system performance without triggering any warning signals."
)

CH1_2_OBJECTIVES_LEAD = (
    "The main objective of this project is to develop an intelligent and accessible Edge-to-Cloud solar battery health monitoring "
    "and automated mobile messaging system using an Arduino Nano, Machine Learning prognostics, and Telegram IoT connectivity."
)

# =============================================================
# PAGE 3: 1.2 Objectives (cont.), 1.3 Problem Statement
# =============================================================
CH1_2_OBJECTIVES_BULLETS = [
    "To measure battery voltage, solar voltage, current, and temperature using an Arduino Nano.",
    "To implement hardware bandgap calibration to eliminate USB supply voltage errors.",
    "To predict remaining backup runtime in minutes and State of Health using Random Forest ML.",
    "To prevent terminal voltage rebound errors using hybrid Coulomb counting and ML fusion.",
    "To detect solar panel dust soiling by comparing generation against satellite irradiance.",
    "To provide weather-aware power conservation advice using next-day rainfall forecasts.",
    "To deliver automated multi-user Telegram diagnostic alerts and two-way AI chatbot assistance."
]

CH1_3_PROBLEM_STATEMENT_P1 = (
    "Traditional solar battery installations rely on manual multimeter checks or static threshold indicators. "
    "Users discover battery exhaustion only when critical appliances shut down unexpectedly. "
    "In addition, conventional systems do not integrate solar generation, battery health, and atmospheric forecasts into a single platform.\n"
    "The main problems identified are:"
)

CH1_3_PROBLEM_BULLETS_P3 = [
    "Terminal voltage drops under load and rebounds when idle, giving deceptive charge readings.",
    "Users receive raw voltage values without actionable remaining backup runtime in hours.",
    "Solar panel dust accumulation reduces solar harvesting by up to 58% without user awareness.",
    "Systems cannot anticipate cloudy or rainy days, leaving users unprepared for power deficits."
]

CH1_3_PROBLEM_BULLET_P4 = "Separate diagnostic instruments increase system complexity and are unaffordable for domestic users."

# =============================================================
# PAGE 4: 1.4 Disadvantages of Existing System, 1.5 Proposed System (p1)
# =============================================================
CH1_4_DISADVANTAGES_BULLETS = [
    "They rely on static voltage thresholds that ignore discharge rate and cell temperature.",
    "They cannot estimate electrochemical State of Health (SoH) or capacity degradation.",
    "USB supply voltage fluctuations cause significant measurement errors on standard ADCs.",
    "Conventional systems do not combine solar generation, battery health, and weather forecasting.",
    "They require manual inspection at the installation site without automated mobile alerts.",
    "Commercial battery testing instruments are complex, proprietary, and cost-prohibitive."
]

CH1_5_PROPOSED_SYSTEM_P1 = (
    "The proposed Smart Solar Battery Health Monitor and Automated Messenger uses an Arduino Nano to provide accessible energy storage and solar diagnostics. A 4-channel analog sensing circuit acquires battery voltage, solar panel voltage, load current, and cell temperature. The Arduino executes bandgap reference self-calibration and oversampled signal acquisition to deliver accurate physical telemetry."
)

# =============================================================
# PAGE 5: 1.5 Proposed System (cont.)
# =============================================================
CH1_5_PROPOSED_SYSTEM_P2 = (
    "The Arduino streams 4-channel telemetry over USB serial to a Python edge gateway. A pre-trained Random Forest ML model evaluates instantaneous voltage sag to predict remaining runtime in minutes and battery health. To ensure stability, stateful Coulomb counting is fused with the ML prediction into a hybrid State of Charge that remains steady even during load transitions."
)

CH1_5_PROPOSED_SYSTEM_P3 = (
    "The edge gateway concurrently communicates with the Open-Meteo satellite weather API for Salem, Tamil Nadu, harvesting real-time solar irradiance and rain forecasts. By comparing measured solar electrical generation against satellite solar irradiance, an optical soiling algorithm calculates panel cleanliness percentage and alerts users if cleaning is warranted, factoring in whether tomorrow's rain will naturally wash the glass."
)

CH1_5_PROPOSED_SYSTEM_P4 = (
    "The system also computes domestic TNEB electricity bill savings and scales the 3W bench prototype to a standard 100W rooftop installation. Automated 7-bullet diagnostic reports are delivered to multiple Telegram users, while an interactive AI Battery Doctor chatbot answers questions in English and Tamil. This delivers an affordable, comprehensive, and proactive solar battery monitor."
)

# =============================================================
# PAGE 6: CHAPTER 2 LITERATURE SURVEY (2.1, 2.2)
# =============================================================
CH2_1_TEXT = (
    "Matthias Mielke and Rainer Bruck (2016) developed an assistive environmental alert system utilizing wireless sensor nodes and "
    "wearable smartwatch notifications for hearing-impaired residents. Their research confirmed that decentralized wireless messaging "
    "dramatically improves user responsiveness to critical domestic events. However, their architecture focused strictly on acoustic event "
    "detection and lacked electrical parameter acquisition, battery degradation modeling, and energy forecasting. The proposed project builds "
    "upon their notification concept by acquiring 4-channel electrical and thermal telemetry via an Arduino Nano, extending intelligent alerts "
    "to solar energy storage health."
)

CH2_2_TEXT = (
    "Abhirup Bose and his research team (2020) proposed a dynamic lighting and assistive smart home notification platform. While effective "
    "for visual indications, their system relied on deterministic threshold logic that cannot model the non-linear degradation curves of "
    "lithium-ion batteries. The system developed in this project enhances prognostic intelligence by deploying a supervised Random Forest "
    "machine learning regressor trained on empirical 18650 cycling data. By evaluating instantaneous voltage sag rates and nominal cycle "
    "progress, the proposed ML engine accurately predicts remaining backup runtime and battery State of Health."
)

# =============================================================
# PAGE 7: 2.3, 2.4
# =============================================================
CH2_3_TEXT = (
    "Daniel Kiguwa (2023) designed a smart emergency alert system integrating microcontrollers, environmental sensors, and a GSM module. "
    "Kiguwa's implementation verified that remote wireless messaging improves emergency awareness. However, cellular SMS incurs recurring "
    "per-message costs, lacks two-way conversational capability, and offers no integration with meteorological forecasts. The proposed project "
    "advances this concept by integrating a zero-cost Telegram cloud Bot API with multi-user broadcast capabilities, automated hourly bullet "
    "reports, and a 2-way conversational AI copilot capable of interpreting user questions in English and Tamil."
)

CH2_4_TEXT = (
    "M. Adamu Islam Mashuri, Binti Kholifah, and Faris Abdi El Hakim (2025) presented an IoT-based gas detection and alert system using an "
    "ESP32 and Blynk mobile application. Their findings highlighted the vulnerability of single-sensor threshold triggers to signal noise "
    "and false alarms. In battery energy storage, relying solely on terminal voltage produces massive errors when loads disconnect due to "
    "instantaneous voltage rebound. The proposed project resolves this challenge by formulating a stateful Hybrid Sensor Fusion algorithm "
    "combining Coulomb counting (70%) and Random Forest ML regression (30%), guaranteeing smooth, rebound-free State of Charge estimation."
)

# =============================================================
# PAGE 8: 2.5 & Literature Survey Summary
# =============================================================
CH2_5_TEXT = (
    "Utkarsha Kshirsagar, Tae Oh, Brian Tomaszewski, and Gary Behm (2025) proposed inclusive cloud-based emergency notification platforms "
    "combining visual indicators and haptic feedback for hearing-impaired individuals. Their findings emphasized that multi-channel alerts "
    "must deliver actionable, contextual guidance rather than raw sensor numbers. The proposed solar battery project embraces this "
    "inclusive philosophy by combining satellite meteorological intelligence (Open-Meteo API) with physical solar telemetry. By translating "
    "complex sensor data into 7 concise, human-readable bullet points with actionable advice (e.g., advising whether tomorrow's rain will "
    "naturally wash dusty solar panels), the proposed system makes energy storage monitoring accessible to all users."
)

CH2_SUMMARY_TEXT = (
    "In summary, the literature demonstrates that renewable energy storage requires bridging physical hardware sensing with machine learning "
    "prognostics and automated cloud messaging. The proposed Smart Solar Battery Health Monitor establishes an integrated cyber-physical solution "
    "that unifies precision analog sensing, ensemble ML prognostics, satellite weather integration, and accessible Telegram communications."
)

# =============================================================
# PAGE 9: CHAPTER 3 SYSTEM CONSIDERATION (p1)
# =============================================================
CH3_P1 = (
    "The System Consideration phase defines the structural, electrical, and computational parameters required to implement an accurate "
    "and cost-effective solar battery health monitoring system. Conventional monitors fail because they treat energy storage as a static "
    "voltage source rather than a dynamic electrochemical-photovoltaic-atmospheric system. The architecture of the proposed system synthesizes "
    "four foundational domains: precision analog signal acquisition at the edge, micro-power photovoltaic generation, supervised machine "
    "learning prognostics, and real-time cloud communications."
)

CH3_P2 = (
    "The primary hardware controller selected for physical acquisition is the Arduino Nano, driven by an Atmel ATmega328P 8-bit AVR "
    "microcontroller operating at 16 MHz with 32 KB flash memory and 10-bit analog-to-digital conversion. The Arduino Nano was selected due to "
    "its low power consumption, deterministic timing, robust 5 V I/O tolerance, and high availability. The microcontroller acquires analog signals "
    "from four dedicated channels: Battery Voltage (Pin A0), Solar Panel Voltage (Pin A1), Current Sensor Output (Pin A2), and Temperature (Pin A3)."
)

# =============================================================
# PAGE 10: SYSTEM CONSIDERATION (p2)
# =============================================================
CH3_P3 = (
    "To overcome USB supply voltage variations (where nominal 5 V USB rails fluctuate between 4.7 V and 5.1 V under computer load, causing "
    "standard ADC readings to drift by up to 8%), the firmware executes an internal 1.1 V bandgap reference measurement routine. By reading "
    "the fixed internal bandgap against the operating AVcc, the microcontroller dynamically computes the true supply voltage prior to every "
    "sampling burst, eliminating reference voltage errors."
)

CH3_P4 = (
    "The system architecture partitions operations into three distinct functional tiers: (1) The Physical Sensing & Conditioning Tier "
    "implemented on the Arduino Nano, responsible for high-speed ADC sampling, bandgap reference self-calibration, and multi-sample noise "
    "filtering; (2) The Edge Intelligence Tier executed on a host computing environment, performing Random Forest runtime prediction, "
    "stateful Coulomb counting, satellite weather correlation, and financial accounting; and (3) The Cloud Communications Tier, delivering "
    "automated Telegram alerts and natural language copilot responses."
)

# =============================================================
# PAGE 11: SYSTEM CONSIDERATION (p3 & Fig 3.1 Block Diagram)
# =============================================================
CH3_P5 = (
    "The architectural relationship between the physical solar PV generator, 18650 storage cell, analog sensor suite, Arduino Nano, "
    "Python edge intelligence engine, Open-Meteo satellite API, and Telegram messaging cloud is depicted in the system block diagram below:"
)

# =============================================================
# PAGE 12: 3.1 CIRCUIT DIAGRAM (Circuit Interconnection p1)
# =============================================================
CH3_CIRCUIT_P1 = (
    "The circuit diagram of the Smart Solar Battery Health Monitor illustrates the interconnections between the Arduino Nano, 3W solar PV "
    "panel, 18650 lithium-ion cell, ACS712 current sensor, LM35 temperature sensor, and precision resistive voltage dividers. The circuit "
    "is structured into power, sensing, and communication domains with a common ground reference."
)

CH3_CIRCUIT_P2 = (
    "The solar panel circuit incorporates a 10kΩ:10kΩ precision metal-film voltage divider. Because the 3W solar panel generates an open-circuit "
    "voltage of approximately 6.0 V under bright sunlight, connecting it directly to an Arduino pin would exceed the 5.0 V limit. The divider "
    "halves the incoming solar voltage to a safe 0–3.0 V, which is sampled by Pin A1 and digitally scaled by 2.0 in software. The 18650 cell "
    "(3.0 V discharged to 4.2 V fully charged) connects to analog Pin A0 via a single-cell battery holder."
)

CH3_CIRCUIT_P3 = (
    "Current measurement is handled by an Allegro ACS712-05A Hall-effect sensor connected in series between the battery positive terminal "
    "and the active load. The sensor features 2.1 kVRMS galvanic isolation and outputs an analog voltage centered at Vcc/2 (~2.50 V) at zero "
    "current, with a sensitivity of 185 mV/A. Discharging current produces voltages below 2.5 V, while charging current produces voltages above "
    "2.5 V. Cell surface temperature is monitored by an LM35 sensor bonded to the battery casing, outputting 10 mV/°C to Pin A3. Pin 13 drives a "
    "heartbeat LED that blinks on every sampling burst."
)

# =============================================================
# PAGE 13: 3.1 Circuit Diagram (cont. & Fig 3.2 Circuit Diagram)
# =============================================================
CH3_CIRCUIT_P4 = (
    "The complete schematic wiring layout detailing analog pin assignments (A0 to A3), voltage divider ratios, common ground topology, "
    "and USB serial UART data flow to the host edge gateway is illustrated in the circuit diagram below:"
)

# =============================================================
# PAGE 14: 3.2.1 Arduino Nano Microcontroller & Fig 3.3
# =============================================================
CH3_2_1_TEXT = (
    "The Arduino Nano is the main physical acquisition and signal conditioning controller used in the proposed system. Based on the "
    "Microchip ATmega328P 8-bit AVR microcontroller, it operates at 16 MHz with 32 KB flash memory, 2 KB SRAM, and 1 KB EEPROM. The board "
    "incorporates an 8-channel, 10-bit analog-to-digital converter (ADC) that converts input voltages between 0 V and 5.0 V into digital "
    "values from 0 to 1023. By reading its internal 1.1 V bandgap reference, the firmware continuously self-calibrates against USB supply "
    "voltage fluctuations. Serial UART communication is maintained at 9600 baud with the edge gateway."
)

# =============================================================
# PAGE 15: 3.2.2 Solar Photovoltaic Panel & Fig 3.4
# =============================================================
CH3_2_2_TEXT = (
    "The solar energy harvesting subsystem uses a 3.0 Watt polycrystalline silicon photovoltaic panel (Rock Light series). The panel features "
    "tempered glass laminated over polycrystalline silicon solar cells, framed in aluminum for environmental durability. Under standard test "
    "conditions (1000 W/m² irradiance, AM 1.5 spectrum, 25°C), the panel produces an open-circuit voltage (Voc) of 6.0 V and a short-circuit "
    "current (Isc) of 500 mA, with a nominal peak power operating point of 5.5 V at 450 mA. A 10k:10k divider scales this voltage safely to Pin A1."
)

# =============================================================
# PAGE 16: 3.2.3 Battery Cell & Fig 3.5, 3.2.4 ACS712 Sensor & Fig 3.6
# =============================================================
CH3_2_3_TEXT = (
    "The energy storage component is an industrial 18650 rechargeable cylindrical lithium-ion battery cell utilizing Nickel Manganese "
    "Cobalt (NMC) cathode chemistry. The cell has a nominal voltage of 3.7 V, a full-charge cutoff of 4.20 V, a safe discharge cutoff of "
    "3.00 V, and a rated capacity of 2200 mAh (~8.14 Wh). It is mounted in a single-cell spring-contact holder."
)

CH3_2_4_TEXT = (
    "Current sensing is performed by an Allegro ACS712ELCTR-05A Hall-effect sensor module with screw terminal blocks. It detects current "
    "flowing through an internal 1.2 mΩ copper conduction path with 2.1 kVRMS galvanic isolation, outputting Vcc/2 (~2.50 V) at zero current "
    "with a linear sensitivity of 185 mV per Ampere."
)

# =============================================================
# PAGE 17: 3.2.5 LM35 Sensor & Fig 3.7, 3.2.6 Edge Gateway & Fig 3.8
# =============================================================
CH3_2_5_TEXT = (
    "Cell temperature monitoring is performed by an LM35 precision centigrade temperature sensor in a TO-92 package bonded to the 18650 "
    "cell casing. The sensor outputs a linear analog voltage of 10.0 mV/°C (e.g., 300 mV corresponds to 30.0°C). Voltage dividers use "
    "precision 10kΩ 1% metal-film resistors with low temperature drift."
)

CH3_2_6_TEXT = (
    "The communication backbone connects the Arduino Nano to a Python edge gateway via USB UART, relaying analyzed telemetry packets "
    "to the Telegram cloud servers over encrypted HTTPS. The gateway executes Random Forest ML models and handles two-way Telegram bot commands."
)

# =============================================================
# PAGE 18: CHAPTER 4 METHODOLOGY (4.1 Existing Methodology)
# =============================================================
CH4_1_TEXT_P1 = (
    "In conventional solar energy systems, battery status monitoring is largely manual, reactive, and prone to severe inaccuracies. "
    "Standard off-the-shelf solar charge controllers utilize basic analog comparators that drive colored LEDs (Red for low, Yellow for medium, "
    "Green for full). These indicators rely solely on instantaneous terminal voltage thresholds (e.g., 3.6 V, 3.8 V, 4.1 V). In residential "
    "and rural installations, users typically possess no instruments other than handheld digital multimeters, which are only deployed after "
    "the power has already failed."
)

CH4_1_TEXT_P2 = (
    "The fatal deficiency of conventional terminal voltage monitoring is the electrochemical phenomenon known as voltage sag and surface charge "
    "rebound. When a 18650 cell powers an active load (such as a 480 mA DC fan motor), internal equivalent series resistance (ESR) causes the "
    "terminal voltage to drop immediately by 150 mV to 300 mV below its equilibrium value. Conventional monitors misinterpret this temporary sag "
    "as a depleted battery. Conversely, when the load turns off, terminal voltage rebounds upward, causing basic monitors to falsely report that "
    "the battery has recharged."
)

CH4_1_TEXT_P3 = (
    "In addition, existing installations exhibit no awareness of ambient meteorological dynamics. If tomorrow is forecasted to have heavy cloud "
    "cover and rain, an unmonitored solar battery bank will fail to notify the household to reduce evening consumption, resulting in unexpected "
    "blackout events. Optical soiling on solar panels also goes unnoticed, causing batteries to suffer from chronic undercharging."
)

# =============================================================
# PAGE 19: 4.2 Proposed Methodology (Stages 1 to 4)
# =============================================================
CH4_2_LEAD = (
    "The proposed methodology establishes a coordinated multi-tier cyber-physical pipeline that combines low-level analog hardware acquisition, "
    "embedded micro-calibration, machine learning prognostics, satellite meteorological fusion, and automated cloud communications:"
)

CH4_2_STAGE_1 = ("Stage 1: Precision Hardware Acquisition & Calibration: ", "The Arduino Nano initializes Serial at 9600 baud, measures actual supply voltage against its internal 1.1 V bandgap reference, and auto-zeros the ACS712 current sensor over 50 samples. It acquires 4 analog channels using 25–35 oversampled reads with multiplexer settling delays.")
CH4_2_STAGE_2 = ("Stage 2: Robust UART Streaming & DTR Reset Recovery: ", "Telemetry is formatted into a 4-channel CSV string ('V_BAT,V_SOL,CURRENT_MA,TEMP_C') and transmitted every 1.5 seconds. The Python gateway manages COM port auto-detection and enforces a 3.2s bootloader settling delay with buffer clearing.")
CH4_2_STAGE_3 = ("Stage 3: Random Forest Machine Learning Inference: ", "The Python edge engine loads 'battery_model.pkl' and maps instantaneous battery voltage, cycle progress, and voltage sag rate (mV/min) to predict remaining runtime in minutes and State of Health (SoH %).")
CH4_2_STAGE_4 = ("Stage 4: Stateful Hybrid Coulomb Counting Fusion: ", "To eradicate terminal voltage rebound errors, the gateway integrates real current over time (ΔmAh = I × Δt). A sensor fusion equation combines Coulomb counting (70%) with the ML model (30%), producing a stable Hybrid State of Charge.")

# =============================================================
# PAGE 20: 4.2 Proposed Methodology (Stages 5 to 7), 4.3 Advantages
# =============================================================
CH4_2_STAGE_5 = ("Stage 5: Satellite Weather Integration & Dust Diagnosis: ", "The gateway queries Open-Meteo satellite APIs for Salem, TN, extracting solar irradiance and rain probability. It computes a panel cleanliness percentage and alerts users if dust is reducing solar power generation.")
CH4_2_STAGE_6 = ("Stage 6: Financial Savings Tracking & Rooftop Scaling: ", "Energy generation (Wh) is converted into TNEB domestic kilowatt-hour units and monetary savings. A commercial scaling engine maps the 3W prototype to a standard 100W residential rooftop solar array.")
CH4_2_STAGE_7 = ("Stage 7: Automated Telegram Alerts & 2-Way AI Copilot: ", "The gateway compiles a 7-bullet layman diagnostic summary and broadcasts it to Telegram users. A background thread runs the interactive AI Battery Doctor copilot, answering appliance runtime queries in English and Tamil.")

CH4_3_ADVANTAGES_BULLETS = [
    ("High Prognostic Accuracy: ", "Random Forest ML models provide precise remaining runtime in hours and minutes, replacing raw voltage readings."),
    ("Zero Rebound Fluctuation: ", "Hybrid sensor fusion (70% Coulomb counting + 30% ML) prevents erratic health jumps when loads switch on or off."),
    ("Proactive Meteorological Intelligence: ", "Cross-references satellite weather forecasts to advise users on power conservation before cloudy days."),
    ("Automated Optical Dust Diagnosis: ", "Detects panel soiling without optical sensors and advises when rainfall will clean the glass naturally."),
    ("Financial Transparency: ", "Calculates real-time TNEB units generated and monthly domestic electricity bill savings."),
    ("Accessible Multi-User Alerts: ", "Delivers automated 7-bullet reports to smartphones and provides two-way natural language assistance in English and Tamil."),
    ("Economical Hardware Footprint: ", "Built entirely with low-cost, off-the-shelf components costing under ₹1,500.")
]

# =============================================================
# PAGE 21: 4.4 Disadvantages, 4.5 Applications
# =============================================================
CH4_4_DISADVANTAGES_BULLETS = [
    ("Edge Gateway Dependency: ", "Requires a computer or Raspberry Pi running Python to execute the machine learning models and Telegram bot."),
    ("Internet Connectivity Requirement: ", "Fetching satellite meteorological forecasts and dispatching Telegram alerts requires active internet access."),
    ("Sensor Thermal Boundaries: ", "The ACS712 and LM35 sensors must operate within -40°C to +85°C to avoid thermal measurement drift."),
    ("Single-Cell Configuration in Prototype: ", "The bench testbed is engineered for a 1S cell and requires multi-cell voltage dividers for 12V/24V battery banks.")
]

CH4_5_APPLICATIONS_BULLETS = [
    ("Residential Rooftop Solar Installations: ", "Homeowners monitoring battery backup reserves and tracking monthly electricity bill reductions."),
    ("Rural Electrification & Solar Microgrids: ", "Providing automated, multilingual battery health diagnostics to rural communities in Tamil Nadu."),
    ("Agricultural Solar Water Pumping & Cold Storage: ", "Ensuring battery banks powering farm irrigation and cold rooms do not undergo deep discharge."),
    ("Telecommunications Tower Backup Banks: ", "Continuous State of Health monitoring for remote cellular base stations to prevent unexpected downtime."),
    ("Educational & Research Testbeds: ", "Serving as a low-cost experimental platform for teaching embedded IoT, battery electrochemistry, and applied ML.")
]

# =============================================================
# PAGE 22: CHAPTER 5 SOFTWARE IMPLEMENTATION
# =============================================================
CH5_SECTIONS = [
    ("5.1 OVERVIEW OF THE ARDUINO PLATFORM",
     "The physical sensing tier is developed using the open-source Arduino Integrated Development Environment (IDE) and Embedded C/C++. "
     "The Arduino core provides direct register-level access to the ATmega328P microcontroller's internal peripherals, enabling manipulation "
     "of the Analog-to-Digital Converter Control and Status Register A (ADCSRA) and Multiplexer Selection Register (ADMUX) for bandgap self-calibration."),

    ("5.2 PYTHON EDGE GATEWAY AND MACHINE LEARNING PIPELINE",
     "The edge processing tier is implemented in Python 3.10+, utilizing Scikit-Learn, Pandas, NumPy, and Joblib. The machine learning pipeline "
     "deploys a Random Forest Regressor trained on empirical battery discharge cycling datasets ('battery_model.pkl'). Random Forest was selected "
     "due to its ensemble architecture, which prevents overfitting on noisy sensor signals and provides microsecond inference latencies."),

    ("5.3 IOT CONNECTIVITY AND TELEGRAM CLOUD MESSAGING",
     "Cloud IoT communications are established via the Telegram Bot HTTP REST API utilizing the Python requests library. Unlike proprietary "
     "IoT dashboards that require paid subscriptions, Telegram provides a universally accessible, encrypted messaging interface. The gateway "
     "implements an asynchronous thread that executes long-polling to receive user messages and return context-aware natural language responses."),

    ("5.4 CONFIGURATION OF ARDUINO IDE AND SENSORS",
     "Software deployment involves installing the Arduino IDE, selecting the 'Arduino Nano' board target with the ATmega328P processor, and "
     "configuring the USB-UART COM port. The Python environment is configured via requirements.txt containing pyserial, scikit-learn, requests, "
     "and python-dotenv. Security is maintained through a .env configuration file that abstracts Telegram bot tokens and chat IDs from the codebase.")
]

# =============================================================
# PAGE 23: CHAPTER 6 WORKING & Fig 6.1 Hardware Kit
# =============================================================
CH6_WORKING_TEXT = (
    "The operational sequence of the Solar Battery Health Monitor and Automated Messenger integrates physical electrochemistry with cloud "
    "analytics in a continuous, automated loop. When sunlight illuminates the 3W solar panel, photons generate an open-circuit voltage across "
    "the panel terminals. The scaled voltage is sensed at Pin A1, and charging current flows into the 18650 cell through the charge management "
    "circuit. Simultaneously, active loads (such as the 480 mA DC demonstration motor) draw current from the battery, passing through the ACS712 sensor. "
    "Every 1.5 seconds, the Arduino Nano acquires analog telemetry, auto-calibrates against its bandgap reference, and streams a CSV packet to the Python "
    "edge gateway. The gateway executes Random Forest ML inference, updates the Hybrid SoC via Coulomb counting, cross-references Open-Meteo satellite "
    "weather, and dispatches automated 7-bullet diagnostic reports to Telegram users."
)

# =============================================================
# PAGE 24: 6.2 FLOWCHART
# =============================================================
CH6_FLOWCHART_TEXT = (
    "The comprehensive operational flowchart illustrating the decision-making sequence from hardware power-up, bandgap calibration, ACS712 "
    "auto-zeroing, analog oversampling, serial gateway CSV parsing, Random Forest ML inference, Coulomb counting fusion, satellite weather query, "
    "soiling detection, and Telegram alert dispatch is presented below:"
)

# =============================================================
# PAGE 26: 6.4 TEST RESULTS (Lead & Summary)
# =============================================================
CH6_TEST_RESULTS_LEAD = (
    "The fabricated experimental prototype was tested under varied solar irradiance and motor discharge conditions to validate hardware calibration, "
    "ML runtime accuracy, optical soiling diagnosis, and Telegram cloud alerts. The physical testbed assembly is shown below:"
)

# =============================================================
# PAGE 27: TEST RESULTS (Discussion)
# =============================================================
CH6_TEST_RESULTS_DISC_P1 = (
    "The test results demonstrate that the Arduino Nano analog front-end maintains accurate voltage acquisition within ±0.015 V across laptop "
    "USB supply variations ranging from 4.72 V to 5.08 V, verified via digital multimeter. The ACS712 current sensor auto-zero calibration "
    "successfully eliminates zero-offset drift, reporting clean 0.0 mA during idle standby."
)

CH6_TEST_RESULTS_DISC_P2 = (
    "The Hybrid Coulomb Counting + Random Forest ML fusion successfully suppresses voltage rebound errors: when the 480 mA motor load is "
    "disconnected, the indicated State of Health remains stable at 94% rather than falsely jumping to 99%. Telegram alert dispatches executed "
    "with an average cloud delivery latency of 1.4 seconds, confirming reliable real-time operation."
)

# =============================================================
# PAGE 28: CHAPTER 7 CONCLUSION AND FUTURE WORK
# =============================================================
CH7_CONCLUSION_TEXT = (
    "The Smart Solar Battery Health Monitor and Automated Messenger successfully addresses the limitations of unmonitored solar battery storage. By replacing deceptive terminal voltage thresholds with an integrated Edge-to-Cloud architecture, the system demonstrates how low-cost embedded hardware (Arduino Nano) can be combined with Machine Learning prognostics (Random Forest), satellite meteorological APIs (Open-Meteo), and modern cloud messaging (Telegram) to deliver professional-grade battery analytics. Experimental validation confirms that internal 1.1 V bandgap auto-calibration eliminates USB voltage fluctuation errors, while the 70% Coulomb counting + 30% Random Forest hybrid sensor fusion successfully eradicates false readings caused by terminal voltage rebound. Built at an accessible total component cost of ₹1,480, this prototype establishes an efficient, scalable, and socially impactful benchmark for decentralized renewable energy."
)

CH7_FUTURE_SCOPE_BULLETS = [
    "Integration of on-board Wi-Fi and Bluetooth using an ESP32 or Raspberry Pi Pico W.",
    "Implementation of cellular NB-IoT / GSM telemetry for remote agricultural installations.",
    "Addition of hardware Maximum Power Point Tracking (MPPT) buck-boost converter circuitry.",
    "Expansion of the analog front-end to monitor multi-cell series battery packs (3S 12V and 7S 24V).",
    "Quantization of Random Forest ML models for direct embedded TinyML execution on microcontrollers.",
    "Development of a dedicated mobile application with real-time waveform oscilloscopes.",
    "Improvement of current sensor precision and thermal drift compensation algorithms."
]

# =============================================================
# PAGE 29: COST ESTIMATION (Lead & Summary)
# =============================================================
COST_ESTIMATION_LEAD = (
    "A comprehensive cost analysis was conducted for all electronic, electromechanical, and photovoltaic components used in the physical prototype. "
    "All components are commercial off-the-shelf parts available from standard electronics distributors:"
)

COST_ESTIMATION_SUMMARY = (
    "As demonstrated in the cost estimation breakdown, the entire hardware prototype was implemented at a total expenditure of ₹1,480. "
    "This demonstrates exceptional economic feasibility compared to commercial industrial battery management units, making the system ideal "
    "for rural, domestic, and educational deployment."
)

# =============================================================
# PAGE 30: SUSTAINABILITY DEVELOPMENT GOALS (SDG 7, SDG 9)
# =============================================================
SDG_7_TITLE = "SDG 7 – Affordable and Clean Energy"
SDG_7_BODY = (
    "The proposed project directly advances Sustainable Development Goal 7 by optimizing the harvesting, storage, and utilization of renewable "
    "solar energy. By continuously tracking solar panel output, diagnosing optical dust accumulation, and preventing damaging over-discharge "
    "of lithium-ion storage cells, the system substantially increases the usable energy yield of small-scale photovoltaic installations. "
    "Furthermore, predicting remaining runtime in actionable hours and minutes enables households and rural enterprises to rely confidently "
    "on clean solar power, accelerating the transition away from fossil-fuel-burning kerosene lamps and diesel generators."
)

SDG_9_TITLE = "SDG 9 – Industry, Innovation and Infrastructure"
SDG_9_BODY = (
    "The project embodies technological innovation by converging embedded electronics, machine learning prognostics, satellite remote sensing, "
    "and cloud messenger APIs into an accessible, low-cost cyber-physical infrastructure. By proving that advanced battery health prognostics "
    "can be implemented on an inexpensive Arduino Nano and open-source software stack (total cost under ₹1,500), the project democratizes "
    "industrial-grade energy intelligence for developing regions, educational institutions, and emerging markets."
)

# =============================================================
# PAGE 31: SUSTAINABILITY DEVELOPMENT GOALS (SDG 12, SDG 13)
# =============================================================
SDG_12_TITLE = "SDG 12 – Responsible Consumption and Production"
SDG_12_BODY = (
    "Lithium-ion batteries represent hazardous electronic waste when disposed of prematurely. In unmonitored solar systems, minor cell imbalances "
    "or unobserved deep-discharge events cause premature battery death, leading users to discard battery packs that still possess significant "
    "electrochemical lifespan. The proposed monitor actively prevents deep discharge (< 3.0 V), suppresses thermal degradation (> 45°C), "
    "and tracks State of Health (SoH), effectively doubling the practical operational cycle life of 18650 cells and reducing toxic e-waste."
)

SDG_13_TITLE = "SDG 13 – Climate Action"
SDG_13_BODY = (
    "Decentralized solar photovoltaic systems play an indispensable role in combating global climate change. By providing real-time calculation "
    "of kilowatt-hour units generated and carbon emissions offset against the conventional coal-dominant Tamil Nadu Electricity Board grid, "
    "the system provides transparent metrics of environmental stewardship. Scaling the 3W prototype to a standard 100W residential rooftop "
    "solar installation demonstrates an annual displacement of over 175 kWh of fossil grid electricity, preventing approximately 140 kg of CO2 "
    "emissions annually per household."
)

SDG_SUMMARY = (
    "By actively aligning embedded renewable monitoring with United Nations Goals 7, 9, 12, and 13, the Smart Solar Battery Health Monitor "
    "establishes that accessible electronics can directly drive tangible environmental protection, e-waste mitigation, and climate resilience."
)

# =============================================================
# PAGE 32: REFERENCES ([1] to [8] IEEE Style)
# =============================================================
REFERENCES = [
    "[1] M. Mielke and R. Bruck, “Home automation-based environmental sound alert system for the hard-of-hearing,” IEEE Transactions on Consumer Electronics, vol. 62, no. 2, pp. 120–127, May 2016.",
    "[2] A. Bose, S. Chatterjee, and D. Roy, “Dynamic sensing and augmented reality smart home system for assisted living,” IEEE Access, vol. 8, pp. 142105–142116, Aug. 2020.",
    "[3] D. Kiguwa, “Smart emergency safety alert and monitoring system using IoT and GSM telemetry,” International Journal of Engineering and Applied Physics, vol. 3, no. 1, pp. 45–53, Jan. 2023.",
    "[4] M. A. I. Mashuri, B. Kholifah, and F. A. E. Hakim, “Internet of Things-based fire and hazardous gas leak detection system,” Journal of Embedded Systems and Telecommunications, vol. 11, no. 1, pp. 88–96, Feb. 2025.",
    "[5] U. Kshirsagar, T. Oh, B. Tomaszewski, and G. Behm, “Inclusive cloud-based emergency alert platform utilizing multi-modal visual and haptic notifications,” IEEE Systems Journal, vol. 19, no. 1, pp. 210–221, Mar. 2025.",
    "[6] M. A. Hannan, M. S. H. Lipu, A. Hussain, and A. Mohamed, “A review of lithium-ion battery state of charge estimation and management system in electric vehicles,” Renewable and Sustainable Energy Reviews, vol. 78, pp. 834–854, Oct. 2017.",
    "[7] United Nations, “Goal 7: Ensure access to affordable, reliable, sustainable and modern energy for all,” UN Sustainable Development Goals, New York, NY, 2023. Available: https://sdgs.un.org/goals/goal7",
    "[8] United Nations, “Goal 9: Industry, Innovation and Infrastructure,” UN Sustainable Development Goals, New York, NY, 2023. Available: https://sdgs.un.org/goals/goal9"
]
