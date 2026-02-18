"""
LaTeX Resume Generator
Generates professional LaTeX resumes with multiple template options
Compatible with Overleaf
"""
import re
from typing import Dict, List


class LaTeXGenerator:
    def __init__(self):
        """Initialize LaTeX generator"""
        self.templates = {
            'modern': self._modern_template,
            'classic': self._classic_template,
            'academic': self._academic_template,
            'two_column': self._two_column_template
        }

    def generate_latex(self, resume_text: str, template: str = 'modern') -> str:
        """
        Generate LaTeX code from resume text

        Args:
            resume_text: Enhanced resume content
            template: Template name (modern, classic, academic, two_column)

        Returns:
            Complete LaTeX code ready for Overleaf
        """
        # Parse resume sections
        sections = self._parse_resume(resume_text)

        # Generate using selected template
        if template in self.templates:
            return self.templates[template](sections)
        else:
            return self.templates['modern'](sections)

    def _parse_resume(self, resume_text: str) -> Dict:
        """Parse resume text into structured sections"""
        sections = {
            'name': '',
            'contact': {},
            'summary': '',
            'experience': [],
            'education': [],
            'skills': [],
            'projects': [],
            'other': []
        }

        lines = resume_text.split('\n')
        current_section = None
        current_content = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Detect section headers
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in ['summary', 'objective', 'profile', 'about']):
                if current_section:
                    self._add_to_section(sections, current_section, current_content)
                current_section = 'summary'
                current_content = []
            elif 'experience' in line_lower or 'work' in line_lower:
                if current_section:
                    self._add_to_section(sections, current_section, current_content)
                current_section = 'experience'
                current_content = []
            elif 'education' in line_lower:
                if current_section:
                    self._add_to_section(sections, current_section, current_content)
                current_section = 'education'
                current_content = []
            elif 'skill' in line_lower:
                if current_section:
                    self._add_to_section(sections, current_section, current_content)
                current_section = 'skills'
                current_content = []
            elif 'project' in line_lower:
                if current_section:
                    self._add_to_section(sections, current_section, current_content)
                current_section = 'projects'
                current_content = []
            else:
                # Extract contact info from first few lines
                if not sections['name'] and '@' not in line and 'http' not in line:
                    sections['name'] = line
                elif '@' in line:
                    sections['contact']['email'] = self._extract_email(line)
                elif 'linkedin' in line_lower:
                    sections['contact']['linkedin'] = self._extract_url(line)
                elif 'github' in line_lower:
                    sections['contact']['github'] = self._extract_url(line)
                elif re.search(r'\+?\d[\d\s\-\(\)]{7,}', line):
                    sections['contact']['phone'] = self._extract_phone(line)
                elif current_section:
                    current_content.append(line)

        # Add last section
        if current_section:
            self._add_to_section(sections, current_section, current_content)

        return sections

    def _add_to_section(self, sections: Dict, section_name: str, content: List):
        """Add parsed content to appropriate section"""
        if section_name == 'summary':
            sections['summary'] = ' '.join(content)
        elif section_name in ['experience', 'education', 'projects']:
            sections[section_name].extend(content)
        elif section_name == 'skills':
            sections['skills'].extend(content)
        else:
            sections['other'].extend(content)

    def _extract_email(self, text: str) -> str:
        """Extract email from text"""
        match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        return match.group(0) if match else ''

    def _extract_url(self, text: str) -> str:
        """Extract URL from text"""
        match = re.search(r'https?://[^\s]+|www\.[^\s]+|linkedin\.com/in/[^\s]+|github\.com/[^\s]+', text)
        return match.group(0) if match else ''

    def _extract_phone(self, text: str) -> str:
        """Extract phone number from text"""
        match = re.search(r'\+?\d[\d\s\-\(\)]{7,}', text)
        return match.group(0) if match else ''

    def _escape_latex(self, text: str) -> str:
        """Escape special LaTeX characters"""
        special_chars = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\^{}',
        }
        for char, escaped in special_chars.items():
            text = text.replace(char, escaped)
        return text

    def _modern_template(self, sections: Dict) -> str:
        """Modern professional template with blue accents"""
        name = sections.get('name', 'Your Name')
        contact = sections.get('contact', {})
        summary = sections.get('summary', '')
        experience = sections.get('experience', [])
        education = sections.get('education', [])
        skills = sections.get('skills', [])

        latex = r'''\documentclass[11pt,a4paper]{article}
\usepackage[left=0.75in,top=0.6in,right=0.75in,bottom=0.6in]{geometry}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{xcolor}
\usepackage{hyperref}

% Define colors
\definecolor{primary}{RGB}{0,51,102}
\definecolor{secondary}{RGB}{100,100,100}

% Custom section formatting
\titleformat{\section}{\Large\bfseries\color{primary}}{}{0em}{}[\titlerule]
\titlespacing{\section}{0pt}{12pt}{6pt}

% Hyperlink setup
\hypersetup{
    colorlinks=true,
    linkcolor=primary,
    filecolor=primary,
    urlcolor=primary,
}

\pagestyle{empty}

\begin{document}

% Name
{\Huge\bfseries\color{primary} ''' + self._escape_latex(name) + r'''}

\vspace{0.3cm}

% Contact Info
{\color{secondary}
'''

        # Add contact info
        contact_parts = []
        if contact.get('email'):
            contact_parts.append(r'\href{mailto:' + contact['email'] + r'}{' + self._escape_latex(contact['email']) + r'}')
        if contact.get('phone'):
            contact_parts.append(self._escape_latex(contact['phone']))
        if contact.get('linkedin'):
            url = contact['linkedin']
            if not url.startswith('http'):
                url = 'https://' + url
            contact_parts.append(r'\href{' + url + r'}{LinkedIn}')
        if contact.get('github'):
            url = contact['github']
            if not url.startswith('http'):
                url = 'https://' + url
            contact_parts.append(r'\href{' + url + r'}{GitHub}')

        latex += ' $\\mid$ '.join(contact_parts)
        latex += r'''
}

\vspace{0.5cm}
'''

        # Summary
        if summary:
            latex += r'''
\section*{Professional Summary}
''' + self._escape_latex(summary) + r'''

'''

        # Experience
        if experience:
            latex += r'''
\section*{Experience}
\begin{itemize}[leftmargin=*,labelsep=0.5em]
'''
            for exp in experience:
                latex += r'\item ' + self._escape_latex(exp) + '\n'
            latex += r'''\end{itemize}

'''

        # Education
        if education:
            latex += r'''
\section*{Education}
\begin{itemize}[leftmargin=*,labelsep=0.5em]
'''
            for edu in education:
                latex += r'\item ' + self._escape_latex(edu) + '\n'
            latex += r'''\end{itemize}

'''

        # Skills
        if skills:
            latex += r'''
\section*{Skills}
'''
            latex += self._escape_latex(' • '.join(skills))

        latex += r'''

\end{document}
'''
        return latex

    def _classic_template(self, sections: Dict) -> str:
        """Classic professional template"""
        name = sections.get('name', 'Your Name')
        contact = sections.get('contact', {})

        latex = r'''\documentclass[11pt,a4paper]{article}
\usepackage[left=1in,top=0.75in,right=1in,bottom=0.75in]{geometry}
\usepackage{enumitem}
\usepackage{hyperref}

\hypersetup{
    colorlinks=true,
    urlcolor=blue,
}

\pagestyle{empty}

\begin{document}

\begin{center}
{\LARGE\textbf{''' + self._escape_latex(name) + r'''}}
\end{center}

\begin{center}
'''
        contact_parts = []
        if contact.get('email'):
            contact_parts.append(self._escape_latex(contact['email']))
        if contact.get('phone'):
            contact_parts.append(self._escape_latex(contact['phone']))

        latex += ' $\\mid$ '.join(contact_parts)
        latex += r'''
\end{center}

\vspace{0.3cm}
\hrule
\vspace{0.5cm}
'''

        # Rest of content
        if sections.get('summary'):
            latex += r'''\textbf{Summary}\\
''' + self._escape_latex(sections['summary']) + r'''

\vspace{0.3cm}
'''

        latex += r'''\end{document}'''
        return latex

    def _academic_template(self, sections: Dict) -> str:
        """Academic CV template"""
        return self._modern_template(sections)  # Simplified for now

    def _two_column_template(self, sections: Dict) -> str:
        """Two-column template"""
        name = sections.get('name', 'Your Name')
        contact = sections.get('contact', {})

        latex = r'''\documentclass[11pt,a4paper]{article}
\usepackage[left=0.5in,top=0.5in,right=0.5in,bottom=0.5in]{geometry}
\usepackage{multicol}
\usepackage{enumitem}
\usepackage{xcolor}
\usepackage{hyperref}

\definecolor{primary}{RGB}{0,51,102}

\hypersetup{
    colorlinks=true,
    urlcolor=primary,
}

\pagestyle{empty}

\begin{document}

{\Large\bfseries\color{primary} ''' + self._escape_latex(name) + r'''}

\vspace{0.2cm}

\begin{multicol}{2}

% Left column content
\textbf{Contact}\\
'''
        if contact.get('email'):
            latex += self._escape_latex(contact['email']) + r'\\'
        if contact.get('phone'):
            latex += self._escape_latex(contact['phone']) + r'\\'

        latex += r'''
\columnbreak

% Right column content
\textbf{Links}\\
'''
        if contact.get('linkedin'):
            latex += r'\href{' + contact.get('linkedin', '') + r'}{LinkedIn}\\'
        if contact.get('github'):
            latex += r'\href{' + contact.get('github', '') + r'}{GitHub}\\'

        latex += r'''
\end{multicol}

\vspace{0.3cm}
\hrule

\end{document}
'''
        return latex
