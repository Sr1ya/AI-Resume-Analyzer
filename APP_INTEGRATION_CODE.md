# App.py Integration Code

This file contains the exact code to add to `app.py` for the assignment features.

---

## Step 1: Add Imports at the Top of app.py

Find the imports section at the top of `app.py` and add these lines:

```python
# Add these imports after the existing imports
from utils.ats_scorer import ATSScorer
from utils.openai_enhancer import OpenAIEnhancer
from utils.pdf_exporter import PDFExporter
from utils.enhanced_analyzer import EnhancedResumeAnalyzer
```

---

## Step 2: Initialize New Components in __init__

In the `ResumeApp` class `__init__` method, add these initializations after the existing ones:

```python
def __init__(self):
    # ... existing code ...

    # Add these new initializers
    self.ats_scorer = ATSScorer()
    self.openai_enhancer = OpenAIEnhancer()
    self.pdf_exporter = PDFExporter()
    self.enhanced_analyzer = EnhancedResumeAnalyzer()
```

---

## Step 3: Update render_analyzer Method

Replace or update the `render_analyzer` method with this enhanced version:

```python
def render_analyzer(self):
    """Render the enhanced resume analyzer page with ATS scoring and AI enhancement"""
    apply_modern_styles()

    # Page Header
    page_header(
        "🎯 AI-Powered Resume Analyzer & ATS Optimizer",
        "Upload your resume and get instant AI-powered feedback with ATS scoring"
    )

    # Create tabs for different analyzer modes
    analyzer_tabs = st.tabs(["📊 ATS Analysis & Enhancement", "🔍 Standard Analyzer", "🤖 AI Deep Analysis"])

    # TAB 1: Enhanced ATS Analysis (NEW - Assignment Feature)
    with analyzer_tabs[0]:
        st.markdown("""
        ### Upload your resume and get:
        - ✅ Comprehensive ATS Score (0-100)
        - ✅ AI-Powered Enhancement (OpenAI + Gemini)
        - ✅ Before/After Comparison
        - ✅ Detailed Recommendations
        - ✅ Professional PDF & DOCX Export
        """)

        # File upload
        col1, col2 = st.columns([2, 1])

        with col1:
            uploaded_file = st.file_uploader(
                "Upload Resume (PDF or DOCX)",
                type=['pdf', 'docx'],
                key="ats_upload"
            )

        with col2:
            st.markdown("### Quick Stats")
            if uploaded_file:
                st.success(f"✅ File: {uploaded_file.name}")
                st.info(f"📦 Size: {uploaded_file.size / 1024:.1f} KB")

        # Job description (optional)
        job_description = st.text_area(
            "📋 Paste Job Description (Optional - for targeted optimization)",
            height=150,
            placeholder="Paste the job description here for better keyword matching and targeted recommendations...",
            key="job_desc_ats"
        )

        if uploaded_file:
            # Extract text from uploaded file
            try:
                resume_text = self.ai_analyzer.extract_text_from_pdf(uploaded_file)

                if not resume_text or len(resume_text.strip()) < 50:
                    st.error("❌ Could not extract enough text from the resume. Please check the file.")
                else:
                    st.success(f"✅ Extracted {len(resume_text)} characters from resume")

                    # Show extraction preview
                    with st.expander("📄 View Extracted Text"):
                        st.text_area("Extracted Content", resume_text[:1000] + "..." if len(resume_text) > 1000 else resume_text, height=200, disabled=True)

                    # Analyze button
                    if st.button("🚀 Analyze & Enhance Resume", type="primary", key="analyze_enhance_btn"):
                        # Use the enhanced analyzer
                        with st.spinner("🔍 Analyzing resume with AI..."):
                            results = self.enhanced_analyzer.analyze_and_enhance(
                                resume_text,
                                job_description if job_description else None
                            )

                            # Store results in session state
                            st.session_state['analysis_results'] = results
                            st.session_state['original_text'] = resume_text
                            st.session_state['enhanced_text'] = results['enhanced_text']

                            # Add score to tracker
                            self.enhanced_analyzer.add_score_to_tracker(
                                results['enhanced_score']['total_score']
                            )

                    # Display results if available
                    if 'analysis_results' in st.session_state:
                        results = st.session_state['analysis_results']

                        st.markdown("---")

                        # Display comparison
                        self.enhanced_analyzer.display_comparison(results)

                        st.markdown("---")

                        # Live Preview
                        if st.checkbox("👁️ Show Side-by-Side Preview", value=False):
                            self.enhanced_analyzer.display_live_preview(
                                st.session_state['original_text'],
                                st.session_state['enhanced_text']
                            )

                        st.markdown("---")

                        # Score Tracker
                        self.enhanced_analyzer.create_score_tracker()

                        st.markdown("---")

                        # Export Options
                        st.subheader("📥 Download Enhanced Resume")

                        export_col1, export_col2 = st.columns(2)

                        with export_col1:
                            # Text download
                            st.download_button(
                                label="📄 Download Enhanced Text (.txt)",
                                data=results['enhanced_text'],
                                file_name="enhanced_resume.txt",
                                mime="text/plain",
                                use_container_width=True
                            )

                        with export_col2:
                            # Note about using Resume Builder for formatted export
                            st.info("💡 Use the Resume Builder to create professional PDF/DOCX from enhanced content")

                        st.markdown("---")

                        # AI Chat
                        self.enhanced_analyzer.create_ai_chat(st.session_state['original_text'])

            except Exception as e:
                st.error(f"❌ Error processing resume: {str(e)}")
                st.code(traceback.format_exc())

    # TAB 2: Keep existing Standard Analyzer
    with analyzer_tabs[1]:
        # Your existing standard analyzer code here
        st.info("This is your existing standard analyzer - keep it as is!")
        # ... existing code ...

    # TAB 3: Keep existing AI Deep Analysis
    with analyzer_tabs[2]:
        # Your existing AI analysis code here
        st.info("This is your existing AI analyzer - keep it as is!")
        # ... existing code ...
```

---

## Step 4: Update Resume Builder to Add PDF Export

Find the `render_builder` method and update the download section:

```python
# In render_builder method, after DOCX generation:

if docx_buffer:
    st.success("✅ Resume generated successfully!")

    # Download buttons
    download_col1, download_col2 = st.columns(2)

    with download_col1:
        # DOCX Download (existing)
        st.download_button(
            label="📄 Download Word (.docx)",
            data=docx_buffer,
            file_name=f"resume_{template_name.lower()}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )

    with download_col2:
        # PDF Download (NEW)
        try:
            with st.spinner("Generating PDF..."):
                pdf_buffer = self.pdf_exporter.convert_docx_to_pdf(
                    docx_buffer,
                    template_name.lower()
                )

            st.download_button(
                label="📄 Download PDF",
                data=pdf_buffer,
                file_name=f"resume_{template_name.lower()}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.warning(f"PDF generation: {str(e)}")
            st.info("💡 Downloading basic PDF version...")

            # Fallback: Create PDF from data
            try:
                pdf_buffer = self.pdf_exporter.create_pdf_from_data(
                    resume_data,
                    template_name.lower()
                )
                st.download_button(
                    label="📄 Download PDF (Basic)",
                    data=pdf_buffer,
                    file_name=f"resume_{template_name.lower()}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e2:
                st.error(f"PDF export failed: {str(e2)}")
```

---

## Step 5: Test the Integration

After making these changes, run the app:

```bash
cd "/home/sriya/Projects/Resume Analyzer/AI-Resume-Analyzer"
source .venv/bin/activate
streamlit run app.py
```

### Test Checklist:

1. ✅ Upload a resume in the new "ATS Analysis & Enhancement" tab
2. ✅ Click "Analyze & Enhance Resume"
3. ✅ Verify ATS scores appear (Before and After)
4. ✅ Check comparison charts display correctly
5. ✅ Test the side-by-side preview toggle
6. ✅ Verify score tracker shows progress
7. ✅ Test AI chat functionality
8. ✅ Download enhanced text
9. ✅ Go to Resume Builder and test PDF export

---

## Quick Integration Alternative

If you want a quicker integration without modifying the entire analyzer:

1. Add a NEW page to the sidebar menu:

```python
# In the __init__ method, add to self.pages:
self.pages = {
    "🏠 HOME": self.render_home,
    "🎯 ATS OPTIMIZER": self.render_ats_optimizer,  # NEW
    "🔍 RESUME ANALYZER": self.render_analyzer,
    "📝 RESUME BUILDER": self.render_builder,
    # ... rest of pages
}
```

2. Add new method:

```python
def render_ats_optimizer(self):
    """NEW: Render ATS Optimizer page for assignment"""
    apply_modern_styles()

    page_header(
        "🎯 ATS Resume Optimizer",
        "AI-Powered Resume Analysis with OpenAI + Gemini"
    )

    # File upload
    uploaded_file = st.file_uploader("Upload Resume", type=['pdf', 'docx'])
    job_description = st.text_area("Job Description (Optional)", height=150)

    if uploaded_file and st.button("Analyze & Enhance"):
        resume_text = self.ai_analyzer.extract_text_from_pdf(uploaded_file)

        results = self.enhanced_analyzer.analyze_and_enhance(
            resume_text,
            job_description
        )

        self.enhanced_analyzer.display_comparison(results)
        self.enhanced_analyzer.create_ai_chat(resume_text)
```

This adds a completely new page without changing existing functionality!

---

## Complete Code Files

All the helper modules are already created:
- ✅ `utils/ats_scorer.py`
- ✅ `utils/openai_enhancer.py`
- ✅ `utils/pdf_exporter.py`
- ✅ `utils/enhanced_analyzer.py`

You just need to integrate them into `app.py` using the code above!

---

**Implementation Time:** 30-60 minutes
**Difficulty:** Easy (mostly copy-paste)
**Result:** Complete assignment implementation with all features!
