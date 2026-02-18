# 🚀 AI-Powered Resume Builder & ATS Optimization Agent

**Your Intelligent Career Partner for Resume Optimization**

An advanced AI-powered application that analyzes, optimizes, and enhances resumes using cutting-edge AI technologies including ApyHub API, OpenAI GPT, and Google Gemini.

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Usage Guide](#usage-guide)
- [API Integration](#api-integration)
- [LaTeX Export](#latex-export)
- [Deployment](#deployment)
- [Developer](#developer)

---

## ✨ Features

### 🎯 Core Features

1. **📊 ATS Score Analysis (ApyHub API)**
   - Resume-job match scoring (0-100)
   - Keyword match analysis
   - Skills gap identification
   - Experience alignment check
   - Industry-standard scoring algorithm

2. **🤖 Dual-AI Enhancement**
   - OpenAI GPT-3.5 content optimization
   - Google Gemini analysis
   - Power word replacement
   - Quantifiable metrics suggestions
   - Automatic keyword injection

3. **📝 Professional Resume Builder**
   - 4 modern templates
   - Real-time preview
   - ATS-optimized formatting
   - Section-wise editing

4. **📄 Multiple Export Formats**
   - Plain Text (.txt)
   - Microsoft Word (.docx) with formatting
   - Professional PDF with styling
   - **LaTeX (.tex) for Overleaf** - 4 templates

5. **🎨 LaTeX Template Selection**
   - 🎨 Modern (Blue accents, professional)
   - 📜 Classic (Traditional, clean)
   - 🎓 Academic (CV style)
   - 📊 Two Column (Compact)

6. **📈 Analytics & Tracking**
   - Before/After comparison
   - Score improvement tracker
   - Radar chart visualizations
   - Progress monitoring

7. **💬 AI Resume Coach**
   - Interactive chat interface
   - Personalized recommendations
   - Real-time feedback

---

## 🛠️ Tech Stack

### Frontend
- **Streamlit** - Interactive web interface
- **Plotly** - Data visualizations
- **Streamlit-Lottie** - Animations

### AI & APIs
- **ApyHub API** - Resume-job match scoring
- **OpenAI GPT-3.5** - Content enhancement
- **Google Gemini** - AI analysis
- **spaCy** - NLP processing

### Document Processing
- **PyPDF2, pdfplumber** - PDF parsing
- **python-docx** - DOCX generation
- **ReportLab** - PDF creation
- **LaTeX Generator** - Overleaf-compatible output

### Database
- **SQLite3** - Local data storage

### Job Search
- **Selenium** - LinkedIn scraping
- **BeautifulSoup4** - Web scraping

---

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.10+** installed
- **pip** package manager
- **Virtual environment** (recommended)
- **Git** (for cloning)
- **API Keys:**
  - ApyHub API key
  - OpenAI API key
  - Google Gemini API key

---

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd AI-Resume-Analyzer
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate

# On Linux/Mac:
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm
```

### 4. Install System Dependencies (Optional)

For full PDF processing capabilities:

**On Ubuntu/Debian:**
```bash
sudo apt-get install poppler-utils
sudo apt-get install tesseract-ocr
```

**On Mac:**
```bash
brew install poppler
brew install tesseract
```

**On Windows:**
- Download poppler from the `poppler/` directory in the project
- Add to system PATH

---

## ⚙️ Configuration

### 1. API Keys Setup

Create or update `utils/.env` file:

```env
# Google Gemini API
GOOGLE_API_KEY=your_gemini_api_key_here

# OpenAI API
OPENAI_API_KEY=your_openai_api_key_here
```

### 2. ApyHub API Setup

Update `creds.txt` file:

```
api key : your_apyhub_api_key_here
```

**Get Your ApyHub API Key:**
1. Visit: https://apyhub.com
2. Sign up for free account
3. Navigate to API Keys section
4. Copy your API key
5. Paste in `creds.txt`

---

## 🚀 Running the Application

### Quick Start

```bash
# Make sure virtual environment is activated
source .venv/bin/activate  # Linux/Mac
# OR
.venv\Scripts\activate  # Windows

# Run the application
streamlit run app.py
```

### Custom Port

```bash
streamlit run app.py --server.port 8501
```

### Access the Application

Once running, open your browser and navigate to:
- **Local:** http://localhost:8501
- **Network:** Will be shown in terminal

---

## 📖 Usage Guide

### 1. ATS Analysis & Enhancement

1. Navigate to **"🔍 RESUME ANALYZER"** → **"📊 ATS Analyzer & Enhancement"**
2. Upload your resume (PDF or DOCX)
3. Paste job description (recommended for better matching)
4. Click **"🚀 Analyze & Enhance Resume"**
5. View:
   - Before/After ATS scores
   - ApyHub match score
   - Detailed recommendations
   - Enhanced resume text

### 2. Resume Building

1. Go to **"📝 RESUME BUILDER"**
2. Fill in your information:
   - Personal details
   - Professional summary
   - Experience
   - Education
   - Projects
   - Skills
3. Select a template
4. Click **"Generate Resume"**
5. Download in your preferred format

### 3. LaTeX Export for Overleaf

1. After analyzing/building resume
2. Select LaTeX template from dropdown:
   - 🎨 Modern
   - 📜 Classic
   - 🎓 Academic
   - 📊 Two Column
3. Click **"📐 Download LaTeX"**
4. Get `.tex` file
5. Upload to **Overleaf.com**
6. Compile to get professional PDF

### 4. Job Search

1. Navigate to **"🎯 JOB SEARCH"**
2. Enter job title and location
3. Filter by experience level
4. View and save relevant jobs

---

## 🔗 API Integration

### ApyHub Resume-Job Match API

**Endpoint:** https://api.apyhub.com/ai/resume-parser/job-match

**Features:**
- Resume-job compatibility scoring
- Keyword matching
- Skills gap analysis
- Experience alignment

**Request Format:**
```json
{
  "resume": "resume text here",
  "job_description": "job description here"
}
```

**Response:**
```json
{
  "data": {
    "match_score": 85,
    "keyword_match": 90,
    "skills_match": 80,
    "experience_match": 85,
    "matched_keywords": [...],
    "missing_keywords": [...]
  }
}
```

### Fallback Mechanism

If ApyHub API is unavailable:
- Automatically falls back to local ATS scorer
- Continues analysis without interruption
- Notifies user of score source

---

## 📐 LaTeX Export

### Templates Available

#### 1. Modern Template
```latex
- Blue section headers (#003366)
- Clickable hyperlinks
- Professional typography
- Clean spacing
```

#### 2. Classic Template
```latex
- Traditional layout
- Centered header
- Standard formatting
- Academic style
```

#### 3. Academic Template
```latex
- CV-style formatting
- Publication-ready
- Detailed sections
```

#### 4. Two Column Template
```latex
- Compact design
- Space-efficient
- Modern layout
```

### Using LaTeX on Overleaf

1. Download `.tex` file from app
2. Go to [Overleaf.com](https://www.overleaf.com)
3. Create new project
4. Upload `.tex` file
5. Click "Compile"
6. Download professional PDF

### LaTeX Features

✅ Proper document structure
✅ Custom colors and styling
✅ Clickable email/LinkedIn/GitHub links
✅ Professional sections
✅ Bullet points and formatting
✅ Easy customization

---

## 📦 Requirements

All dependencies in `requirements.txt`:

```
streamlit==1.31.0
google-generativeai==0.3.2
openai==1.12.0
PyPDF2==3.0.1
pdfplumber==0.10.3
python-docx==1.1.0
reportlab==4.0.9
spacy==3.7.2
plotly==5.18.0
pandas==2.1.4
requests==2.31.0
selenium==4.16.0
beautifulsoup4==4.12.3
Pillow==10.2.0
streamlit-lottie==0.0.5
pytesseract==0.3.10
pdf2image==1.17.0
python-dotenv==1.0.0
```

---

## 🚀 Deployment

### Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect GitHub repository
4. Add secrets (API keys) in settings
5. Deploy!

### Heroku

```bash
# Create Procfile
echo "web: streamlit run app.py" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

### Docker

```bash
# Build image
docker build -t resume-analyzer .

# Run container
docker run -p 8501:8501 resume-analyzer
```

---

## 🔧 Troubleshooting

### Common Issues

**1. Module not found errors:**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

**2. API key errors:**
- Check `utils/.env` for OpenAI and Gemini keys
- Check `creds.txt` for ApyHub key
- Verify keys are valid

**3. PDF extraction fails:**
- Install poppler-utils
- Install tesseract-ocr
- Check file permissions

**4. LaTeX not compiling:**
- Ensure all sections are properly formatted
- Check for special characters
- Use Overleaf's error messages for debugging

---

## 📊 Project Structure

```
AI-Resume-Analyzer/
├── app.py                      # Main application
├── requirements.txt            # Dependencies
├── creds.txt                  # ApyHub API key
├── utils/
│   ├── .env                   # OpenAI & Gemini API keys
│   ├── apyhub_scorer.py      # ApyHub API integration
│   ├── ats_scorer.py         # Local ATS scorer
│   ├── openai_enhancer.py    # OpenAI enhancement
│   ├── ai_resume_analyzer.py # Gemini analyzer
│   ├── latex_generator.py    # LaTeX export
│   ├── pdf_exporter.py       # PDF generation
│   ├── enhanced_analyzer.py  # Main analyzer
│   ├── resume_builder.py     # Resume builder
│   └── resume_parser.py      # Resume parser
├── config/
│   ├── database.py           # Database config
│   ├── job_roles.py          # Job roles data
│   └── courses.py            # Course recommendations
├── jobs/
│   ├── job_search.py         # Job search UI
│   ├── linkedin_scraper.py   # LinkedIn integration
│   └── companies.py          # Company data
├── dashboard/
│   └── dashboard.py          # Analytics dashboard
├── feedback/
│   └── feedback.py           # Feedback system
└── style/
    └── style.css             # Custom styles
```

---

## 🎯 Features Checklist

- ✅ Resume upload (PDF/DOCX)
- ✅ ApyHub ATS scoring
- ✅ OpenAI enhancement
- ✅ Gemini AI analysis
- ✅ Before/After comparison
- ✅ Word export (.docx)
- ✅ PDF export with formatting
- ✅ LaTeX export (4 templates)
- ✅ Overleaf compatibility
- ✅ Live preview
- ✅ Score tracker
- ✅ AI chat interface
- ✅ Job search integration
- ✅ Analytics dashboard

---

## 👨‍💻 Developer

**Aditya**

*AI-Powered Resume Builder & ATS Optimization Agent*

---

## 📄 License

This project is part of an Internshala assignment.

---

## 🙏 Acknowledgments

- **ApyHub** - Resume-job match scoring API
- **OpenAI** - GPT-3.5 for content enhancement
- **Google** - Gemini AI for analysis
- **Streamlit** - Web framework
- **Overleaf** - LaTeX compilation

---

## 📞 Support

For issues or questions:
1. Check [Troubleshooting](#troubleshooting) section
2. Review API documentation
3. Ensure all dependencies are installed
4. Verify API keys are valid

---

**🎉 Ready to optimize your resume and land your dream job!**

**Quick Start:**
```bash
source .venv/bin/activate
streamlit run app.py
```

Open http://localhost:8501 and start analyzing! 🚀
