import streamlit as st

# This must be the absolute first Streamlit command in your script
st.set_page_config(
    page_title="Health Awareness Campaign", page_layout="centered"
)

# Initialize session state for navigation
if "topic" not in st.session_state:
  st.session_state.topic = None

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
