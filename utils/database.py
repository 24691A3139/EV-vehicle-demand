"""
Database module for AI-Powered Smart Study Planner
Handles all SQLite database operations
"""

import sqlite3
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
import json
from config import DATABASE_NAME


class Database:
    def __init__(self, db_name: str = DATABASE_NAME):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        """Create and return a database connection"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tasks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                subject TEXT NOT NULL,
                description TEXT,
                difficulty TEXT NOT NULL,
                priority TEXT NOT NULL,
                estimated_hours REAL NOT NULL,
                deadline DATE,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                scheduled_date DATE,
                scheduled_time TEXT
            )
        """)
        
        # Study sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS study_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER,
                subject TEXT NOT NULL,
                duration_minutes INTEGER NOT NULL,
                session_date DATE NOT NULL,
                session_time TEXT NOT NULL,
                xp_earned INTEGER DEFAULT 0,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (task_id) REFERENCES tasks(id)
            )
        """)
        
        # User progress table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_xp INTEGER DEFAULT 0,
                current_level INTEGER DEFAULT 1,
                current_streak INTEGER DEFAULT 0,
                longest_streak INTEGER DEFAULT 0,
                last_study_date DATE,
                total_study_hours REAL DEFAULT 0,
                tasks_completed INTEGER DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Achievements table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                achievement_key TEXT UNIQUE NOT NULL,
                unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                xp_earned INTEGER DEFAULT 0
            )
        """)
        
        # Subject statistics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subject_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT UNIQUE NOT NULL,
                total_hours REAL DEFAULT 0,
                tasks_completed INTEGER DEFAULT 0,
                last_studied DATE
            )
        """)
        
        # Initialize user progress if not exists
        cursor.execute("SELECT COUNT(*) as count FROM user_progress")
        if cursor.fetchone()['count'] == 0:
            cursor.execute("""
                INSERT INTO user_progress (total_xp, current_level, current_streak, longest_streak)
                VALUES (0, 1, 0, 0)
            """)
        
        conn.commit()
        conn.close()
    
    # ===== TASK OPERATIONS =====
    
    def add_task(self, title: str, subject: str, difficulty: str, priority: str, 
                 estimated_hours: float, deadline: Optional[date] = None, 
                 description: str = "") -> int:
        """Add a new task"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO tasks (title, subject, description, difficulty, priority, 
                             estimated_hours, deadline)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (title, subject, description, difficulty, priority, estimated_hours, deadline))
        
        task_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return task_id
    
    def get_all_tasks(self, status: Optional[str] = None) -> List[Dict]:
        """Get all tasks, optionally filtered by status"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if status:
            cursor.execute("SELECT * FROM tasks WHERE status = ? ORDER BY deadline, priority DESC", (status,))
        else:
            cursor.execute("SELECT * FROM tasks ORDER BY deadline, priority DESC")
        
        tasks = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return tasks
    
    def get_task_by_id(self, task_id: int) -> Optional[Dict]:
        """Get a specific task by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def update_task_status(self, task_id: int, status: str) -> bool:
        """Update task status"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        completed_at = datetime.now() if status == 'completed' else None
        cursor.execute("""
            UPDATE tasks SET status = ?, completed_at = ? WHERE id = ?
        """, (status, completed_at, task_id))
        
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
    
    def update_task_schedule(self, task_id: int, scheduled_date: date, scheduled_time: str) -> bool:
        """Update task schedule"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE tasks SET scheduled_date = ?, scheduled_time = ? WHERE id = ?
        """, (scheduled_date, scheduled_time, task_id))
        
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
    
    # ===== STUDY SESSION OPERATIONS =====
    
    def add_study_session(self, subject: str, duration_minutes: int, 
                         session_date: date, session_time: str,
                         task_id: Optional[int] = None, xp_earned: int = 0,
                         notes: str = "") -> int:
        """Add a study session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO study_sessions (task_id, subject, duration_minutes, 
                                       session_date, session_time, xp_earned, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (task_id, subject, duration_minutes, session_date, session_time, xp_earned, notes))
        
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return session_id
    
    def get_study_sessions(self, start_date: Optional[date] = None, 
                          end_date: Optional[date] = None) -> List[Dict]:
        """Get study sessions within date range"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if start_date and end_date:
            cursor.execute("""
                SELECT * FROM study_sessions 
                WHERE session_date BETWEEN ? AND ?
                ORDER BY session_date DESC, session_time DESC
            """, (start_date, end_date))
        else:
            cursor.execute("""
                SELECT * FROM study_sessions 
                ORDER BY session_date DESC, session_time DESC
            """)
        
        sessions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return sessions
    
    def get_sessions_by_subject(self, subject: str) -> List[Dict]:
        """Get all study sessions for a specific subject"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM study_sessions WHERE subject = ?
            ORDER BY session_date DESC
        """, (subject,))
        
        sessions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return sessions
    
    # ===== USER PROGRESS OPERATIONS =====
    
    def get_user_progress(self) -> Dict:
        """Get current user progress"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM user_progress WHERE id = 1")
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else {}
    
    def update_user_progress(self, xp_gained: int = 0, study_hours: float = 0,
                            tasks_completed: int = 0) -> Dict:
        """Update user progress"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        progress = self.get_user_progress()
        new_xp = progress['total_xp'] + xp_gained
        new_hours = progress['total_study_hours'] + study_hours
        new_tasks = progress['tasks_completed'] + tasks_completed
        
        # Calculate new level
        from config import LEVEL_THRESHOLDS
        new_level = 1
        for level, threshold in enumerate(LEVEL_THRESHOLDS, start=1):
            if new_xp >= threshold:
                new_level = level
        
        cursor.execute("""
            UPDATE user_progress 
            SET total_xp = ?, current_level = ?, total_study_hours = ?, 
                tasks_completed = ?, updated_at = ?
            WHERE id = 1
        """, (new_xp, new_level, new_hours, new_tasks, datetime.now()))
        
        conn.commit()
        conn.close()
        
        return self.get_user_progress()
    
    def update_streak(self, current_date: date) -> Tuple[int, bool]:
        """Update study streak and return (current_streak, is_new_record)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        progress = self.get_user_progress()
        last_study = progress.get('last_study_date')
        current_streak = progress['current_streak']
        longest_streak = progress['longest_streak']
        
        is_new_record = False
        
        if last_study:
            last_study_date = datetime.strptime(last_study, '%Y-%m-%d').date()
            days_diff = (current_date - last_study_date).days
            
            if days_diff == 1:
                current_streak += 1
            elif days_diff > 1:
                current_streak = 1
        else:
            current_streak = 1
        
        if current_streak > longest_streak:
            longest_streak = current_streak
            is_new_record = True
        
        cursor.execute("""
            UPDATE user_progress 
            SET current_streak = ?, longest_streak = ?, last_study_date = ?
            WHERE id = 1
        """, (current_streak, longest_streak, current_date))
        
        conn.commit()
        conn.close()
        
        return current_streak, is_new_record
    
    # ===== ACHIEVEMENT OPERATIONS =====
    
    def unlock_achievement(self, achievement_key: str, xp_earned: int) -> bool:
        """Unlock an achievement"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO achievements (achievement_key, xp_earned)
                VALUES (?, ?)
            """, (achievement_key, xp_earned))
            conn.commit()
            success = True
        except sqlite3.IntegrityError:
            success = False
        
        conn.close()
        return success
    
    def get_unlocked_achievements(self) -> List[Dict]:
        """Get all unlocked achievements"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM achievements ORDER BY unlocked_at DESC")
        achievements = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return achievements
    
    def is_achievement_unlocked(self, achievement_key: str) -> bool:
        """Check if an achievement is unlocked"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as count FROM achievements WHERE achievement_key = ?", 
                      (achievement_key,))
        count = cursor.fetchone()['count']
        conn.close()
        return count > 0
    
    # ===== SUBJECT STATISTICS OPERATIONS =====
    
    def update_subject_stats(self, subject: str, hours: float, tasks_completed: int = 0):
        """Update subject statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO subject_stats (subject, total_hours, tasks_completed, last_studied)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(subject) DO UPDATE SET
                total_hours = total_hours + ?,
                tasks_completed = tasks_completed + ?,
                last_studied = ?
        """, (subject, hours, tasks_completed, date.today(), hours, tasks_completed, date.today()))
        
        conn.commit()
        conn.close()
    
    def get_subject_stats(self) -> List[Dict]:
        """Get statistics for all subjects"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM subject_stats ORDER BY total_hours DESC")
        stats = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return stats
    
    def get_subject_stat(self, subject: str) -> Optional[Dict]:
        """Get statistics for a specific subject"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM subject_stats WHERE subject = ?", (subject,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
