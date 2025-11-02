"""
Analytics Module
Provides productivity insights, visualizations, and performance tracking
"""

from datetime import datetime, date, timedelta
from typing import List, Dict, Tuple
import pandas as pd
import numpy as np
from collections import defaultdict
import config


class AnalyticsEngine:
    def __init__(self, db):
        self.db = db
    
    def get_study_hours_by_week(self, weeks: int = 4) -> Dict[str, float]:
        """
        Get total study hours for each week
        Returns: {week_label: hours}
        """
        end_date = date.today()
        start_date = end_date - timedelta(weeks=weeks)
        
        sessions = self.db.get_study_sessions(start_date, end_date)
        
        # Group by week
        weekly_hours = defaultdict(float)
        
        for session in sessions:
            session_date = session['session_date']
            if isinstance(session_date, str):
                session_date = datetime.strptime(session_date, '%Y-%m-%d').date()
            
            # Get week number
            week_start = session_date - timedelta(days=session_date.weekday())
            week_label = week_start.strftime('%b %d')
            
            hours = session['duration_minutes'] / 60
            weekly_hours[week_label] += hours
        
        return dict(weekly_hours)
    
    def get_study_hours_by_subject(self, days: int = 30) -> Dict[str, float]:
        """
        Get total study hours per subject
        Returns: {subject: hours}
        """
        subject_stats = self.db.get_subject_stats()
        
        subject_hours = {}
        for stat in subject_stats:
            subject_hours[stat['subject']] = stat['total_hours']
        
        return subject_hours
    
    def get_daily_study_pattern(self, days: int = 30) -> Dict[str, float]:
        """
        Get average study hours by day of week
        Returns: {day_name: avg_hours}
        """
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        sessions = self.db.get_study_sessions(start_date, end_date)
        
        # Group by day of week
        day_totals = defaultdict(list)
        
        for session in sessions:
            session_date = session['session_date']
            if isinstance(session_date, str):
                session_date = datetime.strptime(session_date, '%Y-%m-%d').date()
            
            day_name = session_date.strftime('%A')
            hours = session['duration_minutes'] / 60
            day_totals[day_name].append(hours)
        
        # Calculate averages
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_averages = {}
        
        for day in day_names:
            if day in day_totals:
                day_averages[day] = sum(day_totals[day]) / len(day_totals[day])
            else:
                day_averages[day] = 0.0
        
        return day_averages
    
    def get_hourly_study_pattern(self, days: int = 30) -> Dict[int, int]:
        """
        Get study session count by hour of day
        Returns: {hour: session_count}
        """
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        sessions = self.db.get_study_sessions(start_date, end_date)
        
        hourly_counts = defaultdict(int)
        
        for session in sessions:
            session_time = session['session_time']
            hour = int(session_time.split(':')[0])
            hourly_counts[hour] += 1
        
        return dict(hourly_counts)
    
    def get_productivity_heatmap(self, weeks: int = 12) -> pd.DataFrame:
        """
        Generate heatmap data for study activity
        Returns: DataFrame with dates and hours studied
        """
        end_date = date.today()
        start_date = end_date - timedelta(weeks=weeks)
        
        sessions = self.db.get_study_sessions(start_date, end_date)
        
        # Create date range
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Initialize data
        heatmap_data = []
        
        for current_date in date_range:
            day_sessions = [
                s for s in sessions 
                if datetime.strptime(str(s['session_date']), '%Y-%m-%d').date() == current_date.date()
            ]
            
            total_minutes = sum(s['duration_minutes'] for s in day_sessions)
            hours = total_minutes / 60
            
            heatmap_data.append({
                'date': current_date.date(),
                'day': current_date.strftime('%A'),
                'week': current_date.isocalendar()[1],
                'hours': hours
            })
        
        return pd.DataFrame(heatmap_data)
    
    def get_completion_rate(self) -> Dict[str, float]:
        """
        Calculate task completion rates
        """
        all_tasks = self.db.get_all_tasks()
        
        if not all_tasks:
            return {
                'total_tasks': 0,
                'completed': 0,
                'pending': 0,
                'completion_rate': 0.0
            }
        
        completed = sum(1 for t in all_tasks if t['status'] == 'completed')
        pending = sum(1 for t in all_tasks if t['status'] == 'pending')
        in_progress = sum(1 for t in all_tasks if t['status'] == 'in_progress')
        
        completion_rate = (completed / len(all_tasks)) * 100 if all_tasks else 0
        
        return {
            'total_tasks': len(all_tasks),
            'completed': completed,
            'pending': pending,
            'in_progress': in_progress,
            'completion_rate': completion_rate
        }
    
    def get_subject_performance(self) -> List[Dict]:
        """
        Get performance metrics for each subject
        """
        subject_stats = self.db.get_subject_stats()
        all_tasks = self.db.get_all_tasks()
        
        performance = []
        
        for stat in subject_stats:
            subject = stat['subject']
            
            # Get tasks for this subject
            subject_tasks = [t for t in all_tasks if t['subject'] == subject]
            completed_tasks = [t for t in subject_tasks if t['status'] == 'completed']
            
            completion_rate = (len(completed_tasks) / len(subject_tasks) * 100) if subject_tasks else 0
            
            performance.append({
                'subject': subject,
                'total_hours': stat['total_hours'],
                'tasks_completed': stat['tasks_completed'],
                'total_tasks': len(subject_tasks),
                'completion_rate': completion_rate,
                'last_studied': stat['last_studied']
            })
        
        # Sort by total hours
        performance.sort(key=lambda x: x['total_hours'], reverse=True)
        
        return performance
    
    def get_streak_history(self, days: int = 30) -> List[Dict]:
        """
        Get study streak history
        """
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        sessions = self.db.get_study_sessions(start_date, end_date)
        
        # Get unique study dates
        study_dates = set()
        for session in sessions:
            session_date = session['session_date']
            if isinstance(session_date, str):
                session_date = datetime.strptime(session_date, '%Y-%m-%d').date()
            study_dates.add(session_date)
        
        # Build streak history
        history = []
        current_date = start_date
        
        while current_date <= end_date:
            studied = current_date in study_dates
            history.append({
                'date': current_date,
                'studied': studied
            })
            current_date += timedelta(days=1)
        
        return history
    
    def get_progress_over_time(self, weeks: int = 8) -> Dict:
        """
        Track various metrics over time
        """
        end_date = date.today()
        start_date = end_date - timedelta(weeks=weeks)
        
        sessions = self.db.get_study_sessions(start_date, end_date)
        
        # Group by week
        weekly_data = defaultdict(lambda: {
            'hours': 0,
            'sessions': 0,
            'xp': 0
        })
        
        for session in sessions:
            session_date = session['session_date']
            if isinstance(session_date, str):
                session_date = datetime.strptime(session_date, '%Y-%m-%d').date()
            
            week_start = session_date - timedelta(days=session_date.weekday())
            week_label = week_start.strftime('%b %d')
            
            weekly_data[week_label]['hours'] += session['duration_minutes'] / 60
            weekly_data[week_label]['sessions'] += 1
            weekly_data[week_label]['xp'] += session.get('xp_earned', 0)
        
        return dict(weekly_data)
    
    def get_insights(self) -> List[str]:
        """
        Generate personalized insights based on study patterns
        """
        insights = []
        
        # Get data
        progress = self.db.get_user_progress()
        subject_hours = self.get_study_hours_by_subject()
        daily_pattern = self.get_daily_study_pattern()
        hourly_pattern = self.get_hourly_study_pattern()
        completion_stats = self.get_completion_rate()
        
        # Insight 1: Total study time
        total_hours = progress['total_study_hours']
        if total_hours > 100:
            insights.append(f"🎓 Impressive! You've studied for {total_hours:.1f} hours total!")
        elif total_hours > 50:
            insights.append(f"📚 Great progress! {total_hours:.1f} hours of focused study!")
        elif total_hours > 0:
            insights.append(f"🌱 You're building momentum with {total_hours:.1f} hours studied!")
        
        # Insight 2: Strongest subject
        if subject_hours:
            top_subject = max(subject_hours.items(), key=lambda x: x[1])
            insights.append(f"💪 Your strongest subject is {top_subject[0]} with {top_subject[1]:.1f} hours!")
        
        # Insight 3: Best study day
        if daily_pattern:
            best_day = max(daily_pattern.items(), key=lambda x: x[1])
            if best_day[1] > 0:
                insights.append(f"📅 You study most on {best_day[0]}s (avg {best_day[1]:.1f}h)")
        
        # Insight 4: Peak study time
        if hourly_pattern:
            peak_hour = max(hourly_pattern.items(), key=lambda x: x[1])
            time_label = f"{peak_hour[0]:02d}:00"
            insights.append(f"⏰ Your peak study time is around {time_label}")
        
        # Insight 5: Completion rate
        if completion_stats['total_tasks'] > 0:
            rate = completion_stats['completion_rate']
            if rate >= 80:
                insights.append(f"⭐ Excellent completion rate: {rate:.0f}%!")
            elif rate >= 60:
                insights.append(f"✅ Good completion rate: {rate:.0f}%")
            else:
                insights.append(f"💡 Tip: Focus on completing tasks ({rate:.0f}% completion rate)")
        
        # Insight 6: Streak motivation
        streak = progress['current_streak']
        if streak >= 7:
            insights.append(f"🔥 Amazing {streak}-day streak! Keep it going!")
        elif streak >= 3:
            insights.append(f"🔥 {streak}-day streak! You're building consistency!")
        elif streak == 0:
            insights.append("💡 Start a study session today to begin your streak!")
        
        return insights
    
    def get_weekly_summary(self) -> Dict:
        """
        Get comprehensive weekly summary
        """
        from utils.helpers import get_week_dates
        week_dates = get_week_dates()
        
        start_date = week_dates[0]
        end_date = week_dates[-1]
        
        sessions = self.db.get_study_sessions(start_date, end_date)
        
        # Calculate metrics
        total_minutes = sum(s['duration_minutes'] for s in sessions)
        total_hours = total_minutes / 60
        
        # Study days
        study_dates = set(
            datetime.strptime(str(s['session_date']), '%Y-%m-%d').date() 
            for s in sessions
        )
        days_studied = len(study_dates)
        
        # Subject breakdown
        subject_minutes = defaultdict(int)
        for session in sessions:
            subject_minutes[session['subject']] += session['duration_minutes']
        
        subject_breakdown = {
            subject: minutes / 60 
            for subject, minutes in subject_minutes.items()
        }
        
        # Tasks completed this week
        all_tasks = self.db.get_all_tasks(status='completed')
        week_tasks = [
            t for t in all_tasks 
            if t.get('completed_at') and 
            datetime.strptime(t['completed_at'], '%Y-%m-%d %H:%M:%S').date() in week_dates
        ]
        
        return {
            'total_hours': total_hours,
            'total_sessions': len(sessions),
            'days_studied': days_studied,
            'tasks_completed': len(week_tasks),
            'subject_breakdown': subject_breakdown,
            'avg_session_duration': total_minutes / len(sessions) if sessions else 0
        }
    
    def export_data_for_visualization(self, days: int = 30) -> Dict:
        """
        Export data in format ready for visualization
        """
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        sessions = self.db.get_study_sessions(start_date, end_date)
        
        # Convert to list of dicts for easy plotting
        session_data = []
        for session in sessions:
            session_data.append({
                'date': str(session['session_date']),
                'time': session['session_time'],
                'subject': session['subject'],
                'duration_minutes': session['duration_minutes'],
                'duration_hours': session['duration_minutes'] / 60,
                'xp_earned': session.get('xp_earned', 0)
            })
        
        return {
            'sessions': session_data,
            'date_range': {
                'start': str(start_date),
                'end': str(end_date)
            }
        }
