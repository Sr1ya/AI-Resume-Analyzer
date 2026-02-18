"""
OpenAI Resume Enhancement Module
Provides AI-powered resume content enhancement using OpenAI GPT models
"""
import os
import json
from typing import Dict, List
from dotenv import load_dotenv

class OpenAIEnhancer:
    def __init__(self):
        """Initialize OpenAI enhancer"""
        # Load .env from utils directory or parent directory
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        if not os.path.exists(env_path):
            env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'utils', '.env')
        load_dotenv(env_path)

        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-3.5-turbo"  # Using GPT-3.5-turbo for cost-effectiveness

        if not self.api_key:
            print("Warning: OpenAI API key not found. OpenAI features will be limited.")
            self.enabled = False
        else:
            self.enabled = True
            try:
                import openai
                self.client = openai.OpenAI(api_key=self.api_key)
            except ImportError:
                print("Warning: openai package not installed. Run: pip install openai")
                self.enabled = False

    def enhance_resume_content(self, resume_text: str, job_description: str = None) -> Dict:
        """
        Enhance resume content using OpenAI

        Args:
            resume_text: Original resume content
            job_description: Optional job description for targeted enhancement

        Returns:
            Dictionary with enhanced content and suggestions
        """
        if not self.enabled:
            return {
                'enhanced_text': resume_text,
                'suggestions': ['OpenAI API not configured'],
                'error': 'OpenAI API key not found or package not installed'
            }

        try:
            # Create enhancement prompt
            prompt = self._create_enhancement_prompt(resume_text, job_description)

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert resume writer and ATS optimization specialist."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )

            # Extract response
            enhanced_content = response.choices[0].message.content

            # Parse the response
            result = self._parse_enhancement_response(enhanced_content)

            return result

        except Exception as e:
            error_msg = str(e)
            if 'insufficient_quota' in error_msg or '429' in error_msg:
                return {
                    'enhanced_text': resume_text,
                    'suggestions': ['OpenAI API quota exceeded. Using Gemini AI for enhancement instead.'],
                    'error': 'quota_exceeded'
                }
            else:
                return {
                    'enhanced_text': resume_text,
                    'suggestions': [f'OpenAI enhancement unavailable: {error_msg}'],
                    'error': str(e)
                }

    def _create_enhancement_prompt(self, resume_text: str, job_description: str = None) -> str:
        """Create enhancement prompt for OpenAI"""
        base_prompt = f"""Analyze and enhance the following resume for ATS (Applicant Tracking System) optimization.

Original Resume:
{resume_text}

"""

        if job_description:
            base_prompt += f"""Target Job Description:
{job_description}

"""

        base_prompt += """Please provide:
1. Enhanced version of the resume with:
   - Improved grammar and professional phrasing
   - Optimized keywords for ATS systems
   - Stronger action verbs
   - Quantifiable achievements where possible
   - Better formatting and structure

2. Specific improvement suggestions

Format your response as JSON:
{
    "enhanced_text": "improved resume content here",
    "suggestions": ["suggestion 1", "suggestion 2", ...],
    "keywords_added": ["keyword1", "keyword2", ...],
    "improvements_made": ["improvement1", "improvement2", ...]
}
"""
        return base_prompt

    def _parse_enhancement_response(self, response_text: str) -> Dict:
        """Parse OpenAI response"""
        try:
            # Try to parse as JSON
            result = json.loads(response_text)
            return result
        except json.JSONDecodeError:
            # If not JSON, extract text manually
            return {
                'enhanced_text': response_text,
                'suggestions': ['Enhancement completed successfully'],
                'keywords_added': [],
                'improvements_made': []
            }

    def enhance_section(self, section_name: str, section_content: str, job_description: str = None) -> str:
        """
        Enhance a specific resume section

        Args:
            section_name: Name of the section (e.g., 'Summary', 'Experience')
            section_content: Content of the section
            job_description: Optional job description

        Returns:
            Enhanced section content
        """
        if not self.enabled:
            return section_content

        try:
            prompt = f"""Enhance this {section_name} section of a resume for ATS optimization:

{section_content}
"""

            if job_description:
                prompt += f"\nJob Description: {job_description}\n"

            prompt += f"""
Provide an improved version that:
1. Uses strong action verbs
2. Includes quantifiable achievements
3. Optimizes keywords for ATS
4. Maintains professional tone
5. Keeps it concise and impactful

Return only the enhanced {section_name} section text, no explanations.
"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert resume writer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"Error enhancing {section_name}: {str(e)}")
            return section_content

    def generate_professional_summary(self, resume_text: str, job_description: str = None) -> str:
        """Generate a professional summary from resume content"""
        if not self.enabled:
            return "Professional with demonstrated experience in the field."

        try:
            prompt = f"""Based on this resume, create a compelling professional summary (2-3 sentences):

{resume_text}
"""

            if job_description:
                prompt += f"\nTarget Role: {job_description}\n"

            prompt += """
Create a summary that:
1. Highlights key achievements
2. Showcases relevant skills
3. Demonstrates value proposition
4. Uses strong, confident language
5. Is ATS-friendly

Return only the summary text.
"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert resume writer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            return "Professional with demonstrated experience in the field."

    def optimize_keywords(self, resume_text: str, job_description: str) -> List[str]:
        """Extract and suggest optimized keywords"""
        if not self.enabled or not job_description:
            return []

        try:
            prompt = f"""Analyze this job description and suggest 10-15 important keywords that should be in the resume:

Job Description:
{job_description}

Current Resume:
{resume_text}

Return a JSON array of keywords that are missing or underrepresented in the resume:
["keyword1", "keyword2", ...]
"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an ATS optimization expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=300
            )

            result = response.choices[0].message.content.strip()

            # Parse keywords
            try:
                keywords = json.loads(result)
                return keywords if isinstance(keywords, list) else []
            except:
                # Extract keywords manually if not JSON
                keywords = [k.strip() for k in result.split(',')]
                return keywords[:15]

        except Exception as e:
            print(f"Error optimizing keywords: {str(e)}")
            return []

    def check_api_status(self) -> bool:
        """Check if OpenAI API is configured and working"""
        return self.enabled
