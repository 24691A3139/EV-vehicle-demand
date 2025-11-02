"""
Smart Scheduler Module
Context-aware planning that automatically schedules study sessions
"""

from datetime import datetime, date, timedelta, time
from typing import List, Dict, Optional, Tuple
import config
from utils.helpers import (
    calculate_urgency_score, calculate_priority_score,
    get_difficulty_multiplier, generate_time_slots,
    is_within_study_hours, parse_time_string
)


class SmartScheduler:
    def __init__(self, db):
        self.db = db
    
    def calculate_task_score(self, task: Dict, current_date: date = None) -> float:
        """
        Calculate priority score for a task based on multiple factors
        Higher score = higher priority
        """
        if current_date is None:
            current_date = date.today()
        
        # Factor 1: Deadline urgency (0-1)
        deadline = task.get('deadline')
        if deadline:
            if isinstance(deadline, str):
                deadline = datetime.strptime(deadline, '%Y-%m-%d').date()
            urgency_score = calculate_urgency_score(deadline, current_date)
        else:
            urgency_score = 0.3  # Default for tasks without deadline
        
        # Factor 2: Priority level (0-1)
        priority_score = calculate_priority_score(task['priority'])
        
        # Factor 3: Difficulty (inverse - harder tasks get higher priority)
        difficulty_multiplier = get_difficulty_multiplier(task['difficulty'])
        difficulty_score = min(difficulty_multiplier / 2.5, 1.0)
        
        # Factor 4: Estimated hours (longer tasks get slightly higher priority)
        hours_score = min(task['estimated_hours'] / 10, 1.0)
        
        # Weighted combination
        weights = config.AI_RECOMMENDATION_FACTORS
        total_score = (
            urgency_score * weights['deadline_weight'] +
            priority_score * weights['priority_weight'] +
            difficulty_score * weights['difficulty_weight'] +
            hours_score * 0.15
        )
        
        return total_score
    
    def get_available_time_slots(self, target_date: date, 
                                 existing_schedules: List[Dict]) -> List[str]:
        """
        Get available time slots for a given date
        Excludes already scheduled slots
        """
        all_slots = generate_time_slots(
            config.DEFAULT_STUDY_HOURS['start'],
            config.DEFAULT_STUDY_HOURS['end'],
            config.DEFAULT_STUDY_DURATION,
            config.DEFAULT_BREAK_DURATION
        )
        
        # Remove already scheduled slots
        scheduled_times = {
            s['scheduled_time'] for s in existing_schedules 
            if s.get('scheduled_date') == target_date and s.get('scheduled_time')
        }
        
        available_slots = [slot for slot in all_slots if slot not in scheduled_times]
        return available_slots
    
    def auto_schedule_tasks(self, days_ahead: int = 7) -> Dict[str, List[Dict]]:
        """
        Automatically schedule pending tasks for the next N days
        Returns: {date_str: [scheduled_tasks]}
        """
        # Get all pending tasks
        pending_tasks = self.db.get_all_tasks(status='pending')
        
        if not pending_tasks:
            return {}
        
        # Calculate scores for all tasks
        task_scores = []
        for task in pending_tasks:
            score = self.calculate_task_score(task)
            task_scores.append((task, score))
        
        # Sort by score (highest first)
        task_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Schedule tasks across days
        schedule = {}
        current_date = date.today()
        
        for task, score in task_scores:
            scheduled = False
            
            # Try to schedule within the next N days
            for day_offset in range(days_ahead):
                target_date = current_date + timedelta(days=day_offset)
                date_str = target_date.strftime('%Y-%m-%d')
                
                # Get existing schedules for this date
                existing = schedule.get(date_str, [])
                
                # Get available slots
                available_slots = self.get_available_time_slots(target_date, existing)
                
                if not available_slots:
                    continue
                
                # Calculate how many sessions needed for this task
                estimated_hours = task['estimated_hours']
                session_duration_hours = config.DEFAULT_STUDY_DURATION / 60
                sessions_needed = int(estimated_hours / session_duration_hours) + 1
                
                # Try to schedule at least one session
                if len(available_slots) > 0:
                    # Prefer morning slots for high-priority tasks
                    if score > 0.7 and any(int(slot.split(':')[0]) < 12 for slot in available_slots):
                        slot = next(s for s in available_slots if int(s.split(':')[0]) < 12)
                    else:
                        slot = available_slots[0]
                    
                    scheduled_task = {
                        'task_id': task['id'],
                        'title': task['title'],
                        'subject': task['subject'],
                        'scheduled_date': target_date,
                        'scheduled_time': slot,
                        'duration': config.DEFAULT_STUDY_DURATION,
                        'priority_score': score
                    }
                    
                    if date_str not in schedule:
                        schedule[date_str] = []
                    schedule[date_str].append(scheduled_task)
                    
                    # Update database
                    self.db.update_task_schedule(task['id'], target_date, slot)
                    
                    scheduled = True
                    break
            
            if not scheduled:
                # Task couldn't be scheduled - might need more days or manual intervention
                pass
        
        return schedule
    
    def suggest_next_task(self) -> Optional[Dict]:
        """
        Suggest the next best task to work on right now
        Based on current time, deadlines, and priorities
        """
        pending_tasks = self.db.get_all_tasks(status='pending')
        
        if not pending_tasks:
            return None
        
        current_time = datetime.now()
        current_date = date.today()
        current_hour = current_time.hour
        
        # Calculate scores with time-of-day bonus
        best_task = None
        best_score = -1
        
        for task in pending_tasks:
            base_score = self.calculate_task_score(task, current_date)
            
            # Time-of-day adjustments
            time_bonus = 0
            if 8 <= current_hour < 12:  # Morning - good for hard tasks
                if task['difficulty'] in ['Hard', 'Very Hard']:
                    time_bonus = 0.1
            elif 14 <= current_hour < 18:  # Afternoon - good for medium tasks
                if task['difficulty'] == 'Medium':
                    time_bonus = 0.1
            elif 19 <= current_hour < 22:  # Evening - good for easier tasks
                if task['difficulty'] == 'Easy':
                    time_bonus = 0.1
            
            final_score = base_score + time_bonus
            
            if final_score > best_score:
                best_score = final_score
                best_task = task
        
        return best_task
    
    def get_daily_schedule(self, target_date: date = None) -> List[Dict]:
        """
        Get the schedule for a specific day
        """
        if target_date is None:
            target_date = date.today()
        
        # Get all tasks scheduled for this date
        all_tasks = self.db.get_all_tasks()
        
        daily_tasks = []
        for task in all_tasks:
            scheduled_date = task.get('scheduled_date')
            if scheduled_date:
                if isinstance(scheduled_date, str):
                    scheduled_date = datetime.strptime(scheduled_date, '%Y-%m-%d').date()
                
                if scheduled_date == target_date:
                    daily_tasks.append(task)
        
        # Sort by scheduled time
        daily_tasks.sort(key=lambda x: x.get('scheduled_time', '00:00'))
        
        return daily_tasks
    
    def get_weekly_schedule(self, start_date: date = None) -> Dict[str, List[Dict]]:
        """
        Get schedule for the entire week
        Returns: {date_str: [tasks]}
        """
        if start_date is None:
            start_date = date.today()
        
        # Find Monday of the week
        days_since_monday = start_date.weekday()
        monday = start_date - timedelta(days=days_since_monday)
        
        weekly_schedule = {}
        
        for i in range(7):
            day = monday + timedelta(days=i)
            date_str = day.strftime('%Y-%m-%d')
            daily_tasks = self.get_daily_schedule(day)
            weekly_schedule[date_str] = daily_tasks
        
        return weekly_schedule
    
    def reschedule_task(self, task_id: int, new_date: date, new_time: str) -> bool:
        """
        Reschedule a specific task
        """
        # Check if slot is available
        daily_schedule = self.get_daily_schedule(new_date)
        scheduled_times = [t.get('scheduled_time') for t in daily_schedule]
        
        if new_time in scheduled_times:
            return False  # Slot already taken
        
        # Update schedule
        return self.db.update_task_schedule(task_id, new_date, new_time)
    
    def get_study_load_by_day(self, days_ahead: int = 7) -> Dict[str, float]:
        """
        Calculate study load (hours) for each day
        Returns: {date_str: total_hours}
        """
        load = {}
        current_date = date.today()
        
        for i in range(days_ahead):
            target_date = current_date + timedelta(days=i)
            date_str = target_date.strftime('%Y-%m-%d')
            
            daily_tasks = self.get_daily_schedule(target_date)
            total_hours = sum(task.get('estimated_hours', 0) for task in daily_tasks)
            load[date_str] = total_hours
        
        return load
    
    def optimize_schedule(self) -> Dict[str, any]:
        """
        Analyze current schedule and provide optimization suggestions
        """
        weekly_schedule = self.get_weekly_schedule()
        study_load = self.get_study_load_by_day(7)
        
        suggestions = []
        overloaded_days = []
        underutilized_days = []
        
        for date_str, hours in study_load.items():
            if hours > 8:
                overloaded_days.append(date_str)
                suggestions.append(f"⚠️ {date_str}: Overloaded ({hours:.1f}h). Consider redistributing tasks.")
            elif hours < 2 and hours > 0:
                underutilized_days.append(date_str)
            elif hours == 0:
                suggestions.append(f"💡 {date_str}: No tasks scheduled. Good day for review or rest!")
        
        # Check for deadline conflicts
        pending_tasks = self.db.get_all_tasks(status='pending')
        urgent_unscheduled = []
        
        for task in pending_tasks:
            if not task.get('scheduled_date'):
                deadline = task.get('deadline')
                if deadline:
                    if isinstance(deadline, str):
                        deadline = datetime.strptime(deadline, '%Y-%m-%d').date()
                    days_until = (deadline - date.today()).days
                    if days_until <= 3:
                        urgent_unscheduled.append(task['title'])
        
        if urgent_unscheduled:
            suggestions.append(f"🚨 Urgent: {len(urgent_unscheduled)} task(s) with approaching deadlines are unscheduled!")
        
        return {
            'suggestions': suggestions,
            'overloaded_days': overloaded_days,
            'underutilized_days': underutilized_days,
            'urgent_unscheduled': urgent_unscheduled,
            'weekly_load': study_load
        }
