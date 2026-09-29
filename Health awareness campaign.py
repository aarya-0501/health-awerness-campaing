import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="HealthWise Connect — Community Health Awareness",
    page_icon="🩺",
    layout="centered",
)

# --- INITIALIZE SESSION STATE ---
if "current_user" not in st.session_state:
  st.session_state["current_user"] = None
if "active_screen" not in st.session_state:
  st.session_state["active_screen"] = "home"
if "chat_messages" not in st.session_state:
  st.session_state["chat_messages"] = []
if "health_tracker" not in st.session_state:
  st.session_state["health_tracker"] = {
      "water": 0,
      "exercise": 0,
      "sleep": 0,
      "mood": 3,
      "steps": 0,
  }
if "surveys" not in st.session_state:
  st.session_state["surveys"] = []
if "camp_reports" not in st.session_state:
  st.session_state["camp_reports"] = []


# ==========================================
# 1. LOGIN / AUTHENTICATION SCREEN
# ==========================================
if st.session_state["current_user"] is None:
  st.title("🩺 HealthWise Connect")
  st.caption("Community health awareness • Daily wellness • Simple guidance")
  st.markdown("---")

  st.subheader("A healthier community starts with awareness.")
  st.write(
      "Explore health information, track daily habits, check basic health"
      " values and access helpful tools in one simple place."
  )

  role_choice = st.radio(
      "Select Login Role", ["👥 Public User", "🛡️ Admin"], horizontal=True
  )

  with st.form("login_form"):
    if "Admin" in role_choice:
      default_email = "admin@health.org"
      default_pass = "admin123"
    else:
      default_email = "user@example.com"
      default_pass = "user123"

    email = st.text_input("Email Address", value=default_email)
    password = st.text_input("Password", type="password", value=default_pass)

    submitted = st.form_submit_button("Sign In")
    if submitted:
      if "Admin" in role_choice and email == "admin@health.org" and password == "admin123":
        st.session_state["current_user"] = {
            "email": email,
            "name": "Admin Officer",
            "role": "admin",
        }
        st.session_state["active_screen"] = "home"
        st.success("Logged in as Admin successfully!")
        st.rerun()
      elif "Public" in role_choice:
        st.session_state["current_user"] = {
            "email": email,
            "name": email.split("@")[0],
            "role": "public",
        }
        st.session_state["active_screen"] = "home"
        st.success("Logged in successfully!")
        st.rerun()
      else:
        st.error("Invalid credentials. Please check or use demo values.")

  if st.button("Continue as Guest User →"):
    st.session_state["current_user"] = {
        "email": "guest",
        "name": "Guest",
        "role": "guest",
    }
    st.session_state["active_screen"] = "home"
    st.rerun()

# ==========================================
# MAIN APP (LOGGED-IN EXPERIENCE)
# ==========================================
else:
  user = st.session_state["current_user"]

  # Top Bar Info & Logout
  st.sidebar.markdown(f"**Signed in as:** {user['name']} ({user['role'].upper()})")
  if st.sidebar.button("Logout / Switch Account"):
    st.session_state["current_user"] = None
    st.session_state["active_screen"] = "login"
    st.rerun()

  st.sidebar.markdown("---")
  st.sidebar.subheader("Navigation")

  options_list = [
      "Home",
      "My Health Dashboard",
      "Lifestyle Self-Assessment",
      "Basic Health Checkup",
      "Health Camp Mode",
      "Community Health Survey",
      "Awareness Library",
      "Daily Tracker & Steps",
      "Emergency & Hospitals",
      "Health Chatbot",
  ]
  if user["role"] == "admin":
    options_list.append("Admin Control Panel")

  screen = st.sidebar.radio("Go to section", options_list)

  screen_mapping = {
      "Home": "home",
      "My Health Dashboard": "dashboard",
      "Lifestyle Self-Assessment": "quiz",
      "Basic Health Checkup": "checkup",
      "Health Camp Mode": "camp",
      "Community Health Survey": "survey",
      "Awareness Library": "library",
      "Daily Tracker & Steps": "tracker",
      "Emergency & Hospitals": "emergency",
      "Health Chatbot": "chat",
      "Admin Control Panel": "admin",
  }

  current_view = screen_mapping.get(screen, "home")

  # ------------------------------------------
  # HOME SCREEN
  # ------------------------------------------
  if current_view == "home":
    st.title("HealthWise Connect")
    st.caption("Community Health Awareness Portal")

    if user["role"] == "admin":
      st.info("🛡️ Administrator Access active. You can review analytics in the Admin Panel.")

    st.write("A simple health-awareness space you can share with your community.")
    if st.button("↗ Share App Link"):
      st.toast("App link ready to share!")

    st.markdown("### Explore Features")

    col1, col2 = st.columns(2)
    with col1:
      if st.button("📊 My Health Dashboard", use_container_width=True):
        st.session_state["active_screen"] = "dashboard"
        st.rerun()
      if st.button("🩺 Basic Health Checkup", use_container_width=True):
        st.session_state["active_screen"] = "checkup"
        st.rerun()
      if st.button("📝 Community Health Survey", use_container_width=True):
        st.session_state["active_screen"] = "survey"
        st.rerun()
      if st.button("💧 Daily Habit Tracker", use_container_width=True):
        st.session_state["active_screen"] = "tracker"
        st.rerun()
      if st.button("💬 Health Chatbot", use_container_width=True):
        st.session_state["active_screen"] = "chat"
        st.rerun()

    with col2:
      if st.button("📋 Lifestyle Assessment", use_container_width=True):
        st.session_state["active_screen"] = "quiz"
        st.rerun()
      if st.button("🏥 Health Camp Mode", use_container_width=True):
        st.session_state["active_screen"] = "camp"
        st.rerun()
      if st.button("📚 Awareness Library", use_container_width=True):
        st.session_state["active_screen"] = "library"
        st.rerun()
      if st.button("🚨 Emergency & Hospitals", use_container_width=True):
        st.session_state["active_screen"] = "emergency"
        st.rerun()

  # ------------------------------------------
  # DASHBOARD SCREEN
  # ------------------------------------------
  elif current_view == "dashboard":
    st.header("📊 My Health Dashboard")
    st.write("Your latest health values and daily habits at a glance.")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("BMI", st.session_state.get("last_bmi", "—"))
    m2.metric("Blood Pressure", st.session_state.get("last_bp", "—"))
    m3.metric("Pulse", st.session_state.get("last_pulse", "—"))
    m4.metric("Health Score", st.session_state.get("last_score", "—"))

    st.markdown("### Today's Tracking Summary")
    tracker = st.session_state["health_tracker"]
    st.write(f"💧 **Water Consumed:** {tracker['water']} glasses")
    st.write(f"🏃 **Exercise:** {tracker['exercise']} minutes")
    st.write(f"😴 **Sleep:** {tracker['sleep']} hours")
    st.write(f"🙂 **Mood Score:** {tracker['mood']} / 5")

  # ------------------------------------------
  # LIFESTYLE SELF-ASSESSMENT QUIZ
  # ------------------------------------------
  elif current_view == "quiz":
    st.header("📋 Lifestyle Self-Assessment")
    st.write("Answer 7 quick questions about your daily habits to get a health score and personalized tips.")

    with st.form("quiz_form"):
      q1 = st.radio("1. How many servings of fruits or vegetables do you eat in a typical day?", ["Rarely any (0 pts)", "1 serving (1 pt)", "2-3 servings (2 pts)", "4 or more servings (3 pts)"])
      q2 = st.radio("2. How many days a week do you get at least 30 minutes of physical activity?", ["0 days (0 pts)", "1-2 days (1 pt)", "3-4 days (2 pts)", "5+ days (3 pts)"])
      q3 = st.radio("3. On average, how many hours do you sleep per night?", ["Less than 5 hours (0 pts)", "5-6 hours (1 pt)", "6-7 hours (2 pts)", "7-9 hours (3 pts)"])
      q4 = st.radio("4. How many glasses of water do you drink daily?", ["1-2 glasses (0 pts)", "3-4 glasses (1 pt)", "5-6 glasses (2 pts)", "7+ glasses (3 pts)"])
      q5 = st.radio("5. How often do you wash your hands before meals or after using the toilet?", ["Rarely (0 pts)", "Sometimes (1 pt)", "Most of the time (2 pts)", "Always (3 pts)"])
      q6 = st.radio("6. How often do you feel stressed, anxious, or overwhelmed?", ["Almost every day (0 pts)", "A few times a week (1 pt)", "Occasionally (2 pts)", "Rarely (3 pts)"])
      q7 = st.radio("7. When was your last general health checkup?", ["Never / cannot recall (0 pts)", "More than 2 years ago (1 pt)", "Within the last year (2 pts)", "Within the last 6 months (3 pts)"])

      submitted_quiz = st.form_submit_button("Calculate Score")
      if submitted_quiz:
        total_score = sum([int(q[q.find("(")+1:q.find(" pt")]) for q in [q1, q2, q3, q4, q5, q6, q7]])
        pct = int((total_score / 21) * 100)
        st.session_state["last_score"] = f"{pct}%"

        st.success(f"Your Wellness Score: {pct}% ({total_score} / 21 points)")
        if pct >= 80:
          st.markdown("🟢 **Status:** Excellent lifestyle habits!")
        elif pct >= 60:
          st.markdown("🟡 **Status:** Good — room to improve.")
        else:
          st.markdown("🟠 **Status:** Needs attention — prioritize adjustments.")

  # ------------------------------------------
  # BASIC HEALTH CHECKUP
  # ------------------------------------------
  elif current_view == "checkup":
    st.header("🩺 Basic Health Checkup")
    st.write("Just like at a health camp — enter your vitals below.")

    with st.form("checkup_form"):
      ck_name = st.text_input("Your Full Name")
      col_a, col_b = st.columns(2)
      with col_a:
        ck_age = st.number_input("Age", min_value=1, max_value=120, value=28)
        ck_height = st.number_input("Height (cm)", min_value=50.0, value=170.0)
        ck_sys = st.number_input("Systolic BP", min_value=50, value=120)
        ck_sugar = st.number_input("Blood Sugar (mg/dL)", value=95)
      with col_b:
        ck_gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        ck_weight = st.number_input("Weight (kg)", min_value=10.0, value=68.0)
        ck_dia = st.number_input("Diastolic BP", min_value=30, value=80)
        ck_pulse = st.number_input("Pulse Rate (bpm)", min_value=30, value=72)

      ck_submit = st.form_submit_button("Get My Results")
      if ck_submit:
        h_m = ck_height / 100
        bmi = round(ck_weight / (h_m * h_m), 1)
        st.session_state["last_bmi"] = str(bmi)
        st.session_state["last_bp"] = f"{ck_sys}/{ck_dia}"
        st.session_state["last_pulse"] = str(ck_pulse)

        st.markdown("---")
        st.subheader("Checkup Evaluation Summary")
        st.write(f"**Participant:** {ck_name} | {ck_age} yrs | {ck_gender}")
        st.metric("Calculated BMI", bmi)
        st.metric("Blood Pressure", f"{ck_sys}/{ck_dia} mmHg")
        st.metric("Pulse Rate", f"{ck_pulse} bpm")
        st.info("General awareness info based on standard reference ranges, not a medical diagnosis.")

  # ------------------------------------------
  # HEALTH CAMP MODE
  # ------------------------------------------
  elif current_view == "camp":
    st.header("🏥 Health Camp Mode")
    st.write("Quickly record participant information during your campaign.")

    with st.form("camp_form"):
      c_name = st.text_input("Participant Full Name")
      c_age = st.number_input("Participant Age", min_value=1, value=40)
      c_sys = st.number_input("Camp BP Systolic", value=120)
      c_dia = st.number_input("Camp BP Diastolic", value=80)
      c_sugar = st.number_input("Camp Blood Sugar", value=110)

      c_submit = st.form_submit_button("Generate Camp Report")
      if c_submit:
        report = {"name": c_name, "age": c_age, "bp": f"{c_sys}/{c_dia}", "sugar": c_sugar}
        st.session_state["camp_reports"].append(report)
        st.success(f"Report generated successfully for {c_name}!")
        st.json(report)

  # ------------------------------------------
  # COMMUNITY SURVEY
  # ------------------------------------------
  elif current_view == "survey":
    st.header("📝 Community Health Survey")
    st.write("Use this during your awareness campaign to collect simple responses.")

    with st.form("survey_form"):
      s_age = st.selectbox("Age Group", ["Under 18", "18–30", "31–50", "51+"])
      s_exercise = st.selectbox("How often do you exercise?", ["Rarely", "1–2 days/week", "3–4 days/week", "5+ days/week"])
      s_bp = st.selectbox("Do you know your blood pressure?", ["Yes", "No", "Not sure"])
      s_topic = st.selectbox("Which topic would you like to learn about?", ["Nutrition", "Exercise", "Hygiene", "Mental wellbeing", "Diabetes", "Blood pressure"])

      s_submit = st.form_submit_button("Save Survey Response")
      if s_submit:
        st.session_state["surveys"].append({"age": s_age, "exercise": s_exercise, "bp": s_bp, "topic": s_topic})
        st.success(f"Survey response recorded! Total collected: {len(st.session_state['surveys'])}")

  # ------------------------------------------
  # AWARENESS LIBRARY
  # ------------------------------------------
  elif current_view == "library":
    st.header("📚 Health Awareness Library")
    st.write("Simple information for campaign participants.")

    articles = [
        {"cat": "Nutrition", "title": "Balanced Daily Diet", "text": "Eat vegetables, fruits, whole grains and safe water."},
        {"cat": "Exercise", "title": "Daily Movement", "text": "Walking 30 minutes daily improves cardiovascular health."},
        {"cat": "Hygiene", "title": "Hand Hygiene Rules", "text": "Wash hands for 20+ seconds with soap."},
        {"cat": "Wellbeing", "title": "Stress Control", "text": "Get 7-8 hours sleep and practice routine breathing."}
    ]

    filter_cat = st.selectbox("Filter Category", ["All", "Nutrition", "Exercise", "Hygiene", "Wellbeing"])
    for art in articles:
      if filter_cat == "All" or art["cat"] == filter_cat:
        with st.container():
          st.subheader(art["title"])
          st.write(art["text"])
          st.markdown("---")

  # ------------------------------------------
  # DAILY TRACKER & STEPS
  # ------------------------------------------
  elif current_view == "tracker":
    st.header("💧 Daily Health Tracker & Steps")
    st.write("Small daily habits can help build health awareness.")

    tr = st.session_state["health_tracker"]
    tr["water"] = st.number_input("Water (glasses today)", value=tr["water"], min_value=0)
    tr["exercise"] = st.number_input("Exercise (minutes today)", value=tr["exercise"], min_value=0)
    tr["sleep"] = st.number_input("Sleep (hours last night)", value=tr["sleep"], min_value=0.0, max_value=24.0)
    tr["mood"] = st.slider("Mood Wellbeing Check (1 to 5)", min_value=1, max_value=5, value=tr["mood"])
    tr["steps"] = st.number_input("Steps Tracked Today", value=tr["steps"], min_value=0)

    if st.button("Save Today's Habits"):
      st.success("Habits saved successfully!")

  # ------------------------------------------
  # EMERGENCY & HOSPITALS
  # ------------------------------------------
  elif current_view == "emergency":
    st.header("🚨 Emergency & Care")
    st.write("GPS location, nearby hospitals, quick call & directions.")

    st.markdown("### 📍 Location & Nearby Hospitals")
    st.write("Demo Location: Central District (Lat: 28.6139° N, Lng: 77.2090° E)")

    hospitals = [
        {"name": "City General Hospital", "dist": "1.2 km", "phone": "011-23456789"},
        {"name": "Community Care Health Center", "dist": "2.8 km", "phone": "011-87654321"},
        {"name": "St. Jude Emergency Clinic", "dist": "4.1 km", "phone": "011-11223344"}
    ]

    for h in hospitals:
      st.markdown(f"**{h['name']}** — *{h['dist']} away*")
      st.markdown(f"📞 Contact: `{h['phone']}`")
      st.markdown("---")

    st.markdown("### 🚨 Emergency Helplines")
    st.warning("🚑 Ambulance / Emergency Dispatch: **108**")
    st.warning("📞 Universal Emergency Help: **112**")
    st.warning("🧠 Mental Health Counselling (Tele-MANAS): **14416**")

  # ------------------------------------------
  # HEALTH CHATBOT
  # ------------------------------------------
  elif current_view == "chat":
    st.header("💬 Health Chatbot")
    st.write("Ask health questions, get instant offline guidance.")

    for msg in st.session_state["chat_messages"]:
      with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

    if prompt := st.chat_input("Ask about symptoms, diet, hydration, exercise..."):
      st.session_state["chat_messages"].append({"role": "user", "content": prompt})
      with st.chat_message("user"):
        st.markdown(prompt)

      lower = prompt.lower()
      if any(k in lower for k in ["fever", "temperature", "chills"]):
        reply = "Rest, stay hydrated, and monitor temperature. See a doctor if above 102°F or lasting > 2 days."
      elif any(k in lower for k in ["cough", "cold", "sore throat"]):
        reply = "Rest and sip warm fluids. See a doctor if cough lasts over 10 days."
      elif any(k in lower for k in ["dehydrat", "water", "thirst"]):
        reply = "Drink water or ORS solutions. Look for clear/light yellow urine as a sign of hydration."
      elif any(k in lower for k in ["exercise", "walk", "step", "fitness"]):
        reply = "Aim for 30 minutes of physical activity 5 days a week."
      elif any(k in lower for k in ["stress", "anxiety", "mind"]):
        reply = "Take short breathing breaks and ensure 7-8 hours of sleep."
      else:
        reply = "I'm your offline assistant! Try asking about fever, cough, hydration, exercise, or stress management."

      st.session_state["chat_messages"].append({"role": "assistant", "content": reply})
      with st.chat_message("assistant"):
        st.markdown(reply)

  # ------------------------------------------
  # ADMIN CONTROL PANEL
  # ------------------------------------------
  elif current_view == "admin":
    if user["role"] != "admin":
      st.error("Access Denied: Admin rights required.")
    else:
      st.header("🛡️ Admin Control Center")
      st.subheader("Campaign Analytics & Settings")

      total_surveys = len(st.session_state["surveys"])
      total_camps = len(st.session_state["camp_reports"])

      col_c, col_d = st.columns(2)
      col_c.metric("Total Surveys Collected", total_surveys)
      col_d.metric("Camp Checks Recorded", total_camps)

      st.markdown("### Community Insights")
      if total_surveys > 0:
        topics_count = {}
        for s in st.session_state["surveys"]:
          topics_count[s["topic"]] = topics_count.get(s["topic"], 0) + 1
        top_topic = max(topics_count, key=topics_count.get)
        st.write(f"**Top Selected Topic:** {top_topic}")
      else:
        st.write("No survey submissions recorded yet.")

      if st.button("⚠️ Reset Campaign Storage"):
        st.session_state["surveys"] = []
        st.session_state["camp_reports"] = []
        st.success("Campaign data storage has been reset.")

*This is for informational purposes only. For medical advice or diagnosis, consult a professional.*
