# import os
# import json
# import time
# import google.generativeai as genai
# from dotenv import load_dotenv

# load_dotenv()


# class AIScoringService:

#     def __init__(self):
#         genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
#         self.model = genai.GenerativeModel("gemini-2.5-flash")

#     # ----------------------------------
#     # Safe JSON extractor (handles ```json``` wrapping)
#     # ----------------------------------
#     def safe_json_parse(self, text):
#         try:
#             text = text.strip()

#             if text.startswith("```"):
#                 text = text.replace("```json", "")
#                 text = text.replace("```", "")
#                 text = text.strip()

#             return json.loads(text)

#         except Exception as e:
#             print("JSON Parsing Error:", e)
#             return None

#     # ----------------------------------
#     # Trim README
#     # ----------------------------------
#     def trim_readme(self, readme, max_chars=2000):
#         if not readme:
#             return ""
#         return readme[:max_chars]

#     # ----------------------------------
#     # Prepare compact repo summary
#     # ----------------------------------
#     def prepare_repo_summary(self, repo):
#         return {
#             "name": repo.get("name"),
#             "language": repo.get("language"),
#             "stars": repo.get("stars"),
#             "forks": repo.get("forks"),
#             "watchers": repo.get("watchers"),
#             "total_commits": repo.get("commit_stats", {}).get("total_commits", 0),
#             "owner_commits": repo.get("commit_stats", {}).get("owner_commits", 0),
#             "has_collaborators": repo.get("commit_stats", {}).get("has_collaborators", False),
#             "readme": self.trim_readme(repo.get("readme"))
#         }

#     # ----------------------------------
#     # Analyze batch of repos
#     # ----------------------------------
#     def analyze_batch(self, batch_repos):

#         prompt = f"""
# You are a senior AI recruiter and GitHub portfolio evaluator.

# Analyze EACH repository separately.

# Return STRICT JSON only:

# [
#   {{
#     "repo_name": "...",
#     "technical_depth_score": 0-10,
#     "project_complexity_score": 0-10,
#     "code_quality_score": 0-10,
#     "innovation_score": 0-10,
#     "summary": "Short professional evaluation"
#   }}
# ]

# Repositories Data:
# {json.dumps(batch_repos, indent=2)}
# """

#         try:
#             response = self.model.generate_content(prompt)
#             parsed = self.safe_json_parse(response.text)
#             return parsed if parsed else []

#         except Exception as e:
#             print("Gemini Batch Error:", e)
#             time.sleep(8)
#             return []

#     # ----------------------------------
#     # Generate final portfolio score
#     # ----------------------------------
#     def generate_portfolio_score(self, repo_summaries):

#         prompt = f"""
# You are a senior AI hiring evaluator.

# Based on the repository evaluations below, generate:

# Return STRICT JSON:

# {{
#   "portfolio_score": 0-100,
#   "strengths": "...",
#   "weaknesses": "...",
#   "recommendation": "Strong Hire / Hire / Maybe / No Hire"
# }}

# Repository Evaluations:
# {json.dumps(repo_summaries, indent=2)}
# """

#         try:
#             response = self.model.generate_content(prompt)
#             parsed = self.safe_json_parse(response.text)
#             return parsed if parsed else {}

#         except Exception as e:
#             print("Gemini Portfolio Error:", e)
#             time.sleep(8)
#             return {}

#     # ----------------------------------
#     # MAIN METHOD
#     # ----------------------------------
#     def analyze_portfolio(self, github_data):

#         repositories = github_data.get("repositories", [])

#         batch_size = 10
#         all_repo_results = []

#         for i in range(0, len(repositories), batch_size):

#             batch = repositories[i:i + batch_size]

#             print(f"🔍 Processing Batch {i//batch_size + 1}")

#             prepared_batch = [
#                 self.prepare_repo_summary(repo)
#                 for repo in batch
#             ]

#             batch_result = self.analyze_batch(prepared_batch)

#             if batch_result:
#                 all_repo_results.extend(batch_result)

#         if not all_repo_results:
#             return None

#         portfolio_result = self.generate_portfolio_score(all_repo_results)

#         if not portfolio_result:
#             return None

#         return {
#             "portfolio_score": portfolio_result.get("portfolio_score", 0),
#             "strengths": portfolio_result.get("strengths", ""),
#             "weaknesses": portfolio_result.get("weaknesses", ""),
#             "recommendation": portfolio_result.get("recommendation", ""),
#             "repo_analyses": all_repo_results
#         }

#     # ----------------------------------
#     # Save AI result locally
#     # ----------------------------------
#     def save_ai_result(self, result, username):
#         os.makedirs("data/ai_results", exist_ok=True)
#         file_path = f"data/ai_results/{username}_analysis.json"

#         with open(file_path, "w", encoding="utf-8") as f:
#             json.dump(result, f, indent=4)

#         return file_path


# import os
# import json
# import time
# import google.generativeai as genai
# from dotenv import load_dotenv

# load_dotenv()


# class AIScoringService:

#     def __init__(self):
#         genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
#         self.model = genai.GenerativeModel("gemini-2.5-flash")

#     # ----------------------------------
#     # Safe JSON extractor
#     # ----------------------------------
#     def safe_json_parse(self, text):
#         try:
#             text = text.strip()
#             if text.startswith("```"):
#                 text = text.replace("```json", "")
#                 text = text.replace("```", "")
#                 text = text.strip()
#             return json.loads(text)
#         except Exception as e:
#             print("JSON Parsing Error:", e)
#             return None

#     # ----------------------------------
#     # Trim README
#     # ----------------------------------
#     def trim_readme(self, readme, max_chars=2000):
#         if not readme:
#             return ""
#         return readme[:max_chars]

#     # ----------------------------------
#     # Prepare repo summary
#     # ----------------------------------
#     def prepare_repo_summary(self, repo):
#         return {
#             "name": repo.get("name"),
#             "language": repo.get("language"),
#             "stars": repo.get("stars"),
#             "forks": repo.get("forks"),
#             "watchers": repo.get("watchers"),
#             "total_commits": repo.get("commit_stats", {}).get("total_commits", 0),
#             "owner_commits": repo.get("commit_stats", {}).get("owner_commits", 0),
#             "has_collaborators": repo.get("commit_stats", {}).get("has_collaborators", False),
#             "readme": self.trim_readme(repo.get("readme"))
#         }

#     # ----------------------------------
#     # Analyze batch
#     # ----------------------------------
#     def analyze_batch(self, batch_repos):

#         prompt = f"""
# You are a senior AI recruiter.

# Return STRICT JSON only:

# [
#   {{
#     "repo_name": "...",
#     "technical_depth_score": 0-10,
#     "project_complexity_score": 0-10,
#     "code_quality_score": 0-10,
#     "innovation_score": 0-10,
#     "summary": "Short professional evaluation"
#   }}
# ]

# Repositories:
# {json.dumps(batch_repos, indent=2)}
# """

#         try:
#             response = self.model.generate_content(prompt)
#             parsed = self.safe_json_parse(response.text)
#             return parsed if parsed else []
#         except Exception as e:
#             print("Gemini Batch Error:", e)
#             time.sleep(5)
#             return []

#     # ----------------------------------
#     # Final Portfolio Score
#     # ----------------------------------
#     def generate_portfolio_score(self, repo_summaries):

#         prompt = f"""
# Based on the repository evaluations below, return STRICT JSON:

# {{
#   "portfolio_score": 0-100,
#   "strengths": "...",
#   "weaknesses": "...",
#   "recommendation": "Strong Hire / Hire / Maybe / No Hire"
# }}

# Evaluations:
# {json.dumps(repo_summaries, indent=2)}
# """

#         try:
#             response = self.model.generate_content(prompt)
#             parsed = self.safe_json_parse(response.text)
#             return parsed if parsed else {}
#         except Exception as e:
#             print("Gemini Portfolio Error:", e)
#             return {}

#     # ----------------------------------
#     # MAIN METHOD
#     # ----------------------------------
#     def analyze_portfolio(self, github_data):

#         repositories = github_data.get("repositories", [])
#         batch_size = 10
#         all_repo_results = []

#         for i in range(0, len(repositories), batch_size):

#             batch = repositories[i:i + batch_size]
#             prepared_batch = [self.prepare_repo_summary(repo) for repo in batch]

#             print(f"🔍 Processing Batch {i//batch_size + 1}")

#             batch_result = self.analyze_batch(prepared_batch)
#             if batch_result:
#                 all_repo_results.extend(batch_result)

#         if not all_repo_results:
#             return None

#         portfolio_result = self.generate_portfolio_score(all_repo_results)

#         if not portfolio_result:
#             return None

#         return {
#             "portfolio_score": portfolio_result.get("portfolio_score", 0),
#             "strengths": portfolio_result.get("strengths", ""),
#             "weaknesses": portfolio_result.get("weaknesses", ""),
#             "recommendation": portfolio_result.get("recommendation", ""),
#             "repo_analyses": all_repo_results
#         }

#     # ----------------------------------
#     # Save AI Result
#     # ----------------------------------
#     def save_ai_result(self, result, username):
#         os.makedirs("data/ai_results", exist_ok=True)
#         file_path = f"data/ai_results/{username}_analysis.json"

#         with open(file_path, "w", encoding="utf-8") as f:
#             json.dump(result, f, indent=4)

#         return file_path


import os
import json
import time
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class AIScoringService:

    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    # ----------------------------------
    # Safe JSON Parse
    # ----------------------------------
    def safe_json_parse(self, text):
        try:
            text = text.strip()

            if text.startswith("```"):
                text = text.replace("```json", "")
                text = text.replace("```", "")
                text = text.strip()

            return json.loads(text)

        except Exception as e:
            print("JSON Parse Error:", e)
            return None

    # ----------------------------------
    # Trim README
    # ----------------------------------
    def trim_readme(self, readme, max_chars=2000):
        if not readme:
            return ""
        return readme[:max_chars]

    # ----------------------------------
    # Prepare Repo Summary
    # ----------------------------------
    def prepare_repo_summary(self, repo):
        return {
            "name": repo.get("name"),
            "language": repo.get("language"),
            "stars": repo.get("stars"),
            "forks": repo.get("forks"),
            "total_commits": repo.get("commit_stats", {}).get("total_commits", 0),
            "owner_commits": repo.get("commit_stats", {}).get("owner_commits", 0),
            "readme": self.trim_readme(repo.get("readme"))
        }

    # ----------------------------------
    # Analyze Batch
    # ----------------------------------
    def analyze_batch(self, batch_repos):

        prompt = f"""
You are a senior technical recruiter.

Analyze EACH repository and return STRICT JSON:

[
  {{
    "repo_name": "...",
    "technical_depth_score": 0-10,
    "project_complexity_score": 0-10,
    "code_quality_score": 0-10,
    "innovation_score": 0-10,
    "summary": "Short recruiter evaluation"
  }}
]

Repositories:
{json.dumps(batch_repos, indent=2)}
"""

        try:
            response = self.model.generate_content(prompt)
            parsed = self.safe_json_parse(response.text)
            return parsed if parsed else []
        except Exception as e:
            print("Gemini Batch Error:", e)
            time.sleep(3)
            return []

    # ----------------------------------
    # Final Portfolio Evaluation
    # ----------------------------------
    def generate_portfolio_score(self, repo_summaries):

        prompt = f"""
You are a senior recruiter at a top tech company.

Based on the repository evaluations below:

Return STRICT JSON:

{{
  "portfolio_score": 0-100,
  "strengths": "Concise strengths summary",
  "weaknesses": "Concise weaknesses summary",
  "improvement_recommendations": [
      "Clear actionable recommendation 1",
      "Clear actionable recommendation 2",
      "Clear actionable recommendation 3",
      "Clear actionable recommendation 4"
  ]
}}

Make recommendations:
- Specific
- Practical
- Focused on improving GitHub presentation
- Focused on recruiter expectations

Evaluations:
{json.dumps(repo_summaries, indent=2)}
"""

        try:
            response = self.model.generate_content(prompt)
            parsed = self.safe_json_parse(response.text)
            return parsed if parsed else {}
        except Exception as e:
            print("Gemini Portfolio Error:", e)
            return {}

    # ----------------------------------
    # MAIN METHOD
    # ----------------------------------
    def analyze_portfolio(self, github_data):

        repositories = github_data.get("repositories", [])
        batch_size = 10
        all_repo_results = []

        for i in range(0, len(repositories), batch_size):
            batch = repositories[i:i + batch_size]
            prepared_batch = [self.prepare_repo_summary(repo) for repo in batch]
            batch_result = self.analyze_batch(prepared_batch)

            if batch_result:
                all_repo_results.extend(batch_result)

        if not all_repo_results:
            return None

        portfolio_result = self.generate_portfolio_score(all_repo_results)

        if not portfolio_result:
            return None

        return {
            "portfolio_score": portfolio_result.get("portfolio_score", 0),
            "strengths": portfolio_result.get("strengths", ""),
            "weaknesses": portfolio_result.get("weaknesses", ""),
            "improvement_recommendations": portfolio_result.get("improvement_recommendations", []),
            "repo_analyses": all_repo_results
        }

    # ----------------------------------
    # Save AI Result
    # ----------------------------------
    def save_ai_result(self, result, username):
        os.makedirs("data/ai_results", exist_ok=True)
        file_path = f"data/ai_results/{username}_analysis.json"

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4)

        return file_path
