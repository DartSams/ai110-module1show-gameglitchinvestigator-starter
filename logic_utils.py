def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str, low: int = 1, high: int = 100):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
<<<<<<< HEAD
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    raw = raw.strip()

    try:
        if "." in raw:
            f = float(raw)
            if not f.is_integer():
                return False, None, "Enter a whole number."
            value = int(f)
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    if value < low or value > high:
        return False, None, f"Your guess must be between {low} and {high}."

    return True, value, None
=======
    if raw is None:
        return False, None, "Enter a guess."
>>>>>>> 84b8131b2702ea037df39988e84cf5292d82f888

    if raw == "":
        return False, None, "Enter a guess."

<<<<<<< HEAD
def check_guess(guess: int, secret: int) -> str:
=======
    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None

# FIX: moved function to logic_utils.py and flipped the messages, because prior it was saying if the guess was too high, suggest going higher (that's backwards)
def check_guess(guess, secret):
>>>>>>> 84b8131b2702ea037df39988e84cf5292d82f888
    """
    Compare guess to secret and return the outcome string.

    Returns: "Win", "Too High", or "Too Low"
    """
    if guess == secret:
<<<<<<< HEAD
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"
=======
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"
>>>>>>> 84b8131b2702ea037df39988e84cf5292d82f888


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
<<<<<<< HEAD
        points = 100 - 10 * attempt_number
=======
        points = 100 - 10 * (attempt_number + 1)
>>>>>>> 84b8131b2702ea037df39988e84cf5292d82f888
        if points < 10:
            points = 10
        return current_score + points

<<<<<<< HEAD
    if outcome in ("Too High", "Too Low"):
=======
    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
>>>>>>> 84b8131b2702ea037df39988e84cf5292d82f888
        return current_score - 5

    return current_score