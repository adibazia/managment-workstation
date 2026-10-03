from datetime import date
import streamlit as st

st.set_page_config(
    page_title="Work Management Hub",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

from config import COMPANIES, STATUS_DONE, STATUS_PENDING, STATUS_SKIPPED
from database.db_handler import initialize_database
from services.task_service import (
    initialize_day_tasks,
    get_tasks_by_date,
    add_daily_task,
    update_task_status,
    delete_daily_task,
    get_routine_templates,
    add_routine_template,
    delete_routine_template,
    get_daily_note,
    save_daily_note,
    get_outreach_metrics,
    get_all_companies_summary
)
from services.report_service import generate_eod_report, generate_morning_agenda
from ui.styles import inject_styles
from ui.components import render_login, render_task_row
from ui.layout import render_app_header, render_outreach_tracker, render_app_footer

# 1. Initialize
initialize_database()
inject_styles()

# 2. Authentication Check
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    render_login()
    st.stop()

# 3. Sidebar
with st.sidebar:
    st.markdown("### Workspaces")
    if "current_company" not in st.session_state:
        st.session_state["current_company"] = COMPANIES[0]

    selected_company = st.selectbox(
        "Select Active Workspace",
        COMPANIES,
        index=COMPANIES.index(st.session_state["current_company"]),
        key="sidebar_company_select"
    )
    st.session_state["current_company"] = selected_company

    st.markdown("---")
    st.markdown("### Date Selection")
    selected_date = st.date_input("Date", value=date.today(), label_visibility="collapsed")
    selected_date_str = str(selected_date)

    st.markdown("---")
    st.caption(f"Logged in as: **{st.session_state.get('user', 'Adiba')}**")
    if st.button("Sign Out", use_container_width=True):
        st.session_state["authenticated"] = False
        st.rerun()

# 4. Top Quick Workspace Switcher Bar
st.write("")
comp_cols = st.columns(len(COMPANIES))
for idx, comp in enumerate(COMPANIES):
    with comp_cols[idx]:
        is_active = (comp == selected_company)
        btn_type = "primary" if is_active else "secondary"
        if st.button(comp, key=f"quick_comp_{comp}", type=btn_type, use_container_width=True):
            st.session_state["current_company"] = comp
            st.rerun()

# 5. Initialize Tasks
initialize_day_tasks(selected_date_str, selected_company)
current_day_tasks = get_tasks_by_date(selected_date_str, selected_company)

# 6. Hero Header & Outreach Tracker
render_app_header(selected_company, selected_date, current_day_tasks)
render_outreach_tracker(selected_date_str, selected_company)

# 7. Navigation Tabs
tab_tasks, tab_notes, tab_routines, tab_eod, tab_master = st.tabs([
    "Tasks Overview",
    "Daily Scratchpad",
    "Routine Library",
    "WhatsApp EOD Report",
    "Master 5-Company Overview"
])

# --- TAB 1: TASKS OVERVIEW ---
with tab_tasks:
    # Quick Add & Filter Row
    col_input, col_pri, col_cat, col_btn = st.columns([4, 1.2, 1.2, 1.2])
    with col_input:
        new_task_name = st.text_input(
            "Add Task",
            placeholder="Type task details and press Add...",
            label_visibility="collapsed",
            key="input_new_task"
        )
    with col_pri:
        quick_priority = st.selectbox("Priority", ["Medium", "High", "Low"], label_visibility="collapsed", key="quick_pri")
    with col_cat:
        quick_category = st.selectbox("Category", ["General", "Lead Gen", "Client Outreach", "Dev / Tech", "Operations"], label_visibility="collapsed", key="quick_cat")
    with col_btn:
        if st.button("Add Task", type="primary", use_container_width=True):
            if new_task_name.strip():
                add_daily_task(selected_date_str, selected_company, new_task_name, priority=quick_priority, category=quick_category)
                st.rerun()

    # Search & Filter Bar
    f1, f2 = st.columns([3, 1])
    with f1:
        search_query = st.text_input("Search Tasks", placeholder="Search tasks by name...", label_visibility="collapsed", key="search_tasks")
    with f2:
        filter_status = st.selectbox("Filter Status", ["All", "Pending", "Done"], label_visibility="collapsed", key="filter_st")

    st.write("")
    
    # Filter Logic
    filtered_tasks = current_day_tasks
    if search_query.strip():
        filtered_tasks = [t for t in filtered_tasks if search_query.lower() in t['task_name'].lower()]
    if filter_status == "Pending":
        filtered_tasks = [t for t in filtered_tasks if t['status'] == STATUS_PENDING]
    elif filter_status == "Done":
        filtered_tasks = [t for t in filtered_tasks if t['status'] == STATUS_DONE]

    if not filtered_tasks:
        st.info("No matching tasks found. Add a task above to get started.")
    else:
        for t in filtered_tasks:
            def handle_status_change(t_id=t['id'], new_st=None):
                update_task_status(t_id, new_st)
                st.rerun()

            def handle_delete(t_id=t['id']):
                delete_daily_task(t_id)
                st.rerun()

            render_task_row(
                task=t,
                on_status_change=handle_status_change,
                on_delete=handle_delete,
                selected_date_str=selected_date_str,
                selected_company=selected_company
            )

# --- TAB 2: SCRATCHPAD NOTES ---
with tab_notes:
    st.subheader("Daily Work Notes & Accomplishments")
    st.caption("Auto-saved notes that automatically include inside your professional WhatsApp EOD update.")

    existing_note = get_daily_note(selected_date_str, selected_company)
    note_text = st.text_area(
        "Notes Content",
        value=existing_note,
        height=220,
        placeholder="Document meetings, key achievements, or notes for this date...",
        label_visibility="collapsed"
    )

    if st.button("Save Notes", type="primary", use_container_width=False):
        save_daily_note(selected_date_str, selected_company, note_text)
        st.success("Notes saved successfully.")

# --- TAB 3: ROUTINE LIBRARY ---
with tab_routines:
    st.subheader("Permanent Routine Task Library")
    st.caption("Configured routine tasks load automatically every morning.")

    col_r_in, col_r_pri, col_r_btn = st.columns([4, 1.5, 1.5])
    with col_r_in:
        routine_input = st.text_input("Routine Task", placeholder="e.g. Prospect qualification and initial messaging", label_visibility="collapsed", key="input_routine_task")
    with col_r_pri:
        routine_pri = st.selectbox("Routine Priority", ["High", "Medium", "Low"], label_visibility="collapsed", key="r_pri")
    with col_r_btn:
        if st.button("Save Routine", type="primary", use_container_width=True):
            if routine_input.strip():
                add_routine_template(selected_company, routine_input, priority=routine_pri)
                st.rerun()

    st.write("")
    saved_routines = get_routine_templates(selected_company)

    if not saved_routines:
        st.write("No repeating routines saved for this workspace.")
    else:
        for r in saved_routines:
            with st.container(border=True):
                col_lbl, col_act = st.columns([5, 1])
                with col_lbl:
                    st.markdown(f"**{r['task_name']}** &bull; `[{r['priority']}]`")
                with col_act:
                    if st.button("Delete", key=f"del_routine_{r['id']}", use_container_width=True):
                        delete_routine_template(r['id'])
                        st.rerun()

# --- TAB 4: WHATSAPP EOD REPORT ---
with tab_eod:
    st.subheader("Professional WhatsApp Update (Zero Emojis)")
    st.caption("Formatted directly for WhatsApp. Click Copy in the top right of the code box.")

    current_note = get_daily_note(selected_date_str, selected_company)
    outreach_data = get_outreach_metrics(selected_date_str, selected_company)
    formatted_date_str = selected_date.strftime("%A, %d %B %Y")

    report_text = generate_eod_report(
        company=selected_company,
        date_str=selected_date_str,
        formatted_date=formatted_date_str,
        tasks=current_day_tasks,
        daily_note=current_note,
        outreach_stats=outreach_data
    )

    st.code(report_text, language="text")

    st.write("")
    st.subheader("Morning Action Plan Share")
    agenda_text = generate_morning_agenda(selected_company, formatted_date_str, current_day_tasks)
    st.code(agenda_text, language="text")

# --- TAB 5: MASTER 5-COMPANY OVERVIEW ---
with tab_master:
    st.subheader("Master Daily Overview across Workspaces")
    st.caption(f"Status summary for {selected_date.strftime('%A, %d %B %Y')}")

    master_summary = get_all_companies_summary(selected_date_str, COMPANIES)
    for s in master_summary:
        with st.container(border=True):
            c_name, c_tot, c_don, c_pen = st.columns([3, 1, 1, 1])
            with c_name:
                st.markdown(f"### {s['company']}")
            with c_tot:
                st.metric("Total Tasks", s['total'])
            with c_don:
                st.metric("Completed", s['done'])
            with c_pen:
                st.metric("Pending", s['pending'])

# 8. Footer
render_app_footer()