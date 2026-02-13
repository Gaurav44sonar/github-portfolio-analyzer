# # services/github_service.py

# from github import Github
# from github.GithubException import GithubException
# from dotenv import load_dotenv
# import os
# import re

# load_dotenv()


# class GitHubService:
#     def __init__(self):
#         token = os.getenv("GITHUB_TOKEN")
#         self.github = Github(token) if token else Github()

#     # ---------------------------
#     # Extract username from URL
#     # ---------------------------
#     def extract_username(self, url: str) -> str:
#         pattern = r"github\.com/([A-Za-z0-9-]+)"
#         match = re.search(pattern, url)
#         if not match:
#             raise ValueError("Invalid GitHub profile URL.")
#         return match.group(1)

#     # ---------------------------
#     # Fetch user profile data
#     # ---------------------------
#     def get_user_profile(self, username: str) -> dict:
#         try:
#             user = self.github.get_user(username)

#             profile_data = {
#                 "username": user.login,
#                 "name": user.name,
#                 "bio": user.bio,
#                 "followers": user.followers,
#                 "following": user.following,
#                 "public_repos": user.public_repos,
#                 "created_at": user.created_at.isoformat(),
#                 "avatar_url": user.avatar_url,
#                 "profile_url": user.html_url
#             }

#             return profile_data

#         except GithubException as e:
#             raise Exception(f"GitHub API Error: {e}")

#     # ---------------------------
#     # Fetch repositories
#     # ---------------------------
#     def get_user_repositories(self, username: str) -> list:
#         try:
#             user = self.github.get_user(username)
#             repos = user.get_repos()

#             repo_list = []

#             for repo in repos:
#                 repo_list.append({
#                     "name": repo.name,
#                     "description": repo.description,
#                     "language": repo.language,
#                     "stars": repo.stargazers_count,
#                     "forks": repo.forks_count,
#                     "is_fork": repo.fork,
#                     "created_at": repo.created_at,
#                     "updated_at": repo.updated_at,
#                     "has_issues": repo.has_issues,
#                     "topics": repo.get_topics()
#                 })

#             return repo_list

#         except GithubException as e:
#             raise Exception(f"GitHub API Error: {e}")

#     # ---------------------------
#     # Check rate limit
#     # ---------------------------
#     def get_rate_limit_status(self):
#         rate_limit = self.github.get_rate_limit()

#         return {
#             "remaining": rate_limit.raw_data["rate"]["remaining"],
#             "limit": rate_limit.raw_data["rate"]["limit"]
#         }


#     # ---------------------------
#     # Master method
#     # ---------------------------
#     def analyze_profile(self, profile_url: str) -> dict:
#         username = self.extract_username(profile_url)

#         profile = self.get_user_profile(username)
#         repositories = self.get_user_repositories(username)
#         rate_limit = self.get_rate_limit_status()

#         return {
#             "profile": profile,
#             "repositories": repositories,
#             "rate_limit": rate_limit
#         }


from github import Github
from github.GithubException import GithubException
from dotenv import load_dotenv
import os
import re
import base64
import json
from datetime import datetime

load_dotenv()


class GitHubService:
    def __init__(self):
        token = os.getenv("GITHUB_TOKEN")
        self.github = Github(token) if token else Github()

    # ----------------------------
    # Extract username from URL
    # ----------------------------
    def extract_username(self, url: str) -> str:
        pattern = r"github\.com/([A-Za-z0-9-]+)"
        match = re.search(pattern, url)
        if not match:
            raise ValueError("Invalid GitHub profile URL.")
        return match.group(1)

    # ----------------------------
    # Get README content
    # ----------------------------
    def get_readme(self, repo):
        try:
            readme = repo.get_readme()
            content = base64.b64decode(readme.content).decode("utf-8")
            return content
        except:
            return None

    # ----------------------------
    # Get top-level file structure
    # ----------------------------
    def get_structure(self, repo):
        try:
            contents = repo.get_contents("")
            return [item.name for item in contents]
        except:
            return []

    # ----------------------------
    # Advanced Commit Statistics
    # ----------------------------
    def get_commit_data(self, repo, username):
        try:
            commits = repo.get_commits()
            total_commits = commits.totalCount

            owner_commits = 0
            other_commits = 0
            recent_owner_commits = 0

            now = datetime.utcnow()

            # Limit to 200 commits for rate safety
            for commit in commits[:200]:
                try:
                    commit_author = commit.author.login if commit.author else None
                    commit_date = commit.commit.author.date

                    if commit_author == username:
                        owner_commits += 1

                        # Check recent activity
                        if (now - commit_date).days < 30:
                            recent_owner_commits += 1
                    else:
                        other_commits += 1

                except:
                    continue

            has_collaborators = other_commits > 0

            return {
                "total_commits": total_commits,
                "owner_commits": owner_commits,
                "other_commits": other_commits,
                "recent_30_days_owner": recent_owner_commits,
                "has_collaborators": has_collaborators
            }

        except Exception as e:
            print(f"Commit extraction failed for {repo.name}: {e}")
            return {
                "total_commits": 0,
                "owner_commits": 0,
                "other_commits": 0,
                "recent_30_days_owner": 0,
                "has_collaborators": False
            }

    # ----------------------------
    # Extract full repository info
    # ----------------------------
    def extract_repository(self, repo, username):
        return {
            "name": repo.name,
            "description": repo.description,
            "language": repo.language,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "watchers": repo.watchers_count,
            "open_issues": repo.open_issues_count,
            "is_fork": repo.fork,
            "created_at": repo.created_at.isoformat(),
            "updated_at": repo.updated_at.isoformat(),
            "topics": repo.get_topics(),
            "default_branch": repo.default_branch,
            "has_issues": repo.has_issues,
            "license": repo.license.name if repo.license else None,
            "structure": self.get_structure(repo),
            "readme": self.get_readme(repo),
            "commit_stats": self.get_commit_data(repo, username)
        }

    # ----------------------------
    # Extract full profile
    # ----------------------------
    def analyze_profile(self, profile_url: str) -> dict:
        username = self.extract_username(profile_url)

        try:
            user = self.github.get_user(username)

            profile_data = {
                "profile": {
                    "username": user.login,
                    "name": user.name,
                    "bio": user.bio,
                    "followers": user.followers,
                    "following": user.following,
                    "public_repos": user.public_repos,
                    "created_at": user.created_at.isoformat(),
                    "avatar_url": user.avatar_url,
                    "profile_url": user.html_url
                },
                "repositories": []
            }

            repos = user.get_repos()

            for repo in repos:
                print(f"Extracting repository: {repo.name}")
                repo_data = self.extract_repository(repo, username)
                profile_data["repositories"].append(repo_data)

            # ----------------------------
            # Print API Rate Limit
            # ----------------------------
            rate_limit = self.github.get_rate_limit()
            remaining = rate_limit.raw_data["rate"]["remaining"]
            limit = rate_limit.raw_data["rate"]["limit"]

            print("\n========== GitHub API Rate Limit ==========")
            print(f"Remaining Requests: {remaining}")
            print(f"Total Limit: {limit}")
            print("===========================================\n")

            return profile_data

        except GithubException as e:
            raise Exception(f"GitHub API Error: {e}")

    # ----------------------------
    # Save data locally
    # ----------------------------
    def save_to_file(self, data, username):
        os.makedirs("data", exist_ok=True)
        file_path = f"data/{username}_github_data.json"

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        return file_path

    # ----------------------------
    # Rate limit status (optional call)
    # ----------------------------
    def get_rate_limit_status(self):
        rate_limit = self.github.get_rate_limit()
        return {
            "remaining": rate_limit.raw_data["rate"]["remaining"],
            "limit": rate_limit.raw_data["rate"]["limit"]
        }
