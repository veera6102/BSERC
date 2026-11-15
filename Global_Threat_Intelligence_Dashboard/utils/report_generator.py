import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

def generate_pdf_report(df, selected_country=None, selected_region=None, output_filename="intelligence_report.pdf"):
    """
    Generates a structured executive PDF summary report filtered by Country or Region
    using ReportLab flowables.
    """
    # 1. Ensure the directory structure exists
    output_dir = os.path.dirname(output_filename)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # 2. Apply Dataset Filtering Logic
    filtered_df = df.copy()
    scope_title = "Global Overview"
    
    if selected_country and selected_country != "All":
        filtered_df = filtered_df[filtered_df['country_txt'] == selected_country]
        scope_title = f"Country Briefing: {selected_country}"
    elif selected_region and selected_region != "All":
        filtered_df = filtered_df[filtered_df['region_txt'] == selected_region]
        scope_title = f"Regional Analysis: {selected_region}"

    # 3. Compute Key Performance Metrics
    total_incidents = len(filtered_df)
    
    if 'nkill' in filtered_df.columns:
        total_fatalities = int(filtered_df['nkill'].fillna(0).sum())
    else:
        total_fatalities = 0
        
    if 'nwound' in filtered_df.columns:
        total_injuries = int(filtered_df['nwound'].fillna(0).sum())
    else:
        total_injuries = 0
        
    total_casualties = total_fatalities + total_injuries

    # Extract Top Attack Metrics safely
    top_attacks = filtered_df['attacktype1_txt'].value_counts().head(3).to_dict() if total_incidents > 0 else {}
    top_weapons = filtered_df['weaptype1_txt'].value_counts().head(3).to_dict() if total_incidents > 0 else {}

    # 4. Initialize Document Template
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    story = []

    # 5. Define Custom Professional Stylesheets
    styles = getSampleStyleSheet()
    
    # Custom Color Palette
    primary_color = colors.HexColor("#1e3a8a")  # Deep Navy Blue
    secondary_color = colors.HexColor("#475569") # Slate Gray
    text_dark = colors.HexColor("#0f172a")       # Off-Black
    accent_bg = colors.HexColor("#f8fafc")       # Subtle Light Grey

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=24,
        leading=28,
        textColor=primary_color,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        leading=16,
        textColor=secondary_color,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        textColor=primary_color,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['BodyText'],
        fontSize=10,
        leading=14,
        textColor=text_dark,
        spaceAfter=8
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        textColor=colors.white,
        fontName='Helvetica-Bold'
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        textColor=text_dark
    )

    # 6. Build PDF Layout Sections
    # Document Headers
    story.append(Paragraph("🛡️ STRATEGIC INTELLIGENCE BRIEFING", title_style))
    story.append(Paragraph(f"Scope: {scope_title} • Generated Retrospective Analysis", subtitle_style))
    story.append(Spacer(1, 10))

    # Executive Summary Paragraph
    story.append(Paragraph("Executive Summary", h1_style))
    summary_text = (
        f"This automated executive data brief encapsulates historical data variances matching localized parameters "
        f"extracted from the Global Terrorism Database (GTD). Across the evaluated timeline criteria, a baseline volume "
        f"of <b>{total_incidents:,} registered incidents</b> was captured inside the system filters, resulting in "
        f"<b>{total_fatalities:,} confirmed fatalities</b> and <b>{total_injuries:,} reported injuries</b>."
    )
    story.append(Paragraph(summary_text, body_style))
    story.append(Spacer(1, 10))

    # KPI Summary Metric Blocks (Table Layout)
    story.append(Paragraph("Operational KPI Indicators", h1_style))
    kpi_data = [
        [Paragraph("Evaluated Core Metric", table_header_style), Paragraph("Aggregated Value Target", table_header_style)],
        [Paragraph("Total Filtered Incidents", table_cell_style), Paragraph(f"{total_incidents:,}", table_cell_style)],
        [Paragraph("Confirmed Fatalities (NILL)", table_cell_style), Paragraph(f"{total_fatalities:,}", table_cell_style)],
        [Paragraph("Reported Injuries (NWOUND)", table_cell_style), Paragraph(f"{total_injuries:,}", table_cell_style)],
        [Paragraph("Combined Severity Index (Casualties)", table_cell_style), Paragraph(f"{total_casualties:,}", table_cell_style)]
    ]
    
    kpi_table = Table(kpi_data, colWidths=[280, 250])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, accent_bg]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 15))

    # Tactical Vector Breakdowns (Keep together to avoid awkward layout line splits)
    vectors_story = []
    vectors_story.append(Paragraph("Tactical Distribution Matrix (Top Profile Segments)", h1_style))
    
    # Format Top Incident Methods Data Matrix
    method_rows = [[Paragraph("Method / Weapon Profile Class", table_header_style), Paragraph("Historical Incident Count", table_header_style)]]
    for key, val in top_attacks.items():
        method_rows.append([Paragraph(f"Attack: {key}", table_cell_style), Paragraph(f"{val:,}", table_cell_style)])
    for key, val in top_weapons.items():
        method_rows.append([Paragraph(f"Weapon: {key}", table_cell_style), Paragraph(f"{val:,}", table_cell_style)])

    if len(method_rows) > 1:
        vector_table = Table(method_rows, colWidths=[280, 250])
        vector_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), secondary_color),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, accent_bg]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        vectors_story.append(vector_table)
    else:
        vectors_story.append(Paragraph("No specific vector breakdowns available for the chosen criteria subset.", body_style))
        
    story.append(KeepTogether(vectors_story))
    story.append(Spacer(1, 20))

    # Footer/Methodology Safeguard Box
    disclaimer_story = []
    disclaimer_story.append(Paragraph("<b>Methodological Disclaimers & Operational Controls</b>", ParagraphStyle('DisHead', parent=body_style, fontName='Helvetica-Bold', textColor=secondary_color)))
    disclaimer_text = (
        "This platform output document consists of algorithmic retro-analysis summaries structured "
        "from historical records cataloged across the Global Terrorism Database (GTD). All data structures "
        "and metrics reflect strictly retrospective observations up to historical data coverage parameters (1970-2020) "
        "and do not encompass dynamic physical intelligence feeds, tactical adjustments, or forward-looking projections."
    )
    disclaimer_story.append(Paragraph(disclaimer_text, ParagraphStyle('DisText', parent=body_style, fontSize=8, leading=11, textColor=secondary_color)))
    
    disclaimer_box = Table([[disclaimer_story]], colWidths=[530])
    disclaimer_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ('PADDING', (0, 0), (-1, -1), 10),
    ]))
    
    story.append(KeepTogether(disclaimer_box))

    # 7. Compile Document Structure to File Filepath Destination
    doc.build(story)
    return output_filename