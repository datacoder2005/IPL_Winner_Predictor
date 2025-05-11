import streamlit as st
import pandas as pd
import joblib


# Load model
pipe = joblib.load("model.pkl") 
score_pipe = joblib.load("model_1.pkl")

import base64

def add_bg_local(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: top center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )



teams = ['Kolkata Knight Riders', 'Chennai Super Kings', 'Punjab Kings',
         'Rajasthan Royals', 'Mumbai Indians', 'Delhi Capitals',
         'Royal Challengers Bengaluru', 'Sunrisers Hyderabad',
         'Lucknow Super Giants', 'Gujarat Titans']

cities = ['Mumbai', 'Kolkata', 'Hyderabad', 'Chennai', 'Bengaluru', 'Delhi', 
          'Ahmedabad', 'Pune', 'Jaipur', 'Mohali', 'Lucknow', 'Abu Dhabi', 
          'Sharjah', 'Visakhapatnam', 'Dharamsala']

# Session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = "landing"

# 🔹 Landing Page
def landing_page():
    add_bg_local("pic3.jpg")

    st.markdown("<h1 style='text-align: center; color: #000000;'>🏏 IPL Match Predictor App</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px; color: #000000;'>Welcome to the ultimate IPL prediction experience! Choose a tool below to begin.</p>", unsafe_allow_html=True)

    st.markdown("Click below to start predicting match outcomes.")
    if st.button("🔮 Go to Predictor"):
        st.session_state.page = "predictor"
    if st.button("📊 IPL 2008–2024 Report Dashboard"):
        st.session_state.page = "dashboard"
    if st.button("🎯 First Innings Score Predictor"):
        st.session_state.page = "first_innings"


def dashboard_page():
    add_bg_local("pic3.jpg")
    st.title("📊 IPL 2008–2024 Report")
    st.markdown("""<iframe title="Ipl dash" width="800" height="499" src="https://app.powerbi.com/view?r=eyJrIjoiZmMwZDk1MzMtOWE2Ni00NzljLTkwYTYtZWNkNTBjYzk3OTg1IiwidCI6ImIxNzAzMTg1LTJkOTktNDBlNS04NmUxLTNhMjIzMTJmYWY3NiJ9&pageName=0800b03bdec7a499e008" frameborder="0" allowFullScreen="true"></iframe>""",unsafe_allow_html=True)
    if st.button("⬅️ Back to Landing Page"):
       st.session_state.page = "landing"

def first_innings_page():
    add_bg_local("pic3.jpg")
    st.title("📈 First Innings Score Predictor")

    batting_team = st.selectbox("Select Batting Team", sorted(teams))
    bowling_team = st.selectbox("Select Bowling Team", [t for t in teams if t != batting_team])
    city = st.selectbox("Match City", sorted(cities))
    current_score = st.number_input("Current Score", min_value=0)
    overs = st.number_input("Overs Completed", min_value=0.0, max_value=20.0, step=0.1)
    runs_last_30 = st.number_input("Runs Last 5 Overs", min_value=0)
    wickets_lost = st.number_input("Wickets Lost", min_value=0, max_value=10)

    # Derived features
    a = int(overs)
    b = int(round((overs - a) * 10))
    balls_bowled = (a * 6) + b
    balls_left = 120 - balls_bowled
    crr = (current_score * 6 / balls_bowled) if balls_bowled > 0 else 0
    wickets_remaining = 10 - wickets_lost

    # st.markdown(f"🧮 Balls Left: **{balls_left}**")
    # st.markdown(f"📉 Calculated CRR: **{crr:.2f}**")

    if st.button("Predict First Innings Score"):
        input_df = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'city': [city],
            'current_Score': [current_score],
            'balls_left': [balls_left],
            'runs_last_30': [runs_last_30],
            'wickets_remaining': [wickets_remaining],
            'crr': [crr]
        })

        # Load the model
        first_innings_model = joblib.load("model_1.pkl")
        predicted_score = int(first_innings_model.predict(input_df)[0])

        st.markdown(
    f"""
    <div style='background-color: #d4edda; padding: 10px; border-radius: 5px; color: #155724; font-size: 24px; font-weight: bold;'>
        🔮 Predicted First Innings Score: {predicted_score}
    </div>
    """,
    unsafe_allow_html=True
)


        # st.write("📥 Input Data:", input_df)

    if st.button("⬅️ Back to Landing Page"):
        st.session_state.page = "landing"


# 🔹 Predictor Page
def predictor_page():
    st.title("🏏 IPL Match Winner Predictor")

    batting_team = st.selectbox("Select Batting Team", sorted(teams))
    bowling_team = st.selectbox("Select Bowling Team", [t for t in teams if t != batting_team])
    city = st.selectbox("Match City", sorted(cities))
    target = st.number_input("Target Score", min_value=1)
    score = st.number_input("Current Score", min_value=0)
    overs = st.number_input("Overs Completed", min_value=0.0, max_value=20.0, step=0.1)
    wickets = st.number_input("Wickets Lost", min_value=0, max_value=10)

    if st.button("Predict Winner"):
        runs_left = target - score
        a = int(overs)
        b = int(round((overs - a) * 10))
        balls_left = 120 - (6 * a + b)
        wickets_remaining = 10 - wickets
        crr = ((score*6) / (6 * a + b)) if overs > 0 else 0
        rrr = runs_left / (balls_left / 6) if balls_left > 0 else 0

        input_df = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'city': [city],
            'runs_left': [runs_left],
            'balls_left': [balls_left],
            'wickets_remaining': [wickets_remaining],
            'target_runs': [target],
            'crr': [crr],
            'rrr': [rrr]
        })

        proba = pipe.predict_proba(input_df)[0]
        batting_win_prob = round(proba[1] * 100, 2)
        bowling_win_prob = round(proba[0] * 100, 2)

        st.markdown(
            """
            <style>
            .overlay-box {
                background-color: rgba(0, 0, 0, 0.6);
                padding: 20px;
                border-radius: 15px;
                }
                </style>
                """,
                unsafe_allow_html=True
        )
        st.markdown('<div class="overlay-box">', unsafe_allow_html=True)
        st.markdown("## 📊 Win Probabilities")
        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"🧠 <strong style='color:#FFD700'>{batting_team}</strong>", unsafe_allow_html=True)
            st.progress(batting_win_prob / 100)
            st.markdown(f"🎯 Win Chance: **{batting_win_prob:.2f}%**")
            
        with col2:
            st.markdown(f"<p style='text-align:right;color:#FF69B4'><strong>{bowling_team}</strong></p>", unsafe_allow_html=True)
            st.progress(bowling_win_prob / 100)
            st.markdown(f"<p style='text-align:right'>🎯 Win Chance: <strong>{bowling_win_prob:.2f}%</strong></p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    



        # st.write("🔍 Input Data:", input_df)
        # st.write("🔢 Raw Probabilities:", proba)


    if st.button("⬅️ Back to Landing Page"):
       st.session_state.page = "landing"



# 🔹 Display correct page
if st.session_state.page == "landing":
    landing_page()
elif st.session_state.page == "predictor":
    predictor_page()
elif st.session_state.page == "dashboard":
    dashboard_page()
elif st.session_state.page == "first_innings":
    first_innings_page()
