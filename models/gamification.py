"""
Gamification Module
Handles streaks, badges, achievements, XP, and leveling system
"""

from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Tuple
import config
from utils.helpers import calculate_xp_for_session, get_streak_emoji, get_level_emoji


class GamificationEngine:
    def __init__(self, db):
        self.db = db
    
    def award_xp(self, xp_amount: int, reason: str = "") -> Dict:
        """
        Award XP to user and check for level up
        Returns updated progress with level_up flag
        """
        progress = self.db.update_user_progress(xp_gained=xp_amount)
        
        result = {
            'xp_awarded': xp_amount,
            'total_xp': progress['total_xp'],
            'current_level': progress['current_level'],
            'level_up': False,
            'reason': reason
        }
        
        # Check if leveled up (compare with previous level)
        from utils.helpers import calculate_level
        previous_xp = progress['total_xp'] - xp_amount
        previous_level = calculate_level(previous_xp)
        
        if progress['current_level'] > previous_level:
            result['level_up'] = True
            result['new_level'] = progress['current_level']
        
        return result
    
    def record_study_session(self, subject: str, duration_minutes: int,
                            task_id: Optional[int] = None, notes: str = "") -> Dict:
        """
        Record a study session and award XP
        Returns session info with XP and achievements
        """
        # Calculate XP
        xp_earned = calculate_xp_for_session(duration_minutes)
        
        # Record session in database
        session_date = date.today()
        session_time = datetime.now().strftime("%H:%M")
        
        session_id = self.db.add_study_session(
            subject=subject,
            duration_minutes=duration_minutes,
            session_date=session_date,
            session_time=session_time,
            task_id=task_id,
            xp_earned=xp_earned,
            notes=notes
        )
        
        # Award XP
        xp_result = self.award_xp(xp_earned, f"Study session: {duration_minutes} minutes")
        
        # Update streak
        current_streak, is_new_record = self.db.update_streak(session_date)
        
        # Award streak bonus
        if current_streak > 0:
            streak_bonus = config.STREAK_BONUS_XP
            self.award_xp(streak_bonus, f"Streak bonus: {current_streak} days")
            xp_result['xp_awarded'] += streak_bonus
        
        # Update user progress
        hours = duration_minutes / 60
        self.db.update_user_progress(study_hours=hours)
        
        # Update subject stats
        self.db.update_subject_stats(subject, hours)
        
        # Check for achievements
        new_achievements = self.check_and_unlock_achievements(
            session_date=session_date,
            session_time=session_time,
            duration_minutes=duration_minutes,
            current_streak=current_streak
        )
        
        return {
            'session_id': session_id,
            'xp_earned': xp_result['xp_awarded'],
            'total_xp': xp_result['total_xp'],
            'current_level': xp_result['current_level'],
            'level_up': xp_result['level_up'],
            'current_streak': current_streak,
            'is_new_record': is_new_record,
            'new_achievements': new_achievements
        }
    
    def complete_task(self, task_id: int) -> Dict:
        """
        Mark task as completed and award XP
        """
        task = self.db.get_task_by_id(task_id)
        if not task:
            return {'success': False, 'error': 'Task not found'}
        
        # Update task status
        self.db.update_task_status(task_id, 'completed')
        
        # Award XP
        xp_earned = config.XP_PER_TASK_COMPLETION
        
        # Bonus XP for difficulty
        from utils.helpers import get_difficulty_multiplier
        difficulty_bonus = int(xp_earned * (get_difficulty_multiplier(task['difficulty']) - 1))
        total_xp = xp_earned + difficulty_bonus
        
        xp_result = self.award_xp(total_xp, f"Completed: {task['title']}")
        
        # Update progress
        self.db.update_user_progress(tasks_completed=1)
        
        # Update subject stats
        self.db.update_subject_stats(task['subject'], 0, tasks_completed=1)
        
        # Check for achievements
        new_achievements = self.check_task_achievements(task)
        
        return {
            'success': True,
            'task_id': task_id,
            'xp_earned': total_xp,
            'total_xp': xp_result['total_xp'],
            'current_level': xp_result['current_level'],
            'level_up': xp_result['level_up'],
            'new_achievements': new_achievements
        }
    
    def check_and_unlock_achievements(self, session_date: date, session_time: str,
                                     duration_minutes: int, current_streak: int) -> List[Dict]:
        """
        Check and unlock achievements based on study session
        """
        new_achievements = []
        
        # First study achievement
        if not self.db.is_achievement_unlocked('first_study'):
            sessions = self.db.get_study_sessions()
            if len(sessions) == 1:  # Just recorded first session
                if self._unlock_achievement('first_study'):
                    new_achievements.append(config.ACHIEVEMENTS['first_study'])
        
        # Streak achievements
        if current_streak >= 7 and not self.db.is_achievement_unlocked('week_warrior'):
            if self._unlock_achievement('week_warrior'):
                new_achievements.append(config.ACHIEVEMENTS['week_warrior'])
        
        if current_streak >= 14 and not self.db.is_achievement_unlocked('consistency_king'):
            if self._unlock_achievement('consistency_king'):
                new_achievements.append(config.ACHIEVEMENTS['consistency_king'])
        
        if current_streak >= 30 and not self.db.is_achievement_unlocked('month_master'):
            if self._unlock_achievement('month_master'):
                new_achievements.append(config.ACHIEVEMENTS['month_master'])
        
        # Time-based achievements
        hour = int(session_time.split(':')[0])
        
        if hour < 8 and not self.db.is_achievement_unlocked('early_bird'):
            if self._unlock_achievement('early_bird'):
                new_achievements.append(config.ACHIEVEMENTS['early_bird'])
        
        if hour >= 22 and not self.db.is_achievement_unlocked('night_owl'):
            if self._unlock_achievement('night_owl'):
                new_achievements.append(config.ACHIEVEMENTS['night_owl'])
        
        # Marathon runner - 5+ hours in a day
        if not self.db.is_achievement_unlocked('marathon_runner'):
            today_sessions = self.db.get_study_sessions(session_date, session_date)
            total_minutes = sum(s['duration_minutes'] for s in today_sessions)
            if total_minutes >= 300:  # 5 hours
                if self._unlock_achievement('marathon_runner'):
                    new_achievements.append(config.ACHIEVEMENTS['marathon_runner'])
        
        return new_achievements
    
    def check_task_achievements(self, task: Dict) -> List[Dict]:
        """
        Check achievements related to task completion
        """
        new_achievements = []
        
        # Subject master - 20 tasks in one subject
        if not self.db.is_achievement_unlocked('subject_master'):
            subject_stat = self.db.get_subject_stat(task['subject'])
            if subject_stat and subject_stat['tasks_completed'] >= 20:
                if self._unlock_achievement('subject_master'):
                    new_achievements.append(config.ACHIEVEMENTS['subject_master'])
        
        # Deadline crusher - complete task before deadline
        if task.get('deadline'):
            deadline = task['deadline']
            if isinstance(deadline, str):
                deadline = datetime.strptime(deadline, '%Y-%m-%d').date()
            
            if date.today() < deadline:
                # Check how many tasks completed before deadline
                all_tasks = self.db.get_all_tasks(status='completed')
                early_completions = 0
                
                for t in all_tasks:
                    if t.get('deadline') and t.get('completed_at'):
                        t_deadline = t['deadline']
                        if isinstance(t_deadline, str):
                            t_deadline = datetime.strptime(t_deadline, '%Y-%m-%d').date()
                        
                        t_completed = datetime.strptime(t['completed_at'], '%Y-%m-%d %H:%M:%S').date()
                        
                        if t_completed < t_deadline:
                            early_completions += 1
                
                if early_completions >= 10 and not self.db.is_achievement_unlocked('deadline_crusher'):
                    if self._unlock_achievement('deadline_crusher'):
                        new_achievements.append(config.ACHIEVEMENTS['deadline_crusher'])
        
        # Perfect week - complete all scheduled tasks for a week
        if not self.db.is_achievement_unlocked('perfect_week'):
            # Check if all tasks scheduled for current week are completed
            from utils.helpers import get_week_dates
            week_dates = get_week_dates()
            
            all_tasks = self.db.get_all_tasks()
            week_tasks = [
                t for t in all_tasks 
                if t.get('scheduled_date') and 
                datetime.strptime(str(t['scheduled_date']), '%Y-%m-%d').date() in week_dates
            ]
            
            if week_tasks:
                completed_count = sum(1 for t in week_tasks if t['status'] == 'completed')
                if completed_count == len(week_tasks) and len(week_tasks) >= 5:
                    if self._unlock_achievement('perfect_week'):
                        new_achievements.append(config.ACHIEVEMENTS['perfect_week'])
        
        return new_achievements
    
    def _unlock_achievement(self, achievement_key: str) -> bool:
        """
        Internal method to unlock an achievement
        """
        achievement = config.ACHIEVEMENTS.get(achievement_key)
        if not achievement:
            return False
        
        success = self.db.unlock_achievement(achievement_key, achievement['xp_reward'])
        
        if success:
            # Award XP
            self.award_xp(achievement['xp_reward'], f"Achievement: {achievement['name']}")
        
        return success
    
    def get_progress_summary(self) -> Dict:
        """
        Get comprehensive progress summary
        """
        progress = self.db.get_user_progress()
        achievements = self.db.get_unlocked_achievements()
        
        # Calculate next level info
        from utils.helpers import get_xp_for_next_level
        xp_needed, next_threshold = get_xp_for_next_level(
            progress['total_xp'], 
            progress['current_level']
        )
        
        # Get achievement progress
        total_achievements = len(config.ACHIEVEMENTS)
        unlocked_count = len(achievements)
        
        return {
            'total_xp': progress['total_xp'],
            'current_level': progress['current_level'],
            'level_emoji': get_level_emoji(progress['current_level']),
            'xp_for_next_level': xp_needed,
            'next_level_threshold': next_threshold,
            'current_streak': progress['current_streak'],
            'longest_streak': progress['longest_streak'],
            'streak_emoji': get_streak_emoji(progress['current_streak']),
            'total_study_hours': progress['total_study_hours'],
            'tasks_completed': progress['tasks_completed'],
            'achievements_unlocked': unlocked_count,
            'total_achievements': total_achievements,
            'achievement_progress': (unlocked_count / total_achievements) * 100
        }
    
    def get_leaderboard_stats(self) -> Dict:
        """
        Get stats for leaderboard/comparison
        """
        progress = self.db.get_user_progress()
        subject_stats = self.db.get_subject_stats()
        
        # Find strongest subject
        strongest_subject = None
        max_hours = 0
        
        for stat in subject_stats:
            if stat['total_hours'] > max_hours:
                max_hours = stat['total_hours']
                strongest_subject = stat['subject']
        
        return {
            'total_xp': progress['total_xp'],
            'level': progress['current_level'],
            'streak': progress['current_streak'],
            'total_hours': progress['total_study_hours'],
            'tasks_completed': progress['tasks_completed'],
            'strongest_subject': strongest_subject,
            'strongest_subject_hours': max_hours
        }
    
    def get_daily_goal_progress(self, target_hours: float = 2.0) -> Dict:
        """
        Check progress towards daily study goal
        """
        today = date.today()
        sessions = self.db.get_study_sessions(today, today)
        
        total_minutes = sum(s['duration_minutes'] for s in sessions)
        hours_today = total_minutes / 60
        
        progress_percent = min((hours_today / target_hours) * 100, 100)
        
        return {
            'hours_today': hours_today,
            'target_hours': target_hours,
            'progress_percent': progress_percent,
            'goal_met': hours_today >= target_hours,
            'sessions_count': len(sessions)
        }
    
    def get_weekly_goal_progress(self, target_hours: float = 14.0) -> Dict:
        """
        Check progress towards weekly study goal
        """
        from utils.helpers import get_week_dates
        week_dates = get_week_dates()
        
        start_date = week_dates[0]
        end_date = week_dates[-1]
        
        sessions = self.db.get_study_sessions(start_date, end_date)
        
        total_minutes = sum(s['duration_minutes'] for s in sessions)
        hours_this_week = total_minutes / 60
        
        progress_percent = min((hours_this_week / target_hours) * 100, 100)
        
        return {
            'hours_this_week': hours_this_week,
            'target_hours': target_hours,
            'progress_percent': progress_percent,
            'goal_met': hours_this_week >= target_hours,
            'sessions_count': len(sessions),
            'days_studied': len(set(s['session_date'] for s in sessions))
        }
