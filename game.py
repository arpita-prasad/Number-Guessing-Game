import streamlit as st
import random

st.set_page_config(page_title="Number Guessing Game", page_icon="🎲", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(120deg, #f8fafc 0%, #e0eafc 50%, #f9e7fe 100%);
        min-height: 100vh;
        background-attachment: fixed;
    }
    .main-title {font-size:2.5em; font-weight:700; color:#3a3a3a; margin-bottom:0.1em;}
    .subtitle {font-size:1.15em; color:#666; margin-bottom:1.5em;}
    .diff-btn {
        padding:0.5em 1.5em;
        border-radius:1.5em;
        border:none;
        font-size:1.1em;
        margin:0 0.5em 0.7em 0.5em;
        background-color:#f4f4f4;
        color:#333;
        transition:background 0.2s;
    }
    .diff-btn-selected {
        background-color:#3777f0;
        color:white;
        font-weight:600;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎲 Number Guessing Game</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Guess the secret number between <b>1</b> and <b>100</b>. Select your difficulty and start playing!</div>', unsafe_allow_html=True)

# Session State
if "difficulty" not in st.session_state:
    st.session_state.difficulty = None
if "max_attempts" not in st.session_state:
    st.session_state.max_attempts = 10
if "secret_number" not in st.session_state:
    st.session_state.secret_number = None
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "game_active" not in st.session_state:
    st.session_state.game_active = False
if "message" not in st.session_state:
    st.session_state.message = ""

# Difficulty Selection
diffs = [("Easy", 10), ("Medium", 7), ("Hard", 5)]
diff_cols = st.columns(len(diffs))
for i, (label, attempts) in enumerate(diffs):
    btn_class = "diff-btn diff-btn-selected" if st.session_state.difficulty == label else "diff-btn"
    if diff_cols[i].button(label, key=label, help=f"{attempts} attempts", use_container_width=True):
        st.session_state.difficulty = label
        st.session_state.max_attempts = attempts
        st.session_state.secret_number = None
        st.session_state.attempts = 0
        st.session_state.game_active = False
        st.session_state.message = ""

# Start Game Button
if st.session_state.difficulty and not st.session_state.game_active:
    st.write(f"**Selected difficulty:** {st.session_state.difficulty} ({st.session_state.max_attempts} attempts)")
    if st.button("Start Game", type="primary"):
        st.session_state.secret_number = random.randint(1, 100)
        st.session_state.attempts = 0
        st.session_state.game_active = True
        st.session_state.message = ""

# Main Game
if st.session_state.game_active:
    st.write(f"**Attempts left:** {st.session_state.max_attempts - st.session_state.attempts}")
    guess = st.number_input("Enter your guess:", min_value=1, max_value=100, step=1, key="guess_input")
    if st.button("Guess"):
        st.session_state.attempts += 1
        if guess == st.session_state.secret_number:
            st.success(f"🎉 Correct! You guessed the number in {st.session_state.attempts} attempts.")
            st.session_state.game_active = False
        elif st.session_state.attempts >= st.session_state.max_attempts:
            st.error(f"❌ Game Over! The number was {st.session_state.secret_number}.")
            st.session_state.game_active = False
        elif guess < st.session_state.secret_number:
            st.info("Too low. Try a higher number.")
        else:
            st.info("Too high. Try a lower number.")

# Play Again
if st.session_state.difficulty and not st.session_state.game_active and st.session_state.secret_number is not None:
    if st.button("Play Again"):
        st.session_state.secret_number = random.randint(1, 100)
        st.session_state.attempts = 0
        st.session_state.game_active = True
        st.session_state.message = ""