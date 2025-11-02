"""
Helper functions for AI-Powered Smart Study Planner
"""

from datetime import datetime, date, timedelta, time
from typing import List, Dict, Tuple
import config


def calculate_xp_for_session(duration_minutes: int) -> int:
    """Calculate XP earned for a study session"""
    hours = duration_minutes / 60
    return int(hours * config.XP_PER_HOUR)


def calculate_level(total_xp: int) -> int:
    """Calculate user level based on total XP"""
    level = 1
    for lvl, threshold in enumerate(config.LEVEL_THRESHOLDS, start=1):
        if total_xp >= threshold:
            level = lvl
    return level


def get_xp_for_next_level(current_xp: int, current_level: int) -> Tuple[int, int]:
    """
    Get XP needed for next level
    Returns: (xp_needed, next_level_threshold)
    """
    if current_level >= len(config.LEVEL_THRESHOLDS):
        return 0, config.LEVEL_THRESHOLDS[-1]
    
    next_threshold = config.LEVEL_THRESHOLDS[current_level]
    xp_needed = next_threshold - current_xp
    return xp_needed, next_threshold


def format_duration(minutes: int) -> str:
    """Format duration in minutes to human-readable string"""
    if minutes < 60:
        return f"{minutes}m"
    hours = minutes // 60
    mins = minutes % 60
    if mins == 0:
        return f"{hours}h"
    return f"{hours}h {mins}m"


def get_difficulty_multiplier(difficulty: str) -> float:
    """Get time multiplier for difficulty level"""
    return config.DIFFICULTY_LEVELS.get(difficulty, {}).get("multiplier", 1.0)


def get_default_duration(difficulty: str) -> int:
    """Get default study duration for difficulty level"""
    return config.DIFFICULTY_LEVELS.get(difficulty, {}).get("default_duration", 45)


def calculate_urgency_score(deadline: date, current_date: date = None) -> float:
    """
    Calculate urgency score based on deadline
    Returns: 0.0 (not urgent) to 1.0 (very urgent)
    """
    if not deadline:
        return 0.0
    
    if current_date is None:
        current_date = date.today()
    
    days_until = (deadline - current_date).days
    
    if days_until < 0:
        return 1.0  # Overdue
    elif days_until == 0:
        return 1.0  # Due today
    elif days_until <= 3:
        return 0.9
    elif days_until <= 7:
        return 0.7
    elif days_until <= 14:
        return 0.5
    elif days_until <= 30:
        return 0.3
    else:
        return 0.1


def calculate_priority_score(priority: str) -> float:
    """
    Calculate priority score
    Returns: 0.0 to 1.0
    """
    priority_map = {
        "Urgent": 1.0,
        "High": 0.75,
        "Medium": 0.5,
        "Low": 0.25
    }
    return priority_map.get(priority, 0.5)


def get_time_of_day_category(hour: int) -> str:
    """Categorize time of day"""
    if 5 <= hour < 8:
        return "Early Morning"
    elif 8 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 17:
        return "Afternoon"
    elif 17 <= hour < 21:
        return "Evening"
    else:
        return "Night"


def generate_time_slots(start_hour: int, end_hour: int, 
                       slot_duration: int = 60, break_duration: int = 15) -> List[str]:
    """
    Generate available time slots for a day
    Returns list of time strings in HH:MM format
    """
    slots = []
    current_time = time(start_hour, 0)
    end_time = time(end_hour, 0)
    
    while current_time < end_time:
        slots.append(current_time.strftime("%H:%M"))
        
        # Add slot duration + break
        total_minutes = slot_duration + break_duration
        hours_to_add = total_minutes // 60
        minutes_to_add = total_minutes % 60
        
        current_datetime = datetime.combine(date.today(), current_time)
        current_datetime += timedelta(hours=hours_to_add, minutes=minutes_to_add)
        current_time = current_datetime.time()
    
    return slots


def is_within_study_hours(hour: int) -> bool:
    """Check if hour is within default study hours"""
    return config.DEFAULT_STUDY_HOURS["start"] <= hour < config.DEFAULT_STUDY_HOURS["end"]


def get_week_dates(target_date: date = None) -> List[date]:
    """Get all dates for the week containing target_date"""
    if target_date is None:
        target_date = date.today()
    
    # Find Monday of the week
    days_since_monday = target_date.weekday()
    monday = target_date - timedelta(days=days_since_monday)
    
    # Generate all 7 days
    return [monday + timedelta(days=i) for i in range(7)]


def get_date_range(days: int, end_date: date = None) -> Tuple[date, date]:
    """
    Get date range for the last N days
    Returns: (start_date, end_date)
    """
    if end_date is None:
        end_date = date.today()
    start_date = end_date - timedelta(days=days - 1)
    return start_date, end_date


def format_date_relative(target_date: date) -> str:
    """Format date relative to today (e.g., 'Today', 'Tomorrow', 'In 3 days')"""
    today = date.today()
    delta = (target_date - today).days
    
    if delta == 0:
        return "Today"
    elif delta == 1:
        return "Tomorrow"
    elif delta == -1:
        return "Yesterday"
    elif delta > 1:
        return f"In {delta} days"
    else:
        return f"{abs(delta)} days ago"


def get_streak_emoji(streak: int) -> str:
    """Get emoji based on streak length"""
    if streak == 0:
        return "💤"
    elif streak < 3:
        return "🔥"
    elif streak < 7:
        return "🔥🔥"
    elif streak < 14:
        return "🔥🔥🔥"
    elif streak < 30:
        return "🔥🔥🔥🔥"
    else:
        return "🔥🔥🔥🔥🔥"


def get_level_emoji(level: int) -> str:
    """Get emoji based on level"""
    if level < 3:
        return "🌱"
    elif level < 5:
        return "🌿"
    elif level < 7:
        return "🌳"
    elif level < 10:
        return "⭐"
    else:
        return "👑"


def calculate_completion_rate(completed: int, total: int) -> float:
    """Calculate completion rate as percentage"""
    if total == 0:
        return 0.0
    return (completed / total) * 100


def get_study_recommendation_time() -> str:
    """Get recommended study time based on current time"""
    current_hour = datetime.now().hour
    
    if current_hour < 8:
        return "Morning (8:00 AM)"
    elif current_hour < 14:
        return "Afternoon (2:00 PM)"
    elif current_hour < 18:
        return "Evening (6:00 PM)"
    else:
        return "Tomorrow Morning (8:00 AM)"


def parse_time_string(time_str: str) -> time:
    """Parse time string in HH:MM format"""
    try:
        return datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        return time(9, 0)  # Default to 9 AM


def get_color_for_subject(subject: str) -> str:
    """Get a consistent color for a subject"""
    colors = [
        "#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", 
        "#98D8C8", "#F7DC6F", "#BB8FCE", "#85C1E2",
        "#F8B739", "#52B788", "#E76F51", "#2A9D8F"
    ]
    # Use hash to get consistent color for same subject
    index = hash(subject) % len(colors)
    return colors[index]


def validate_task_data(title: str, subject: str, difficulty: str, 
                      priority: str, estimated_hours: float) -> Tuple[bool, str]:
    """
    Validate task data
    Returns: (is_valid, error_message)
    """
    if not title or len(title.strip()) == 0:
        return False, "Title cannot be empty"
    
    if not subject or len(subject.strip()) == 0:
        return False, "Subject cannot be empty"
    
    if difficulty not in config.DIFFICULTY_LEVELS:
        return False, f"Invalid difficulty level: {difficulty}"
    
    if priority not in config.PRIORITY_LEVELS:
        return False, f"Invalid priority level: {priority}"
    
    if estimated_hours <= 0:
        return False, "Estimated hours must be greater than 0"
    
    if estimated_hours > config.MAX_DAILY_STUDY_HOURS:
        return False, f"Estimated hours cannot exceed {config.MAX_DAILY_STUDY_HOURS}"
    
    return True, ""


def get_motivational_message(streak: int, level: int) -> str:
    """Get a motivational message based on progress"""
    messages = {
        "streak_0": [
            "Start your study journey today! 🚀",
            "Every expert was once a beginner. Let's begin! 💪",
            "Your future self will thank you for starting now! 🌟"
        ],
        "streak_low": [
            "Great start! Keep the momentum going! 🔥",
            "You're building a great habit! 📚",
            "Consistency is key. You're doing amazing! ⭐"
        ],
        "streak_medium": [
            "Impressive streak! You're on fire! 🔥🔥",
            "Your dedication is inspiring! Keep it up! 💎",
            "You're crushing it! Stay focused! 🎯"
        ],
        "streak_high": [
            "Unstoppable! You're a study machine! 🚀",
            "Legendary streak! You're an inspiration! 👑",
            "Phenomenal dedication! Keep soaring! 🦅"
        ]
    }
    
    if streak == 0:
        category = "streak_0"
    elif streak < 7:
        category = "streak_low"
    elif streak < 21:
        category = "streak_medium"
    else:
        category = "streak_high"
    
    import random
    return random.choice(messages[category])
