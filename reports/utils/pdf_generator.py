from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io

class PDFGenerator:
    @staticmethod
    def generate_pdf(data):
        """Generate PDF report using reportlab"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(letter),
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Create the story (content) for the PDF
        story = []
        styles = getSampleStyleSheet()
        
        # Add title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30
        )
        title = Paragraph("Report Summary", title_style)
        story.append(title)
        
        # Add summary section
        summary_title = Paragraph("Summary", styles['Heading2'])
        story.append(summary_title)
        story.append(Spacer(1, 12))
        
        # Convert summary dict to table data
        summary_data = [[k.replace('_', ' ').title(), str(v)] for k, v in data['summary'].items()]
        summary_table = Table(summary_data, colWidths=[200, 200])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Add details section
        detail_key = next(k for k in data.keys() if k != 'summary')
        details_title = Paragraph(f"Detailed {detail_key.title()}", styles['Heading2'])
        story.append(details_title)
        story.append(Spacer(1, 12))
        
        # Convert details to table data
        if data[detail_key]:
            # Get headers from first item
            headers = list(data[detail_key][0].keys())
            detail_data = [headers]  # First row is headers
            
            # Add data rows
            for item in data[detail_key]:
                row = [str(item[col]) for col in headers]
                detail_data.append(row)
            
            # Calculate column widths based on content
            col_widths = [max(len(str(row[i])) * 8 for row in detail_data) for i in range(len(headers))]
            col_widths = [min(max(width, 80), 200) for width in col_widths]  # Set min/max widths
            
            detail_table = Table(detail_data, colWidths=col_widths)
            detail_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header row background
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header row text color
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header row font
                ('FONTSIZE', (0, 0), (-1, 0), 12),  # Header row font size
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header row padding
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # Data rows background
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),  # Data rows text color
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Data rows font
                ('FONTSIZE', (0, 1), (-1, -1), 10),  # Data rows font size
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Data rows alignment
                ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Table grid
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])  # Alternating rows
            ]))
            story.append(detail_table)
        
        # Build PDF
        doc.build(story)
        pdf = buffer.getvalue()
        buffer.close()
        
        return pdf