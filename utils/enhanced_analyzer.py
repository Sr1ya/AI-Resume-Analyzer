"""
Enhanced Resume Analyzer
Integrates ATS Scoring, Dual-AI Enhancement, and Comparison Features
"""
import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Tuple
from .ats_scorer import ATSScorer
from .apyhub_scorer import ApyHubScorer
from .openai_enhancer import OpenAIEnhancer
from .ai_resume_analyzer import AIResumeAnalyzer


class EnhancedResumeAnalyzer:
    def __init__(self):
        """Initialize enhanced analyzer with all AI components"""
        self.ats_scorer = ATSScorer()
        self.apyhub_scorer = ApyHubScorer()
        self.openai_enhancer = OpenAIEnhancer()
        self.gemini_analyzer = AIResumeAnalyzer()

    def analyze_and_enhance(self, resume_text: str, job_description: str = None) -> Dict:
        """
        Complete analysis and enhancement workflow

        Args:
            resume_text: Original resume content
            job_description: Optional job description for targeted enhancement

        Returns:
            Dictionary with all analysis results and enhanced content
        """
        results = {}

        # Step 1: Initial ATS Scoring using ApyHub API
        st.write("🔍 **Step 1:** Calculating initial resume-job match score with ApyHub API...")
        initial_score = self.apyhub_scorer.calculate_match_score(resume_text, job_description)
        results['initial_score'] = initial_score

        # Show source
        st.caption(f"📊 Score Source: {initial_score.get('source', 'Unknown')}")

        # Display initial score
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "ATS Score (Before)",
                f"{initial_score['total_score']:.1f}/100",
                delta=initial_score['grade']
            )
        with col2:
            st.metric(
                "Recommendations",
                initial_score['improvements_needed']
            )
        with col3:
            grade_color = self._get_grade_color(initial_score['total_score'])
            st.markdown(f"### <span style='color: {grade_color}'>{initial_score['grade']}</span>",
                       unsafe_allow_html=True)

        # Step 2: AI Enhancement
        st.write("\n✨ **Step 2:** Enhancing resume with AI...")

        enhanced_text = resume_text
        all_suggestions = []

        # Try OpenAI enhancement first
        openai_enhanced = False
        if self.openai_enhancer.enabled:
            with st.spinner("Enhancing with OpenAI..."):
                openai_result = self.openai_enhancer.enhance_resume_content(resume_text, job_description)
                if openai_result.get('error') == 'quota_exceeded':
                    st.warning("⚠️ OpenAI API quota exceeded. Using Gemini AI for enhancement.")
                    all_suggestions.extend(openai_result.get('suggestions', []))
                elif 'enhanced_text' in openai_result and openai_result['enhanced_text'] != resume_text:
                    enhanced_text = openai_result['enhanced_text']
                    all_suggestions.extend(openai_result.get('suggestions', []))
                    openai_enhanced = True
                    st.success("✅ OpenAI enhancement complete")
                else:
                    st.info("ℹ️ OpenAI enhancement unavailable. Using Gemini AI.")

        # If OpenAI didn't enhance, use rule-based enhancement
        if not openai_enhanced:
            with st.spinner("Applying ATS optimization rules..."):
                enhanced_text = self._apply_ats_enhancement(resume_text, initial_score, job_description)
                st.success("✅ ATS optimization applied")

        # Get Gemini analysis for additional insights
        with st.spinner("Getting additional insights from Gemini..."):
            try:
                gemini_result = self.gemini_analyzer.analyze_resume_with_gemini(
                    resume_text,
                    job_description if job_description else None
                )
                if gemini_result and 'recommendations' in gemini_result:
                    all_suggestions.extend(gemini_result.get('recommendations', []))
                st.success("✅ Gemini analysis complete")
            except Exception as e:
                st.warning(f"Gemini analysis skipped: {str(e)}")

        results['enhanced_text'] = enhanced_text
        results['suggestions'] = all_suggestions

        # Step 3: Enhanced ATS Scoring using ApyHub API
        st.write("\n📊 **Step 3:** Calculating enhanced resume-job match score with ApyHub API...")
        enhanced_score = self.apyhub_scorer.calculate_match_score(enhanced_text, job_description)
        results['enhanced_score'] = enhanced_score

        # Show source
        st.caption(f"📊 Score Source: {enhanced_score.get('source', 'Unknown')}")

        # Calculate improvement
        improvement = self.ats_scorer.get_improvement_suggestions(
            initial_score['total_score'],
            enhanced_score['total_score']
        )
        results['improvement'] = improvement

        # Display improvement
        if improvement['improvement'] > 0:
            st.success(f"🎉 **Score Improved!** {initial_score['total_score']:.1f} → {enhanced_score['total_score']:.1f} (+{improvement['improvement']:.1f} points, +{improvement['improvement_percentage']:.1f}%)")
        elif improvement['improvement'] == 0:
            st.info("ℹ️ Score remained the same. Consider additional optimizations.")
        else:
            st.warning("⚠️ Score decreased. This may happen if formatting changed. Review recommendations.")

        return results

    def display_comparison(self, results: Dict):
        """Display side-by-side comparison of original vs enhanced"""
        st.subheader("📊 Before vs After Comparison")

        # Score comparison
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📄 Original Resume")
            self._display_score_card(results['initial_score'], "Before")

        with col2:
            st.markdown("### ✨ Enhanced Resume")
            self._display_score_card(results['enhanced_score'], "After")

        # Radar chart comparison
        st.subheader("📈 Score Breakdown Comparison")
        self._display_radar_chart(
            results['initial_score']['breakdown'],
            results['enhanced_score']['breakdown']
        )

        # Detailed recommendations
        st.subheader("💡 Improvement Recommendations")

        # Initial recommendations
        if results['initial_score']['recommendations']:
            with st.expander("📋 ATS Recommendations", expanded=True):
                for i, rec in enumerate(results['initial_score']['recommendations'], 1):
                    st.warning(f"{i}. {rec}")

        # AI suggestions
        if results.get('suggestions'):
            with st.expander("🤖 AI Enhancement Suggestions", expanded=True):
                for i, sug in enumerate(results['suggestions'][:10], 1):  # Limit to top 10
                    st.info(f"{i}. {sug}")

    def display_live_preview(self, original_text: str, enhanced_text: str):
        """Display side-by-side live preview"""
        st.subheader("👁️ Live Preview")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Original**")
            st.text_area("", original_text, height=400, key="original_preview", disabled=True)

        with col2:
            st.markdown("**Enhanced**")
            st.text_area("", enhanced_text, height=400, key="enhanced_preview", disabled=True)

    def _display_score_card(self, score_data: Dict, label: str):
        """Display a score card with breakdown"""
        st.metric(
            "Total Score",
            f"{score_data['total_score']:.1f}/100",
            delta=None
        )

        st.markdown("**Score Breakdown:**")
        for category, score in score_data['breakdown'].items():
            category_name = category.replace('_', ' ').title()
            max_score = 25 if category in ['section_completeness', 'keyword_optimization'] else \
                       20 if category == 'formatting' else \
                       15
            percentage = (score / max_score) * 100
            st.progress(percentage / 100, text=f"{category_name}: {score:.1f}/{max_score}")

    def _display_radar_chart(self, initial_breakdown: Dict, enhanced_breakdown: Dict):
        """Display radar chart comparing scores"""
        categories = [c.replace('_', ' ').title() for c in initial_breakdown.keys()]

        fig = go.Figure()

        # Original scores
        fig.add_trace(go.Scatterpolar(
            r=list(initial_breakdown.values()),
            theta=categories,
            fill='toself',
            name='Original',
            line=dict(color='#FF6B6B')
        ))

        # Enhanced scores
        fig.add_trace(go.Scatterpolar(
            r=list(enhanced_breakdown.values()),
            theta=categories,
            fill='toself',
            name='Enhanced',
            line=dict(color='#4ECDC4')
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 25]
                )
            ),
            showlegend=True,
            title="ATS Score Category Comparison",
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

    def _get_grade_color(self, score: float) -> str:
        """Get color based on grade"""
        if score >= 90:
            return "#22C55E"  # Green
        elif score >= 80:
            return "#3B82F6"  # Blue
        elif score >= 70:
            return "#F59E0B"  # Amber
        elif score >= 60:
            return "#EF4444"  # Red
        else:
            return "#DC2626"  # Dark Red

    def create_score_tracker(self, session_state_key: str = 'score_history'):
        """Create a score improvement tracker"""
        import pandas as pd
        import plotly.express as px
        from datetime import datetime

        if session_state_key not in st.session_state:
            st.session_state[session_state_key] = []

        # Display tracker
        if st.session_state[session_state_key]:
            st.subheader("📈 Score Improvement Tracker")

            df = pd.DataFrame(st.session_state[session_state_key])

            # Line chart
            fig = px.line(
                df,
                x='version',
                y='score',
                title='ATS Score Progress',
                markers=True,
                labels={'version': 'Version', 'score': 'ATS Score'}
            )
            fig.update_yaxes(range=[0, 100])
            fig.update_traces(line_color='#4ECDC4', marker_size=10)

            st.plotly_chart(fig, use_container_width=True)

            # Stats
            if len(st.session_state[session_state_key]) > 1:
                first_score = st.session_state[session_state_key][0]['score']
                latest_score = st.session_state[session_state_key][-1]['score']
                total_improvement = latest_score - first_score

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("First Score", f"{first_score:.1f}/100")
                with col2:
                    st.metric("Current Score", f"{latest_score:.1f}/100")
                with col3:
                    st.metric(
                        "Total Improvement",
                        f"{total_improvement:+.1f}",
                        delta=f"{(total_improvement/first_score*100):+.1f}%"
                    )

    def add_score_to_tracker(self, score: float, session_state_key: str = 'score_history'):
        """Add a score to the tracker"""
        from datetime import datetime

        if session_state_key not in st.session_state:
            st.session_state[session_state_key] = []

        st.session_state[session_state_key].append({
            'timestamp': datetime.now(),
            'score': score,
            'version': len(st.session_state[session_state_key]) + 1
        })

    def create_ai_chat(self, resume_text: str):
        """Create AI feedback chat interface"""
        st.subheader("💬 AI Resume Coach")

        # Initialize chat history
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []

        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input("Ask for resume improvement suggestions..."):
            # Add user message
            st.session_state.chat_history.append({
                "role": "user",
                "content": prompt
            })

            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)

            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    if self.openai_enhancer.enabled:
                        try:
                            chat_prompt = f"""Based on this resume:

{resume_text[:1000]}... (truncated)

User question: {prompt}

Provide specific, actionable advice for improving the resume. Be concise and practical."""

                            response = self.openai_enhancer.client.chat.completions.create(
                                model="gpt-3.5-turbo",
                                messages=[
                                    {"role": "system", "content": "You are an expert resume coach and career advisor. Provide specific, actionable advice."},
                                    {"role": "user", "content": chat_prompt}
                                ],
                                temperature=0.7,
                                max_tokens=500
                            )

                            ai_response = response.choices[0].message.content
                        except Exception as e:
                            ai_response = f"I encountered an error: {str(e)}. Please try rephrasing your question."
                    else:
                        ai_response = "OpenAI API not configured. Please add your OPENAI_API_KEY to the .env file for chat functionality."

                    st.markdown(ai_response)

                    # Add assistant message to history
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": ai_response
                    })

    def _apply_ats_enhancement(self, resume_text: str, initial_score: Dict, job_description: str = None) -> str:
        """Apply rule-based ATS enhancement to improve resume"""
        import re

        enhanced_text = resume_text

        # Power words to add
        power_words = ['Achieved', 'Implemented', 'Developed', 'Led', 'Managed', 'Created',
                      'Improved', 'Increased', 'Reduced', 'Optimized', 'Designed', 'Executed',
                      'Collaborated', 'Spearheaded', 'Established', 'Streamlined']

        # Replace weak verbs with power words
        weak_to_strong = {
            r'\bworked on\b': 'Developed',
            r'\bhelped with\b': 'Contributed to',
            r'\bresponsible for\b': 'Led',
            r'\bdid\b': 'Executed',
            r'\bmade\b': 'Created',
            r'\bwas part of\b': 'Collaborated on',
            r'\bused\b': 'Utilized',
            r'\bhandled\b': 'Managed'
        }

        for weak, strong in weak_to_strong.items():
            enhanced_text = re.sub(weak, strong, enhanced_text, flags=re.IGNORECASE)

        # Add quantifiable metrics where possible
        # Look for achievements and try to make them more specific
        lines = enhanced_text.split('\n')
        enhanced_lines = []

        for line in lines:
            # If line contains achievements but no numbers, suggest adding them
            if any(word in line.lower() for word in ['improved', 'increased', 'reduced', 'achieved']):
                if not re.search(r'\d+%|\d+x|\$\d+', line):
                    # Add placeholder for metrics
                    line = line.rstrip() + " (measurable impact achieved)"
            enhanced_lines.append(line)

        enhanced_text = '\n'.join(enhanced_lines)

        # Add job description keywords if provided
        if job_description:
            # Extract key technical terms from job description
            tech_terms = re.findall(r'\b[A-Z][a-zA-Z]+(?:\.[a-z]+)?(?:\s+[A-Z][a-zA-Z]+)*\b', job_description)
            # Common tech keywords
            common_tech = ['Python', 'Java', 'JavaScript', 'React', 'Node.js', 'SQL', 'AWS',
                          'Docker', 'Kubernetes', 'Agile', 'Scrum', 'CI/CD', 'Git']

            missing_keywords = []
            for keyword in common_tech:
                if keyword.lower() in job_description.lower() and keyword not in resume_text:
                    missing_keywords.append(keyword)

            if missing_keywords and 'skills' not in enhanced_text.lower():
                enhanced_text += f"\n\nRELEVANT SKILLS: {', '.join(missing_keywords[:10])}"

        return enhanced_text
