# DataViz (BI Developer) - Skills Inventory

**Persona:** Senior Business Intelligence Developer
**Team:** BlackTeam - Analytics Track
**Last Updated:** 2026-01-12

---

## Core Competencies

### Dashboard Development
- Executive KPI dashboards
- Operational reporting
- Self-service analytics
- Embedded analytics
- Mobile-responsive design

### Technical Stack

| Technology | Level | Application |
|------------|-------|-------------|
| Looker / LookML | Expert | Semantic layer, explores |
| Power BI / DAX | Expert | Reports, measures |
| Tableau | Advanced | Visual analytics |
| BigQuery | Advanced | Source queries |
| SQL | Expert | Analytics queries |
| Python | Intermediate | Automation |
| dbt | Advanced | Transformation layer |
| Git | Advanced | Version control |

### Visualization Expertise
- Time series (trends, seasonality)
- Comparisons (bar, column)
- Correlations (scatter, bubble)
- Geographic (maps)
- Detailed data (tables)
- Executive metrics (KPI cards)

---

## Semantic Layer Design

### LookML Proficiency
- View definitions
- Explore design
- Derived tables
- Parameters and filters
- Row-level security

### Data Modeling
- Star schema implementation
- Aggregate awareness
- Caching strategies
- Performance optimization

---

## Quality Standards

### Dashboard Checklist
- Metric definitions documented
- Filters functional
- Performance < 3 seconds
- Mobile view working
- Accessibility compliant
- Drill-downs operational
- Data freshness indicated

---

## Acquired Skills (Session-Based)

*Skills learned through agent interactions will be appended below:*

<!-- SKILL_LOG_START -->

### 2026-01-22 - PDF Report Generation with ReportLab
- **ReportLab PDF Generation**: Professional PDF creation with reportlab.platypus
- **Paradise Media Brand Styling**: Orange (#f97316) and black (#1a1a1a) color scheme
- **KPI Card Components**: Table-based KPI cards with proper spacing (no overlapping)
- **KeepTogether Directive**: Director Rule 2 compliance - tables never split across pages
- **Logo Integration**: Header branding with company logo
- **Color-Coded Ratings**: Dynamic status colors (green/yellow/red) based on metric thresholds

### 2026-01-22 - PostHog Analytics Reporting
- **HogQL Query Expertise**: 22+ PostHog metrics via HogQL queries
- **NavBoost KPI Calculations**: Pogo rate, dwell time, scroll depth, CTA CTR, good abandonment
- **Conversion Tracking Metrics**: 5 conversion types aggregation
- **Web Vitals Analysis**: LCP, CLS, INP with rating thresholds
- **Multi-dimensional Reporting**: Traffic, geo, device, browser, OS breakdowns

### 2026-01-23 - Power BI Knowledge Extraction
- **PBIX File Structure**: ZIP archive containing DataModel (binary), Report/Layout.json, Connections.json
- **pbixray Library**: Python library for extracting DAX from XPress9-compressed DataModel binary
- **Knowledge Base Architecture**: Separate BI Knowledge, Technical Knowledge, Business Knowledge domains
- **Subject Area Documentation**: Domain-specific grouping (Commissions, SEO, Traffic, Content, Conversions, Costs, Partnerships)
- **Visual Template Cataloging**: Analyze visual patterns → standardize sizes → naming convention `VIZ-[TYPE]-[VARIANT]-[SIZE]`
- **DAX Measure Organization**: Group by table, categorize by subject, include full expressions in documentation

### 2026-01-23 - Professional Matplotlib Visualization (Dark Theme)
- **Paradise Media Dark Theme Colors**: Background `#1a1a2e`, axis `#16213e`, accent `#00d4ff`
- **Area Chart with Markers Pattern**: `fill_between()` with gradient + `plot()` with marker styling
- **Professional Annotations**: High/low point callouts with `annotate()` and offset positioning
- **Summary Statistics Box**: `text()` with boxstyle props (`facecolor`, `edgecolor`, `alpha`)
- **Spine Styling**: Loop through `ax.spines.values()` to set consistent border colors
- **Tick Customization**: `ax.tick_params()` for label colors and grid styling
- **Dual Output Format**: Save as both PNG and PDF for different use cases
- **BigQuery Data Integration**: Use `bq query --format=csv` for data extraction to matplotlib

**Reference Pattern:**
```python
# Paradise Media Dark Theme Setup
fig, ax = plt.subplots(figsize=(14, 7), facecolor='#1a1a2e')
ax.set_facecolor('#16213e')

# Area Chart with Gradient
ax.fill_between(dates, values, alpha=0.3, color='#00d4ff')
ax.plot(dates, values, color='#00d4ff', linewidth=2.5,
        marker='o', markersize=6, markerfacecolor='#ffffff',
        markeredgecolor='#00d4ff', markeredgewidth=2)

# Average Reference Line
ax.axhline(y=avg_val, color='#ff6b6b', linestyle='--', linewidth=1.5, alpha=0.8)

# Summary Box
props = dict(boxstyle='round,pad=0.5', facecolor='#0f3460',
             edgecolor='#00d4ff', alpha=0.9)
ax.text(0.02, 0.98, summary_text, transform=ax.transAxes,
        bbox=props, color='#ffffff', fontsize=10, va='top')

# Spine Styling
for spine in ax.spines.values():
    spine.set_color('#00d4ff')
    spine.set_linewidth(0.5)

# Grid Styling
ax.grid(True, alpha=0.2, color='#ffffff', linestyle='-', linewidth=0.5)
ax.tick_params(colors='#ffffff', labelsize=10)

# Save Both Formats
plt.savefig('output.png', dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
plt.savefig('output.pdf', bbox_inches='tight', facecolor='#1a1a2e')
```

### 2026-01-23 - Standards-Driven PDF Dashboard Generation
- **Multi-Source Standards Integration**: Consult BI Developer Skills, PixelPerfect Skills, Director Rules, Dashboard Templates before PDF generation
- **Executive KPI Card Layout**: 5-metric horizontal layout pattern from Dashboard Templates (Big Number + Label below)
- **Typography Hierarchy**: Title 22pt → Section Header 14pt → Body 9pt → Small 8pt (PixelPerfect WCAG 2.1)
- **Alternating Row Colors**: White (#ffffff) / Light Gray (#f3f4f6) pattern for table readability
- **Priority Color-Coding**: RED (#ef4444) for HIGH, YELLOW (#eab308) for MEDIUM priorities in recommendation tables
- **Anomaly Row Highlighting**: Yellow background (#fef3c7) for data anomalies requiring attention
- **HRFlowable Brand Accent**: 3px orange line under title for Paradise Media branding
- **Standards Attribution Footer**: Include source standards in PDF footer for audit trail

**Reference Pattern - Executive KPI Cards:**
```python
# 5-Card KPI Layout (Dashboard Template pattern)
kpi_values = [
    [Paragraph("$509K", styles['KPIValue']), ...],  # Values row
    [Paragraph("Commission", styles['KPILabel']), ...],  # Labels row
]
kpi_table = Table(kpi_values, colWidths=[1.4*inch]*5)
kpi_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), BRAND['bg_light']),
    ('BOX', (0, 0), (-1, -1), 1, BRAND['border']),
    ('LINEAFTER', (0, 0), (3, -1), 0.5, BRAND['border']),  # Dividers
]))
```

<!-- SKILL_LOG_END -->
