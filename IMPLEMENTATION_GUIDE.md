# Implementation Guide - Assignment Features

**Project:** AI-Powered Resume Builder & ATS Optimization Agent
**Developer:** Aditya
**Date:** February 18, 2026

---

## 🎯 New Modules Created

### 1. **ATS Scorer** (`utils/ats_scorer.py`)

**Purpose:** Provides comprehensive ATS scoring based on multiple criteria

**Features:**
- Section completeness analysis (25 points)
- Keyword optimization scoring (25 points)
- Formatting checks (20 points)
- Content quality evaluation (15 points)
- Action words analysis (15 points)
- Total score out of 100
- Detailed recommendations
- Before/After comparison support

**Usage:**
```python
from utils.ats_scorer import ATSScorer

scorer = ATSScorer()
result = scorer.calculate_ats_score(resume_text, job_description)

print(f"ATS Score: {result['total_score']}/100")
print(f"Grade: {result['grade']}")
print(f"Recommendations: {result['recommendations']}")
```

---

### 2. **OpenAI Enhancer** (`utils/openai_enhancer.py`)

**Purpose:** AI-powered resume enhancement using OpenAI GPT models

**Features:**
- Full resume content enhancement
- Section-specific improvements
- Professional summary generation
- Keyword optimization
- Grammar and phrasing improvements
- Works alongside Gemini API for dual-AI enhancement

**Usage:**
```python
from utils.openai_enhancer import OpenAIEnhancer

enhancer = OpenAIEnhancer()

# Enhance full resume
result = enhancer.enhance_resume_content(resume_text, job_description)
enhanced_text = result['enhanced_text']
suggestions = result['suggestions']

# Enhance specific section
enhanced_summary = enhancer.enhance_section('Summary', summary_text, job_description)

# Generate professional summary
summary = enhancer.generate_professional_summary(resume_text, job_description)

# Get keyword suggestions
keywords = enhancer.optimize_keywords(resume_text, job_description)
```

---

### 3. **PDF Exporter** (`utils/pdf_exporter.py`)

**Purpose:** Convert Word documents to PDF and create PDFs from resume data

**Features:**
- DOCX to PDF conversion
- Direct PDF creation from resume data
- Professional formatting with custom styles
- Cross-platform support (Windows/Mac/Linux)
- Multiple template styles

**Usage:**
```python
from utils.pdf_exporter import PDFExporter

exporter = PDFExporter()

# Convert DOCX buffer to PDF
pdf_buffer = exporter.convert_docx_to_pdf(docx_buffer, template_style='modern')

# Create PDF directly from data
pdf_buffer = exporter.create_pdf_from_data(resume_data, template_style='modern')

# Download PDF
st.download_button(
    label="📄 Download PDF",
    data=pdf_buffer,
    file_name="resume.pdf",
    mime="application/pdf"
)
```

---

## 🔧 Integration Steps

### **Step 1: Update Environment Variables**

Add to `utils/.env`:
```env
# Existing
GOOGLE_API_KEY=your_gemini_api_key_here

# New - OpenAI API
OPENAI_API_KEY=your_openai_api_key_here
```

Get OpenAI API key from: https://platform.openai.com/api-keys

---

### **Step 2: Integrate ATS Scoring**

**In Resume Analyzer Section:**

```python
from utils.ats_scorer import ATSScorer

# Initialize scorer
ats_scorer = ATSScorer()

# Calculate initial score
initial_score = ats_scorer.calculate_ats_score(original_resume_text, job_description)

# Display score
st.metric(
    label="ATS Score (Before Enhancement)",
    value=f"{initial_score['total_score']}/100",
    delta=initial_score['grade']
)

# Show score breakdown
st.subheader("Score Breakdown")
for category, score in initial_score['breakdown'].items():
    st.progress(score / 25)  # Normalize to 0-1
    st.write(f"{category.replace('_', ' ').title()}: {score:.1f}/25")

# Show recommendations
st.subheader("Improvement Recommendations")
for rec in initial_score['recommendations']:
    st.warning(f"⚠️ {rec}")
```

---

### **Step 3: Integrate Dual-AI Enhancement**

**Combine OpenAI + Gemini for better results:**

```python
from utils.openai_enhancer import OpenAIEnhancer
from utils.ai_resume_analyzer import AIResumeAnalyzer

# Initialize both enhancers
openai_enhancer = OpenAIEnhancer()
gemini_analyzer = AIResumeAnalyzer()

# Get enhancement from both AIs
openai_result = openai_enhancer.enhance_resume_content(resume_text, job_description)
gemini_result = gemini_analyzer.analyze_resume(resume_text, job_description)

# Combine results
combined_suggestions = []
combined_suggestions.extend(openai_result.get('suggestions', []))
combined_suggestions.extend(gemini_result.get('recommendations', []))

# Use the best enhanced text (or combine)
enhanced_text = openai_result['enhanced_text']

# Calculate new ATS score
enhanced_score = ats_scorer.calculate_ats_score(enhanced_text, job_description)

# Show improvement
improvement = ats_scorer.get_improvement_suggestions(
    initial_score['total_score'],
    enhanced_score['total_score']
)

st.success(f"✅ Score improved by {improvement['improvement_percentage']:.1f}%!")
```

---

### **Step 4: Add Before/After Comparison**

```python
# Create comparison view
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Original Resume")
    st.metric(
        "ATS Score",
        f"{initial_score['total_score']}/100",
        delta=None
    )
    st.text_area("Content", original_resume_text, height=400, disabled=True)

with col2:
    st.subheader("✨ Enhanced Resume")
    st.metric(
        "ATS Score",
        f"{enhanced_score['total_score']}/100",
        delta=f"+{improvement['improvement']}",
        delta_color="normal"
    )
    st.text_area("Content", enhanced_text, height=400, disabled=True)

# Score comparison chart
import plotly.graph_objects as go

fig = go.Figure()
categories = list(initial_score['breakdown'].keys())
categories = [c.replace('_', ' ').title() for c in categories]

fig.add_trace(go.Scatterpolar(
    r=list(initial_score['breakdown'].values()),
    theta=categories,
    fill='toself',
    name='Original'
))

fig.add_trace(go.Scatterpolar(
    r=list(enhanced_score['breakdown'].values()),
    theta=categories,
    fill='toself',
    name='Enhanced'
))

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 25])),
    showlegend=True,
    title="ATS Score Comparison"
)

st.plotly_chart(fig)
```

---

### **Step 5: Add PDF Export to Resume Builder**

**In the Resume Builder section:**

```python
from utils.pdf_exporter import PDFExporter

pdf_exporter = PDFExporter()

# After generating DOCX
if docx_buffer:
    col1, col2 = st.columns(2)

    with col1:
        # DOCX download
        st.download_button(
            label="📄 Download Word (.docx)",
            data=docx_buffer,
            file_name=f"resume_{template_name}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    with col2:
        # PDF download
        try:
            pdf_buffer = pdf_exporter.convert_docx_to_pdf(docx_buffer, template_name.lower())
            st.download_button(
                label="📄 Download PDF",
                data=pdf_buffer,
                file_name=f"resume_{template_name}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"PDF generation error: {str(e)}")
            # Fallback: create PDF from data directly
            pdf_buffer = pdf_exporter.create_pdf_from_data(resume_data, template_name.lower())
            st.download_button(
                label="📄 Download PDF (Basic)",
                data=pdf_buffer,
                file_name=f"resume_{template_name}.pdf",
                mime="application/pdf"
            )
```

---

## 🎁 Bonus Features Implementation

### **Feature 1: Live Preview**

```python
# Add live preview panel
st.subheader("🔄 Live Preview")

# Create placeholder for preview
preview_placeholder = st.empty()

# As AI enhances content, update preview
with st.spinner("Enhancing resume..."):
    for section in ['summary', 'experience', 'education', 'skills']:
        # Enhance section
        enhanced_section = openai_enhancer.enhance_section(section, original_section, job_description)

        # Update preview in real-time
        preview_placeholder.markdown(f"### {section.title()}\n{enhanced_section}")
        time.sleep(0.5)  # Small delay for visual effect
```

---

### **Feature 2: Comparison Mode**

```python
# Toggle for comparison mode
comparison_mode = st.toggle("📊 Show Comparison Mode", value=False)

if comparison_mode:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Original Resume")
        st.markdown(original_resume_text)

    with col2:
        st.markdown("### Enhanced Resume")
        # Highlight changes
        enhanced_html = highlight_changes(original_resume_text, enhanced_text)
        st.markdown(enhanced_html, unsafe_allow_html=True)
```

---

### **Feature 3: Score Improvement Tracker**

```python
# Store scores in session state
if 'score_history' not in st.session_state:
    st.session_state.score_history = []

# Add new score
st.session_state.score_history.append({
    'timestamp': datetime.now(),
    'score': enhanced_score['total_score'],
    'version': len(st.session_state.score_history) + 1
})

# Display tracker
st.subheader("📈 Score Improvement Tracker")

# Create line chart
import plotly.express as px

df = pd.DataFrame(st.session_state.score_history)
fig = px.line(
    df,
    x='version',
    y='score',
    title='ATS Score Progress',
    markers=True
)
fig.update_yaxes(range=[0, 100])
st.plotly_chart(fig)

# Show improvement stats
if len(st.session_state.score_history) > 1:
    first_score = st.session_state.score_history[0]['score']
    latest_score = st.session_state.score_history[-1]['score']
    total_improvement = latest_score - first_score

    st.metric(
        "Total Improvement",
        f"{total_improvement:+.1f} points",
        delta=f"{(total_improvement/first_score*100):.1f}%"
    )
```

---

### **Feature 4: AI Feedback Chat**

```python
# Add chat interface
st.subheader("💬 AI Resume Coach")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Chat input
user_question = st.chat_input("Ask for resume improvement suggestions...")

if user_question:
    # Add user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_question
    })

    # Get AI response
    with st.spinner("AI is thinking..."):
        prompt = f"""Based on this resume:
{resume_text}

User question: {user_question}

Provide specific, actionable advice for improving the resume."""

        if openai_enhancer.enabled:
            response = openai_enhancer.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert resume coach."},
                    {"role": "user", "content": prompt}
                ]
            )
            ai_response = response.choices[0].message.content
        else:
            ai_response = "OpenAI API not configured. Please add your API key."

    # Add AI response
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": ai_response
    })

# Display chat
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
```

---

## 📊 Complete Enhanced Flow

```python
# Complete Resume Enhancement Flow

def enhanced_resume_flow():
    st.title("🚀 AI-Powered Resume Builder & ATS Optimizer")

    # Step 1: Input
    tab1, tab2 = st.tabs(["Upload Resume", "Manual Entry"])

    with tab1:
        uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=['pdf', 'docx'])
        if uploaded_file:
            resume_text = extract_text_from_file(uploaded_file)

    with tab2:
        resume_text = build_resume_manually()

    if not resume_text:
        st.stop()

    # Optional: Job Description
    job_description = st.text_area("Paste Job Description (Optional)", height=150)

    if st.button("🎯 Analyze & Enhance Resume", type="primary"):

        # Step 2: Initial ATS Scoring
        with st.spinner("Calculating ATS score..."):
            ats_scorer = ATSScorer()
            initial_score = ats_scorer.calculate_ats_score(resume_text, job_description)

        st.subheader("📊 Initial ATS Score")
        st.metric("Score", f"{initial_score['total_score']}/100", delta=initial_score['grade'])

        # Step 3: AI Enhancement (Dual AI)
        with st.spinner("Enhancing with AI (OpenAI + Gemini)..."):
            # OpenAI enhancement
            openai_enhancer = OpenAIEnhancer()
            openai_result = openai_enhancer.enhance_resume_content(resume_text, job_description)

            # Gemini enhancement
            gemini_analyzer = AIResumeAnalyzer()
            gemini_result = gemini_analyzer.analyze_resume_with_job_description(resume_text, job_description)

            # Combine results
            enhanced_text = openai_result['enhanced_text']

        # Step 4: New ATS Score
        enhanced_score = ats_scorer.calculate_ats_score(enhanced_text, job_description)

        # Step 5: Show Comparison
        improvement = ats_scorer.get_improvement_suggestions(
            initial_score['total_score'],
            enhanced_score['total_score']
        )

        st.success(f"✅ Score improved from {initial_score['total_score']} to {enhanced_score['total_score']} (+{improvement['improvement_percentage']:.1f}%)")

        # Step 6: Comparison Mode
        show_comparison(resume_text, enhanced_text, initial_score, enhanced_score)

        # Step 7: Template Selection & Generation
        st.subheader("📄 Choose Template")
        template = st.selectbox("Select Template", ["Modern", "Minimal", "Professional", "Creative"])

        if st.button("Generate Resume"):
            # Generate DOCX
            docx_buffer = generate_docx(enhanced_text, template)

            # Generate PDF
            pdf_exporter = PDFExporter()
            pdf_buffer = pdf_exporter.convert_docx_to_pdf(docx_buffer, template.lower())

            # Download buttons
            col1, col2 = st.columns(2)
            with col1:
                st.download_button("📄 Download DOCX", docx_buffer, "resume.docx")
            with col2:
                st.download_button("📄 Download PDF", pdf_buffer, "resume.pdf")

        # Bonus: AI Chat
        st.subheader("💬 Ask AI for More Help")
        # Add chat interface here
```

---

## ✅ Checklist for Complete Implementation

- [x] ATS Scorer module created
- [x] OpenAI Enhancer module created
- [x] PDF Exporter module created
- [ ] Integrate ATS scoring into app.py
- [ ] Add before/after comparison view
- [ ] Implement live preview feature
- [ ] Add score improvement tracker
- [ ] Create AI feedback chat interface
- [ ] Update .env.example with new keys
- [ ] Test all features end-to-end
- [ ] Deploy to Vercel/Render

---

## 🚀 Next Steps

1. **Update `app.py`** to integrate new modules
2. **Add new UI components** for comparison, live preview, and chat
3. **Test with sample resumes** to ensure quality
4. **Update documentation** with usage examples
5. **Deploy application** to production

---

**Developer:** Aditya
**Status:** Modules Created - Ready for Integration
**Date:** February 18, 2026
