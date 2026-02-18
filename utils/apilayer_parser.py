"""
APILayer Resume Parser API
Uses APILayer's Resume Parser for comprehensive resume analysis
API: https://marketplace.apilayer.com/resume_parser-api
"""
import requests
import json
from typing import Dict, List


class APILayerParser:
    def __init__(self):
        """Initialize APILayer Resume Parser with API credentials"""
        # Read API key from creds.txt
        try:
            with open('creds.txt', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if 'api key' in line.lower():
                        self.api_key = line.split(':')[1].strip()
                        break
        except Exception as e:
            print(f"Error reading creds.txt: {e}")
            self.api_key = "cwU371cDOnoF1zKkyThr9fmK5oRR9iam"

        self.api_url = "https://api.apilayer.com/resume_parser/upload"
        self.enabled = True if self.api_key else False

    def parse_resume(self, resume_text: str, job_description: str = None) -> Dict:
        """
        Parse resume using APILayer Resume Parser API

        Args:
            resume_text: Resume content
            job_description: Optional job description for matching

        Returns:
            Dictionary with parsed resume data and ATS score
        """
        try:
            headers = {
                'apikey': self.api_key
            }

            # APILayer expects file upload, so we'll send text as file
            files = {
                'file': ('resume.txt', resume_text.encode('utf-8'), 'text/plain')
            }

            # Make API request
            response = requests.post(
                self.api_url,
                headers=headers,
                files=files,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                return self._parse_response(data, resume_text, job_description)
            else:
                print(f"APILayer API error: {response.status_code} - {response.text}")
                return self._fallback_score(resume_text, job_description)

        except Exception as e:
            print(f"APILayer API exception: {str(e)}")
            return self._fallback_score(resume_text, job_description)

    def calculate_ats_score(self, resume_text: str, job_description: str = None) -> Dict:
        """
        Calculate ATS score from parsed resume data

        Args:
            resume_text: Resume content
            job_description: Optional job description for matching

        Returns:
            Dictionary with ATS score and analysis
        """
        parsed_data = self.parse_resume(resume_text, job_description)

        # Calculate ATS score based on parsed data
        score_breakdown = self._calculate_score_breakdown(parsed_data, job_description)
        total_score = sum(score_breakdown.values())

        return {
            'total_score': total_score,
            'grade': self._get_grade(total_score),
            'breakdown': score_breakdown,
            'recommendations': self._generate_recommendations(parsed_data, score_breakdown),
            'improvements_needed': self._count_improvements_needed(total_score),
            'match_percentage': total_score,
            'source': 'APILayer Resume Parser',
            'parsed_data': parsed_data
        }

    def _parse_response(self, data: Dict, resume_text: str, job_description: str = None) -> Dict:
        """Parse APILayer API response"""
        try:
            # Extract parsed information
            parsed = {
                'name': data.get('name', ''),
                'email': data.get('email', ''),
                'phone': data.get('phone', ''),
                'location': data.get('location', ''),
                'linkedin': data.get('linkedin_url', ''),
                'github': data.get('github_url', ''),
                'summary': data.get('summary', ''),
                'experience': data.get('experience', []),
                'education': data.get('education', []),
                'skills': data.get('skills', []),
                'certifications': data.get('certifications', []),
                'languages': data.get('languages', []),
                'total_experience': data.get('total_experience_years', 0),
                'raw_text': resume_text
            }

            return parsed

        except Exception as e:
            print(f"Error parsing APILayer response: {e}")
            return {
                'name': '',
                'email': '',
                'phone': '',
                'skills': [],
                'experience': [],
                'education': [],
                'raw_text': resume_text
            }

    def _calculate_score_breakdown(self, parsed_data: Dict, job_description: str = None) -> Dict:
        """Calculate ATS score breakdown from parsed data"""
        scores = {
            'section_completeness': 0,
            'keyword_optimization': 0,
            'formatting': 0,
            'content_quality': 0,
            'action_words': 0
        }

        # Section completeness (25 points)
        section_score = 0
        if parsed_data.get('name'):
            section_score += 5
        if parsed_data.get('email'):
            section_score += 5
        if parsed_data.get('phone'):
            section_score += 3
        if parsed_data.get('experience') and len(parsed_data['experience']) > 0:
            section_score += 6
        if parsed_data.get('education') and len(parsed_data['education']) > 0:
            section_score += 3
        if parsed_data.get('skills') and len(parsed_data['skills']) > 0:
            section_score += 3
        scores['section_completeness'] = min(section_score, 25)

        # Keyword optimization (25 points)
        skills_count = len(parsed_data.get('skills', []))
        if skills_count >= 10:
            scores['keyword_optimization'] = 25
        elif skills_count >= 7:
            scores['keyword_optimization'] = 20
        elif skills_count >= 5:
            scores['keyword_optimization'] = 15
        elif skills_count >= 3:
            scores['keyword_optimization'] = 10
        else:
            scores['keyword_optimization'] = 5

        # Formatting (20 points)
        format_score = 20  # APILayer parsed it, so format is good
        scores['formatting'] = format_score

        # Content quality (15 points)
        quality_score = 0
        if parsed_data.get('summary'):
            quality_score += 5
        if parsed_data.get('total_experience', 0) > 0:
            quality_score += 5
        if parsed_data.get('certifications'):
            quality_score += 3
        if parsed_data.get('linkedin') or parsed_data.get('github'):
            quality_score += 2
        scores['content_quality'] = min(quality_score, 15)

        # Action words (15 points)
        raw_text = parsed_data.get('raw_text', '')
        power_words = ['achieved', 'implemented', 'developed', 'led', 'managed',
                      'created', 'improved', 'increased', 'reduced', 'optimized']
        action_count = sum(1 for word in power_words if word in raw_text.lower())
        if action_count >= 8:
            scores['action_words'] = 15
        elif action_count >= 5:
            scores['action_words'] = 12
        elif action_count >= 3:
            scores['action_words'] = 9
        else:
            scores['action_words'] = 5

        return scores

    def _generate_recommendations(self, parsed_data: Dict, scores: Dict) -> List[str]:
        """Generate recommendations based on parsed data and scores"""
        recommendations = []

        # Section completeness recommendations
        if not parsed_data.get('summary'):
            recommendations.append("Add a professional summary to highlight your key achievements")

        if not parsed_data.get('linkedin') and not parsed_data.get('github'):
            recommendations.append("Include LinkedIn or GitHub profile for better visibility")

        # Skills recommendations
        skills_count = len(parsed_data.get('skills', []))
        if skills_count < 5:
            recommendations.append("Add more relevant technical skills (aim for 8-12 skills)")

        # Experience recommendations
        if not parsed_data.get('experience') or len(parsed_data['experience']) == 0:
            recommendations.append("Add work experience with quantifiable achievements")

        # Certifications
        if not parsed_data.get('certifications'):
            recommendations.append("Include relevant certifications if you have any")

        # Score-based recommendations
        if scores.get('action_words', 0) < 12:
            recommendations.append("Use more action verbs (achieved, implemented, led, managed)")

        return recommendations

    def _count_improvements_needed(self, score: float) -> int:
        """Count number of improvements needed based on score"""
        if score >= 85:
            return 1
        elif score >= 70:
            return 3
        elif score >= 50:
            return 5
        else:
            return 7

    def _fallback_score(self, resume_text: str, job_description: str = None) -> Dict:
        """Fallback scoring when API is unavailable"""
        from .ats_scorer import ATSScorer

        scorer = ATSScorer()
        result = scorer.calculate_ats_score(resume_text, job_description)
        result['source'] = 'Local ATS Scorer (APILayer unavailable)'
        return result

    def _get_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        if score >= 95:
            return "A+"
        elif score >= 90:
            return "A"
        elif score >= 85:
            return "A-"
        elif score >= 80:
            return "B+"
        elif score >= 75:
            return "B"
        elif score >= 70:
            return "B-"
        elif score >= 65:
            return "C+"
        elif score >= 60:
            return "C"
        elif score >= 55:
            return "C-"
        elif score >= 50:
            return "D"
        else:
            return "F"

    def get_parsed_resume_data(self, resume_text: str) -> Dict:
        """
        Get structured resume data from APILayer parser

        Args:
            resume_text: Resume content

        Returns:
            Parsed resume data with all sections
        """
        return self.parse_resume(resume_text)
