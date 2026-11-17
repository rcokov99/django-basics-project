"""Custom template filters for displaying doctor ratings."""
from django import template

register = template.Library()


@register.filter
def stars(rating):
    """Convert an average rating into a string of filled and empty stars.
    Returns 'No reviews yet' if the rating is none, zero or not a number.
    """
    if rating is None:
        return "No reviews yet"

    try:
        numeric_rating = float(rating)
    except (ValueError, TypeError):
        return "No reviews yet"

    if numeric_rating <= 0:
        return "No reviews yet"

    rounded = int(numeric_rating+0.5)
    rounded = max(1, min(5, rounded))

    filled = "★" * rounded
    empty = "☆" * (5 - rounded)

    return f"{filled}{empty}"
