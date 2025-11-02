"""
Configuration file for AI-Powered Smart Study Planner
"""

# Database Configuration
DATABASE_NAME = "study_planner.db"

# Gamification Settings
XP_PER_HOUR = 100
XP_PER_TASK_COMPLETION = 50
STREAK_BONUS_XP = 25

# Level thresholds (XP required for each level)
LEVEL_THRESHOLDS = [
    0,      # Level 1
    500,    # Level 2
    1200,   # Level 3
    2000,   # Level 4
    3000,   # Level 5
    4500,   # Level 6
    6500,   # Level 7
    9000,   # Level 8
    12000,  # Level 9
    15500,  # Level 10
]

# Achievement Badges
ACHIEVEMENTS = {
    "first_study": {
        "name": "First Steps",
        "description": "Complete your first study session",
        "icon": "🎯",
        "xp_reward": 50
    },
    "week_warrior": {
        "name": "Week Warrior",
        "description": "Maintain a 7-day study streak",
        "icon": "🔥",
        "xp_reward": 200
    },
    "month_master": {
        "name": "Month Master",
        "description": "Maintain a 30-day study streak",
        "icon": "👑",
        "xp_reward": 500
    },
    "early_bird": {
        "name": "Early Bird",
        "description": "Study before 8 AM",
        "icon": "🌅",
        "xp_reward": 75
    },
    "night_owl": {
        "name": "Night Owl",
        "description": "Study after 10 PM",
        "icon": "🦉",
        "xp_reward": 75
    },
    "marathon_runner": {
        "name": "Marathon Runner",
        "description": "Study for 5+ hours in a day",
        "icon": "🏃",
        "xp_reward": 150
    },
    "subject_master": {
        "name": "Subject Master",
        "description": "Complete 20 tasks in a single subject",
        "icon": "📚",
        "xp_reward": 300
    },
    "perfect_week": {
        "name": "Perfect Week",
        "description": "Complete all scheduled tasks for a week",
        "icon": "⭐",
        "xp_reward": 250
    },
    "deadline_crusher": {
        "name": "Deadline Crusher",
        "description": "Complete 10 tasks before their deadline",
        "icon": "💪",
        "xp_reward": 200
    },
    "consistency_king": {
        "name": "Consistency King",
        "description": "Study every day for 14 days",
        "icon": "👑",
        "xp_reward": 350
    }
}

# Study Session Settings
DEFAULT_STUDY_DURATION = 45  # minutes
DEFAULT_BREAK_DURATION = 15  # minutes
MAX_DAILY_STUDY_HOURS = 12
MIN_STUDY_SESSION = 15  # minutes

# Difficulty Levels
DIFFICULTY_LEVELS = {
    "Easy": {"multiplier": 1.0, "default_duration": 30},
    "Medium": {"multiplier": 1.5, "default_duration": 45},
    "Hard": {"multiplier": 2.0, "default_duration": 60},
    "Very Hard": {"multiplier": 2.5, "default_duration": 90}
}

# Priority Levels
PRIORITY_LEVELS = ["Low", "Medium", "High", "Urgent"]

# Common Subjects (can be customized by user)
DEFAULT_SUBJECTS = [
    "Mathematics",
    "Physics",
    "Chemistry",
    "Biology",
    "Computer Science",
    "English",
    "History",
    "Geography",
    "Economics",
    "Other"
]

# AI Recommendation Settings
AI_RECOMMENDATION_FACTORS = {
    "deadline_weight": 0.35,
    "difficulty_weight": 0.25,
    "priority_weight": 0.20,
    "last_studied_weight": 0.15,
    "completion_rate_weight": 0.05
}

# Analytics Settings
ANALYTICS_LOOKBACK_DAYS = 30
HEATMAP_WEEKS = 12

# UI Theme Colors
THEME_COLORS = {
    "primary": "#6366f1",
    "secondary": "#8b5cf6",
    "success": "#10b981",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "info": "#3b82f6"
}

# Time Slots for Scheduling (24-hour format)
DEFAULT_STUDY_HOURS = {
    "start": 6,  # 6 AM
    "end": 23    # 11 PM
}
