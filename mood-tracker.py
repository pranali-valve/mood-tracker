from __future__ import annotations
import calendar
import csv
from datetime import date,datetime
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
DATA_FILE = Path(__file__).with_name("moods.csv")
IMAGE_FILE = Path(__file__).with_name("mood_calendar.png")

MOODS = {
    "happy": ("Happy", "#F9C74F"),
    "calm": ("Calm", "#90BE6D"),
    "sad": ("Sad", "#577590"),
    "angry": ("Angry", "#F94144"),
    "tired": ("Tired", "#9D4EDD"),
    "excited": ("Excited", "#F9844A"),
}


def read_moods() -> dict[str, str]:
    """Return saved moods as {YYYY-MM-DD: mood_key}."""
    if not DATA_FILE.exists():
        return {}

    with DATA_FILE.open("r", newline="", encoding="utf-8") as file:
        return {row["date"]: row["mood"] for row in csv.DictReader(file)}


def save_moods(moods: dict[str, str]) -> None:
    with DATA_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["date", "mood"])
        writer.writeheader()
        for day, mood in sorted(moods.items()):
            writer.writerow({"date": day, "mood": mood})


def add_mood() -> None:
    print("\nAvailable moods:")
    for key, (label, _) in MOODS.items():
        print(f"  {key:<8} {label}")

    entered_date = input("\nDate (YYYY-MM-DD, leave blank for today): ").strip()
    if not entered_date:
        entered_date = date.today().isoformat()
    try:
        datetime.strptime(entered_date, "%Y-%m-%d")
    except ValueError:
        print("Please use a real date in YYYY-MM-DD format.")
        return

    mood = input("Mood: ").strip().lower()
    if mood not in MOODS:
        print("That mood is not in the list. Please try again.")
        return

    moods = read_moods()
    moods[entered_date] = mood
    save_moods(moods)
    print(f"Saved {MOODS[mood][0]} for {entered_date}.")


def create_calendar(year: int, month: int) -> None:
    moods = read_moods()
    month_days = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]

    fig, axis = plt.subplots(figsize=(10, 7))
    fig.patch.set_facecolor("#FFF9F0")
    axis.set_facecolor("#FFF9F0")
    axis.set_xlim(0, 7)
    axis.set_ylim(0, len(month_days) + 0.8)
    axis.axis("off")
    axis.set_title(f"My Mood Calendar — {month_name} {year}", fontsize=20,
                   fontweight="bold", color="#3D405B", pad=20)

    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for column, weekday in enumerate(weekdays):
        axis.text(column + 0.5, len(month_days) + 0.25, weekday,
                  ha="center", va="center", fontsize=12, fontweight="bold",
                  color="#3D405B")

    for row, week in enumerate(month_days):
        y = len(month_days) - row - 1
        for column, day_number in enumerate(week):
            day_key = f"{year:04d}-{month:02d}-{day_number:02d}" if day_number else ""
            mood_key = moods.get(day_key)
            fill = MOODS[mood_key][1] if mood_key else "#FFFFFF"

            axis.add_patch(Rectangle((column + 0.04, y + 0.04), 0.92, 0.92,
                                     facecolor=fill, edgecolor="#E5E0D8",
                                     linewidth=1.2))
            if day_number:
                axis.text(column + 0.13, y + 0.82, str(day_number), fontsize=11,
                          color="#3D405B", ha="left", va="top")
            if mood_key:
                label, _ = MOODS[mood_key]
                axis.text(column + 0.5, y + 0.45, label, fontsize=11,
                          fontweight="bold",
                          color="#3D405B", ha="center", va="center")

    legend_items = [label for label, _ in MOODS.values()]
    fig.text(0.5, 0.025, "   ".join(legend_items), ha="center", fontsize=10,
             color="#3D405B")
    plt.tight_layout(rect=(0, 0.06, 1, 1))
    plt.savefig(IMAGE_FILE, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    print(f"Calendar saved as: {IMAGE_FILE}")
    plt.show()  # Opens the calendar window after it is saved.
    plt.close(fig)


def choose_month() -> tuple[int, int]:
    today = date.today()
    raw = input(f"Month to display (YYYY-MM, blank for {today:%Y-%m}): ").strip()
    if not raw:
        return today.year, today.month
    try:
        selected = datetime.strptime(raw, "%Y-%m")
        return selected.year, selected.month
    except ValueError:
        print("Invalid month. Showing the current month instead.")
        return today.year, today.month


def main() -> None:
    print("=" * 38)
    print("       COLORFUL MOOD TRACKER")
    print("=" * 38)

    while True:
        print("\n1. Add or update a mood")
        print("2. Create monthly calendar")
        print("3. Exit")
        choice = input("Choose 1, 2, or 3: ").strip()

        if choice == "1":
            add_mood()
        elif choice == "2":
            year, month = choose_month()
            create_calendar(year, month)
        elif choice == "3":
            print("Goodbye! Keep noticing how you feel.")
            break
        else:
            print("Please choose 1, 2, or 3.")


if __name__ == "__main__":
    main()
