import streamlit as st

# Session state initialization for login and navigation
if "logged_in" not in st.session_state:
  st.session_state.logged_in = False
if "topic" not in st.session_state:
  st.session_state.topic = None
if "messages" not in st.session_state:
  st.session_state.messages = []

# --- 1. LOGIN PAGE ---
if not st.session_state.logged_in:
  st.title("🔐 Health Awareness Campaign - Login")
  st.write("Please enter your credentials to access the portal.")

  username = st.text_input("Username")
  password = st.text_input("Password", type="password")

  if st.button("Login"):
    # Simple hardcoded credentials check (Change as needed)
    if username == "admin" and password == "health123":
      st.session_state.logged_in = True
      st.success("Login successful!")
      st.rerun()
    else:
      st.error("Invalid username or password (Try admin / health123)")

# --- 2. MAIN APP DASHBOARD ---
else:
  st.sidebar.title("Navigation")
  app_mode = st.sidebar.radio("Choose a section", ["Campaign Hub", "Health AI Chatbot"])

  if st.sidebar.button("Log Out"):
    st.session_state.logged_in = False
    st.session_state.topic = None
    st.rerun()

  # --- SECTION A: CAMPAIGN HUB ---
  if app_mode == "Campaign Hub":
    information = {
        "Healthy Diet": (
            "Eat fruits, vegetables, whole grains and other nutritious foods."
        ),
        "Exercise & Fitness": (
            "Regular physical activity helps maintain overall fitness and"
            " well-being."
        ),
        "Mental Health": (
            "Take adequate rest, stay connected with others and seek professional"
            " help when needed."
        ),
        "Disease Prevention": (
            "Maintain hygiene, follow recommended preventive measures and get"
            " appropriate checkups."
        ),
        "Personal Hygiene": (
            "Wash your hands regularly and maintain good personal cleanliness."
        ),
        "Water & Hydration": (
            "Drink adequate fluids according to your individual needs and"
            " circumstances."
        ),
        "Emergency Information": (
            "In an emergency, contact your local emergency medical service."
        ),
    }

    if st.session_state.topic is None:
      st.title("HEALTH AWARENESS CAMPAIGN")
      st.write("Select a topic below to learn more:")

      for topic in information.keys():
        if st.button(topic, use_container_width=True):
          st.session_state.topic = topic
          st.rerun()

    else:
      st.title(st.session_state.topic)
      st.write(information[st.session_state.topic])

      if st.button("← Back"):
        st.session_state.topic = None
        st.rerun()

  # --- SECTION B: HEALTH CHATBOT ---
  elif app_mode == "Health AI Chatbot":
    st.title("💬 Health Assistant Chatbot")
    st.write(
        "Ask me anything regarding general wellness, nutrition, or campaign"
        " topics!"
    )

    # Display chat history
    for message in st.session_state.messages:
      with st.chat_message(message["role"]):
        st.markdown(message["content"])

    # Handle user input
    if prompt := st.chat_input("Type your health question here..."):
      st.session_state.messages.append({"role": "user", "content": prompt})
      with st.chat_message("user"):
        st.markdown(prompt)

      # Basic rule-based smart response generation
      response = (
          "That's a great question! For tailored health guidance, remember to"
          " maintain healthy habits, stay hydrated, and consult a professional"
          " if you have specific symptoms."
      )

      query = prompt.lower()
      if "diet" in query or "food" in query or "eat" in query:
        response = (
            "Eating a balanced diet rich in leafy greens, proteins, and whole"
            " grains supports long-term energy and immunity."
        )
      elif "exercise" in query or "workout" in query or "fitness" in query:
        response = (
            "Aim for at least 30 minutes of moderate physical activity most days"
            " of the week."
        )
      elif "water" in query or "hydrate" in query:
        response = (
            "Staying hydrated helps regulate body temperature and maintain skin"
            " and organ health. Try drinking 8 glasses a day."
        )
      elif "mental" in query or "stress" in query or "sleep" in query:
        response = (
            "Prioritizing 7-8 hours of sleep and practicing mindfulness can"
            " significantly improve mental wellness."
        )

      st.session_state.messages.append(
          {"role": "assistant", "content": response}
      )
      with st.chat_message("assistant"):
        st.markdown(response)
