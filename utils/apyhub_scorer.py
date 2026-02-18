"""
ApyHub Resume-Job Match Score API
Uses ApyHub's SharpAPI to calculate resume-job match score
API: https://apyhub.com/utility/sharpapi-resume-job-match-score
"""
import requests
import json
from typing import Dict


class ApyHubScorer:
    def __init__(self):
        """Initialize ApyHub scorer with API credentials"""
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
            self.api_key = "APY0o4dRZKgNHEiFOQ8UeTKqAhaFxgiy2NIeDV96TyQXICQo7uAEZ6Jg2NBRJgV0EoZ0ZtMibtvz"

        self.api_url = "https://api.apyhub.com/ai/resume-parser/job-match"
        self.enabled = True if self.api_key else False

    def calculate_match_score(self, resume_text: str, job_description: str = None) -> Dict:
        """
        Calculate resume-job match score using ApyHub API

        Args:
            resume_text: Resume content
            job_description: Job description to match against

        Returns:
            Dictionary with match score and analysis
        """
        if not job_description:
            # If no job description, use fallback scoring
            return self._fallback_score(resume_text)

        try:
            headers = {
                'apy-token': self.api_key,
                'Content-Type': 'application/json'
            }

            payload = {
                'resume': resume_text,
                'job_description': job_description
            }

            # Make API request
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                return self._parse_response(data, resume_text)
            else:
                print(f"ApyHub API error: {response.status_code} - {response.text}")
                return self._fallback_score(resume_text, job_description)

        except Exception as e:
            print(f"ApyHub API exception: {str(e)}")
            return self._fallback_score(resume_text, job_description)

    def _parse_response(self, data: Dict, resume_text: str) -> Dict:
        """Parse ApyHub API response"""
        try:
            # ApyHub returns match score (0-100)
            match_score = data.get('data', {}).get('match_score', 0)

            # Convert to our format
            total_score = float(match_score)

            # Get detailed analysis if available
            analysis = data.get('data', {})

            return {
                'total_score': total_score,
                'grade': self._get_grade(total_score),
                'breakdown': {
                    'keyword_match': analysis.get('keyword_match', 0),
                    'skills_match': analysis.get('skills_match', 0),
                    'experience_match': analysis.get('experience_match', 0),
                    'overall_match': total_score
                },
                'recommendations': self._generate_recommendations(total_score, analysis),
                'improvements_needed': self._count_improvements_needed(total_score),
                'match_percentage': total_score,
                'source': 'ApyHub API',
                'matched_keywords': analysis.get('matched_keywords', []),
                'missing_keywords': analysis.get('missing_keywords', [])
            }
        except Exception as e:
            print(f"Error parsing ApyHub response: {e}")
            return self._fallback_score(resume_text)

    def _generate_recommendations(self, score: float, analysis: Dict) -> list:
        """Generate recommendations based on score and analysis"""
        recommendations = []

        if score < 50:
            recommendations.append("Significant improvements needed to match job requirements")
        elif score < 70:
            recommendations.append("Good foundation, but several key areas need enhancement")
        elif score < 85:
            recommendations.append("Strong match with minor improvements possible")
        else:
            recommendations.append("Excellent match with job requirements")

        # Add keyword-based recommendations
        missing_keywords = analysis.get('missing_keywords', [])
        if missing_keywords:
            recommendations.append(f"Add these missing keywords: {', '.join(missing_keywords[:5])}")

        # Skills match recommendations
        skills_match = analysis.get('skills_match', 0)
        if skills_match < 70:
            recommendations.append("Highlight more relevant technical skills from job description")

        # Experience match recommendations
        experience_match = analysis.get('experience_match', 0)
        if experience_match < 70:
            recommendations.append("Better align your experience with job requirements")

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
        result['source'] = 'Local ATS Scorer (ApyHub unavailable)'
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
