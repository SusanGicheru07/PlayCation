import math

def calculate_singing_points(duration_sec, loudness, pitch_variance):
    """
    Calculate singing points based on:
    - Duration of singing
    - Loudness (enthusiasm)
    - Pitch variance (creativity)

    Returns a total points value.
    """

    # Normalize values to keep scoring reasonable
    duration_score = min(duration_sec / 10, 10) * 10        # Max 100 points
    loudness_score = max(min((loudness + 60) / 2, 100), 0)  # Range -60 dB to 0 dB → 0-100 points
    creativity_score = min(pitch_variance / 50, 100)         # Based on pitch variation

    # Weighted total (you can tweak weights)
    total_points = (
        (0.4 * duration_score) +
        (0.3 * loudness_score) +
        (0.3 * creativity_score)
    )

    return round(total_points, 2)
