import streamlit as st
import json
import os
import plotly.graph_objects as go
from services.github_service import GitHubService
from services.ai_scoring_service import AIScoringService

st.set_page_config(page_title="AI GitHub Portfolio Analyzer", layout="wide")

st.title("🚀 AI-Powered GitHub Portfolio Analyzer")
st.markdown("### Transform Your GitHub Into Recruiter-Ready Proof")

st.markdown("""
This AI system evaluates your GitHub profile like a senior recruiter and provides:

✔ Portfolio Score  
✔ Strengths & Weaknesses  
✔ Personalized Improvement Roadmap  
✔ Repository-Level Analysis  
""")

# ----------------------------------------
# Circular Gauge
# ----------------------------------------

def show_score_gauge(score):

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Portfolio Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#00C49F"},
            'steps': [
                {'range': [0, 50], 'color': "#ff4d4d"},
                {'range': [50, 75], 'color': "#ffa500"},
                {'range': [75, 100], 'color': "#2ecc71"}
            ],
        }
    ))

    fig.update_layout(height=350)
    st.plotly_chart(fig, width="stretch")

# ----------------------------------------
# INPUT
# ----------------------------------------

url = st.text_input("🔗 Enter GitHub Profile URL")

if st.button("⚡ Analyze Portfolio"):

    if not url:
        st.error("Please enter a GitHub profile URL.")
        st.stop()

    # STEP 1: Fetch GitHub Data
    with st.spinner("🔍 Fetching GitHub data..."):
        github_service = GitHubService()
        github_data = github_service.analyze_profile(url)
        username = github_data["profile"]["username"]
        github_file = github_service.save_to_file(github_data, username)

    # STEP 2: Run AI
    with st.spinner("🤖 Running AI Portfolio Evaluation..."):
        ai_service = AIScoringService()
        portfolio_result = ai_service.analyze_portfolio(github_data)

        if not portfolio_result:
            st.error("AI analysis failed.")
            st.stop()

        ai_file = ai_service.save_ai_result(portfolio_result, username)

    # STEP 3: Load Result
    with open(ai_file, "r", encoding="utf-8") as f:
        result = json.load(f)

    # STEP 4: Display
    st.divider()
    show_score_gauge(result["portfolio_score"])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💪 Strengths")
        st.success(result["strengths"])

    with col2:
        st.subheader("⚠ Weaknesses")
        st.warning(result["weaknesses"])

    # ----------------------------------------
    # Improvement Section
    # ----------------------------------------

    st.divider()
    st.header("🚀 How to Improve Your GitHub Profile")

    for i, rec in enumerate(result["improvement_recommendations"], 1):
        st.markdown(f"""
        <div style="
            background-color:#111827;
            padding:15px;
            border-radius:10px;
            margin-bottom:10px;
            border-left:5px solid #00C49F;">
            <strong>{i}. {rec}</strong>
        </div>
        """, unsafe_allow_html=True)

    # ----------------------------------------
    # Repo-Level Analysis
    # ----------------------------------------

    st.divider()
    st.header("📂 Repository-Level Analysis")

    for repo in result["repo_analyses"]:
        with st.expander(f"🔎 {repo.get('repo_name')}"):

            col1, col2 = st.columns(2)

            col1.metric("Technical Depth", repo.get("technical_depth_score", 0))
            col1.metric("Complexity", repo.get("project_complexity_score", 0))
            col2.metric("Code Quality", repo.get("code_quality_score", 0))
            col2.metric("Innovation", repo.get("innovation_score", 0))

            st.write("### Summary")
            st.write(repo.get("summary"))

    # ----------------------------------------
    # STEP 5: Delete Files After Display
    # ----------------------------------------

    try:
        if os.path.exists(github_file):
            os.remove(github_file)
        if os.path.exists(ai_file):
            os.remove(ai_file)
    except:
        pass
