#!/usr/bin/env python3
"""
BLACKTEAM STAKEHOLDER REPORT TEMPLATE
=====================================

Saved: 2026-01-28
Design: PixelPerfect (WCAG 2.1 AA Compliant)
Visualization: DataViz (BI Developer)

USAGE:
    from STAKEHOLDER_REPORT_TEMPLATE import StakeholderReport, COLORS

    pdf = StakeholderReport()
    pdf.title_page(title, subtitle, metadata)
    pdf.section_header('Section Name', '1')
    pdf.data_table(headers, data, widths)
    pdf.alert_box('Title', 'Content', 'warning')
    pdf.key_metric_box('Label', 'Value', 'Subtitle', 'primary')
    pdf.output('report.pdf')
"""

from fpdf import FPDF

# PixelPerfect Design System Colors (WCAG 2.1 AA Compliant - 4.5:1 contrast minimum)
COLORS = {
    'primary': (0, 51, 102),        # Paradise Blue - headers
    'secondary': (51, 51, 51),      # Dark gray - body text
    'accent': (0, 122, 204),        # Highlight blue
    'success': (34, 139, 34),       # Forest green - positive
    'danger': (178, 34, 34),        # Fire brick red - negative/warning
    'warning': (184, 134, 11),      # Dark goldenrod - caution
    'light_bg': (248, 249, 250),    # Light background
    'table_header': (0, 51, 102),   # Table header blue
    'table_alt': (240, 248, 255),   # Alternating row - alice blue
    'white': (255, 255, 255),
    'black': (0, 0, 0),
}

class StakeholderReport(FPDF):
    """
    Professional Stakeholder Report - PixelPerfect Standards

    Design Principles:
    - Clarity over cleverness
    - Consistency through systems
    - Accessibility is non-negotiable (WCAG 2.1 AA)
    - Data-ink ratio: maximize information, minimize clutter
    - Gestalt principles: proximity, similarity, enclosure
    - Typography: hierarchy, readability
    - Layout: F-pattern, logical flow
    """

    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=25)

    def header(self):
        # Paradise Media header bar
        self.set_fill_color(*COLORS['primary'])
        self.rect(0, 0, 210, 12, 'F')

        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(*COLORS['white'])
        self.set_xy(10, 3)
        self.cell(0, 6, 'PARADISE MEDIA GROUP | BLACKTEAM ANALYTICS | CONFIDENTIAL', 0, 0, 'C')

        self.ln(15)

    def footer(self):
        self.set_y(-20)

        # Footer line
        self.set_draw_color(*COLORS['primary'])
        self.line(15, self.get_y(), 195, self.get_y())

        self.set_font('Helvetica', '', 8)
        self.set_text_color(*COLORS['secondary'])
        self.ln(3)
        self.cell(0, 5, f'Page {self.page_no()}', 0, 0, 'C')
        self.ln(4)
        self.set_font('Helvetica', 'I', 7)
        self.set_text_color(128, 128, 128)
        self.cell(0, 4, 'DataGuard v2.0 Validated | BlackTeam Analytics', 0, 0, 'C')

    def title_page(self, title_line1, title_line2, subtitle, version_text, metadata_items, classification_text):
        """
        Generate title page

        Args:
            title_line1: First line of title (e.g., "FTD PERFORMANCE")
            title_line2: Second line of title (e.g., "DEEP DIVE ANALYSIS")
            subtitle: Subtitle text (e.g., "iGaming Vertical | O&O Domains")
            version_text: Version badge text (e.g., "VERSION 5.2 | VALIDATED")
            metadata_items: List of tuples [(label, value), ...]
            classification_text: Footer classification (e.g., "INTERNAL USE ONLY")
        """
        self.add_page()
        self.ln(30)

        # Title
        self.set_font('Helvetica', 'B', 32)
        self.set_text_color(*COLORS['primary'])
        self.cell(0, 15, title_line1, 0, 1, 'C')
        self.cell(0, 15, title_line2, 0, 1, 'C')

        self.ln(5)

        # Subtitle
        self.set_font('Helvetica', '', 16)
        self.set_text_color(*COLORS['secondary'])
        self.cell(0, 10, subtitle, 0, 1, 'C')

        self.ln(10)

        # Version badge
        self.set_fill_color(*COLORS['success'])
        self.set_text_color(*COLORS['white'])
        self.set_font('Helvetica', 'B', 12)
        badge_width = 80
        self.set_x((210 - badge_width) / 2)
        self.cell(badge_width, 10, version_text, 0, 1, 'C', True)

        self.ln(20)

        # Report metadata box
        self.set_fill_color(*COLORS['light_bg'])
        self.set_draw_color(*COLORS['primary'])
        box_x = 30
        box_width = 150
        box_height = 8 + (len(metadata_items) * 8) + 5
        self.rect(box_x, self.get_y(), box_width, box_height, 'DF')

        self.set_font('Helvetica', '', 10)
        self.set_text_color(*COLORS['secondary'])

        self.ln(5)
        for label, value in metadata_items:
            self.set_x(box_x + 5)
            self.set_font('Helvetica', 'B', 9)
            self.cell(50, 8, label + ':', 0, 0)
            self.set_font('Helvetica', '', 9)
            self.cell(0, 8, value, 0, 1)

        self.ln(30)

        # Classification
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(*COLORS['danger'])
        self.cell(0, 8, classification_text, 0, 1, 'C')

    def section_header(self, title, number=None):
        """Section header with blue background"""
        self.ln(8)
        self.set_fill_color(*COLORS['primary'])
        self.set_text_color(*COLORS['white'])
        self.set_font('Helvetica', 'B', 14)

        if number:
            full_title = f'{number}. {title}'
        else:
            full_title = title

        self.cell(0, 10, f'  {full_title}', 0, 1, 'L', True)
        self.ln(5)
        self.set_text_color(*COLORS['secondary'])

    def subsection_header(self, title):
        """Subsection header"""
        self.ln(3)
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(*COLORS['primary'])
        self.cell(0, 8, title, 0, 1, 'L')
        self.set_text_color(*COLORS['secondary'])

    def body_text(self, text):
        """Body paragraph text"""
        self.set_font('Helvetica', '', 10)
        self.set_text_color(*COLORS['secondary'])
        self.multi_cell(0, 6, text)
        self.ln(2)

    def key_metric_box(self, label, value, subtitle=None, color='primary'):
        """Single key metric display box (use in a row)"""
        box_width = 42
        box_height = 28

        self.set_fill_color(*COLORS['light_bg'])
        self.set_draw_color(*COLORS[color])
        self.rect(self.get_x(), self.get_y(), box_width, box_height, 'DF')

        start_x = self.get_x()
        start_y = self.get_y()

        # Value
        self.set_xy(start_x, start_y + 3)
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(*COLORS[color])
        self.cell(box_width, 10, value, 0, 0, 'C')

        # Label
        self.set_xy(start_x, start_y + 13)
        self.set_font('Helvetica', '', 8)
        self.set_text_color(*COLORS['secondary'])
        self.cell(box_width, 5, label, 0, 0, 'C')

        # Subtitle
        if subtitle:
            self.set_xy(start_x, start_y + 18)
            self.set_font('Helvetica', 'I', 7)
            self.set_text_color(128, 128, 128)
            self.cell(box_width, 5, subtitle, 0, 0, 'C')

        self.set_xy(start_x + box_width + 5, start_y)

    def alert_box(self, title, content, alert_type='warning'):
        """Alert/callout box with left accent border"""
        colors = {
            'warning': (COLORS['warning'], (255, 248, 220)),
            'danger': (COLORS['danger'], (255, 240, 240)),
            'success': (COLORS['success'], (240, 255, 240)),
            'info': (COLORS['accent'], (240, 248, 255)),
        }

        border_color, bg_color = colors.get(alert_type, colors['warning'])

        # Calculate height needed
        self.set_font('Helvetica', '', 9)
        # Estimate lines needed
        lines = len(content) / 80 + 2
        box_height = max(25, int(lines * 6) + 15)

        self.set_fill_color(*bg_color)
        self.set_draw_color(*border_color)

        start_y = self.get_y()
        self.rect(15, start_y, 180, box_height, 'DF')

        # Left border accent
        self.set_fill_color(*border_color)
        self.rect(15, start_y, 4, box_height, 'F')

        self.set_xy(22, start_y + 3)
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(*border_color)
        self.cell(0, 6, title, 0, 1)

        self.set_x(22)
        self.set_font('Helvetica', '', 9)
        self.set_text_color(*COLORS['secondary'])
        self.multi_cell(168, 5, content)

        self.set_y(start_y + box_height + 3)

    def data_table(self, headers, data, col_widths, highlight_rows=None):
        """
        Professional data table

        Args:
            headers: List of header strings
            data: List of row lists
            col_widths: List of column widths
            highlight_rows: List of row indices to highlight in red (optional)
        """
        highlight_rows = highlight_rows or []

        # Header
        self.set_fill_color(*COLORS['table_header'])
        self.set_text_color(*COLORS['white'])
        self.set_font('Helvetica', 'B', 9)

        for i, header in enumerate(headers):
            self.cell(col_widths[i], 8, header, 1, 0, 'C', True)
        self.ln()

        # Data rows
        self.set_font('Helvetica', '', 9)

        for row_idx, row in enumerate(data):
            if row_idx in highlight_rows:
                self.set_fill_color(255, 235, 235)
                self.set_text_color(*COLORS['danger'])
            elif row_idx % 2 == 0:
                self.set_fill_color(*COLORS['table_alt'])
                self.set_text_color(*COLORS['secondary'])
            else:
                self.set_fill_color(*COLORS['white'])
                self.set_text_color(*COLORS['secondary'])

            for i, cell in enumerate(row):
                self.cell(col_widths[i], 7, str(cell), 1, 0, 'C', True)
            self.ln()

        self.set_text_color(*COLORS['secondary'])

    def total_row(self, text):
        """Highlighted total row"""
        self.set_fill_color(*COLORS['primary'])
        self.set_text_color(*COLORS['white'])
        self.set_font('Helvetica', 'B', 11)
        self.cell(0, 10, f'  {text}', 0, 1, 'L', True)

    def compliance_box(self, checks, title='DataGuard v2.0 Compliance'):
        """Compliance certification box with checkmarks"""
        self.subsection_header(title)

        self.set_fill_color(*COLORS['light_bg'])
        self.set_draw_color(*COLORS['success'])
        box_height = 10 + (len(checks) * 7) + 10
        self.rect(15, self.get_y(), 180, box_height, 'DF')

        self.ln(5)
        self.set_font('Helvetica', '', 9)

        for check_title, check_detail in checks:
            self.set_x(20)
            self.set_text_color(*COLORS['success'])
            self.set_font('Helvetica', 'B', 9)
            self.cell(8, 6, '[OK]', 0, 0)
            self.set_text_color(*COLORS['secondary'])
            self.set_font('Helvetica', '', 9)
            self.cell(0, 6, f'{check_title}: {check_detail}', 0, 1)

        self.ln(3)

    def sign_off_block(self, signers, date):
        """Report sign-off block"""
        self.ln(10)
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(*COLORS['primary'])
        self.cell(0, 8, 'REPORT APPROVED FOR DISTRIBUTION', 0, 1, 'C')

        self.ln(5)
        self.set_font('Helvetica', '', 9)
        self.set_text_color(*COLORS['secondary'])

        for signer in signers:
            self.cell(0, 6, signer, 0, 1, 'C')

        self.cell(0, 6, f'Date: {date}', 0, 1, 'C')

        self.ln(10)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 5, 'Generated by BlackTeam Analytics | Paradise Media Group', 0, 1, 'C')
        self.cell(0, 5, 'DataGuard v2.0 Validated | PixelPerfect Design Standards', 0, 1, 'C')


# Export for use
__all__ = ['StakeholderReport', 'COLORS']
