"""
Advanced ATS (Applicant Tracking System) Scorer
Provides detailed resume scoring based on multiple criteria
"""
import re
from typing import Dict, List, Tuple
import spacy

class ATSScorer:
    def __init__(self):
        """Initialize ATS Scorer with NLP model"""
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except:
            import subprocess
            subprocess.run(['python', '-m', 'spacy', 'download', 'en_core_web_sm'])
            self.nlp = spacy.load('en_core_web_sm')

        # ATS-friendly keywords and sections
        self.essential_sections = {
            'contact': ['email', 'phone', 'address', 'linkedin', 'location'],
            'summary': ['summary', 'objective', 'profile', 'about'],
            'experience': ['experience', 'work history', 'employment', 'professional experience'],
            'education': ['education', 'academic', 'degree', 'university', 'college'],
            'skills': ['skills', 'technical skills', 'core competencies', 'expertise']
        }

        # Common ATS-friendly power words
        self.power_words = [
            'achieved', 'improved', 'trained', 'managed', 'created', 'resolved',
            'volunteered', 'influenced', 'increased', 'decreased', 'ideas', 'negotiated',
            'launched', 'revenue', 'under budget', 'won', 'designed', 'delivered',
            'exceeded', 'improved', 'reduced', 'saved', 'built', 'developed',
            'led', 'optimized', 'implemented', 'streamlined', 'automated'
        ]

        # Common ATS formatting issues
        self.formatting_checks = {
            'special_characters': r'[★☆●○■□▪▫◆◇]',
            'tables_columns': r'\t{2,}',
            'headers_footers': r'(Page \d+|\\header|\\footer)',
            'images_graphics': r'(\[image\]|\[graphic\])',
        }

    def calculate_ats_score(self, resume_text: str, job_description: str = None) -> Dict:
        """
        Calculate comprehensive ATS score

        Args:
            resume_text: The resume content
            job_description: Optional job description for keyword matching

        Returns:
            Dictionary containing scores and recommendations
        """
        scores = {}
        recommendations = []

        # 1. Section Completeness Score (25 points)
        section_score, section_recs = self._check_sections(resume_text)
        scores['section_completeness'] = section_score
        recommendations.extend(section_recs)

        # 2. Keyword Optimization Score (25 points)
        keyword_score, keyword_recs = self._check_keywords(resume_text, job_description)
        scores['keyword_optimization'] = keyword_score
        recommendations.extend(keyword_recs)

        # 3. Formatting Score (20 points)
        format_score, format_recs = self._check_formatting(resume_text)
        scores['formatting'] = format_score
        recommendations.extend(format_recs)

        # 4. Content Quality Score (15 points)
        content_score, content_recs = self._check_content_quality(resume_text)
        scores['content_quality'] = content_score
        recommendations.extend(content_recs)

        # 5. Action Words Score (15 points)
        action_score, action_recs = self._check_action_words(resume_text)
        scores['action_words'] = action_score
        recommendations.extend(action_recs)

        # Calculate total score
        total_score = sum(scores.values())

        return {
            'total_score': round(total_score, 2),
            'breakdown': scores,
            'recommendations': recommendations,
            'grade': self._get_grade(total_score),
            'improvements_needed': len(recommendations)
        }

    def _check_sections(self, text: str) -> Tuple[float, List[str]]:
        """Check if all essential sections are present"""
        text_lower = text.lower()
        found_sections = []
        missing_sections = []
        recommendations = []

        for section, keywords in self.essential_sections.items():
            if any(keyword in text_lower for keyword in keywords):
                found_sections.append(section)
            else:
                missing_sections.append(section)
                recommendations.append(f"Add '{section.title()}' section to your resume")

        score = (len(found_sections) / len(self.essential_sections)) * 25

        if score < 20:
            recommendations.append("Your resume is missing essential sections. Add all required sections for better ATS compatibility.")

        return score, recommendations

    def _check_keywords(self, text: str, job_description: str = None) -> Tuple[float, List[str]]:
        """Check keyword density and relevance"""
        recommendations = []

        # Basic keyword check
        doc = self.nlp(text.lower())

        # Extract nouns and proper nouns (potential keywords)
        keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN'] and len(token.text) > 2]
        unique_keywords = set(keywords)

        # Calculate keyword density
        total_words = len([token for token in doc if not token.is_punct and not token.is_space])
        keyword_density = len(keywords) / total_words if total_words > 0 else 0

        score = 0

        # Optimal keyword density is 2-4%
        if 0.02 <= keyword_density <= 0.04:
            score = 25
        elif 0.01 <= keyword_density < 0.02 or 0.04 < keyword_density <= 0.06:
            score = 20
            recommendations.append("Adjust keyword density to 2-4% for optimal ATS performance")
        else:
            score = 15
            recommendations.append("Add more relevant keywords from the job description")

        # If job description provided, check matching
        if job_description:
            jd_doc = self.nlp(job_description.lower())
            jd_keywords = set([token.text for token in jd_doc if token.pos_ in ['NOUN', 'PROPN'] and len(token.text) > 2])

            matching_keywords = unique_keywords.intersection(jd_keywords)
            match_rate = len(matching_keywords) / len(jd_keywords) if jd_keywords else 0

            if match_rate < 0.3:
                recommendations.append(f"Only {match_rate*100:.1f}% keyword match with job description. Add more relevant keywords.")

        if len(unique_keywords) < 20:
            recommendations.append("Increase the number of relevant keywords (target: 20-30 keywords)")

        return score, recommendations

    def _check_formatting(self, text: str) -> Tuple[float, List[str]]:
        """Check for ATS-friendly formatting"""
        score = 20
        recommendations = []

        # Check for problematic special characters
        if re.search(self.formatting_checks['special_characters'], text):
            score -= 5
            recommendations.append("Remove special characters (bullets, symbols) - use simple hyphens or asterisks")

        # Check for excessive tabs/columns
        if re.search(self.formatting_checks['tables_columns'], text):
            score -= 3
            recommendations.append("Avoid complex tables or multi-column layouts - use simple single-column format")

        # Check line length (too short might indicate formatting issues)
        lines = text.split('\n')
        avg_line_length = sum(len(line) for line in lines) / len(lines) if lines else 0

        if avg_line_length < 20:
            score -= 3
            recommendations.append("Some lines are too short - check for formatting issues")

        # Check for consistent spacing
        if '\t' in text:
            score -= 2
            recommendations.append("Replace tabs with spaces for better ATS compatibility")

        # Check for proper capitalization
        if text.isupper() or text.islower():
            score -= 2
            recommendations.append("Use proper capitalization - avoid all caps or all lowercase")

        if score < 15:
            recommendations.append("Major formatting issues detected. Simplify layout for ATS systems.")

        return max(score, 0), recommendations

    def _check_content_quality(self, text: str) -> Tuple[float, List[str]]:
        """Check content quality metrics"""
        score = 15
        recommendations = []

        # Check resume length
        word_count = len(text.split())

        if word_count < 300:
            score -= 5
            recommendations.append("Resume is too short (under 300 words). Add more details about your experience.")
        elif word_count > 800:
            score -= 2
            recommendations.append("Resume might be too long. Keep it concise (500-800 words optimal).")

        # Check for numbers and metrics
        numbers = re.findall(r'\d+%|\$\d+|\d+\+|increased by \d+|reduced \d+', text.lower())

        if len(numbers) < 3:
            score -= 3
            recommendations.append("Add quantifiable achievements with numbers and metrics (e.g., 'increased sales by 25%')")

        # Check for bullet points (ATS-friendly way to list achievements)
        bullet_indicators = text.count('•') + text.count('-') + text.count('*')

        if bullet_indicators < 5:
            score -= 2
            recommendations.append("Use bullet points to list achievements and responsibilities")

        return max(score, 0), recommendations

    def _check_action_words(self, text: str) -> Tuple[float, List[str]]:
        """Check for strong action words"""
        text_lower = text.lower()
        recommendations = []

        # Count power words
        found_power_words = [word for word in self.power_words if word in text_lower]

        # Calculate score based on usage
        score = min((len(found_power_words) / 10) * 15, 15)  # Max 15 points

        if score < 10:
            recommendations.append(f"Use more action verbs (found {len(found_power_words)}, target 10+): {', '.join(self.power_words[:10])}")

        # Check for passive voice
        passive_indicators = ['was ', 'were ', 'been ', 'being ']
        passive_count = sum(text_lower.count(indicator) for indicator in passive_indicators)

        if passive_count > 5:
            score -= 2
            recommendations.append("Reduce passive voice. Use active voice for stronger impact (e.g., 'Led team' instead of 'Team was led')")

        return max(score, 0), recommendations

    def _get_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        if score >= 90:
            return 'A+ (Excellent - ATS Optimized)'
        elif score >= 80:
            return 'A (Very Good - Minor improvements needed)'
        elif score >= 70:
            return 'B (Good - Some improvements recommended)'
        elif score >= 60:
            return 'C (Fair - Needs optimization)'
        elif score >= 50:
            return 'D (Poor - Major improvements needed)'
        else:
            return 'F (Critical - Complete revision required)'

    def get_improvement_suggestions(self, original_score: float, enhanced_score: float) -> Dict:
        """Generate improvement report comparing original vs enhanced resume"""
        improvement = enhanced_score - original_score
        improvement_pct = (improvement / original_score * 100) if original_score > 0 else 0

        return {
            'original_score': round(original_score, 2),
            'enhanced_score': round(enhanced_score, 2),
            'improvement': round(improvement, 2),
            'improvement_percentage': round(improvement_pct, 2),
            'status': 'Improved' if improvement > 0 else 'Unchanged' if improvement == 0 else 'Decreased'
        }
