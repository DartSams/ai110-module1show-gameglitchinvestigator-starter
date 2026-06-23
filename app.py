import random
import streamlit as st
# FIX: Refactored core logic into logic_utils.py using AI-assisted move
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score


ATTEMPT_LIMIT_MAP = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}

_HINT_MESSAGES = {
    "Win": "🎉 Correct!",
    "Too High": "📉 Go LOWER!",
    "Too Low": "📈 Go HIGHER!",
}


def start_new_game(difficulty: str):
    low, high = get_range_for_difficulty(difficulty)
    # FIX: Previously new game always used 1–100; now respects selected difficulty range
    st.session_state.secret = random.randint(low, high)
    # FIX: Reset all state values so game does not stay stuck after win/loss
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.last_difficulty = difficulty


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("Guessing game with consistent rules and stable state.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit = ATTEMPT_LIMIT_MAP[difficulty]
low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# FIX: Ensure game resets automatically when difficulty changes to prevent out-of-range secret
if "last_difficulty" not in st.session_state:
    start_new_game(difficulty)
else:
    if st.session_state.last_difficulty != difficulty:
        start_new_game(difficulty)

attempts_used = st.session_state.attempts
attempts_left = attempt_limit - attempts_used

st.subheader("Make a guess")

# FIX: Previously hardcoded 1–100; now dynamically reflects selected difficulty range
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempts_left}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts used:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

colA, colB = st.columns(2)
with colA:
    new_game = st.button("New Game 🔁")
with colB:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    # FIX: Previously did not fully reset state; now calls centralized reset function
    start_new_game(difficulty)
    st.success("New game started.")
    st.rerun()

# FIX: Prevent further guessing after win/loss but allow proper reset
if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success(
            f"You already won! The secret was {st.session_state.secret}. "
            f"Final score: {st.session_state.score}"
        )
    else:
        st.error(
            f"Game over. The secret was {st.session_state.secret}. "
            f"Score: {st.session_state.score}"
        )
    st.stop()

# FIX: Switched to form so pressing Enter submits instead of silently rerunning
with st.form("guess_form"):
    raw_guess = st.text_input("Enter your guess:")
    submit = st.form_submit_button("Submit Guess 🚀")

if submit:
    if attempts_left <= 0:
        st.session_state.status = "lost"
        st.error(
            f"Out of attempts! The secret was {st.session_state.secret}. "
            f"Score: {st.session_state.score}"
        )
        st.stop()

    ok, guess_int, err = parse_guess(raw_guess, low, high)

    # FIX: Attempts now increment consistently once per submission
    st.session_state.attempts += 1

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        # FIX: check_guess now lives in logic_utils; returns outcome string (no tuple)
        outcome = check_guess(guess_int, st.session_state.secret)
        message = _HINT_MESSAGES[outcome]

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

st.divider()
st.write("Guess history:", st.session_state.history)
st.caption("Fixed version with stable secret, correct hints, proper resets, and consistent range handling.")