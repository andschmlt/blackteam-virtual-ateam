#!/usr/bin/env python3
"""
SEO & Content Analysis PDF Generator
Fixed table formatting - No text overlay issues
Version: 2.1.0
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
    'primary': colors.HexColor('#f97316'),
    'primary_dark': colors.HexColor('#ea580c'),
    'secondary': colors.HexColor('#1a1a1a'),
    'accent': colors.HexColor('#22c55e'),
    'warning': colors.HexColor('#eab308'),
    'danger': colors.HexColor('#ef4444'),
    'light_gray': colors.HexColor('#f5f5f5'),
    'medium_gray': colors.HexColor('#e5e5e5'),
    'dark_gray': colors.HexColor('#525252'),
    'white': colors.white,
    'black': colors.black,
}

LOGO_PATH = "/mnt/c/Users/andre/Downloads/paradisemedia.jpg"


class SEOReportPDF:
    def __init__(self, output_path, domain):
        self.output_path = output_path
        self.domain = domain
        self.elements = []
        self.styles = getSampleStyleSheet()
        self._setup_styles()

    def _setup_styles(self):
        """Setup custom styles"""
        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            fontSize=20,
            textColor=COLORS['secondary'],
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
        ))

        self.styles.add(ParagraphStyle(
            name='ReportSubtitle',
            fontSize=10,
            textColor=COLORS['dark_gray'],
            spaceAfter=4,
            alignment=TA_CENTER,
        ))

        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            fontSize=13,
            textColor=COLORS['primary'],
            spaceBefore=16,
            spaceAfter=8,
            fontName='Helvetica-Bold',
        ))

        self.styles.add(ParagraphStyle(
            name='SubsectionHeader',
            fontSize=10,
            textColor=COLORS['secondary'],
            spaceBefore=10,
            spaceAfter=4,
            fontName='Helvetica-Bold',
        ))

        # Override existing BodyText style
        self.styles['BodyText'].fontSize = 9
        self.styles['BodyText'].textColor = COLORS['secondary']
        self.styles['BodyText'].spaceAfter = 4
        self.styles['BodyText'].leading = 12

        self.styles.add(ParagraphStyle(
            name='SmallText',
            fontSize=8,
            textColor=COLORS['dark_gray'],
            spaceAfter=3,
            leading=10,
        ))

        # Table cell styles
        self.styles.add(ParagraphStyle(
            name='TableCell',
            fontSize=7,
            leading=9,
            textColor=COLORS['secondary'],
            wordWrap='CJK',
        ))

        self.styles.add(ParagraphStyle(
            name='TableCellRight',
            fontSize=7,
            leading=9,
            textColor=COLORS['secondary'],
            alignment=TA_RIGHT,
        ))

        self.styles.add(ParagraphStyle(
            name='TableHeader',
            fontSize=8,
            fontName='Helvetica-Bold',
            textColor=COLORS['white'],
        ))

        self.styles.add(ParagraphStyle(
            name='FooterText',
            fontSize=8,
            textColor=COLORS['dark_gray'],
            alignment=TA_CENTER,
        ))

    def add_header(self, period):
        """Add header with logo"""
        if os.path.exists(LOGO_PATH):
            logo = Image(LOGO_PATH, width=1.4*inch, height=0.45*inch)
            logo.hAlign = 'CENTER'
            self.elements.append(logo)
            self.elements.append(Spacer(1, 10))

        self.elements.append(Paragraph("SEO & Content Deep Dive Analysis", self.styles['ReportTitle']))
        self.elements.append(Paragraph(f"<b>{self.domain}</b>", self.styles['ReportSubtitle']))
        self.elements.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | {period}", self.styles['ReportSubtitle']))
        self.elements.append(Spacer(1, 6))
        self.elements.append(HRFlowable(width="100%", thickness=2, color=COLORS['primary']))
        self.elements.append(Spacer(1, 12))

    def add_section(self, title):
        """Add section header"""
        self.elements.append(Spacer(1, 6))
        self.elements.append(Paragraph(title, self.styles['SectionHeader']))
        self.elements.append(HRFlowable(width="100%", thickness=1, color=COLORS['medium_gray']))
        self.elements.append(Spacer(1, 6))

    def add_subsection(self, title):
        """Add subsection header"""
        self.elements.append(Spacer(1, 4))
        self.elements.append(Paragraph(title, self.styles['SubsectionHeader']))

    def add_text(self, text, style='BodyText'):
        """Add paragraph text"""
        self.elements.append(Paragraph(text, self.styles[style]))

    def add_spacer(self, height=10):
        """Add vertical space"""
        self.elements.append(Spacer(1, height))

    def add_kpi_row(self, kpis):
        """Add KPI cards"""
        cards = []
        card_width = 1.4 * inch

        kpi_value_style = ParagraphStyle(
            'KPIValue',
            fontSize=18,
            textColor=COLORS['primary'],
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
        )

        kpi_label_style = ParagraphStyle(
            'KPILabel',
            fontSize=8,
            textColor=COLORS['dark_gray'],
            alignment=TA_CENTER,
        )

        for value, label in kpis:
            card_content = [
                [Paragraph(str(value), kpi_value_style)],
                [Paragraph(label, kpi_label_style)]
            ]
            card = Table(card_content, colWidths=[card_width])
            card.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), COLORS['light_gray']),
                ('BOX', (0, 0), (-1, -1), 2, COLORS['primary']),
                ('TOPPADDING', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
                ('TOPPADDING', (0, 1), (-1, 1), 4),
                ('BOTTOMPADDING', (0, 1), (-1, 1), 8),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            cards.append(card)

        row_table = Table([cards], colWidths=[card_width + 8] * len(kpis))
        row_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]))

        self.elements.append(row_table)
        self.elements.append(Spacer(1, 12))

    def add_seo_table(self, headers, data):
        """
        Add SEO analysis table with FIXED column widths
        Prevents text overlay by using Paragraph objects with word wrap
        """
        # Column widths optimized for SEO data (Page/ETV/Keywords/P1/P2-3/P4-10)
        # Total width: ~6.5 inches
        num_cols = len(headers)

        if num_cols == 6:
            col_widths = [2.3*inch, 0.65*inch, 0.7*inch, 0.55*inch, 0.55*inch, 0.55*inch]
        elif num_cols == 5:
            col_widths = [2.6*inch, 0.8*inch, 0.8*inch, 0.6*inch, 0.6*inch]
        elif num_cols == 4:
            col_widths = [3.0*inch, 1.0*inch, 1.0*inch, 1.0*inch]
        elif num_cols == 3:
            col_widths = [3.5*inch, 1.5*inch, 1.0*inch]
        else:
            col_widths = [6.5*inch / num_cols] * num_cols

        # Convert headers to Paragraphs
        header_row = [Paragraph(str(h), self.styles['TableHeader']) for h in headers]

        # Convert data cells to Paragraphs with wrapping
        processed_data = []
        for row in data:
            new_row = []
            for i, cell in enumerate(row):
                if i == 0:
                    # First column (Page/URL) - left aligned, wrap text
                    new_row.append(Paragraph(str(cell), self.styles['TableCell']))
                else:
                    # Other columns - right aligned
                    new_row.append(Paragraph(str(cell), self.styles['TableCellRight']))
            processed_data.append(new_row)

        table_data = [header_row] + processed_data
        table = Table(table_data, colWidths=col_widths, repeatRows=1)

        style_commands = [
            # Header - Orange background
            ('BACKGROUND', (0, 0), (-1, 0), COLORS['primary']),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
            ('TOPPADDING', (0, 0), (-1, 0), 4),

            # Body - minimal padding to reduce whitespace
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
        self.elements.append(Spacer(1, 10))

    def add_metric_table(self, headers, data):
        """Add simple metric table (2-3 columns)"""
        num_cols = len(headers)
        if num_cols == 2:
            col_widths = [4.0*inch, 2.0*inch]
        else:
            col_widths = [3.0*inch, 1.5*inch, 1.5*inch]

        header_row = [Paragraph(str(h), self.styles['TableHeader']) for h in headers]

        processed_data = []
        for row in data:
            new_row = []
            for i, cell in enumerate(row):
                if i == 0:
                    new_row.append(Paragraph(str(cell), self.styles['TableCell']))
                else:
                    new_row.append(Paragraph(str(cell), self.styles['TableCellRight']))
            processed_data.append(new_row)

        table_data = [header_row] + processed_data
        table = Table(table_data, colWidths=col_widths, repeatRows=1)

        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), COLORS['primary']),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
            ('TOPPADDING', (0, 0), (-1, 0), 4),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
            ('TOPPADDING', (0, 1), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [COLORS['white'], COLORS['light_gray']]),
            ('GRID', (0, 0), (-1, -1), 0.5, COLORS['medium_gray']),
            ('LINEBELOW', (0, 0), (-1, 0), 2, COLORS['primary_dark']),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))

        self.elements.append(KeepTogether([table]))
        self.elements.append(Spacer(1, 10))

    def add_alert_box(self, title, items, alert_type='warning'):
        """Add alert/info box"""
        border_color = COLORS['warning'] if alert_type == 'warning' else COLORS['danger']

        content = [[Paragraph(f"<b>{title}</b>", self.styles['BodyText'])]]
        for item in items:
            content.append([Paragraph(f"- {item}", self.styles['SmallText'])])

        table = Table(content, colWidths=[6.0*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), COLORS['light_gray']),
            ('BOX', (0, 0), (-1, -1), 2, border_color),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        self.elements.append(KeepTogether([table]))
        self.elements.append(Spacer(1, 10))

    def add_page_break(self):
        """Force page break"""
        self.elements.append(PageBreak())

    def _add_footer(self, canvas, doc):
        """Add page footer"""
        canvas.saveState()
        canvas.setFont('Helvetica', 7)
        canvas.setFillColor(COLORS['dark_gray'])

        canvas.drawString(0.75*inch, 0.5*inch, "SEO & Content Deep Dive Analysis")
        canvas.drawCentredString(4.25*inch, 0.5*inch, f"Page {doc.page}")
        canvas.drawRightString(7.75*inch, 0.5*inch, f"{self.domain} | {datetime.now().strftime('%Y-%m-%d')}")

        canvas.setStrokeColor(COLORS['primary'])
        canvas.setLineWidth(1)
        canvas.line(0.75*inch, 0.65*inch, 7.75*inch, 0.65*inch)

        canvas.restoreState()

    def build(self):
        """Build and save PDF"""
        doc = SimpleDocTemplate(
            self.output_path,
            pagesize=letter,
            rightMargin=0.6*inch,
            leftMargin=0.6*inch,
            topMargin=0.6*inch,
            bottomMargin=0.75*inch
        )
        doc.build(self.elements, onFirstPage=self._add_footer, onLaterPages=self._add_footer)
        return self.output_path


def generate_northeasttimes_report():
    """Generate northeasttimes.com SEO & Content Analysis PDF"""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_path = f"/home/andre/analysis/northeasttimes_SEO_Content_DeepDive_v3_{timestamp}.pdf"

    pdf = SEOReportPDF(output_path, "northeasttimes.com")

    # HEADER
    pdf.add_header("PostHog 14d | BigQuery YTD | DataForSEO Current")

    # EXECUTIVE SUMMARY
    pdf.add_section("EXECUTIVE SUMMARY")

    pdf.add_kpi_row([
        ("29,532", "Keywords"),
        ("163", "Position 1"),
        ("$140,964", "ETV/Month"),
        ("$184,527", "Commission YTD"),
    ])

    pdf.add_subsection("Domain Authority & SEO Health")
    pdf.add_metric_table(
        headers=["Metric", "Value"],
        data=[
            ["Total Organic Keywords", "29,532"],
            ["Keywords in Position 1", "163"],
            ["Keywords in Position 2-3", "232"],
            ["Keywords in Position 4-10", "1,280"],
            ["Estimated Traffic Value", "$140,964/month"],
            ["New Keywords (30 days)", "24,979"],
            ["Keywords Lost (30 days)", "10,408"],
        ]
    )

    pdf.add_subsection("Revenue Performance (YTD 2026)")
    pdf.add_metric_table(
        headers=["Metric", "Value"],
        data=[
            ["Total Affiliate Clicks", "108,265"],
            ["Total FTDs", "630"],
            ["Total Commission", "$184,527.00"],
            ["Avg Commission per FTD", "$292.90"],
            ["Top Revenue Page", "/fast-payout-online-casinos/ ($84,657)"],
        ]
    )

    # TOP 20 PAGES - SEO ANALYSIS
    pdf.add_page_break()
    pdf.add_section("TOP 20 PAGES - SEO Analysis (DataForSEO)")

    pdf.add_seo_table(
        headers=["Page", "ETV", "Keywords", "P1", "P2-3", "P4-10"],
        data=[
            ["/entertainment/king-of-prussia-mall/", "$35,241", "275", "0", "3", "57"],
            ["/zach-wheeler-injury/", "$22,325", "160", "0", "2", "5"],
            ["/fast-payout-online-casinos/", "$20,359", "5,716", "138", "110", "407"],
            ["/ (Homepage)", "$8,140", "178", "14", "13", "22"],
            ["/2025/12/22/eagles-aj-brown-bills-trade/", "$4,651", "348", "2", "0", "5"],
            ["/philly-cheesesteaks/", "$3,640", "200", "0", "0", "10"],
            ["/2025/12/19/philly-plane-crash/", "$3,367", "184", "2", "3", "18"],
            ["/2025/11/28/rare-aurora-borealis-pennsylvania/", "$2,441", "22", "3", "5", "2"],
            ["/presque-isle-state-park-pennsylvania/", "$2,137", "189", "0", "0", "36"],
            ["/philly-rooftop-bars/", "$2,126", "98", "0", "1", "7"],
            ["/2026/01/18/community-calendar-68/", "$1,736", "452", "0", "0", "1"],
            ["/2025/12/10/franklin-mall-for-sale/", "$1,295", "81", "0", "0", "3"],
            ["/seed-banks-international-shipping/", "$1,257", "128", "0", "2", "27"],
            ["/philadelphia-restaurants/", "$1,184", "94", "0", "0", "0"],
            ["/2026/01/16/pga-wanamaker-history/", "$1,115", "78", "0", "0", "1"],
            ["/entertainment/citizens-bank-park/", "$1,088", "332", "0", "0", "28"],
            ["/2024/12/25/franklin-mills-original-name/", "$973", "51", "0", "3", "4"],
            ["/california/best-sports-betting-sites/", "$969", "94", "0", "0", "1"],
            ["/california/gambling/", "$801", "106", "0", "5", "33"],
            ["/entertainment/thc-gummies/", "$742", "233", "0", "6", "45"],
        ]
    )

    # TOP 5 DEEP DIVE
    pdf.add_subsection("Top 5 Pages - Deep Dive Analysis")

    pdf.add_text("<b>1. /entertainment/king-of-prussia-mall/ - HIGHEST TRAFFIC VALUE ($35,241/mo)</b>")
    pdf.add_text("Keywords: 275 | P1: 0 | P2-3: 3 | P4-10: 57")
    pdf.add_text("Top Keywords: 'king of prussia mall' (Position 9, 165K searches), 'plaza at king of prussia' (Position 3)")
    pdf.add_text("<b>Recommendation:</b> Add FAQ schema, store directory, current hours/events to capture featured snippets.")
    pdf.add_spacer(6)

    pdf.add_text("<b>2. /zach-wheeler-injury/ - SPORTS NEWS ($22,325/mo)</b>")
    pdf.add_text("Position 2 for 'zack wheeler' (74,000 monthly searches)")
    pdf.add_text("<b>Recommendation:</b> Add sports article schema, create evergreen Phillies hub, update regularly.")
    pdf.add_spacer(6)

    pdf.add_text("<b>3. /fast-payout-online-casinos/ - REVENUE POWERHOUSE ($20,359 ETV, $84,657 YTD Revenue)</b>")
    pdf.add_text("Keywords: 5,716 | P1: 138 | Scroll Depth: 21.8% | CTA CTR: 4.6%")
    pdf.add_text("<b>Critical Issue:</b> Users only see 22% of content. Move CTAs above fold, add 'Quick Picks' summary.")
    pdf.add_spacer(6)

    pdf.add_text("<b>4. Homepage - BRAND AUTHORITY ($8,140/mo)</b>")
    pdf.add_text("P1: 14 (likely branded) | Dwell: 356s | Scroll: 37.4% | CTA CTR: 1.6%")
    pdf.add_text("<b>Recommendation:</b> Add Organization schema, improve internal linking to top pages.")
    pdf.add_spacer(6)

    pdf.add_text("<b>5. /2025/12/22/eagles-aj-brown-bills-trade/ - NEWS SUCCESS ($4,651/mo)</b>")
    pdf.add_text("Position 1 for 'a j brown trade' (12,100 searches) - Model for successful news content.")

    # BOTTOM 20 / ISSUES
    pdf.add_page_break()
    pdf.add_section("CRITICAL ISSUES - Pages Requiring Immediate Action")

    pdf.add_alert_box(
        "CRITICAL: /high-payout-casinos/ - 45.5% Pogo Rate",
        [
            "Sessions: 251 | CTA CTR: 0.1% (FAILING)",
            "Root Cause: Title overpromises, content doesn't match intent",
            "FIX: Rewrite intro, add payout percentages above fold, or redirect to /fast-payout-online-casinos/",
        ],
        alert_type='danger'
    )

    pdf.add_alert_box(
        "CATASTROPHIC: /au/best-payid-casinos/ - 100% Pogo Rate",
        [
            "Every Google visitor leaves immediately",
            "Root Cause: US users landing on AU content, no geo-targeting",
            "FIX: Implement hreflang tags, add geo-redirect, or noindex",
        ],
        alert_type='danger'
    )

    pdf.add_alert_box(
        "MONETIZATION GAP: News Articles",
        [
            "Multiple news articles drive traffic but 0.1-0.2% CTA CTR",
            "/2026/01/21/philly-resident-charged-bensalem-shooting-2/ - 915 sessions, 0.1% CTA",
            "FIX: Use display ads, newsletter signups, or related evergreen content links instead of affiliate CTAs",
        ],
        alert_type='warning'
    )

    # KEYWORD OPPORTUNITIES
    pdf.add_section("KEYWORD OPPORTUNITIES")

    pdf.add_metric_table(
        headers=["Keyword", "Position", "Volume"],
        data=[
            ["plane crash in philly", "10", "246,000"],
            ["king of prussia mall", "9", "165,000"],
            ["zack wheeler", "2", "74,000"],
            ["best cheesesteak northeast philly", "5", "40,500"],
            ["franklin mills mall", "9", "33,100"],
            ["playing slots online real money", "8", "27,100"],
        ]
    )

    # REVENUE BY PAGE
    pdf.add_section("REVENUE PERFORMANCE BY PAGE (YTD 2026)")

    pdf.add_seo_table(
        headers=["Page", "Clicks", "FTDs", "Commission", "Niche"],
        data=[
            ["/fast-payout-online-casinos/", "35,703", "463", "$84,657", "Casino"],
            ["/online-gambling-facts/", "21,654", "50", "$54,960", "Casino"],
            ["/entertainment/thc-gummies/", "13,056", "0", "$3,502", "Psych"],
            ["/offshore-sportsbooks/", "2,664", "2", "$7,479", "Betting"],
            ["/2024/08/12/adult-dating-sites/", "4,207", "4", "$3,101", "Dating"],
            ["/california/betting/", "587", "20", "$4,102", "Betting"],
            ["/tx/online-casinos/", "619", "11", "$3,579", "Casino"],
            ["/tx/betting/", "433", "10", "$2,905", "Betting"],
            ["/au/fast-payout-casinos/", "984", "5", "$2,894", "Casino"],
            ["DOMAIN TOTAL", "108,265", "630", "$184,527", "-"],
        ]
    )

    # STRATEGIC RECOMMENDATIONS
    pdf.add_page_break()
    pdf.add_section("STRATEGIC RECOMMENDATIONS")

    pdf.add_subsection("SEO Priority Actions (Ranked by Impact)")

    pdf.add_text("<b>1. Fix /high-payout-casinos/ pogo rate - IMMEDIATE</b>")
    pdf.add_text("Owner: B-RANK | Audit intent, rewrite above-fold, consider redirect to /fast-payout-online-casinos/")
    pdf.add_spacer(4)

    pdf.add_text("<b>2. Implement hreflang for AU/international content - TECHNICAL SEO</b>")
    pdf.add_text("Owner: B-TECH | Add hreflang tags, geo-redirect, audit all international pages")
    pdf.add_spacer(4)

    pdf.add_text("<b>3. Optimize /fast-payout-online-casinos/ for featured snippets - PROTECT REVENUE</b>")
    pdf.add_text("Owner: B-RANK | Add FAQ schema, summary tables, voice search optimization")
    pdf.add_spacer(4)

    pdf.add_text("<b>4. Build internal linking structure - SITE-WIDE</b>")
    pdf.add_text("Owner: B-CONT | Create topic clusters, related content modules, breadcrumbs")
    pdf.add_spacer(4)

    pdf.add_text("<b>5. Create more Philadelphia local content - TRAFFIC GROWTH</b>")
    pdf.add_text("Owner: B-NINA | Target local keywords, neighborhood guides, event coverage")

    pdf.add_subsection("Content Priority Actions")

    pdf.add_text("<b>1. Move CTAs above the fold on affiliate pages</b>")
    pdf.add_text("Current scroll depth: 13-22% on affiliate content. Users missing 78-87% of page content.")
    pdf.add_spacer(4)

    pdf.add_text("<b>2. Create 'Quick Answer' summaries at top of long-form content</b>")
    pdf.add_text("Capture featured snippets, improve UX, reduce pogo rate.")
    pdf.add_spacer(4)

    pdf.add_text("<b>3. Develop monetization strategy for news content</b>")
    pdf.add_text("News drives traffic but not revenue. Consider programmatic ads, newsletter signups, sponsorships.")
    pdf.add_spacer(4)

    pdf.add_text("<b>4. Use /seed-banks-international-shipping/ as content template</b>")
    pdf.add_text("Best CTA CTR on site (8.0%), specific intent, strong engagement.")

    # FOOTER
    pdf.add_spacer(20)
    pdf.add_text("Report generated by Virtual ATeam | B-RANK, B-NINA, B-ALEX, B-DANA | Validated by W-LARS, W-VERA, W-INGA", style='FooterText')

    output = pdf.build()
    print(f"PDF generated: {output}")
    print(f"Size: {os.path.getsize(output):,} bytes")
    return output


if __name__ == "__main__":
    generate_northeasttimes_report()
