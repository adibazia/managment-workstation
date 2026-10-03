from config import STATUS_DONE, STATUS_PENDING, STATUS_SKIPPED

def generate_eod_report(company, date_str, formatted_date, tasks, daily_note="", outreach_stats=None):
    """
    Generates a natural, human-written WhatsApp message without robotic formatting or emojis.
    Uses WhatsApp formatting (*bold* headers and clean hyphen bullets).
    """
    completed_tasks = [t for t in tasks if t['status'] == STATUS_DONE]
    pending_tasks = [t for t in tasks if t['status'] == STATUS_PENDING]
    skipped_tasks = [t for t in tasks if t['status'] == STATUS_SKIPPED]

    lines = []
    lines.append(f"*{company} - End of Day Progress Update*")
    lines.append(f"Date: {formatted_date}")
    lines.append("------------------------------------------")

    # Completed Section
    if completed_tasks:
        lines.append("\n*Completed Tasks:*")
        for item in completed_tasks:
            pri = f"[{item['priority'].upper()}] " if item['priority'] == 'High' else ""
            cat = f"({item['category']}) " if item['category'] != 'General' else ""
            lines.append(f"- {pri}{cat}{item['task_name']}")
    else:
        lines.append("\n*Completed Tasks:* None")

    # Pending / In-Progress Section
    if pending_tasks:
        lines.append("\n*Pending / In-Progress Tasks:*")
        for item in pending_tasks:
            pri = f"[{item['priority'].upper()}] " if item['priority'] == 'High' else ""
            rem = f" [Reminder: {item['reminder_date']}]" if item['reminder_date'] else ""
            lines.append(f"- {pri}{item['task_name']}{rem}")

    # Skipped Section
    if skipped_tasks:
        lines.append("\n*On Hold / Skipped:*")
        for item in skipped_tasks:
            lines.append(f"- {item['task_name']}")

    # Outreach Numbers (Lead Generation Specific)
    if outreach_stats and (outreach_stats.get('researched', 0) > 0 or outreach_stats.get('contacted', 0) > 0):
        lines.append("\n*Outreach & Lead Gen Metrics:*")
        lines.append(f"- Profiles Researched: {outreach_stats.get('researched', 0)}")
        lines.append(f"- Outreach Sent: {outreach_stats.get('contacted', 0)}")
        lines.append(f"- Responses Received: {outreach_stats.get('replies', 0)}")

    # Key Daily Notes / Scratchpad Summary
    if daily_note and daily_note.strip():
        lines.append("\n*Key Notes & Operational Summary:*")
        for note_line in daily_note.strip().splitlines():
            if note_line.strip():
                lines.append(f"- {note_line.strip()}")

    lines.append("\n------------------------------------------")
    lines.append("_Professional Work Record - End of Update_")
    return "\n".join(lines)

def generate_morning_agenda(company, formatted_date, tasks):
    """
    Generates a morning agenda shareable on WhatsApp.
    """
    pending_tasks = [t for t in tasks if t['status'] == STATUS_PENDING]
    lines = []
    lines.append(f"*{company} - Morning Action Plan*")
    lines.append(f"Date: {formatted_date}")
    lines.append("------------------------------------------")

    if pending_tasks:
        lines.append("\n*Today's Priority Agenda:*")
        for idx, item in enumerate(pending_tasks, start=1):
            pri = f"[{item['priority'].upper()}] " if item['priority'] == 'High' else ""
            lines.append(f"{idx}. {pri}{item['task_name']}")
    else:
        lines.append("\nNo pending agenda items queued.")

    lines.append("\n------------------------------------------")
    return "\n".join(lines)