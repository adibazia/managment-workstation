import streamlit as st
from config import STATUS_DONE, STATUS_PENDING
from services.task_service import get_outreach_metrics, update_outreach_metric

def render_app_header(company, selected_date, tasks):
    """Executive Navy Banner with White Text and Stat Boxes."""
    formatted_date = selected_date.strftime("%A, %d %B %Y")
    total_count = len(tasks)
    completed_count = len([t for t in tasks if t['status'] == STATUS_DONE])
    pending_count = len([t for t in tasks if t['status'] == STATUS_PENDING])

    st.markdown(f"""
        <div class="exec-banner">
            <div>
                <h1 class="banner-title">{company}</h1>
                <p class="banner-sub">{formatted_date} &bull; Executive Operations Portal</p>
            </div>
            <div style="display: flex; gap: 14px;">
                <div class="stat-pill">
                    <div class="stat-val">{total_count}</div>
                    <div class="stat-name">Total</div>
                </div>
                <div class="stat-pill">
                    <div class="stat-val" style="color: #34D399;">{completed_count}</div>
                    <div class="stat-name">Done</div>
                </div>
                <div class="stat-pill">
                    <div class="stat-val" style="color: #F87171;">{pending_count}</div>
                    <div class="stat-name">Pending</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_outreach_tracker(date_str, company):
    """Daily Lead Generation & Outreach Target Counter Bar."""
    metrics = get_outreach_metrics(date_str, company)
    
    with st.container(border=True):
        st.markdown("<p style='font-size: 13px; font-weight: 700; color: #475569; margin: 0 0 10px 0; text-transform: uppercase;'>Daily Lead Gen & Outreach Target Counter</p>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"**Researched Leads:** `{metrics['researched']}`")
            b_sub, b_add = st.columns(2)
            with b_sub:
                if st.button("-5", key="sub_res", use_container_width=True):
                    update_outreach_metric(date_str, company, "researched", -5)
                    st.rerun()
            with b_add:
                if st.button("+5", key="add_res", use_container_width=True):
                    update_outreach_metric(date_str, company, "researched", 5)
                    st.rerun()

        with col2:
            st.markdown(f"**Messages Sent:** `{metrics['contacted']}`")
            b_sub2, b_add2 = st.columns(2)
            with b_sub2:
                if st.button("-1", key="sub_con", use_container_width=True):
                    update_outreach_metric(date_str, company, "contacted", -1)
                    st.rerun()
            with b_add2:
                if st.button("+1", key="add_con", use_container_width=True):
                    update_outreach_metric(date_str, company, "contacted", 1)
                    st.rerun()

        with col3:
            st.markdown(f"**Responses Received:** `{metrics['replies']}`")
            b_sub3, b_add3 = st.columns(2)
            with b_sub3:
                if st.button("-1", key="sub_rep", use_container_width=True):
                    update_outreach_metric(date_str, company, "replies", -1)
                    st.rerun()
            with b_add3:
                if st.button("+1", key="add_rep", use_container_width=True):
                    update_outreach_metric(date_str, company, "replies", 1)
                    st.rerun()

def render_app_footer():
    """Minimalist Professional Footer."""
    st.markdown("""
        <div style="margin-top: 50px; padding: 20px 0; border-top: 1px solid #E2E8F0; text-align: center;">
            <p style="margin: 0; font-size: 13px; color: #64748B; font-weight: 600;">
                Work Management Hub &bull; Dedicated Executive System &bull; Secure Local Database
            </p>
        </div>
    """, unsafe_allow_html=True)