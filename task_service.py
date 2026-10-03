from datetime import datetime, timedelta
from database.db_handler import get_connection
from config import STATUS_PENDING, STATUS_DONE

def initialize_day_tasks(date_str, company):
    """Loads daily recurring routines and auto-rolls over pending tasks from yesterday."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as count FROM daily_tasks WHERE task_date = ? AND company = ?", (date_str, company))
    if cursor.fetchone()['count'] == 0:
        # 1. Load routine templates
        cursor.execute("SELECT task_name, priority, category FROM routine_templates WHERE company = ?", (company,))
        routines = cursor.fetchall()
        for idx, r in enumerate(routines):
            cursor.execute("""
            INSERT INTO daily_tasks (task_date, company, task_name, status, priority, category, sort_order)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (date_str, company, r['task_name'], STATUS_PENDING, r['priority'], r['category'], idx))

        # 2. Auto-rollover pending tasks from yesterday
        try:
            cur_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            prev_date_str = str(cur_date - timedelta(days=1))
            cursor.execute("""
            SELECT task_name, priority, category FROM daily_tasks 
            WHERE task_date = ? AND company = ? AND status = ?
            """, (prev_date_str, company, STATUS_PENDING))
            rollover_tasks = cursor.fetchall()
            base_idx = len(routines)
            for i, task in enumerate(rollover_tasks):
                name = task['task_name']
                if not name.startswith("[Rollover] "):
                    name = f"[Rollover] {name}"
                cursor.execute("""
                INSERT INTO daily_tasks (task_date, company, task_name, status, priority, category, sort_order)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (date_str, company, name, STATUS_PENDING, task['priority'], task['category'], base_idx + i))
        except Exception:
            pass

        conn.commit()
    conn.close()

def get_tasks_by_date(date_str, company):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, task_date, company, task_name, status, priority, category, reminder_date, sort_order 
    FROM daily_tasks 
    WHERE task_date = ? AND company = ? 
    ORDER BY sort_order ASC, id ASC
    """, (date_str, company))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def add_daily_task(date_str, company, task_name, priority="Medium", category="General", reminder_date=""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COALESCE(MIN(sort_order), 0) - 1 as new_min FROM daily_tasks WHERE task_date = ? AND company = ?", (date_str, company))
    min_order = cursor.fetchone()['new_min']
    cursor.execute("""
    INSERT INTO daily_tasks (task_date, company, task_name, status, priority, category, reminder_date, sort_order)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (date_str, company, task_name.strip(), STATUS_PENDING, priority, category, reminder_date, min_order))
    conn.commit()
    conn.close()

def update_task_status(task_id, new_status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE daily_tasks SET status = ? WHERE id = ?", (new_status, task_id))
    conn.commit()
    conn.close()

def update_task_details(task_id, priority, category, reminder_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE daily_tasks SET priority = ?, category = ?, reminder_date = ? WHERE id = ?
    """, (priority, category, reminder_date, task_id))
    conn.commit()
    conn.close()

def move_task_up(task_id, date_str, company):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, sort_order FROM daily_tasks WHERE task_date = ? AND company = ? ORDER BY sort_order ASC, id ASC", (date_str, company))
    all_tasks = cursor.fetchall()
    task_ids = [t['id'] for t in all_tasks]
    if task_id in task_ids:
        idx = task_ids.index(task_id)
        if idx > 0:
            prev_task = all_tasks[idx - 1]
            curr_task = all_tasks[idx]
            cursor.execute("UPDATE daily_tasks SET sort_order = ? WHERE id = ?", (prev_task['sort_order'], curr_task['id']))
            cursor.execute("UPDATE daily_tasks SET sort_order = ? WHERE id = ?", (curr_task['sort_order'], prev_task['id']))
            conn.commit()
    conn.close()

def delete_daily_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM daily_tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

# Outreach Tracker Functions
def get_outreach_metrics(date_str, company):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT researched, contacted, replies FROM outreach_metrics WHERE metric_date = ? AND company = ?", (date_str, company))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return {"researched": 0, "contacted": 0, "replies": 0}

def update_outreach_metric(date_str, company, field, delta):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT researched, contacted, replies FROM outreach_metrics WHERE metric_date = ? AND company = ?", (date_str, company))
    row = cursor.fetchone()
    if not row:
        cursor.execute("INSERT INTO outreach_metrics (metric_date, company, researched, contacted, replies) VALUES (?, ?, 0, 0, 0)", (date_str, company))
        conn.commit()
    cursor.execute(f"UPDATE outreach_metrics SET {field} = MAX(0, {field} + ?) WHERE metric_date = ? AND company = ?", (delta, date_str, company))
    conn.commit()
    conn.close()

# Routine & Daily Note Functions
def get_routine_templates(company):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, task_name, priority, category FROM routine_templates WHERE company = ?", (company,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_routine_template(company, task_name, priority="Medium", category="General"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO routine_templates (company, task_name, priority, category) VALUES (?, ?, ?, ?)", (company, task_name.strip(), priority, category))
    conn.commit()
    conn.close()

def delete_routine_template(template_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM routine_templates WHERE id = ?", (template_id,))
    conn.commit()
    conn.close()

def get_daily_note(date_str, company):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT note_content FROM daily_notes WHERE task_date = ? AND company = ?", (date_str, company))
    row = cursor.fetchone()
    conn.close()
    return row['note_content'] if row and row['note_content'] else ""

def save_daily_note(date_str, company, content):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO daily_notes (task_date, company, note_content)
    VALUES (?, ?, ?)
    ON CONFLICT(task_date, company) DO UPDATE SET note_content = excluded.note_content
    """, (date_str, company, content))
    conn.commit()
    conn.close()

def get_all_companies_summary(date_str, companies):
    """Returns overview across all workspaces for the master view."""
    conn = get_connection()
    cursor = conn.cursor()
    summary = []
    for comp in companies:
        cursor.execute("SELECT COUNT(*) as total FROM daily_tasks WHERE task_date = ? AND company = ?", (date_str, comp))
        total = cursor.fetchone()['total']
        cursor.execute("SELECT COUNT(*) as done FROM daily_tasks WHERE task_date = ? AND company = ? AND status = ?", (date_str, comp, STATUS_DONE))
        done = cursor.fetchone()['done']
        summary.append({
            "company": comp,
            "total": total,
            "done": done,
            "pending": total - done
        })
    conn.close()
    return summary