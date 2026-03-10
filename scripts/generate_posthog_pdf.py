#!/usr/bin/env python3
"""
PostHog Analytics PDF Report Generator
DataViz Professional Output - Director Rule 2 Compliant (No Broken Tables)

Version: 2.0.0
Created: 2026-01-22
Persona: DataViz (Senior BI Developer)
Colors: Orange & Black (Paradise Media Brand)
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from datetime import datetime
import os

# Color Palette (Paradise Media Brand - Orange & Black)
COLORS = {
    'primary': colors.HexColor('#f97316'),      # Orange
    'primary_dark': colors.HexColor('#ea580c'), # Dark Orange
    'secondary': colors.HexColor('#1a1a1a'),    # Black
    'accent': colors.HexColor('#22c55e'),       # Green (good)
    'warning': colors.HexColor('#eab308'),      # Yellow (warning)
    'danger': colors.HexColor('#ef4444'),       # Red (bad)
    'light_gray': colors.HexColor('#f5f5f5'),
    'medium_gray': colors.HexColor('#e5e5e5'),
    'dark_gray': colors.HexColor('#525252'),
    'white': colors.white,
    'black': colors.black,
}

# Logo path
LOGO_PATH = "/mnt/c/Users/andre/Downloads/paradisemedia.jpg"

def get_rating_color(rating):
    if 'Good' in rating or 'Excellent' in rating:
        return COLORS['accent']
    elif 'Improvement' in rating:
        return COLORS['warning']
    elif 'Poor' in rating:
        return COLORS['danger']
    return COLORS['dark_gray']


class PDFReport:
    def __init__(self, output_path, title="PostHog Analytics Report"):
        self.output_path = output_path
        self.title = title
        self.elements = []
        self.styles = getSampleStyleSheet()
        self._setup_styles()

    def _setup_styles(self):
        """Setup custom styles - Orange & Black theme"""

        # Title style
        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=self.styles['Heading1'],
            fontSize=22,
            textColor=COLORS['secondary'],
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
        ))

        # Subtitle
        self.styles.add(ParagraphStyle(
            name='ReportSubtitle',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=COLORS['dark_gray'],
            spaceAfter=4,
            alignment=TA_CENTER,
        ))

        # Section header - Orange
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=COLORS['primary'],
            spaceBefore=20,
            spaceAfter=10,
            fontName='Helvetica-Bold',
        ))

        # Subsection header
        self.styles.add(ParagraphStyle(
            name='SubsectionHeader',
            parent=self.styles['Heading3'],
            fontSize=11,
            textColor=COLORS['secondary'],
            spaceBefore=12,
            spaceAfter=6,
            fontName='Helvetica-Bold',
        ))

        # Body text
        self.styles['BodyText'].fontSize = 9
        self.styles['BodyText'].textColor = COLORS['secondary']
        self.styles['BodyText'].spaceAfter = 4

        # KPI Value - Large
        self.styles.add(ParagraphStyle(
            name='KPIValue',
            parent=self.styles['Normal'],
            fontSize=24,
            textColor=COLORS['primary'],
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            leading=28,
        ))

        # KPI Label
        self.styles.add(ParagraphStyle(
            name='KPILabel',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=COLORS['dark_gray'],
            alignment=TA_CENTER,
            spaceBefore=4,
        ))

        # Status styles
        self.styles.add(ParagraphStyle(
            name='StatusGood',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=COLORS['accent'],
            fontName='Helvetica-Bold',
        ))

        self.styles.add(ParagraphStyle(
            name='StatusWarning',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=COLORS['warning'],
            fontName='Helvetica-Bold',
        ))

        self.styles.add(ParagraphStyle(
            name='StatusBad',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=COLORS['danger'],
            fontName='Helvetica-Bold',
        ))

        # Footer
        self.styles.add(ParagraphStyle(
            name='FooterText',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=COLORS['dark_gray'],
            alignment=TA_CENTER,
        ))

    def add_logo_header(self, domain, generated_at, period):
        """Add header with Paradise Media logo"""
        # Logo
        if os.path.exists(LOGO_PATH):
            logo = Image(LOGO_PATH, width=1.5*inch, height=0.5*inch)
            logo.hAlign = 'CENTER'
            self.elements.append(logo)
            self.elements.append(Spacer(1, 12))

        # Title
        self.elements.append(Paragraph("PostHog Analytics Report", self.styles['ReportTitle']))
        self.elements.append(Paragraph(f"<b>{domain}</b>", self.styles['ReportSubtitle']))
        self.elements.append(Paragraph(f"Generated: {generated_at} | Period: {period}", self.styles['ReportSubtitle']))

        # Orange divider line
        self.elements.append(Spacer(1, 8))
        self.elements.append(HRFlowable(width="100%", thickness=3, color=COLORS['primary']))
        self.elements.append(Spacer(1, 16))

    def add_section(self, title):
        """Add section header with line break before"""
        self.elements.append(Spacer(1, 8))
        self.elements.append(Paragraph(title, self.styles['SectionHeader']))
        self.elements.append(HRFlowable(width="100%", thickness=1, color=COLORS['medium_gray']))
        self.elements.append(Spacer(1, 8))

    def add_subsection(self, title):
        """Add subsection header"""
        self.elements.append(Spacer(1, 6))
        self.elements.append(Paragraph(title, self.styles['SubsectionHeader']))

    def add_text(self, text, style='BodyText'):
        """Add body text"""
        self.elements.append(Paragraph(text, self.styles[style]))

    def add_spacer(self, height=12):
        """Add vertical space"""
        self.elements.append(Spacer(1, height))

    def add_kpi_row(self, kpis):
        """
        Add KPI cards in a row - FIXED: No overlapping
        kpis is list of (value, label) tuples
        """
        num_kpis = len(kpis)
        card_width = 1.5 * inch

        # Build individual card tables
        cards = []
        for value, label in kpis:
            card_content = [
                [Paragraph(str(value), self.styles['KPIValue'])],
                [Paragraph(label, self.styles['KPILabel'])]
            ]
            card = Table(card_content, colWidths=[card_width])
            card.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), COLORS['light_gray']),
                ('BOX', (0, 0), (-1, -1), 2, COLORS['primary']),
                ('TOPPADDING', (0, 0), (-1, 0), 15),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
                ('TOPPADDING', (0, 1), (-1, 1), 5),
                ('BOTTOMPADDING', (0, 1), (-1, 1), 12),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            cards.append(card)

        # Create row table with cards
        row_table = Table([cards], colWidths=[card_width + 10] * num_kpis)
        row_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ]))

        self.elements.append(row_table)
        self.elements.append(Spacer(1, 16))

    def add_table(self, headers, data, col_widths=None, wrap_cols=None):
        """
        Add professional table - Director Rule 2: NO BROKEN TABLES
        Uses KeepTogether to prevent page splits

        Args:
            headers: List of column headers
            data: List of row data
            col_widths: Optional list of column widths
            wrap_cols: List of column indices that should wrap text (default: [0] for first column)
        """
        # Default: wrap first column (usually URLs/page names)
        if wrap_cols is None:
            wrap_cols = [0]

        # Create cell style for wrapped text
        cell_style = ParagraphStyle(
            'TableCell',
            parent=self.styles['Normal'],
            fontSize=8,
            leading=10,
            textColor=COLORS['secondary'],
            wordWrap='CJK',  # Enables breaking at any character
        )

        cell_style_right = ParagraphStyle(
            'TableCellRight',
            parent=cell_style,
            alignment=TA_RIGHT,
        )

        header_style = ParagraphStyle(
            'TableHeader',
            parent=self.styles['Normal'],
            fontSize=9,
            fontName='Helvetica-Bold',
            textColor=COLORS['white'],
        )

        # Convert headers to Paragraphs
        header_row = [Paragraph(str(h), header_style) for h in headers]

        # Convert data cells to Paragraphs with proper wrapping
        processed_data = []
        for row in data:
            new_row = []
            for i, cell in enumerate(row):
                if i in wrap_cols:
                    # Wrap text in first/specified columns
                    new_row.append(Paragraph(str(cell), cell_style))
                else:
                    # Right-align numeric columns
                    new_row.append(Paragraph(str(cell), cell_style_right))
            processed_data.append(new_row)

        table_data = [header_row] + processed_data

        if col_widths is None:
            num_cols = len(headers)
            col_widths = [6.5*inch / num_cols] * num_cols

        table = Table(table_data, colWidths=col_widths, repeatRows=1)

        style_commands = [
            # Header - Orange background
            ('BACKGROUND', (0, 0), (-1, 0), COLORS['primary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), COLORS['white']),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('TOPPADDING', (0, 0), (-1, 0), 6),

            # Body - reduced padding
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
            ('TOPPADDING', (0, 1), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),

            # Alternating rows
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [COLORS['white'], COLORS['light_gray']]),

            # Grid - subtle
            ('GRID', (0, 0), (-1, -1), 0.5, COLORS['medium_gray']),
            ('LINEBELOW', (0, 0), (-1, 0), 2, COLORS['primary_dark']),

            # Alignment
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]

        table.setStyle(TableStyle(style_commands))

        # KeepTogether prevents table from splitting across pages
        self.elements.append(KeepTogether([table]))
        self.elements.append(Spacer(1, 12))

    def add_seo_table(self, headers, data):
        """
        Add SEO analysis table with proper column widths for Page/ETV/Keywords/P1/P2-3/P4-10
        Specifically designed for DataForSEO Top 20 pages tables
        """
        # Optimized column widths for SEO data (total ~6.5 inches)
        # Page: 2.4in, ETV: 0.7in, Keywords: 0.7in, P1: 0.6in, P2-3: 0.6in, P4-10: 0.6in
        col_widths = [2.4*inch, 0.65*inch, 0.7*inch, 0.55*inch, 0.55*inch, 0.55*inch]

        # Adjust if fewer columns
        if len(headers) < 6:
            col_widths = col_widths[:len(headers)]

        # Cell styles
        cell_style = ParagraphStyle(
            'SEOCell',
            parent=self.styles['Normal'],
            fontSize=7,
            leading=9,
            textColor=COLORS['secondary'],
            wordWrap='CJK',
        )

        cell_style_right = ParagraphStyle(
            'SEOCellRight',
            parent=cell_style,
            alignment=TA_RIGHT,
        )

        header_style = ParagraphStyle(
            'SEOHeader',
            parent=self.styles['Normal'],
            fontSize=8,
            fontName='Helvetica-Bold',
            textColor=COLORS['white'],
        )

        # Convert headers
        header_row = [Paragraph(str(h), header_style) for h in headers]

        # Convert data - first column wraps, rest right-aligned
        processed_data = []
        for row in data:
            new_row = []
            for i, cell in enumerate(row):
                if i == 0:
                    # URL column - wrap text
                    new_row.append(Paragraph(str(cell), cell_style))
                else:
                    new_row.append(Paragraph(str(cell), cell_style_right))
            processed_data.append(new_row)

        table_data = [header_row] + processed_data
        table = Table(table_data, colWidths=col_widths, repeatRows=1)

        style_commands = [
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), COLORS['primary']),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
            ('TOPPADDING', (0, 0), (-1, 0), 4),

            # Body - minimal padding
            ('BOTTOMPADDING', (0, 1), (-1, -1), 2),
            ('TOPPADDING', (0, 1), (-1, -1), 2),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),

            # Alternating rows
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [COLORS['white'], COLORS['light_gray']]),

            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, COLORS['medium_gray']),
            ('LINEBELOW', (0, 0), (-1, 0), 2, COLORS['primary_dark']),

            # Alignment
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]

        table.setStyle(TableStyle(style_commands))
        self.elements.append(KeepTogether([table]))
        self.elements.append(Spacer(1, 12))

    def add_rating_table(self, headers, data, rating_col=2):
        """Add table with color-coded rating column"""
        table_data = [headers] + data
        num_cols = len(headers)
        col_widths = [6.5*inch / num_cols] * num_cols

        table = Table(table_data, colWidths=col_widths, repeatRows=1)

        style_commands = [
            ('BACKGROUND', (0, 0), (-1, 0), COLORS['primary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), COLORS['white']),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, COLORS['medium_gray']),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]

        # Color-code rating cells
        for i, row in enumerate(data, start=1):
            if len(row) > rating_col:
                rating = str(row[rating_col])
                bg_color = get_rating_color(rating)
                style_commands.append(('BACKGROUND', (rating_col, i), (rating_col, i), bg_color))
                style_commands.append(('TEXTCOLOR', (rating_col, i), (rating_col, i), COLORS['white']))
                style_commands.append(('FONTNAME', (rating_col, i), (rating_col, i), 'Helvetica-Bold'))

        table.setStyle(TableStyle(style_commands))
        self.elements.append(KeepTogether([table]))
        self.elements.append(Spacer(1, 16))

    def add_status_badge(self, status, is_good=True):
        """Add status badge"""
        style = 'StatusGood' if is_good else 'StatusWarning'
        icon = "✓" if is_good else "⚠"
        self.elements.append(Paragraph(f"{icon} {status}", self.styles[style]))
        self.elements.append(Spacer(1, 8))

    def add_alert_box(self, title, items, alert_type='warning'):
        """Add alert/info box"""
        border_color = COLORS['warning'] if alert_type == 'warning' else COLORS['danger']

        content = [[Paragraph(f"<b>⚠ {title}</b>", self.styles['BodyText'])]]
        for item in items:
            content.append([Paragraph(f"• {item}", self.styles['BodyText'])])

        table = Table(content, colWidths=[6.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), COLORS['light_gray']),
            ('BOX', (0, 0), (-1, -1), 2, border_color),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        self.elements.append(KeepTogether([table]))
        self.elements.append(Spacer(1, 16))

    def add_page_break(self):
        """Force page break"""
        self.elements.append(PageBreak())

    def _add_footer(self, canvas, doc):
        """Add page footer"""
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(COLORS['dark_gray'])

        # Left: Report name
        canvas.drawString(0.75*inch, 0.5*inch, "PostHog Analytics Report")

        # Center: Page number
        canvas.drawCentredString(4.25*inch, 0.5*inch, f"Page {doc.page}")

        # Right: Domain and date
        canvas.drawRightString(7.75*inch, 0.5*inch, f"hudsonreporter.com | {datetime.now().strftime('%Y-%m-%d')}")

        # Orange line above footer
        canvas.setStrokeColor(COLORS['primary'])
        canvas.setLineWidth(1)
        canvas.line(0.75*inch, 0.7*inch, 7.75*inch, 0.7*inch)

        canvas.restoreState()

    def build(self):
        """Build and save PDF"""
        doc = SimpleDocTemplate(
            self.output_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.85*inch
        )
        doc.build(self.elements, onFirstPage=self._add_footer, onLaterPages=self._add_footer)
        return self.output_path


def generate_hudsonreporter_pdf():
    """Generate professional PDF report for hudsonreporter.com"""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_path = f"/home/andre/reports/hudsonreporter/posthog_report_{timestamp}.pdf"

    pdf = PDFReport(output_path)

    # === HEADER WITH LOGO ===
    pdf.add_logo_header(
        domain="hudsonreporter.com",
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
        period="Last 7 Days"
    )

    # === OVERVIEW KPIs ===
    pdf.add_section("Overview")
    pdf.add_kpi_row([
        ("2,718", "Total Events"),
        ("685", "Unique Users"),
        ("706", "Sessions"),
        ("3", "Conversions"),
    ])

    # === CONVERSIONS ===
    pdf.add_section("Conversions")
    pdf.add_table(
        headers=["Conversion Type", "Count"],
        data=[
            ["Content Consumed", "2"],
            ["Session Summary", "1"],
            ["TOTAL", "3"],
        ],
        col_widths=[4.5*inch, 2*inch]
    )
    pdf.add_status_badge("Conversion Tracker DEPLOYED", is_good=True)

    # === WEB VITALS ===
    pdf.add_section("Core Web Vitals")
    pdf.add_rating_table(
        headers=["Metric", "Value", "Rating"],
        data=[
            ["LCP (Largest Contentful Paint)", "2,076ms", "Needs Improvement"],
            ["CLS (Cumulative Layout Shift)", "0.107", "Needs Improvement"],
            ["INP (Interaction to Next Paint)", "306ms", "Needs Improvement"],
        ],
        rating_col=2
    )

    # === NAVBOOST METRICS ===
    pdf.add_section("NavBoost Engagement Metrics")

    pdf.add_subsection("Dwell Time (Target: > 90s)")
    pdf.add_kpi_row([
        ("7.7s", "Average"),
        ("1.5s", "Median"),
    ])

    pdf.add_table(
        headers=["Rating", "Sessions", "% of Total"],
        data=[
            ["Very Bad (<10s)", "4", "66.7%"],
            ["Weak (10-30s)", "2", "33.3%"],
            ["Normal (30-90s)", "0", "0%"],
            ["Strong (>90s)", "0", "0%"],
        ],
        col_widths=[2.5*inch, 2*inch, 2*inch]
    )

    pdf.add_subsection("NavBoost Events")
    pdf.add_table(
        headers=["Event", "Count"],
        data=[
            ["navboost:session_start", "443"],
            ["navboost:scroll_zone", "159"],
            ["navboost:cta_visible", "121"],
            ["navboost:session_end", "6"],
        ],
        col_widths=[4.5*inch, 2*inch]
    )
    pdf.add_status_badge("NavBoost Tracker DEPLOYED", is_good=True)

    # === DAILY TREND ===
    pdf.add_section("Daily Trend (Last 7 Days)")
    pdf.add_table(
        headers=["Date", "Events", "Users"],
        data=[
            ["2026-01-22", "1,214", "342"],
            ["2026-01-21", "1,504", "348"],
        ],
        col_widths=[2.5*inch, 2*inch, 2*inch]
    )

    # === PAGE BREAK ===
    pdf.add_page_break()

    # === EVENT BREAKDOWN ===
    pdf.add_section("Event Breakdown (Top 10)")
    pdf.add_table(
        headers=["Event", "Count"],
        data=[
            ["$pageview", "820"],
            ["$web_vitals", "603"],
            ["navboost:session_start", "443"],
            ["$pageleave", "394"],
            ["navboost:scroll_zone", "159"],
            ["$autocapture", "124"],
            ["navboost:cta_visible", "121"],
            ["$set", "24"],
            ["ad:impression", "19"],
            ["navboost:session_end", "6"],
        ],
        col_widths=[4.5*inch, 2*inch]
    )

    # === TOP PAGES ===
    pdf.add_section("Top Pages")
    pdf.add_table(
        headers=["Page", "Views"],
        data=[
            ["/", "118"],
            ["/news/west-new-york/west-new-york-approves...", "52"],
            ["/author/moses/", "41"],
            ["/sports/heat-knicks-rivalry/", "28"],
            ["/environment/nj-approves-air-permit-nese/", "27"],
            ["/entertainment/hollywood-star-skips...", "16"],
            ["/site/news.cfm", "10"],
            ["/news/", "7"],
            ["/robert-burns-supper/", "6"],
            ["/entertainment/", "6"],
        ],
        col_widths=[4.5*inch, 2*inch]
    )

    # === TRAFFIC SOURCES ===
    pdf.add_section("Traffic Sources")
    pdf.add_table(
        headers=["Referrer", "Count"],
        data=[
            ["(direct)", "586"],
            ["www.newsbreakapp.com", "55"],
            ["hudsonreporter.com", "50"],
            ["www.google.com", "49"],
            ["www.bing.com", "23"],
            ["en.wikipedia.org", "7"],
            ["duckduckgo.com", "7"],
            ["news.google.com", "6"],
            ["search.yahoo.com", "6"],
            ["www.facebook.com", "6"],
        ],
        col_widths=[4.5*inch, 2*inch]
    )

    # === PAGE BREAK ===
    pdf.add_page_break()

    # === GEOGRAPHIC ===
    pdf.add_section("Geographic Distribution")
    pdf.add_table(
        headers=["Country", "Events"],
        data=[
            ["United States", "1,562"],
            ["China", "328"],
            ["Sierra Leone", "136"],
            ["Singapore", "124"],
            ["Pakistan", "99"],
            ["Poland", "75"],
            ["Philippines", "68"],
            ["Ireland", "49"],
            ["United Kingdom", "28"],
            ["Slovakia", "23"],
        ],
        col_widths=[4.5*inch, 2*inch]
    )

    # === TECHNICAL BREAKDOWN ===
    pdf.add_section("Technical Breakdown")

    pdf.add_subsection("Device Type")
    pdf.add_table(
        headers=["Device", "Count", "% of Total"],
        data=[
            ["Desktop", "1,585", "58.3%"],
            ["Mobile", "1,121", "41.2%"],
            ["Tablet", "12", "0.4%"],
        ],
        col_widths=[2.5*inch, 2*inch, 2*inch]
    )

    pdf.add_subsection("Browser")
    pdf.add_table(
        headers=["Browser", "Count"],
        data=[
            ["Chrome", "2,040"],
            ["Mobile Safari", "346"],
            ["Microsoft Edge", "179"],
            ["Firefox", "99"],
            ["Safari", "29"],
        ],
        col_widths=[4.5*inch, 2*inch]
    )

    pdf.add_subsection("Operating System")
    pdf.add_table(
        headers=["OS", "Count"],
        data=[
            ["Windows", "1,142"],
            ["Android", "758"],
            ["iOS", "362"],
            ["Mac OS X", "275"],
            ["Linux", "158"],
        ],
        col_widths=[4.5*inch, 2*inch]
    )

    # === SESSION METRICS ===
    pdf.add_section("Session Metrics")
    pdf.add_kpi_row([
        ("0%", "Bounce Rate"),
        ("670", "Total Sessions"),
    ])

    # === MISSING STATS ===
    pdf.add_section("Statistics Still Missing")
    pdf.add_alert_box(
        "These metrics require additional tracking or configuration:",
        [
            "New vs Returning Users - Requires person identification",
            "Engagement Score - Requires all NavBoost components",
            "Page Load Time (TTFB) - Not in current Web Vitals",
            "Exit Pages - Requires pageleave analysis",
            "User Flow / Funnel - Requires PostHog funnel config",
        ],
        alert_type='warning'
    )

    # Footer note
    pdf.add_spacer(20)
    pdf.add_text("Report generated by PostHog Analytics Automation v2.0 | DataViz (Paradise Media BI Team)", style='FooterText')

    # Build
    output = pdf.build()
    print(f"PDF generated: {output}")
    return output


if __name__ == "__main__":
    generate_hudsonreporter_pdf()
