import streamlit as st

# -----------------------
# Session state for storing all contracts and feedback
# -----------------------
if 'risk_data' not in st.session_state:
    st.session_state.risk_data = []

# -----------------------
# AI Analysis Function (Simple Rule-Based)
# -----------------------
def ai_analysis(contract_value, duration, penalty, scope):
    delay = 'High' if duration > 18 else 'Medium' if duration > 12 else 'Low'
    cost = 'High' if scope == 'Low' else 'Medium' if scope == 'Medium' else 'Low'
    claim = 'High' if penalty == 'No' else 'Low'

    insights = []
    if delay == 'High':
        insights.append("Long project duration")
    if cost == 'High':
        insights.append("Low scope clarity")
    if claim == 'High':
        insights.append("No penalty clause")

    return delay, cost, claim, insights

# -----------------------
# Helper function for colored risk
# -----------------------
def risk_badge(risk):
    color = {"Low": "🟢 Low", "Medium": "🟡 Medium", "High": "🔴 High"}
    return color.get(risk, risk)

# -----------------------
# App Header
# -----------------------
st.set_page_config(page_title="AI Contract Risk Demo", layout="wide")
st.title("🏗️ AI-Driven Contractual Risk Demo")
st.write("Interactive prototype to demonstrate AI risk analysis, consultant review, owner decision, and feedback loop.")
st.markdown("---")

# -----------------------
# Step 1: Contractor Input Form
# -----------------------
st.header("Step 1: Contractor Form")
with st.form("contractor_form"):
    col1, col2 = st.columns(2)
    with col1:
        contract_value = st.number_input("Contract Value", min_value=0)
        duration = st.number_input("Project Duration (months)", min_value=1)
    with col2:
        penalty = st.selectbox("Delay Penalty", ["Select", "Yes", "No"])
        scope = st.selectbox("Scope Clarity", ["Select", "Low", "Medium", "High"])
    submit_button = st.form_submit_button("Submit for AI Analysis")

if submit_button:
    if penalty == "Select" or scope == "Select":
        st.error("Please select valid options for Penalty and Scope")
    else:
        delay_risk, cost_risk, claim_risk, insights = ai_analysis(contract_value, duration, penalty, scope)
        st.session_state.current_analysis = {
            'contract_value': contract_value,
            'duration': duration,
            'penalty': penalty,
            'scope': scope,
            'delay_risk': delay_risk,
            'cost_risk': cost_risk,
            'claim_risk': claim_risk,
            'insights': insights
        }
        st.success("✅ AI Analysis completed!")
        st.markdown("### AI Risk Analysis Results:")
        col1, col2, col3 = st.columns(3)
        col1.metric("Delay Risk", risk_badge(delay_risk))
        col2.metric("Cost Risk", risk_badge(cost_risk))
        col3.metric("Claim Risk", risk_badge(claim_risk))
        st.info("**Insights / Flags:** " + ", ".join(insights) if insights else "No major flags.")

st.markdown("---")

# -----------------------
# Step 2: Consultant Review
# -----------------------
if 'current_analysis' in st.session_state and st.session_state.current_analysis is not None:
    st.header("Step 2: Consultant Review")
    analysis = st.session_state.current_analysis

    # Ensure delay_risk exists and provide fallback
    delay_default = analysis.get('delay_risk', 'Low')
    try:
        index = ["Low", "Medium", "High"].index(delay_default)
    except ValueError:
        index = 0  # fallback to Low

    adjust_delay = st.selectbox("Adjust Delay Risk (if needed)", ["Low", "Medium", "High"], index=index)
    
    if st.button("Confirm Consultant Review"):
        analysis['delay_risk'] = adjust_delay
        st.session_state.current_analysis = analysis
        st.success("✅ Consultant review confirmed.")

st.markdown("---")

# -----------------------
# Step 3: Owner Decision
# -----------------------
if 'current_analysis' in st.session_state and st.session_state.current_analysis is not None:
    st.header("Step 3: Owner Decision")
    owner_decision = st.radio("Select Owner Decision", ["Approve", "Hold", "Reject", "Partial Approval"])
    if st.button("Submit Owner Decision"):
        analysis = st.session_state.current_analysis
        analysis['owner_decision'] = owner_decision
        st.session_state.risk_data.append(analysis)
        st.session_state.current_analysis = None
        st.success(f"✅ Owner decision '{owner_decision}' saved!")

st.markdown("---")

# -----------------------
# Step 4: Dashboard & Feedback Loop
# -----------------------
if st.session_state.risk_data:
    st.header("Step 4: Dashboard & Feedback Loop")
    for i, item in enumerate(st.session_state.risk_data, start=1):
        with st.container():
            st.markdown(f"### Contract #{i}")
            col1, col2, col3, col4 = st.columns(4)
            col1.write(f"**Value:** {item['contract_value']}")
            col2.write(f"**Duration:** {item['duration']} months")
            col3.write(f"**Penalty:** {item['penalty']}")
            col4.write(f"**Scope:** {item['scope']}")
            col1.metric("Delay Risk", risk_badge(item['delay_risk']))
            col2.metric("Cost Risk", risk_badge(item['cost_risk']))
            col3.metric("Claim Risk", risk_badge(item['claim_risk']))
            col4.info("Insights: " + ", ".join(item['insights']) if item['insights'] else "No major flags.")
            st.success("Owner Decision: " + item.get('owner_decision', 'Pending'))
            st.markdown("---")
