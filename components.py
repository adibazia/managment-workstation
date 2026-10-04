import streamlit as st
from database.db_handler import get_system_settings
from services.task_service import update_task_details, move_task_up
from config import STATUS_DONE, STATUS_PENDING, STATUS_SKIPPED

def render_login():
    """Executive Clean Login Card with Adiba Zia Designed Footer."""
    settings = get_system_settings()

    st.markdown("""
        <div style="max-width: 450px; margin: 45px auto 25px auto; padding: 32px 36px; background: #FFFFFF; border-radius: 14px; box-shadow: 0 10px 30px rgba(11, 25, 44, 0.08); border: 1px solid #E2E8F0; text-align: center;">
            <div style="background: linear-gradient(135deg, #070F2B 0%, #1E3E62 100%); width: 54px; height: 54px; border-radius: 12px; margin: 0 auto 16px auto; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 15px rgba(7, 15, 43, 0.25);">
                <span style="color: #38BDF8; font-size: 26px; font-weight: 800;">M</span>
            </div>
            <h2 style="color: #070F2B; margin: 0 0 6px 0; font-size: 26px; font-weight: 800; letter-spacing: -0.5px;">Management Workstation</h2>
            <p style="color: #64748B; font-size: 14px; margin: 0; font-weight: 500;">Secure executive access portal</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.3, 1])
    with col2:
        with st.container(border=True):
            with st.form("login_form", clear_on_submit=False):
                username_input = st.text_input("Username", key="login_user", placeholder="Enter username", autocomplete="username")
                password_input = st.text_input("Password", type="password", key="login_pass", placeholder="Enter password", autocomplete="current-password")
                st.write("")
                submit = st.form_submit_button("Sign In to Workstation", use_container_width=True)

                if submit:
                    if username_input == settings["username"] and password_input == settings["password"]:
                        st.session_state["authenticated"] = True
                        st.session_state["user"] = username_input
                        st.rerun()
                    else:
                        st.error("Invalid credentials. Please verify your username and password.")

    # Transparent footer
    st.markdown("""
        <div style="margin-top: 70px; text-align: center; opacity: 0.55;">
            <p style="font-size: 13px; font-weight: 600; color: #64748B; letter-spacing: 0.5px; margin: 0;">
                System designed by Adiba Zia
            </p>
        </div>
    """, unsafe_allow_html=True)

def render_task_row(task, on_status_change, on_delete, selected_date_str, selected_company, show_priority=True, show_reminders=True):
    """Clean ClickUp style task row."""
    task_id = task['id']
    task_name = task['task_name']
    status = task['status']
    priority = task['priority'] if 'priority' in task.keys() and task['priority'] else "Medium"
    category = task['category'] if 'category' in task.keys() and task['category'] else "General"
    reminder = task['reminder_date'] if 'reminder_date' in task.keys() and task['reminder_date'] else ""

    is_done = (status == STATUS_DONE)
    is_skipped = (status == STATUS_SKIPPED)

    # Priority Badges
    priority_html = ""
    if show_priority:
        if priority == "High":
            priority_html = "<span class='badge-high'>HIGH</span>"
        elif priority == "Medium":
            priority_html = "<span class='badge-med'>MED</span>"
        else:
            priority_html = "<span class='badge-low'>LOW</span>"

    # Status Badge
    if is_done:
        status_html = "<span class='badge-done'>DONE</span>"
    elif is_skipped:
        status_html = "<span class='badge-low'>SKIPPED</span>"
    else:
        status_html = "<span class='badge-pending'>PENDING</span>"

    with st.container(border=True):
        col_main, col_tags = st.columns([5, 2.5])
        
        with col_main:
            if is_done:
                st.markdown(f"<span style='text-decoration: line-through; color: #94A3B8; font-size: 15px;'>{task_name}</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='color: #0F172A; font-size: 15px; font-weight: 700;'>{task_name}</span>", unsafe_allow_html=True)
            
            if show_reminders and reminder:
                st.markdown(f"<span style='font-size: 12px; color: #D97706; font-weight: 600;'>Follow-up Reminder: {reminder}</span>", unsafe_allow_html=True)

        with col_tags:
            cat_html = f"<span style='font-size: 11px; background: #F1F5F9; color: #475569; padding: 3px 8px; border-radius: 4px; font-weight: 600; margin-right: 6px;'>{category}</span>" if category != "General" else ""
            st.markdown(f"<div style='text-align: right;'>{cat_html}{priority_html} {status_html}</div>", unsafe_allow_html=True)

        st.write("")
        c_done, c_skip, c_up, c_more, c_del = st.columns([1.2, 1, 0.8, 1.2, 0.8])
        
        with c_done:
            if not is_done:
                if st.button("Complete", key=f"btn_done_{task_id}", use_container_width=True):
                    on_status_change(task_id, STATUS_DONE)
            else:
                if st.button("Re-open", key=f"btn_pend_{task_id}", use_container_width=True):
                    on_status_change(task_id, STATUS_PENDING)

        with c_skip:
            if not is_skipped:
                if st.button("Skip", key=f"btn_skip_{task_id}", use_container_width=True):
                    on_status_change(task_id, STATUS_SKIPPED)
            else:
                if st.button("Restore", key=f"btn_restore_{task_id}", use_container_width=True):
                    on_status_change(task_id, STATUS_PENDING)

        with c_up:
            if st.button("▲ Up", key=f"btn_up_{task_id}", use_container_width=True):
                move_task_up(task_id, selected_date_str, selected_company)
                st.rerun()

        with c_more:
            with st.popover("⋮ More", use_container_width=True):
                st.markdown("**Task Details**")
                p_opts = ["High", "Medium", "Low"]
                curr_p_idx = p_opts.index(priority) if priority in p_opts else 1
                new_p = st.selectbox("Priority", p_opts, index=curr_p_idx, key=f"pop_p_{task_id}")

                c_opts = ["General", "Lead Gen", "Client Outreach", "Dev / Tech", "Operations"]
                curr_c_idx = c_opts.index(category) if category in c_opts else 0
                new_c = st.selectbox("Category", c_opts, index=curr_c_idx, key=f"pop_c_{task_id}")

                new_rem = st.text_input("Follow-up Date", value=reminder, key=f"pop_r_{task_id}")

                if st.button("Save", key=f"save_pop_{task_id}", use_container_width=True):
                    update_task_details(task_id, new_p, new_c, new_rem.strip())
                    st.rerun()

        with c_del:
            if st.button("✕", key=f"btn_del_{task_id}", use_container_width=True):
                on_delete(task_id)
