# 🚀 AI-Powered GitHub Portfolio Analyzer  
### Turn Your GitHub Into Recruiter-Ready Proof

> An AI-driven evaluation engine that analyzes GitHub profiles like a senior technical recruiter and generates a structured portfolio score, strengths, weaknesses, and personalized improvement roadmap.

---

## Video Link

▶️ Click below to watch the demonstration:

https://drive.google.com/file/d/1qk9iTzTOCUskZMUeeVHCyxtUAOS0G9sR/view?usp=drive_link


## 🎯 The Problem

For students and early-career developers, GitHub is their primary portfolio.

However, most profiles:

- ❌ Lack structured and professional README documentation  
- ❌ Fail to communicate real-world impact  
- ❌ Have inconsistent commit history  
- ❌ Contain incomplete or empty repositories  
- ❌ Do not clearly signal technical depth to recruiters  

A strong GitHub profile can open doors.  
A weak one silently closes them.

There is no standardized way to objectively evaluate GitHub portfolio readiness.

---

## 💡 The Solution

**AI GitHub Portfolio Analyzer** evaluates GitHub profiles using:

- 📂 Public repositories
- 📄 README content analysis
- 📊 Commit activity patterns
- ⭐ Code structure & project complexity
- 🤖 AI-powered recruiter simulation (Gemini API)

It generates:

- 🏆 Overall Portfolio Score (0–100)
- 💪 Strengths Summary
- ⚠ Weaknesses Summary
- 🚀 Personalized Improvement Recommendations (3–4 actionable steps)
- 📁 Repository-Level Technical Analysis

All in under 2 minutes.

---

## 🧠 How It Works

### 🔹 Step 1 – GitHub Data Extraction

Using GitHub API, the system extracts:

- Repository metadata
- README files
- Language usage
- Commit statistics
- Stars, forks, and project activity

Data is temporarily stored as JSON.

---

### 🔹 Step 2 – AI Evaluation (Gemini API)

Each repository is evaluated on:

- Technical Depth (0–10)
- Project Complexity (0–10)
- Code Quality (0–10)
- Innovation (0–10)

Repositories are processed in batches for efficient API usage.

---

### 🔹 Step 3 – Portfolio Scoring

The final portfolio score is generated using AI insights.

```
Portfolio Score = AI Evaluation of:
    - Technical Depth
    - Code Quality
    - Complexity
    - Innovation
    - Documentation Quality
    - Consistency
```

The system then produces:

- Structured strengths
- Identified weaknesses
- 3–4 personalized improvement suggestions

---

## 🖥️ User Experience

The UI includes:

- 🎯 Circular Portfolio Score Gauge
- 📊 Side-by-side Strengths & Weaknesses
- 🚀 Improvement Roadmap Section
- 📂 Expandable Repository-Level Analysis
- ⚡ Real-time AI evaluation

Designed for clarity, professionalism, and recruiter impact.

---

## 🛠️ Tech Stack

### 🔹 Frontend
- Streamlit
- Plotly (Interactive Score Gauge)

### 🔹 Backend
- Python
- PyGithub (GitHub API)
- Google Gemini API (AI Evaluation Engine)

### 🔹 Environment
- dotenv
- JSON-based temporary storage (auto-deleted after display)

---

## 🔄 Complete Pipeline

1️⃣ User enters GitHub profile URL  
2️⃣ GitHub data is fetched and saved temporarily  
3️⃣ Repository data is sent to Gemini AI  
4️⃣ AI generates portfolio evaluation  
5️⃣ AI result is saved to JSON  
6️⃣ Results are displayed in UI  
7️⃣ Temporary files are automatically deleted  

No database required.

---

## 📊 Example Output

- Portfolio Score: 45 / 100  
- Strengths: Strong full-stack development in flagship project  
- Weaknesses: Multiple underdeveloped repositories  
- Improvement Suggestions:
  - Improve README structure with problem-solution format
  - Archive or clean incomplete repositories
  - Maintain consistent commit activity
  - Highlight measurable impact in documentation

---

## 🚀 Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/github-portfolio-analyzer.git
cd github-portfolio-analyzer
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate:

**Windows**
```bash
venv\Scripts\activate
```

**Mac/Linux**
```bash
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Add Environment Variables

Create a `.env` file in root directory:

```
GITHUB_TOKEN=your_github_personal_access_token
GEMINI_API_KEY=your_gemini_api_key
```

---

### 5️⃣ Run Application

```bash
streamlit run app.py
```

---



## 📈 Evaluation Criteria Alignment

| Criteria | How This Project Meets It |
|-----------|---------------------------|
| Impact (20%) | Evaluates GitHub in under 2 minutes |
| Innovation (20%) | AI-based recruiter simulation |
| Technical Execution (20%) | Modular backend + structured scoring |
| User Experience (25%) | Clean UI + visual score gauge |
| Presentation (15%) | Structured README + live demo |

---

## 🏆 Why This Project Matters

This tool ensures students walk away knowing:

- How strong their GitHub profile is
- What recruiters notice first
- Which repositories need improvement
- Clear next steps to become recruiter-ready

It transforms GitHub from a code dump into a professional portfolio.

---

## 🎥 Demo Video

A working demo video is included as required in the hackathon submission guidelines.

---

## 🔮 Future Enhancements

- 📄 Downloadable Recruiter Report (PDF)
- 📊 Skill Radar Visualization
- 📅 GitHub Activity Heatmap
- 🧠 Role-Based Portfolio Matching (AI / Frontend / Backend)
- 🔍 Resume-to-GitHub Alignment Analyzer

---
