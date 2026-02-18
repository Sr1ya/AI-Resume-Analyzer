"""
Apideck ATS Score Checker
Uses Apideck API to check ATS score of resumes
"""
import requests
import json
from typing import Dict


class ApideckATSScorer:
    def __init__(self):
        """Initialize Apideck ATS scorer with credentials"""
        # Read credentials from creds.txt
        try:
            with open('creds.txt', 'r') as f:
                lines = f.readlines()
                self.app_id = lines[0].split(':')[1].strip()
                self.api_key = lines[1].split(':')[1].strip()
        except Exception as e:
            print(f"Error reading creds.txt: {e}")
            # Fallback to hardcoded values
            self.app_id = "jjvCJ2aUSdghUXkNPD0ovBS6bxCkCKujyVqPD0p"
            self.api_key = "sk_live_6b6f18ce-fabe-4f18-855c-0a2c8de16c12-k3eaDYZHz3ydL9WSPD0p-a00d5249-f83d-4bb2-8e08-f83872e94514"

        self.base_url = "https://unify.apideck.com/ats"
        self.enabled = True

    def check_ats_score(self, resume_text: str, job_description: str = None) -> Dict:
        """
        Check ATS score using Apideck API

        Args:
            resume_text: Resume content
            job_description: Optional job description for matching

        Returns:
            Dictionary with ATS score and analysis
        """
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'X-APIDECK-APP-ID': self.app_id,
                'Content-Type': 'application/json'
            }

            payload = {
                'resume': resume_text,
                'job_description': job_description if job_description else ""
            }

            # Make API request
            response = requests.post(
                f"{self.base_url}/score",
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                return self._parse_response(data)
            else:
                print(f"Apideck API error: {response.status_code} - {response.text}")
                return self._fallback_score(resume_text, job_description)

        except Exception as e:
            print(f"Apideck API exception: {str(e)}")
            return self._fallback_score(resume_text, job_description)

    def _parse_response(self, data: Dict) -> Dict:
        """Parse Apideck API response"""
        try:
            score = data.get('score', 0)

            return {
                'total_score': score,
                'grade': self._get_grade(score),
                'breakdown': data.get('breakdown', {}),
                'recommendations': data.get('recommendations', []),
                'improvements_needed': len(data.get('recommendations', [])),
                'match_percentage': data.get('match_percentage', 0),
                'source': 'Apideck API'
            }
        except Exception as e:
            print(f"Error parsing Apideck response: {e}")
            return self._fallback_score("", None)

    def _fallback_score(self, resume_text: str, job_description: str = None) -> Dict:
        """Fallback scoring when API is unavailable"""
        from .ats_scorer import ATSScorer

        scorer = ATSScorer()
        result = scorer.calculate_ats_score(resume_text, job_description)
        result['source'] = 'Local ATS Scorer (Apideck unavailable)'
        return result

    def _get_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        if score >= 90:
            return "A+"
        elif score >= 85:
            return "A"
        elif score >= 80:
            return "A-"
        elif score >= 75:
            return "B+"
        elif score >= 70:
            return "B"
        elif score >= 65:
            return "B-"
        elif score >= 60:
            return "C+"
        elif score >= 55:
            return "C"
        elif score >= 50:
            return "C-"
        else:
            return "F"
