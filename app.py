

# import streamlit as st
# import json
# import os
# from services.github_service import GitHubService
# from services.ai_scoring_service import AIScoringService

# st.set_page_config(page_title="GitHub Portfolio Analyzer", layout="wide")

# st.title("🚀 AI-Powered GitHub Portfolio Analyzer")

# # ----------------------------------------
# # Sidebar Input Option
# # ----------------------------------------

# st.sidebar.header("📂 Data Source")

# data_source = st.sidebar.radio(
#     "Choose Input Method",
#     ["Enter GitHub URL", "Upload Existing JSON File"]
# )

# # ----------------------------------------
# # OPTION 1: Fetch from GitHub
# # ----------------------------------------

# if data_source == "Enter GitHub URL":

#     url = st.text_input("Enter GitHub Profile URL")

#     if st.button("🔍 Fetch GitHub Data"):
#         try:
#             service = GitHubService()
#             data = service.analyze_profile(url)

#             username = data["profile"]["username"]
#             file_path = service.save_to_file(data, username)

#             st.success("✅ GitHub Data Extracted Successfully!")
#             st.write(f"Saved locally at: {file_path}")

#             st.session_state["github_data"] = data

#         except Exception as e:
#             st.error(str(e))


# # ----------------------------------------
# # OPTION 2: Upload JSON
# # ----------------------------------------

# elif data_source == "Upload Existing JSON File":

#     uploaded_file = st.file_uploader("Upload GitHub JSON File", type=["json"])

#     if uploaded_file:
#         try:
#             data = json.load(uploaded_file)
#             st.success("✅ JSON Loaded Successfully!")
#             st.session_state["github_data"] = data
#         except:
#             st.error("Invalid JSON file.")


# # ----------------------------------------
# # Show Profile Info
# # ----------------------------------------

# if "github_data" in st.session_state:

#     github_data = st.session_state["github_data"]
#     username = github_data["profile"]["username"]

#     st.divider()
#     st.header("👤 Profile Overview")
#     st.json(github_data["profile"])
#     st.write("Total Repositories:", len(github_data["repositories"]))

#     # ----------------------------------------
#     # AI SCORING SECTION
#     # ----------------------------------------

#     st.divider()
#     st.header("🤖 AI Portfolio Evaluation")

#     result_path = f"data/ai_results/{username}_analysis.json"

#     if st.button("⚡ Run AI Scoring"):

#         scorer = AIScoringService()

#         with st.spinner("Running AI Analysis... ⏳"):
#             portfolio_result = scorer.analyze_portfolio(github_data)

#         if portfolio_result:
#             file_path = scorer.save_ai_result(portfolio_result, username)
#             st.success(f"✅ AI Analysis Saved at: {file_path}")
#         else:
#             st.error("AI analysis failed.")

#     # ----------------------------------------
#     # ALWAYS LOAD FROM FILE (Safe Mode)
#     # ----------------------------------------

#     if os.path.exists(result_path):

#         with open(result_path, "r", encoding="utf-8") as f:
#             saved_result = json.load(f)

#         st.success("📂 Loaded Saved AI Analysis")

#         # ----------------------------------------
#         # Portfolio Score
#         # ----------------------------------------

#         st.subheader("🏆 Portfolio Score")
#         st.metric("Overall Score", f"{saved_result['portfolio_score']} / 100")

#         st.write("### 💪 Strengths")
#         st.write(saved_result["strengths"])

#         st.write("### ⚠ Weaknesses")
#         st.write(saved_result["weaknesses"])

#         st.write("### 📌 Hiring Recommendation")
#         st.write(saved_result["recommendation"])

#         # ----------------------------------------
#         # Repo Level Analysis
#         # ----------------------------------------

#         st.divider()
#         st.header("📂 Repository-Level Analysis")

#         for repo in saved_result["repo_analyses"]:
#             with st.expander(f"🔎 {repo.get('repo_name')}"):

#                 col1, col2 = st.columns(2)

#                 col1.metric("Technical Depth", repo.get("technical_depth_score", 0))
#                 col1.metric("Complexity", repo.get("project_complexity_score", 0))

#                 col2.metric("Code Quality", repo.get("code_quality_score", 0))
#                 col2.metric("Innovation", repo.get("innovation_score", 0))

#                 st.write("### Summary")
#                 st.write(repo.get("summary"))

#     else:
#         st.info("⚡ Run AI scoring to generate portfolio analysis.")

# else:
#     st.info("⬆ Please fetch GitHub data or upload a JSON file first.")


import streamlit as st
import json
import os
from services.github_service import GitHubService
from services.ai_scoring_service import AIScoringService

st.set_page_config(page_title="GitHub Portfolio Analyzer", layout="wide")

st.title("🚀 AI-Powered GitHub Portfolio Analyzer")

st.markdown("### Turn Your GitHub Into Recruiter-Ready Proof")

# ----------------------------------------
# INPUT URL
# ----------------------------------------

url = st.text_input("Enter GitHub Profile URL")

if st.button("⚡ Analyze Portfolio"):

    if not url:
        st.error("Please enter a GitHub profile URL.")
        st.stop()

    # ----------------------------------------
    # STEP 1: Fetch GitHub Data
    # ----------------------------------------

    with st.spinner("🔍 Fetching GitHub data..."):

        try:
            github_service = GitHubService()
            github_data = github_service.analyze_profile(url)

            username = github_data["profile"]["username"]

            github_file_path = github_service.save_to_file(
                github_data, username
            )

        except Exception as e:
            st.error(f"GitHub Error: {e}")
            st.stop()

    st.success("✅ GitHub Data Fetched Successfully")
    st.write(f"Saved at: {github_file_path}")

    # ----------------------------------------
    # STEP 2: Run Gemini AI Analysis
    # ----------------------------------------

    with st.spinner("🤖 Running AI Portfolio Evaluation..."):

        try:
            ai_service = AIScoringService()

            portfolio_result = ai_service.analyze_portfolio(
                github_data
            )

            if not portfolio_result:
                st.error("AI analysis failed.")
                st.stop()

            ai_file_path = ai_service.save_ai_result(
                portfolio_result, username
            )

        except Exception as e:
            st.error(f"AI Error: {e}")
            st.stop()

    st.success("🎯 AI Analysis Completed")
    st.write(f"AI Analysis saved at: {ai_file_path}")

    # ----------------------------------------
    # STEP 3: Load Stored AI Result
    # ----------------------------------------

    with open(ai_file_path, "r", encoding="utf-8") as f:
        saved_result = json.load(f)

    # ----------------------------------------
    # STEP 4: Display Results
    # ----------------------------------------

    st.divider()
    st.header("🏆 Portfolio Score")

    st.metric("Overall Score", f"{saved_result['portfolio_score']} / 100")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💪 Strengths")
        st.write(saved_result["strengths"])

    with col2:
        st.subheader("⚠ Weaknesses")
        st.write(saved_result["weaknesses"])

    st.subheader("📌 Hiring Recommendation")
    st.write(saved_result["recommendation"])

    # ----------------------------------------
    # Repo-Level Analysis
    # ----------------------------------------

    st.divider()
    st.header("📂 Repository-Level Analysis")

    for repo in saved_result["repo_analyses"]:
        with st.expander(f"🔎 {repo.get('repo_name')}"):

            col1, col2 = st.columns(2)

            col1.metric("Technical Depth", repo.get("technical_depth_score", 0))
            col1.metric("Complexity", repo.get("project_complexity_score", 0))

            col2.metric("Code Quality", repo.get("code_quality_score", 0))
            col2.metric("Innovation", repo.get("innovation_score", 0))

            st.write("### Summary")
            st.write(repo.get("summary"))
