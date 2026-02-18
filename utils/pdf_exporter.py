"""
PDF Export Module
Converts Word documents to PDF format for resume download
"""
import os
import platform
from io import BytesIO
from typing import Optional
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY


class PDFExporter:
    def __init__(self):
        """Initialize PDF exporter"""
        self.page_size = letter  # US Letter size
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Set up custom paragraph styles"""
        # Name style
        self.styles.add(ParagraphStyle(
            name='ResumeName',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))

        # Contact info style
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#7f8c8d'),
            spaceAfter=12,
            alignment=TA_CENTER
        ))

        # Section heading style
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2c3e50'),
            spaceBefore=12,
            spaceAfter=6,
            fontName='Helvetica-Bold',
            borderWidth=0,
            borderColor=colors.HexColor('#3498db'),
            borderPadding=2,
            borderRadius=0,
        ))

        # Body text style
        self.styles.add(ParagraphStyle(
            name='ResumeBody',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=6,
            alignment=TA_JUSTIFY,
            leading=14
        ))

        # Bullet point style
        self.styles.add(ParagraphStyle(
            name='BulletPoint',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#34495e'),
            leftIndent=20,
            spaceAfter=4,
            bulletIndent=10,
            leading=13
        ))

    def convert_docx_to_pdf(self, docx_buffer: BytesIO, template_style: str = 'modern') -> BytesIO:
        """
        Convert DOCX buffer to PDF

        Args:
            docx_buffer: BytesIO containing DOCX data
            template_style: Style of template ('modern', 'minimal', 'professional', 'creative')

        Returns:
            BytesIO containing PDF data
        """
        try:
            # Try using docx2pdf if available (Windows/Mac)
            if platform.system() in ['Windows', 'Darwin']:
                return self._convert_using_docx2pdf(docx_buffer)
            else:
                # For Linux, use reportlab to create PDF from parsed DOCX
                return self._convert_using_python_docx(docx_buffer, template_style)

        except Exception as e:
            print(f"Error converting DOCX to PDF: {str(e)}")
            # Fallback: create basic PDF
            return self._create_fallback_pdf()

    def _convert_using_docx2pdf(self, docx_buffer: BytesIO) -> BytesIO:
        """Convert using docx2pdf library (Windows/Mac)"""
        import tempfile
        from docx2pdf import convert

        # Save DOCX to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as docx_temp:
            docx_temp.write(docx_buffer.getvalue())
            docx_path = docx_temp.name

        # Convert to PDF
        pdf_path = docx_path.replace('.docx', '.pdf')
        convert(docx_path, pdf_path)

        # Read PDF into buffer
        with open(pdf_path, 'rb') as pdf_file:
            pdf_buffer = BytesIO(pdf_file.read())

        # Clean up temp files
        os.unlink(docx_path)
        os.unlink(pdf_path)

        return pdf_buffer

    def _convert_using_python_docx(self, docx_buffer: BytesIO, template_style: str) -> BytesIO:
        """Convert by parsing DOCX and recreating in PDF"""
        from docx import Document

        # Parse DOCX
        docx_buffer.seek(0)
        doc = Document(docx_buffer)

        # Create PDF
        pdf_buffer = BytesIO()
        pdf = SimpleDocTemplate(
            pdf_buffer,
            pagesize=self.page_size,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )

        # Build PDF content
        story = []

        for para in doc.paragraphs:
            if para.text.strip():
                # Determine style based on formatting
                if para.style.name.startswith('Heading'):
                    style = self.styles['SectionHeading']
                elif len(para.text) < 50 and para.runs and para.runs[0].bold:
                    style = self.styles['ResumeName']
                else:
                    style = self.styles['ResumeBody']

                # Add paragraph to story
                story.append(Paragraph(para.text, style))
                story.append(Spacer(1, 0.1*inch))

        # Build PDF
        pdf.build(story)
        pdf_buffer.seek(0)

        return pdf_buffer

    def create_pdf_from_data(self, resume_data: dict, template_style: str = 'modern') -> BytesIO:
        """
        Create PDF directly from resume data

        Args:
            resume_data: Dictionary containing resume information
            template_style: Style of template

        Returns:
            BytesIO containing PDF data
        """
        pdf_buffer = BytesIO()
        pdf = SimpleDocTemplate(
            pdf_buffer,
            pagesize=self.page_size,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )

        story = []

        # Personal Information
        personal_info = resume_data.get('personal_info', {})
        if personal_info.get('full_name'):
            story.append(Paragraph(personal_info['full_name'], self.styles['ResumeName']))

        # Contact details
        contact_parts = []
        if personal_info.get('email'):
            contact_parts.append(personal_info['email'])
        if personal_info.get('phone'):
            contact_parts.append(personal_info['phone'])
        if personal_info.get('location'):
            contact_parts.append(personal_info['location'])

        if contact_parts:
            story.append(Paragraph(' | '.join(contact_parts), self.styles['ContactInfo']))
            story.append(Spacer(1, 0.2*inch))

        # Summary
        if resume_data.get('summary'):
            story.append(Paragraph('PROFESSIONAL SUMMARY', self.styles['SectionHeading']))
            story.append(Paragraph(resume_data['summary'], self.styles['ResumeBody']))
            story.append(Spacer(1, 0.15*inch))

        # Experience
        experiences = resume_data.get('experiences', [])
        if experiences:
            story.append(Paragraph('EXPERIENCE', self.styles['SectionHeading']))
            for exp in experiences:
                # Company and role
                if exp.get('role') and exp.get('company'):
                    story.append(Paragraph(
                        f"<b>{exp['role']}</b> - {exp['company']}",
                        self.styles['ResumeBody']
                    ))

                # Duration
                if exp.get('duration'):
                    story.append(Paragraph(
                        f"<i>{exp['duration']}</i>",
                        self.styles['ResumeBody']
                    ))

                # Description
                if exp.get('description'):
                    desc_lines = exp['description'].split('\n')
                    for line in desc_lines:
                        if line.strip():
                            story.append(Paragraph(
                                f"• {line.strip()}",
                                self.styles['BulletPoint']
                            ))

                story.append(Spacer(1, 0.1*inch))

        # Education
        education = resume_data.get('education', [])
        if education:
            story.append(Paragraph('EDUCATION', self.styles['SectionHeading']))
            for edu in education:
                if edu.get('degree') and edu.get('school'):
                    story.append(Paragraph(
                        f"<b>{edu['degree']}</b> - {edu['school']}",
                        self.styles['ResumeBody']
                    ))
                if edu.get('year'):
                    story.append(Paragraph(
                        f"<i>{edu['year']}</i>",
                        self.styles['ResumeBody']
                    ))
                story.append(Spacer(1, 0.1*inch))

        # Skills
        skills = resume_data.get('skills_categories', {})
        all_skills = []
        for category, skill_list in skills.items():
            if skill_list:
                all_skills.extend(skill_list)

        if all_skills:
            story.append(Paragraph('SKILLS', self.styles['SectionHeading']))
            story.append(Paragraph(', '.join(all_skills), self.styles['ResumeBody']))
            story.append(Spacer(1, 0.15*inch))

        # Projects
        projects = resume_data.get('projects', [])
        if projects:
            story.append(Paragraph('PROJECTS', self.styles['SectionHeading']))
            for proj in projects:
                if proj.get('name'):
                    story.append(Paragraph(f"<b>{proj['name']}</b>", self.styles['ResumeBody']))
                if proj.get('description'):
                    story.append(Paragraph(proj['description'], self.styles['BulletPoint']))
                story.append(Spacer(1, 0.1*inch))

        # Build PDF
        pdf.build(story)
        pdf_buffer.seek(0)

        return pdf_buffer

    def _create_fallback_pdf(self) -> BytesIO:
        """Create a fallback PDF in case of errors"""
        pdf_buffer = BytesIO()
        pdf = SimpleDocTemplate(pdf_buffer, pagesize=self.page_size)

        story = [
            Paragraph("Resume", self.styles['ResumeName']),
            Spacer(1, 0.5*inch),
            Paragraph("PDF export encountered an error. Please download the Word version instead.", self.styles['ResumeBody'])
        ]

        pdf.build(story)
        pdf_buffer.seek(0)

        return pdf_buffer
