# import streamlit as st
# from services.github_service import GitHubService

# st.title("GitHub Analyzer - Test Module")

# url = st.text_input("Enter GitHub Profile URL")

# if st.button("Fetch Data"):
#     try:
#         service = GitHubService()
#         data = service.analyze_profile(url)

#         st.success("Profile Fetched Successfully!")

#         st.subheader("Profile Info")
#         st.json(data["profile"])

#         st.subheader("Repositories Count")
#         st.write(len(data["repositories"]))

#         st.subheader("Rate Limit Status")
#         st.json(data["rate_limit"])

#     except Exception as e:
#         st.error(str(e))


import streamlit as st
from services.github_service import GitHubService

st.title("GitHub Full Analyzer")

url = st.text_input("Enter GitHub Profile URL")

if st.button("Extract Full Data"):
    try:
        service = GitHubService()
        data = service.analyze_profile(url)

        username = data["profile"]["username"]
        file_path = service.save_to_file(data, username)

        st.success("Data Extracted Successfully!")
        st.write(f"Saved locally at: {file_path}")

        st.write("Total Repositories:", len(data["repositories"]))
        
        st.subheader("Rate Limit Status")
        st.json(data["rate_limit"])

    except Exception as e:
        st.error(str(e))
