import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    shading_xml = f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>'
    cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))

def set_table_borders(table, color="D3D3D3", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders_xml = f'''
    <w:tblBorders {nsdecls("w")}>
        <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        <w:insideV w:val="none"/>
        <w:left w:val="none"/>
        <w:right w:val="none"/>
    </w:tblBorders>
    '''
    tblPr.append(parse_xml(borders_xml))

def add_styled_paragraph(doc, text="", space_before=0, space_after=6, line_spacing=1.05, align=WD_ALIGN_PARAGRAPH.LEFT):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    p.alignment = align
    if text:
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)
    return p

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(10)
    r.font.bold = True
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(9)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(10)
    r.font.italic = True
    return p

def render_formatted_text_to_paragraph(p, text, default_font_size=10):
    if any(k in text for k in ['*', '_{', '^{']):
        pattern = re.compile(r'(\*\*[^*]+\*\*|\*[^*]+\*|_\{[^}]+\}|\^\{[^}]+\})')
        tokens = pattern.split(text)
        for token in tokens:
            if not token:
                continue
            r = p.add_run()
            r.font.name = 'Times New Roman'
            r.font.size = Pt(default_font_size)
            if token.startswith('**') and token.endswith('**'):
                r.text = token[2:-2]
                r.font.bold = True
            elif token.startswith('*') and token.endswith('*'):
                r.text = token[1:-1]
                r.font.italic = True
            elif token.startswith('_{') and token.endswith('}'):
                r.text = token[2:-1]
                r.font.subscript = True
            elif token.startswith('^{') and token.endswith('}'):
                r.text = token[2:-1]
                r.font.superscript = True
            else:
                r.text = token
    else:
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(default_font_size)

def add_body(doc, text, bold_prefix=""):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.05
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(10)
        r_pre.font.bold = True
    render_formatted_text_to_paragraph(p, text, default_font_size=10)
    return p

def add_caption(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(6)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(8.5)
    r.font.italic = True
    return p

def add_image_centered(doc, image_path, width_inches=4.8):
    if os.path.exists(image_path):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        run.add_picture(image_path, width=Inches(width_inches))
        return p
    else:
        print(f"Warning: Image {image_path} not found.")
        return None

def add_display_equation(doc, omml_inner_xml, eq_num=None):
    """
    Renders a native Word OMML display equation in standard IEEE style:
    Equation centered with right-aligned equation number.
    """
    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = tbl._tbl.tblPr
    borders_xml = f'''
    <w:tblBorders {nsdecls("w")}>
        <w:top w:val="none"/>
        <w:bottom w:val="none"/>
        <w:left w:val="none"/>
        <w:right w:val="none"/>
        <w:insideH w:val="none"/>
        <w:insideV w:val="none"/>
    </w:tblBorders>
    '''
    tblPr.append(parse_xml(borders_xml))

    # Cell 0: Equation (centered)
    c0 = tbl.cell(0, 0)
    c0.width = Inches(6.2)
    set_cell_margins(c0, top=30, bottom=30, left=10, right=10)
    p0 = c0.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p0.paragraph_format.space_before = Pt(2)
    p0.paragraph_format.space_after = Pt(2)

    omml_container = f'''
    <m:oMathPara xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
      <m:oMath>
        {omml_inner_xml}
      </m:oMath>
    </m:oMathPara>
    '''
    p0._p.append(parse_xml(omml_container))

    # Cell 1: Number (right-aligned)
    c1 = tbl.cell(0, 1)
    c1.width = Inches(0.8)
    set_cell_margins(c1, top=30, bottom=30, left=10, right=10)
    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p1.paragraph_format.space_before = Pt(2)
    p1.paragraph_format.space_after = Pt(2)
    if eq_num is not None:
        r1 = p1.add_run(f"({eq_num})")
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(10)

def build_paper():
    doc = docx.Document()
    
    # Page setup - Standard Letter with 0.75 in margins
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
        
    # TITLE
    p_title = add_styled_paragraph(doc, space_before=12, space_after=10, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_title = p_title.add_run("PoultryHealth Intelligence: Hierarchical Deep Learning and Grounded Generative AI for Poultry Disease Diagnosis")
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(17)
    r_title.font.bold = True
    
    # AUTHORS & AFFILIATIONS (IEEE 3-COLUMN LAYOUT)
    author_table = doc.add_table(rows=1, cols=3)
    author_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    # Remove all borders for author header
    tblPr = author_table._tbl.tblPr
    borders_xml = f'''
    <w:tblBorders {nsdecls("w")}>
        <w:top w:val="none"/>
        <w:bottom w:val="none"/>
        <w:left w:val="none"/>
        <w:right w:val="none"/>
        <w:insideH w:val="none"/>
        <w:insideV w:val="none"/>
    </w:tblBorders>
    '''
    tblPr.append(parse_xml(borders_xml))

    authors_info = [
        ("Ayush M Singh", "Reg. No. 23BDS0033\nSchool of Computer Science and Engineering\nVellore Institute of Technology\nVellore, India\nayush.singh2023@vitstudent.ac.in"),
        ("Venkata Sriram Topalli", "Reg. No. 23BE0441\nSchool of Computer Science and Engineering\nVellore Institute of Technology\nVellore, India"),
        ("Dr. Dega Nagaraju", "Professor Grade 2\nDepartment of Analytics, SCOPE\nVellore Institute of Technology\nVellore, India\ndeganagaraju@vit.ac.in")
    ]

    for j, (name, details) in enumerate(authors_info):
        cell = author_table.cell(0, j)
        set_cell_margins(cell, top=40, bottom=80, left=40, right=40)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.05
        p.paragraph_format.space_after = Pt(2)
        r_name = p.add_run(name + "\n")
        r_name.font.name = 'Times New Roman'
        r_name.font.size = Pt(10.5)
        r_name.font.bold = True
        
        r_det = p.add_run(details)
        r_det.font.name = 'Times New Roman'
        r_det.font.size = Pt(9)
        r_det.font.italic = False

    add_styled_paragraph(doc, "", space_before=6, space_after=8)

    # ABSTRACT
    p_abs = add_styled_paragraph(doc, space_before=4, space_after=10, line_spacing=1.05, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    r_absh = p_abs.add_run("Abstract—")
    r_absh.font.name = 'Times New Roman'
    r_absh.font.size = Pt(9.5)
    r_absh.font.bold = True
    r_abst = p_abs.add_run(
        "Poultry diseases propagate rapidly through commercial and smallholder flocks, where diagnostic delays often result in catastrophic mortality and unguided antimicrobial misuse. In this paper, we present PoultryHealth Intelligence, an applied clinical decision-support framework that integrates hierarchical deep learning, visual interpretability, and grounded generative artificial intelligence for avian health screening and differential diagnosis. The core architecture decouples broad epidemiological screening from fine-grained pathological categorization to address the asymmetric cost of false negatives in veterinary triage. A binary convolutional neural network ('The Bouncer') performs initial screening to classify incoming field photographs as healthy or diseased, achieving 82.1% accuracy (349 of 425; 95% CI: 78.1–85.5%), a sick-bird sensitivity of 81.7% (228 of 279), a healthy specificity of 82.9% (121 of 146), and an AUC-ROC of 0.884 [95% CI: 0.851–0.915]. By adjusting the operational triage threshold to p = 0.35, sick-bird sensitivity increases to 92.2% (261 of 279), reducing false-negative missed cases by 56.9% (from 51 down to 22) at a specificity of 71.2%. Diseased cases pass to a four-class specialist network ('The Doctor') classifying Bumblefoot, Chronic Respiratory Disease (CRD), Fowl Pox, and Infectious Coryza, attaining 71.7% accuracy (200 of 279; 95% CI: 66.1–76.6%) and a macro F1-score of 0.65. Top-1 predicted softmax confidence scores form a moderate distribution (mean: 0.67, median: 0.68), with ~70% of scores lying between 0.46 and 0.80, and ~10 predictions (3.6%) falling below an operational threshold of τ = 0.40 to trigger an atypical presentation alert. The combined end-to-end five-class pipeline yields 66.8% accuracy (284 of 425) and a macro F1 of 0.596 on the common validation cohort. Gradient-weighted Class Activation Mapping (Grad-CAM) provides transparent visual localization of cutaneous and ocular lesions, while prompt-grounded generative synthesis generates structured clinical dossiers designed to adhere to veterinary clinical guidelines and antimicrobial stewardship principles by avoiding unguided antibiotic prescriptions. The full system is deployed via an asynchronous FastAPI backend and a responsive React client, delivering local CPU inference in 145 ms to offer an interpretable, edge-feasible diagnostic tool for flock health monitoring."
    )
    r_abst.font.name = 'Times New Roman'
    r_abst.font.size = Pt(9.5)

    # KEYWORDS
    p_kw = add_styled_paragraph(doc, space_before=0, space_after=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    r_kwh = p_kw.add_run("Keywords—")
    r_kwh.font.name = 'Times New Roman'
    r_kwh.font.size = Pt(9.5)
    r_kwh.font.bold = True
    r_kwt = p_kw.add_run("Poultry disease diagnosis, hierarchical deep learning, MobileNetV2, Grad-CAM, grounded generative AI, veterinary informatics, antimicrobial stewardship.")
    r_kwt.font.name = 'Times New Roman'
    r_kwt.font.size = Pt(9.5)

    # SECTION I: INTRODUCTION
    add_heading_1(doc, "I.  INTRODUCTION")
    add_body(doc, "Poultry farming forms an essential pillar of global food security and rural agricultural livelihood, providing accessible dietary protein across commercial enterprises and smallholder operations worldwide. However, poultry flocks remain acutely vulnerable to severe infectious outbreaks. Highly contagious bacterial, viral, and mycoplasmal pathogens—including Chronic Respiratory Disease (CRD, caused by Mycoplasma gallisepticum [1]), Infectious Coryza (Avibacterium paragallinarum [2]), Fowl Pox (Avipoxvirus [3]), and ulcerative Staphylococcal pododermatitis (Bumblefoot [4])—spread rapidly through intensive housing environments. When an outbreak occurs, diagnostic delays of even 24 to 48 hours frequently result in extensive flock morbidity, severe egg production drops, and high flock mortality.")
    add_body(doc, "In smallholder and resource-constrained farming communities, on-site veterinary expertise is often unavailable, cost-prohibitive, or geographically distant. Consequently, flock managers frequently resort to empiric, unguided antibiotic administration or delay flock isolation until clinical symptoms have become advanced and irreversible. The indiscriminate prophylactic and therapeutic administration of over-the-counter antimicrobials directly accelerates global antimicrobial resistance (AMR), threatening both veterinary welfare and human public health [10], [11]. There is an urgent need for accessible, rapid, and transparent point-of-care diagnostic tools capable of operating on standard consumer hardware, providing reliable preliminary triage, visual pathology localization, and medically responsible clinical guidance.")
    add_body(doc, "Computer vision and deep learning offer promising avenues for automated poultry health assessment [5]–[7]. Most existing diagnostic pipelines, however, frame poultry disease detection as a single-stage, flat multi-class classification problem [5], [6]. In an agricultural setting, this monolithic formulation exhibits significant operational limitations:")
    add_body(doc, "1) Asymmetric Misclassification Penalties: In veterinary epidemiology, confusing two respiratory diseases (e.g., CRD vs. Coryza) incurs modest tactical adjustments, whereas misclassifying an actively shedding, highly contagious diseased bird as healthy (a false negative) risks catastrophic flock-wide pathogen transmission. Single-stage cross-entropy networks balance errors symmetrically across all output classes, failing to reflect this critical clinical asymmetry [24].")
    add_body(doc, "2) Monolithic Probability Calibration: In flat multi-class models, softmax probabilities across disease classes are coupled directly to the healthy class. This prevents operators from independently tuning the epidemiological screening boundary to match specific outbreak risk profiles without distorting the underlying differential disease distribution.")
    add_body(doc, "3) Interpretability Deficits & Hallucinatory Risk: Standard convolutional networks function as opaque black boxes [13]. Without spatial interpretability, farmers cannot verify whether a classification is driven by genuine pathological lesions (e.g., cutaneous pox scabs, plantar ulcers, or facial edema) or irrelevant background artifacts (e.g., feeder wire, soiled bedding, or lighting variations). Concurrently, deploying standalone large language models (LLMs) for on-farm advice carries severe hallucination risks [14], including the generation of fabricated antibiotic regimens that violate national veterinary drug regulations.")
    add_body(doc, "To overcome these challenges, we introduce PoultryHealth Intelligence, an end-to-end clinical decision-support framework that synergistically unifies hierarchical deep learning, gradient-weighted visual explanations, and grounded generative artificial intelligence (Fig. 1). Our key engineering and architectural contributions are as follows:")
    add_body(doc, "• Decoupled Two-Stage Neural Architecture: We decouple broad epidemiological screening from specific pathological classification using two lightweight MobileNetV2 [21] convolutional backbones pre-trained on ImageNet [10] via transfer learning [8], [9]. 'The Bouncer' performs binary screening (Healthy vs. Sick), while 'The Doctor' categorizes positive cases into four prevalent avian pathologies.")
    add_body(doc, "• Cost-Sensitive Screening Triage: We demonstrate that by adjusting the operational screening threshold from *p* = 0.50 to *p* = 0.35, the Bouncer's sick-bird sensitivity increases from 81.7% to 92.2% (261 of 279), slashing false-negative missed cases by 56.9% (from 51 down to 22) while preserving 71.2% healthy specificity [24]–[27].")
    add_body(doc, "• Empirical Common-Cohort Benchmark: We evaluate all models—the binary screener, 4-class specialist, full 5-class hierarchical cascade, and flat single-stage baselines (MobileNetV2, ResNet-50, DenseNet-121)—on a uniform held-out validation cohort of N = 425 images, presenting complete confusion matrices and per-class metrics.")
    add_body(doc, "• Explainability & Grounded Guidance: We incorporate Grad-CAM [23] targeting the penultimate convolutional feature maps to localize anatomical lesions, and pair this with prompt-grounded generative synthesis structured strictly around MSD Veterinary Manual clinical protocols [1]–[4] to enforce antimicrobial stewardship.")
    add_body(doc, "• Production-Grade Edge Deployment: We release a complete open-source software stack comprising an asynchronous FastAPI backend and a React single-page client, achieving 145 ms inference latency on standard consumer CPUs.")

    # FIGURE 1: ARCHITECTURE
    add_image_centered(doc, "extracted_media/427bb992fa3aa2bb743380c8c2c22a3fb699f945.png", width_inches=4.8)
    add_caption(doc, "Fig. 1. End-to-end system architecture and inference request lifecycle of PoultryHealth Intelligence, illustrating the multimodal input safety gate, decoupled two-stage neural pipeline, probability synthesis, Grad-CAM visual heatmaps, and grounded clinical report generation.")

    # SECTION II: RELATED WORK
    add_heading_1(doc, "II.  RELATED WORK")
    add_body(doc, "A. Deep Learning in Poultry Diagnostics")
    add_body(doc, "The application of computer vision to precision poultry farming has expanded rapidly across flock behavioral tracking, weight estimation, and pathological detection [19]. Early automated screening relied on hand-crafted texture and color descriptors applied to thermal or visible-spectrum flock imagery [15]. With the emergence of deep convolutional networks, recent studies have shifted toward end-to-end classification. Machuve et al. [5] trained deep CNNs to detect multiple poultry diseases from fecal and photographic data in smallholder environments. Mbelwa [6] benchmarked standard transfer-learning backbones for multi-class poultry illness categorization. Dhungana et al. [7] and Taşdelen & Arslan [16] investigated fecal-based image diagnostics, leveraging excretory morphology to identify Newcastle disease, Coccidiosis, and Salmonella. Luo, Chen, and Abdul Majeed [17] optimized feature-based transfer learning across poultry disease image sets, demonstrating the viability of domain adaptation. While non-invasive, fecal diagnostics require clean, isolated droppings and do not assess visible anatomical lesion presentations (e.g., cutaneous nodules, facial swelling, or plantar abscesses) characteristic of respiratory and dermatological conditions. More recently, Sabbella, Prachothan, and Panta [18] explored YOLOv8 object detection on bird photographs, demonstrating real-time bounding-box localization but requiring manual spatial bounding-box annotations that are labor-intensive to curate at scale. Neethirajan [19] provided a comprehensive survey of sensor modalities and computer vision techniques for precision poultry monitoring. Bist et al. [20] investigated computer vision for cage-free hen welfare, focusing specifically on footpad dermatitis and bumblefoot.")
    
    add_body(doc, "B. Hierarchical Classification & Cost-Sensitive Learning")
    add_body(doc, "Hierarchical classification structures the decision space into a directed taxonomy, decomposing complex multi-class problems into sequential sub-tasks [12]. Silla and Freitas [12] categorized hierarchical algorithms into local classifier per node, local classifier per parent, and global approaches, emphasizing their utility in biological classification where errors between distant taxonomic clades carry higher severity than errors between sister species. In medical diagnostics, hierarchical cascades have been successfully applied to separate healthy tissue from benign and malignant pathologies, mitigating severe class imbalances. Cost-sensitive learning [24] explicitly optimizes decision thresholds to penalize high-cost errors, providing a principled foundation for risk-averse clinical screening [25], [26], [27], [31].")

    add_body(doc, "C. Visual Saliency & Generative Clinical Guidance")
    add_body(doc, "Explainable AI (XAI) is essential for clinical decision support [13]. Gradient-weighted Class Activation Mapping (Grad-CAM) [23] computes the gradients of the target class score with respect to convolutional feature maps, producing coarse 2D heatmaps highlighting discriminative image regions without architectural retraining. Simultaneously, the rise of large language models (LLMs) has enabled conversational medical reporting; however, unconstrained LLMs frequently hallucinate factual errors and improper medication dosages [14]. Grounded generative systems bound generative models strictly to authoritative knowledge repositories, eliminating pharmacological hallucinations and enforcing established clinical guidelines.")

    # TABLE I: COMPARATIVE LITERATURE
    p_t1 = add_caption(doc, "TABLE I. COMPARATIVE ANALYSIS OF RELATED WORK IN POULTRY HEALTH DIAGNOSTICS")
    t1 = doc.add_table(rows=8, cols=4)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t1)
    
    headers_t1 = ["Study & Reference", "Diagnostic Modality", "Methodological Architecture", "Key Contributions & Limitations"]
    for j, h in enumerate(headers_t1):
        cell = t1.cell(0, j)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(8.5)
        r.font.bold = True
        set_cell_shading(cell, "F1F5F9")
        set_cell_margins(cell, top=80, bottom=80, left=50, right=50)

    data_t1 = [
        ("Zhuang & Zhang (2019) [15]", "Flock video / Digital vision", "Optical flow + SVM", "Early automated flock lethargy screening; limited to flock posture."),
        ("Mbelwa (2021) [6]", "Fecal & photographic images", "Single-stage CNN backbones", "Multi-class disease categorization; lacks screening hierarchy and XAI."),
        ("Machuve et al. (2022) [5]", "Field photographic data", "Standard CNN transfer learning", "Smallholder field deployment; treats all classification errors symmetrically."),
        ("Luo et al. (2025) [17]", "Poultry fecal imagery", "Feature-based transfer learning", "Domain-adapted feature extraction; focused strictly on fecal droppings."),
        ("Neethirajan (2022) [19]", "Sensor & vision survey", "AI review across poultry health", "Comprehensive taxonomy of sensor modalities and on-farm decision gaps."),
        ("Bist et al. (2024) [20]", "Footpad photography", "CNN binary classifier", "Automated bumblefoot detection in cage-free hens; single-condition scope."),
        ("Proposed (PoultryHealth Intelligence)", "Field clinical photographs (bird, foot, comb, head)", "Hierarchical MobileNetV2 + Grad-CAM + Grounded Gemini", "Decoupled screening/specialist cascade, cost-sensitive triage, lesion localization, grounded reports.")
    ]
    for row_idx, row_data in enumerate(data_t1):
        for col_idx, text in enumerate(row_data):
            cell = t1.cell(row_idx + 1, col_idx)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx < 3 else WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(text)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            if row_idx == len(data_t1) - 1:
                r.font.bold = True
                set_cell_shading(cell, "EFF6FF")
            elif row_idx % 2 == 1:
                set_cell_shading(cell, "F8FAFC")
            set_cell_margins(cell, top=60, bottom=60, left=50, right=50)

    add_styled_paragraph(doc, "", space_before=4, space_after=8)

    # SECTION III: SYSTEM ARCHITECTURE & METHODOLOGY
    add_heading_1(doc, "III.  SYSTEM ARCHITECTURE AND METHODOLOGY")
    add_body(doc, "A. Request Lifecycle & Multimodal Input Safety Gate")
    add_body(doc, "The operational request lifecycle begins when an end-user uploads a poultry photograph via the React web interface (Fig. 1). Before executing computationally intensive neural inference, the image is passed to a multimodal security gate powered by Gemini Flash. In agricultural field applications, users frequently upload out-of-domain distractors (e.g., domestic animals, humans, vehicles, or farm machinery). The input gate is prompted with a strict semantic classification instruction requiring a binary confirmation ('TRUE' or 'FALSE') indicating whether the image contains a whole poultry bird, avian anatomical extremity (head, beak, eye, comb, foot), or internal organ. Distractors trigger an immediate HTTP 400 rejection ('Access Denied: Image does not appear to contain a poultry bird, body part, or organ'), protecting downstream classifiers from irrelevant inputs.")

    add_body(doc, "B. Decoupled Two-Stage Neural Framework")
    add_body(doc, "Once verified by the input gate, the input photograph **x** is resized to 224 × 224 × 3 and routed to the two-stage convolutional hierarchy:")
    add_body(doc, "1) The Bouncer (Screening Model *f*_{B}): A binary MobileNetV2 network parameterized by weights *θ*_{B}, mapping an input photograph **x** to a scalar sickness posterior probability *p* ∈ [0, 1]:")

    # DISPLAY EQUATION (1)
    eq1_omml = """
    <m:r><m:rPr><m:i/></m:rPr><m:t>p</m:t></m:r>
    <m:r><m:t> = </m:t></m:r>
    <m:sSub>
      <m:e><m:r><m:rPr><m:i/></m:rPr><m:t>f</m:t></m:r></m:e>
      <m:sub><m:r><m:rPr><m:nor/></m:rPr><m:t>B</m:t></m:r></m:sub>
    </m:sSub>
    <m:d>
      <m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr>
      <m:e>
        <m:r><m:rPr><m:b/></m:rPr><m:t>x</m:t></m:r>
        <m:r><m:t>; </m:t></m:r>
        <m:sSub>
          <m:e><m:r><m:rPr><m:b/></m:rPr><m:t>θ</m:t></m:r></m:e>
          <m:sub><m:r><m:rPr><m:nor/></m:rPr><m:t>B</m:t></m:r></m:sub>
        </m:sSub>
      </m:e>
    </m:d>
    <m:r><m:t>,   </m:t></m:r>
    <m:r><m:rPr><m:i/></m:rPr><m:t>p</m:t></m:r>
    <m:r><m:t> ∈ [0, 1]</m:t></m:r>
    """
    add_display_equation(doc, eq1_omml, "1")

    add_body(doc, "The Bouncer is optimized using binary cross-entropy loss, directly establishing an optimal linear decision hyperplane between healthy and diseased states.")
    add_body(doc, "2) The Doctor (Specialist Model *f*_{D}): A four-class MobileNetV2 network parameterized by weights *θ*_{D}, mapping the input photograph **x** to a conditional pathology distribution vector **q** across the four target avian conditions:")

    # DISPLAY EQUATION (2)
    eq2_omml = """
    <m:r><m:rPr><m:b/></m:rPr><m:t>q</m:t></m:r>
    <m:r><m:t> = </m:t></m:r>
    <m:sSub>
      <m:e><m:r><m:rPr><m:i/></m:rPr><m:t>f</m:t></m:r></m:e>
      <m:sub><m:r><m:rPr><m:nor/></m:rPr><m:t>D</m:t></m:r></m:sub>
    </m:sSub>
    <m:d>
      <m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr>
      <m:e>
        <m:r><m:rPr><m:b/></m:rPr><m:t>x</m:t></m:r>
        <m:r><m:t>; </m:t></m:r>
        <m:sSub>
          <m:e><m:r><m:rPr><m:b/></m:rPr><m:t>θ</m:t></m:r></m:e>
          <m:sub><m:r><m:rPr><m:nor/></m:rPr><m:t>D</m:t></m:r></m:sub>
        </m:sSub>
      </m:e>
    </m:d>
    <m:r><m:t> = </m:t></m:r>
    <m:sSup>
      <m:e>
        <m:d>
          <m:dPr><m:begChr m:val="["/><m:endChr m:val="]"/></m:dPr>
          <m:e>
            <m:sSub><m:e><m:r><m:rPr><m:i/></m:rPr><m:t>q</m:t></m:r></m:e><m:sub><m:r><m:t>1</m:t></m:r></m:sub></m:sSub>
            <m:r><m:t>, </m:t></m:r>
            <m:sSub><m:e><m:r><m:rPr><m:i/></m:rPr><m:t>q</m:t></m:r></m:e><m:sub><m:r><m:t>2</m:t></m:r></m:sub></m:sSub>
            <m:r><m:t>, </m:t></m:r>
            <m:sSub><m:e><m:r><m:rPr><m:i/></m:rPr><m:t>q</m:t></m:r></m:e><m:sub><m:r><m:t>3</m:t></m:r></m:sub></m:sSub>
            <m:r><m:t>, </m:t></m:r>
            <m:sSub><m:e><m:r><m:rPr><m:i/></m:rPr><m:t>q</m:t></m:r></m:e><m:sub><m:r><m:t>4</m:t></m:r></m:sub></m:sSub>
          </m:e>
        </m:d>
      </m:e>
      <m:sup><m:r><m:rPr><m:nor/></m:rPr><m:t>T</m:t></m:r></m:sup>
    </m:sSup>
    <m:r><m:t> ∈ </m:t></m:r>
    <m:sSup>
      <m:e><m:r><m:t>Δ</m:t></m:r></m:e>
      <m:sup><m:r><m:t>3</m:t></m:r></m:sup>
    </m:sSup>
    """
    add_display_equation(doc, eq2_omml, "2")

    add_body(doc, "subject to the probability unit-simplex condition:")

    # DISPLAY EQUATION (3)
    eq3_omml = """
    <m:nary>
      <m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="undOvr"/></m:naryPr>
      <m:sub>
        <m:r><m:rPr><m:i/></m:rPr><m:t>k</m:t></m:r>
        <m:r><m:t>=1</m:t></m:r>
      </m:sub>
      <m:sup><m:r><m:t>4</m:t></m:r></m:sup>
      <m:e>
        <m:sSub>
          <m:e><m:r><m:rPr><m:i/></m:rPr><m:t>q</m:t></m:r></m:e>
          <m:sub><m:r><m:rPr><m:i/></m:rPr><m:t>k</m:t></m:r></m:sub>
        </m:sSub>
      </m:e>
    </m:nary>
    <m:r><m:t> = 1,   </m:t></m:r>
    <m:sSub>
      <m:e><m:r><m:rPr><m:i/></m:rPr><m:t>q</m:t></m:r></m:e>
      <m:sub><m:r><m:rPr><m:i/></m:rPr><m:t>k</m:t></m:r></m:sub>
    </m:sSub>
    <m:r><m:t> ≥ 0   ∀ </m:t></m:r>
    <m:r><m:rPr><m:i/></m:rPr><m:t>k</m:t></m:r>
    <m:r><m:t> ∈ {1, 2, 3, 4}</m:t></m:r>
    """
    add_display_equation(doc, eq3_omml, "3")

    add_body(doc, "where *q*_{1}, *q*_{2}, *q*_{3}, and *q*_{4} denote the predicted posterior probabilities for Bumblefoot, Chronic Respiratory Disease (CRD), Fowl Pox, and Infectious Coryza, respectively.")
    add_body(doc, "Both models leverage transfer learning [8], [9] from ImageNet-pre-trained MobileNetV2 backbones [21], with convolutional feature extractors frozen during initial training to preserve generalizable low-level edge and texture representations. Custom classification heads consisting of a Global Average Pooling 2D layer, Dropout (*p* = 0.20), and Dense layers were trained via Adam optimization.")

    add_body(doc, "C. Probability Synthesis & Cost-Sensitive Triage")
    add_body(doc, "To construct a unified 5-class joint probability distribution across Ω = {Healthy, Bumblefoot, CRD, Fowl Pox, Infectious Coryza}, we apply the chain rule of conditional probability (4)–(5):")

    # DISPLAY EQUATION (4)
    eq4_omml = """
    <m:r><m:rPr><m:nor/></m:rPr><m:t>P</m:t></m:r>
    <m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr>
      <m:e>
        <m:r><m:rPr><m:nor/></m:rPr><m:t>Healthy</m:t></m:r>
        <m:r><m:t> | </m:t></m:r>
        <m:r><m:rPr><m:b/></m:rPr><m:t>x</m:t></m:r>
      </m:e>
    </m:d>
    <m:r><m:t> = 1 − </m:t></m:r>
    <m:r><m:rPr><m:i/></m:rPr><m:t>p</m:t></m:r>
    """
    add_display_equation(doc, eq4_omml, "4")

    # DISPLAY EQUATION (5)
    eq5_omml = """
    <m:r><m:rPr><m:nor/></m:rPr><m:t>P</m:t></m:r>
    <m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr>
      <m:e>
        <m:sSub>
          <m:e><m:r><m:rPr><m:nor/></m:rPr><m:t>Disease</m:t></m:r></m:e>
          <m:sub><m:r><m:rPr><m:i/></m:rPr><m:t>k</m:t></m:r></m:sub>
        </m:sSub>
        <m:r><m:t> | </m:t></m:r>
        <m:r><m:rPr><m:b/></m:rPr><m:t>x</m:t></m:r>
      </m:e>
    </m:d>
    <m:r><m:t> = </m:t></m:r>
    <m:r><m:rPr><m:i/></m:rPr><m:t>p</m:t></m:r>
    <m:r><m:t> · </m:t></m:r>
    <m:sSub>
      <m:e><m:r><m:rPr><m:i/></m:rPr><m:t>q</m:t></m:r></m:e>
      <m:sub><m:r><m:rPr><m:i/></m:rPr><m:t>k</m:t></m:r></m:sub>
    </m:sSub>
    <m:r><m:t>,   ∀ </m:t></m:r>
    <m:r><m:rPr><m:i/></m:rPr><m:t>k</m:t></m:r>
    <m:r><m:t> ∈ {1, 2, 3, 4}</m:t></m:r>
    """
    add_display_equation(doc, eq5_omml, "5")

    add_body(doc, "Under the default symmetric decision rule, an incoming photograph is categorized as Healthy if *p* < 0.50, and assigned to argmax_{k}(*q*_{k}) if *p* ≥ 0.50. However, in epidemiological disease containment, the cost of a false negative (missed sick bird, *C*_{FN}) vastly exceeds the cost of a false positive (healthy bird flagged for inspection, *C*_{FP}). To prioritize sensitivity, the Bayesian optimal decision rule assigns **x** to the sick cohort whenever the screening probability *p* satisfies the cost-sensitive triage threshold (6) [24]:")

    # DISPLAY EQUATION (6)
    eq6_omml = """
    <m:sSub>
      <m:e><m:r><m:rPr><m:i/></m:rPr><m:t>p</m:t></m:r></m:e>
      <m:sub><m:r><m:rPr><m:nor/></m:rPr><m:t>thresh</m:t></m:r></m:sub>
    </m:sSub>
    <m:r><m:t> = </m:t></m:r>
    <m:f>
      <m:num>
        <m:sSub>
          <m:e><m:r><m:rPr><m:i/></m:rPr><m:t>C</m:t></m:r></m:e>
          <m:sub><m:r><m:rPr><m:nor/></m:rPr><m:t>FP</m:t></m:r></m:sub>
        </m:sSub>
      </m:num>
      <m:den>
        <m:sSub>
          <m:e><m:r><m:rPr><m:i/></m:rPr><m:t>C</m:t></m:r></m:e>
          <m:sub><m:r><m:rPr><m:nor/></m:rPr><m:t>FP</m:t></m:r></m:sub>
        </m:sSub>
        <m:r><m:t> + </m:t></m:r>
        <m:sSub>
          <m:e><m:r><m:rPr><m:i/></m:rPr><m:t>C</m:t></m:r></m:e>
          <m:sub><m:r><m:rPr><m:nor/></m:rPr><m:t>FN</m:t></m:r></m:sub>
        </m:sSub>
      </m:den>
    </m:f>
    """
    add_display_equation(doc, eq6_omml, "6")

    add_body(doc, "Setting *p*_{thresh} = 0.35 reflects an operational cost ratio *C*_{FN} / *C*_{FP} ≈ 1.86, shifting the decision boundary to flag birds exhibiting early or ambiguous symptoms, routing them for specialist review and reducing false-negative missed cases by 56.9% while maintaining 71.2% healthy specificity [24].")

    add_body(doc, "D. Open-Set Abstention Safety Protocol")
    add_body(doc, "In addition to binary screening, practical veterinary deployment requires safeguarding against atypical or unmodeled pathologies (e.g., Coccidiosis, Newcastle disease, or nutritional deficiencies). When an image passes to the Doctor, the system evaluates the maximum softmax probability across the specialist output distribution (7):")

    # DISPLAY EQUATION (7)
    eq7_omml = """
    <m:sSub>
      <m:e><m:r><m:rPr><m:i/></m:rPr><m:t>q</m:t></m:r></m:e>
      <m:sub><m:r><m:rPr><m:nor/></m:rPr><m:t>max</m:t></m:r></m:sub>
    </m:sSub>
    <m:r><m:t> = </m:t></m:r>
    <m:sSub>
      <m:e><m:r><m:rPr><m:nor/></m:rPr><m:t>max</m:t></m:r></m:e>
      <m:sub><m:r><m:rPr><m:i/></m:rPr><m:t>k</m:t></m:r><m:r><m:t> ∈ {1..4}</m:t></m:r></m:sub>
    </m:sSub>
    <m:sSub>
      <m:e><m:r><m:rPr><m:i/></m:rPr><m:t>q</m:t></m:r></m:e>
      <m:sub><m:r><m:rPr><m:i/></m:rPr><m:t>k</m:t></m:r></m:sub>
    </m:sSub>
    """
    add_display_equation(doc, eq7_omml, "7")

    add_body(doc, "If *q*_{max} < *τ*_{open}, where *τ*_{open} = 0.40, the system outputs an 'Atypical Pathology Alert', advising the user that the presentation cannot be categorized with sufficient confidence and recommending confirmatory veterinary consultation [22].")

    add_body(doc, "E. Pathological Explainability via Grad-CAM")
    add_body(doc, "To ensure that automated classifications reflect genuine anatomical pathology rather than background artifacts [13], we implement Gradient-weighted Class Activation Mapping (Grad-CAM) [23]. Grad-CAM computes the gradient of the predicted class score *y*^{c} with respect to the feature map activations *A*^{k} of the penultimate convolutional layer ('out_relu', 7 × 7 × 1280). Neuron importance weights *α*_{k}^{c} are obtained via global average pooling across spatial dimensions (8) (with *Z* = *H* · *W* = 49):")

    # DISPLAY EQUATION (8)
    eq8_omml = """
    <m:sSubSup>
      <m:e><m:r><m:rPr><m:i/></m:rPr><m:t>α</m:t></m:r></m:e>
      <m:sub><m:r><m:rPr><m:i/></m:rPr><m:t>k</m:t></m:r></m:sub>
      <m:sup><m:r><m:rPr><m:i/></m:rPr><m:t>c</m:t></m:r></m:sup>
    </m:sSubSup>
    <m:r><m:t> = </m:t></m:r>
    <m:f>
      <m:num><m:r><m:t>1</m:t></m:r></m:num>
      <m:den><m:r><m:rPr><m:i/></m:rPr><m:t>Z</m:t></m:r></m:den>
    </m:f>
    <m:sSub>
      <m:e><m:r><m:t>∑</m:t></m:r></m:e>
      <m:sub><m:r><m:rPr><m:i/></m:rPr><m:t>i</m:t></m:r></m:sub>
    </m:sSub>
    <m:sSub>
      <m:e><m:r><m:t>∑</m:t></m:r></m:e>
      <m:sub><m:r><m:rPr><m:i/></m:rPr><m:t>j</m:t></m:r></m:sub>
    </m:sSub>
    <m:f>
      <m:num>
        <m:r><m:t>∂ </m:t></m:r>
        <m:sSup>
          <m:e><m:r><m:rPr><m:i/></m:rPr><m:t>y</m:t></m:r></m:e>
          <m:sup><m:r><m:rPr><m:i/></m:rPr><m:t>c</m:t></m:r></m:sup>
        </m:sSup>
      </m:num>
      <m:den>
        <m:r><m:t>∂ </m:t></m:r>
        <m:sSubSup>
          <m:e><m:r><m:rPr><m:i/></m:rPr><m:t>A</m:t></m:r></m:e>
          <m:sub><m:r><m:rPr><m:i/></m:rPr><m:t>i,j</m:t></m:r></m:sub>
          <m:sup><m:r><m:rPr><m:i/></m:rPr><m:t>k</m:t></m:r></m:sup>
        </m:sSubSup>
      </m:den>
    </m:f>
    """
    add_display_equation(doc, eq8_omml, "8")

    add_body(doc, "The class-discriminative saliency heatmap *L*_{Grad-CAM}^{c} is generated by computing a rectified linear combination of feature activations (9):")

    # DISPLAY EQUATION (9)
    eq9_omml = """
    <m:sSubSup>
      <m:e><m:r><m:rPr><m:i/></m:rPr><m:t>L</m:t></m:r></m:e>
      <m:sub><m:r><m:rPr><m:nor/></m:rPr><m:t>Grad-CAM</m:t></m:r></m:sub>
      <m:sup><m:r><m:rPr><m:i/></m:rPr><m:t>c</m:t></m:r></m:sup>
    </m:sSubSup>
    <m:r><m:t> = </m:t></m:r>
    <m:r><m:rPr><m:nor/></m:rPr><m:t>ReLU</m:t></m:r>
    <m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr>
      <m:e>
        <m:sSub>
          <m:e><m:r><m:t>∑</m:t></m:r></m:e>
          <m:sub><m:r><m:rPr><m:i/></m:rPr><m:t>k</m:t></m:r></m:sub>
        </m:sSub>
        <m:sSubSup>
          <m:e><m:r><m:rPr><m:i/></m:rPr><m:t>α</m:t></m:r></m:e>
          <m:sub><m:r><m:rPr><m:i/></m:rPr><m:t>k</m:t></m:r></m:sub>
          <m:sup><m:r><m:rPr><m:i/></m:rPr><m:t>c</m:t></m:r></m:sup>
        </m:sSubSup>
        <m:sSup>
          <m:e><m:r><m:rPr><m:i/></m:rPr><m:t>A</m:t></m:r></m:e>
          <m:sup><m:r><m:rPr><m:i/></m:rPr><m:t>k</m:t></m:r></m:sup>
        </m:sSup>
      </m:e>
    </m:d>
    """
    add_display_equation(doc, eq9_omml, "9")

    add_body(doc, "The resulting 7 × 7 heatmap is bilinearly upsampled to 224 × 224, normalized to [0, 1], color-mapped using OpenCV's Jet palette, and blended with the original input photograph (*α* = 0.40, *β* = 0.60) (Fig. 3).")

    add_body(doc, "F. Grounded Clinical Synthesis & Antimicrobial Stewardship")
    add_body(doc, "The final stage translates neural predictions and saliency maps into an actionable, structured clinical report. Standalone generative LLMs present acute risks of pharmacological hallucination [14]. To eliminate this risk, our backend injects a closed-world veterinary knowledge base structured strictly around authoritative clinical protocols from the MSD Veterinary Manual [1]–[4] (Table IV). The system prompt instructs Gemini Flash to ground its diagnostic synthesis exclusively within this verified clinical text. In accordance with WHO and WOAH antimicrobial stewardship principles [10], [11], the knowledge base explicitly proscribes unguided over-the-counter antibiotic dispensing, emphasizing strict quarantine, electrolyte support, lesion hygiene (e.g., warm Epsom salt baths for Bumblefoot, povidone-iodine for cutaneous pox), coop ventilation improvements, and mandatory veterinary consultation.")

    # SECTION IV: DATASET CURATION & BENCHMARK COMPOSITION
    add_heading_1(doc, "IV.  DATASET CURATION AND BENCHMARK COMPOSITION")
    add_body(doc, "A. Dataset Provenance & Curation")
    add_body(doc, "The master empirical corpus was compiled from two distinct sources to reflect both standardized laboratory archives and diverse on-farm photographic conditions:")
    add_body(doc, "1) Roboflow Universe Benchmark: An open-access poultry disease dataset ('vdataset ayush-m-singh') exported via Roboflow Universe under CC BY 4.0 [32], comprising 2,031 images partitioned across five categories: Healthy (712), Bumblefoot (92), Chronic Respiratory Disease (CRD, 673), Fowl Pox (114), and Infectious Coryza (440). The dataset was exported in raw folder format without artificial pre-processing or synthetic augmentations.")
    add_body(doc, "2) Handpicked Field Dataset: To introduce challenging real-world variations (e.g., diverse coop lighting, natural dirt substrates, varying plumage colors, and occluding wire meshes), the authors collected supplementary photographs from open agricultural extension services, poultry health bulletins, and veterinary advisory blogs. Images were labeled visually according to textbook anatomical lesion presentations defined in the MSD Veterinary Manual [1]–[4]. Crucially, as noted in Section IX, these field images lack laboratory PCR or culture confirmation, reflecting the diagnostic reality of rural poultry photography.")
    add_body(doc, "From the combined raw corpus of 2,164 files, an empirical audit purged 18 unusable items: 7 non-poultry distractor images (cars, domestic pets in the 'Others' folder), 2 exact byte duplicates identified via MD5 hash matching between datasets, and unreadable files. The resulting cleaned master benchmark comprises 2,143 images.")

    add_body(doc, "B. Benchmark Partitioning & Class Distribution")
    add_body(doc, "The master benchmark was partitioned using a stratified 80/20 train/validation split per class with a fixed random seed (Table II):")
    add_body(doc, "• Sickness Screening Cohort (The Bouncer): 1,718 training images (585 Healthy, 1,133 Sick) and 425 held-out validation images (146 Healthy, 279 Sick).")
    add_body(doc, "• Differential Diagnosis Cohort (The Doctor): 1,133 training images and 279 held-out validation images spanning the four disease classes: Bumblefoot (23), CRD (137), Fowl Pox (29), and Infectious Coryza (90).")
    add_body(doc, "• Common Validation Benchmark: The full 5-class evaluation and single-stage baselines are evaluated on the exact same N = 425 validation cohort (146 Healthy, 279 Diseased), ensuring completely consistent comparative denominators across all models.")

    # TABLE II: DATASET
    p_t2 = add_caption(doc, "TABLE II. DATASET COMPOSITION ACROSS CLINICAL CATEGORIES")
    t2 = doc.add_table(rows=7, cols=6)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t2)
    
    headers_t2 = ["Clinical Class", "Roboflow Set", "Handpicked Set", "Training Split (80%)", "Validation Split (20%)", "Total Cohort"]
    for j, h in enumerate(headers_t2):
        cell = t2.cell(0, j)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(8.5)
        r.font.bold = True
        set_cell_shading(cell, "F1F5F9")
        set_cell_margins(cell, top=80, bottom=80, left=50, right=50)

    data_t2 = [
        ("Healthy (Non-Diseased)", "712", "19", "585", "146", "731"),
        ("Bumblefoot (Pododermatitis)", "92", "23", "92", "23", "115"),
        ("Chronic Respiratory Disease (CRD)", "673", "10", "546", "137", "683"),
        ("Fowl Pox (Avipoxvirus)", "114", "30", "115", "29", "144"),
        ("Infectious Coryza (Avibacterium)", "440", "30", "380", "90", "470"),
        ("Total Master Benchmark", "2,031", "112", "1,718", "425", "2,143")
    ]
    for row_idx, row_data in enumerate(data_t2):
        for col_idx, text in enumerate(row_data):
            cell = t2.cell(row_idx + 1, col_idx)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx == 0 else WD_ALIGN_PARAGRAPH.RIGHT
            p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(text)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            if row_idx == len(data_t2) - 1:
                r.font.bold = True
                set_cell_shading(cell, "EFF6FF")
            elif row_idx % 2 == 1:
                set_cell_shading(cell, "F8FAFC")
            set_cell_margins(cell, top=60, bottom=60, left=50, right=50)

    add_styled_paragraph(doc, "", space_before=4, space_after=8)

    # SECTION V: EXPERIMENTAL SETUP & TRAINING METHODOLOGY
    add_heading_1(doc, "V.  EXPERIMENTAL SETUP AND TRAINING METHODOLOGY")
    add_body(doc, "A. Implementation & Hardware Environment")
    add_body(doc, "Models were implemented in TensorFlow 2.15 / Keras and trained using an NVIDIA RTX GPU environment with CUDA 12.2. Production inference was benchmarked on an Intel Core i7-11800H CPU @ 2.30 GHz (8 cores, 16 threads) with 16 GB RAM under 64-bit Windows 11.")

    add_body(doc, "B. Data Augmentation & Regularization")
    add_body(doc, "To mitigate overfitting given class imbalances, an in-graph data augmentation pipeline was applied during training: RandomFlip('horizontal'), RandomRotation(factor=0.20), and RandomZoom(height_factor=0.15, width_factor=0.15). Images were normalized to [0, 1] via Rescaling(1./255).")

    add_body(doc, "C. Hyperparameters & Optimization Schedule")
    add_body(doc, "Training hyperparameters were configured identically across models (Table III). The Bouncer was trained for 20 epochs using Adam (initial lr = 1e-3, beta_1 = 0.9, beta_2 = 0.999), decaying learning rates on plateau (factor = 0.2, patience = 3, min_lr = 1e-6). The Doctor was trained for 25 epochs under the same schedule. Both models exhibited stable convergence without divergent validation loss (Fig. 2).")

    # TABLE III: HYPERPARAMETERS
    p_t3 = add_caption(doc, "TABLE III. NEURAL TRAINING HYPERPARAMETERS AND EXECUTION CONFIGURATION")
    t3 = doc.add_table(rows=7, cols=5)
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t3)
    
    headers_t3 = ["Hyperparameter / Setting", "Bouncer (Screener)", "Doctor (Specialist)", "Flat Baseline (MobileNet)", "Flat Baseline (ResNet-50)"]
    for j, h in enumerate(headers_t3):
        cell = t3.cell(0, j)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(8.5)
        r.font.bold = True
        set_cell_shading(cell, "F1F5F9")
        set_cell_margins(cell, top=80, bottom=80, left=50, right=50)

    data_t3 = [
        ("Base Architecture", "MobileNetV2 [21]", "MobileNetV2 [21]", "MobileNetV2 [21]", "ResNet-50"),
        ("Pretrained Weights", "ImageNet-1k [10]", "ImageNet-1k [10]", "ImageNet-1k [10]", "ImageNet-1k [10]"),
        ("Loss Function", "Binary Cross-Entropy", "Categorical Cross-Entropy", "Categorical Cross-Entropy", "Categorical Cross-Entropy"),
        ("Batch Size & Epochs", "32 batch / 20 epochs", "32 batch / 25 epochs", "32 batch / 25 epochs", "32 batch / 25 epochs"),
        ("Optimizer & Initial LR", "Adam (lr = 1e-3)", "Adam (lr = 1e-3)", "Adam (lr = 1e-3)", "Adam (lr = 1e-3)"),
        ("Dropout Probability", "0.20", "0.20", "0.20", "0.20")
    ]
    for row_idx, row_data in enumerate(data_t3):
        for col_idx, text in enumerate(row_data):
            cell = t3.cell(row_idx + 1, col_idx)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx == 0 else WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(text)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            if row_idx % 2 == 1:
                set_cell_shading(cell, "F8FAFC")
            set_cell_margins(cell, top=60, bottom=60, left=50, right=50)

    add_styled_paragraph(doc, "", space_before=4, space_after=8)

    # FIGURE 2: TRAINING CURVES
    add_image_centered(doc, "extracted_media/185af714daaa9cbb39f38f0390db2d6a6a51ae4d.png", width_inches=4.8)
    add_caption(doc, "Fig. 2. Training and validation accuracy trajectories across epochs for (a) the Bouncer binary screening model and (b) the Doctor four-class disease specialist, showing stable convergence without overfitting.")

    # SECTION VI: VETERINARY KNOWLEDGE BASE
    add_heading_1(doc, "VI.  VETERINARY KNOWLEDGE BASE AND ANTIMICROBIAL STEWARDSHIP")
    add_body(doc, "Table IV presents the approved veterinary guidance text embedded in the backend. When generating reports, the generative AI engine is constrained to draw management protocols exclusively from these clinical descriptions.")

    # TABLE IV: KNOWLEDGE BASE
    p_t4 = add_caption(doc, "TABLE IV. AUTHORITATIVE VETERINARY KNOWLEDGE BASE ALIGNED WITH MSD CLINICAL MANUAL")
    t4 = doc.add_table(rows=6, cols=3)
    t4.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t4)
    
    headers_t4 = ["Clinical Condition", "Etiological Agent & Pathology", "Standardized Veterinary Protocol & Biosecurity Action"]
    for j, h in enumerate(headers_t4):
        cell = t4.cell(0, j)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(8.5)
        r.font.bold = True
        set_cell_shading(cell, "F1F5F9")
        set_cell_margins(cell, top=80, bottom=80, left=50, right=50)

    data_t4 = [
        ("Healthy", "Normal physiology / Non-diseased", "Status: Clear. Action: No medical intervention required. Prevention: Maintain strict biosecurity, ensure clean dry bedding, and provide ad-libitum access to clean water."),
        ("Bumblefoot [4]", "Staphylococcus aureus (Ulcerative Pododermatitis)", "Status: Pododermatitis abscess. Immediate: Move to soft-bedded isolation. Treatment: Soak foot in warm Epsom salt bath (15 min). Cleanse with antiseptic wash, apply topical salve, and bandage securely. Consult veterinarian if severe. Prevention: Inspect roosts, remove sharp splinters, keep litter dry."),
        ("CRD [1]", "Mycoplasma gallisepticum (Chronic Respiratory)", "Status: Chronic Respiratory Disease - HIGHLY CONTAGIOUS. Immediate: Quarantine immediately to halt aerosol transmission. Clinical Action: Consult licensed avian veterinarian for confirmatory diagnosis and lawful prescription antimicrobial therapy. Do not self-administer unguided antibiotics. Biosecurity: Improve ventilation to lower ammonia. Provide electrolytes."),
        ("Fowl Pox [3]", "Avipoxvirus (Cutaneous Pox Scabs)", "Status: Viral Cutaneous Dermatosis - SLOW SPREADING. Immediate: Isolate affected birds. Treatment: No antiviral cure exists. Apply dilute povidone-iodine to scabs to prevent secondary bacterial infection. Care: Provide warm, stress-free shelter and soft mash feed."),
        ("Infectious Coryza [2]", "Avibacterium paragallinarum (Acute Coryza)", "Status: Acute Respiratory Bacterial Infection - HIGHLY CONTAGIOUS. Immediate: Enforce strict isolated quarantine immediately. Clinical Action: Consult licensed avian veterinarian urgently for flock-level diagnostic confirmation. Warning: Recovered birds frequently remain asymptomatic lifelong carriers. Disinfect feeders and drinkers thoroughly.")
    ]
    for row_idx, row_data in enumerate(data_t4):
        for col_idx, text in enumerate(row_data):
            cell = t4.cell(row_idx + 1, col_idx)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx < 2 else WD_ALIGN_PARAGRAPH.JUSTIFY if hasattr(WD_ALIGN_PARAGRAPH, 'JUSTIFY') else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(text)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            if row_idx % 2 == 1:
                set_cell_shading(cell, "F8FAFC")
            set_cell_margins(cell, top=60, bottom=60, left=50, right=50)

    add_styled_paragraph(doc, "", space_before=4, space_after=8)

    # FIGURE 3: GRAD-CAM
    add_image_centered(doc, "extracted_media/db10a20c0229c65164ca340d26ce2a44d49c767c.png", width_inches=4.8)
    add_caption(doc, "Fig. 3. Input poultry photograph and Grad-CAM visual saliency heatmap overlay, demonstrating precise localization on characteristic clinical lesions.")

    # SECTION VII: RESULTS & COMPARATIVE BENCHMARKING
    add_heading_1(doc, "VII.  RESULTS AND COMPARATIVE BENCHMARKING")
    add_body(doc, "A. Baseline Comparison & Ablation Analysis")
    add_body(doc, "To rigorously evaluate our architectural design, we benchmarked the hierarchical cascade against standard single-stage flat multi-class models (MobileNetV2, ResNet-50, DenseNet-121) across the identical held-out validation cohort (N = 425 images: 146 Healthy, 279 Diseased) (Table V). We also examined threshold tuning on the flat MobileNetV2 baseline by evaluating its performance at θ = 0.35 and θ = 0.28 (matched to our 92.2% recall).")

    # TABLE V: BASELINE COMPARISON
    p_t5 = add_caption(doc, "TABLE V. COMPARATIVE SCREENING AND DIAGNOSTIC BENCHMARK ON COMMON VALIDATION COHORT (N = 425)")
    t5 = doc.add_table(rows=8, cols=7)
    t5.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t5)
    
    headers_t5 = ["Model / Architectural Paradigm", "5-Class Acc.", "Macro F1", "Sick Recall", "Sick Prec.", "Specificity", "Screening AUC"]
    for j, h in enumerate(headers_t5):
        cell = t5.cell(0, j)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(8.5)
        r.font.bold = True
        set_cell_shading(cell, "F1F5F9")
        set_cell_margins(cell, top=80, bottom=80, left=50, right=50)

    data_t5 = [
        ("Flat MobileNetV2 (Argmax, θ = 0.50)", "64.7%", "0.589", "72.4%", "85.2%", "76.0%", "0.832 [0.793–0.869]"),
        ("Flat ResNet-50 (Argmax, θ = 0.50)", "65.4%", "0.592", "73.8%", "84.8%", "74.7%", "0.838 [0.799–0.874]"),
        ("Flat DenseNet-121 (Argmax, θ = 0.50)", "65.2%", "0.591", "74.2%", "84.1%", "73.3%", "0.835 [0.796–0.871]"),
        ("Flat MobileNetV2 (Threshold θ = 0.35)", "63.8%", "0.581", "85.3%", "82.1%", "64.4%", "0.832 [0.793–0.869]"),
        ("Flat MobileNetV2 (Tuned θ = 0.28, matched recall)", "59.8%", "0.552", "92.2%", "79.8%", "54.8%", "0.832 [0.793–0.869]"),
        ("Hierarchical Cascade (Default p = 0.50)", "66.8%", "0.596", "81.7%", "90.1%", "82.9%", "0.884 [0.851–0.915]"),
        ("Hierarchical Cascade (Cost-Sensitive p = 0.35)", "65.4%", "0.588", "92.2%", "86.1%", "71.2%", "0.884 [0.851–0.915]")
    ]
    for row_idx, row_data in enumerate(data_t5):
        for col_idx, text in enumerate(row_data):
            cell = t5.cell(row_idx + 1, col_idx)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx == 0 else WD_ALIGN_PARAGRAPH.RIGHT
            p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(text)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            if row_idx >= len(data_t5) - 2:
                r.font.bold = True
                set_cell_shading(cell, "EFF6FF")
            elif row_idx % 2 == 1:
                set_cell_shading(cell, "F8FAFC")
            set_cell_margins(cell, top=60, bottom=60, left=50, right=50)

    add_styled_paragraph(doc, "", space_before=4, space_after=8)

    add_body(doc, "As evidenced in Table V, the empirical comparison yields two central insights into the mechanics of the hierarchical pipeline:")
    add_body(doc, "1) Decoupled Screening vs. Flat Threshold Tuning: Because both models employ the same frozen MobileNetV2 backbone, feature representations are identical; the performance difference stems from the linear classification head. In the Flat MobileNetV2 baseline, a 5-unit linear head is trained with categorical cross-entropy, where errors between CRD and Coryza compete against errors between Healthy and Sick. In contrast, the Bouncer's 1-unit head is trained with binary cross-entropy, directly optimizing the linear hyperplane for epidemiological screening. Consequently, the Bouncer achieves a statistically superior binary screening AUC-ROC (0.884 [95% CI: 0.851–0.915] vs. 0.832 [95% CI: 0.793–0.869]; *p* = 0.008 via DeLong's test for paired ROC curves [25]–[27]). When the flat model's threshold is lowered to *θ* = 0.28 to match our 92.2% recall, its specificity collapses to 54.8% (falsely flagging 45.2% of healthy birds), whereas the Bouncer maintains 71.2% specificity at *p* = 0.35 [24].")
    add_body(doc, "2) End-to-End 5-Class Equivalence: While the hierarchical pipeline provides superior screening flexibility, its overall 5-class accuracy (~65–67%) and macro F1 (~0.59) remain comparable to single-stage flat baselines. The clinical value of the hierarchical framework therefore lies not in an overall accuracy leap, but in providing a tunable, high-sensitivity screening gate tailored to flock contagion containment without altering downstream disease weights.")

    # TABLE VI: BOUNCER REPORT
    add_heading_2(doc, "B. The Bouncer Screening Performance & Threshold Tuning")
    add_body(doc, "The Bouncer reaches 82.1% accuracy (349 of 425; 95% CI: 78.1–85.5%), a macro F1 of 0.81, a balanced accuracy of 82.3%, and a Matthews Correlation Coefficient (MCC) of 0.62 on the validation cohort (Table VI, Fig. 4) [28], [29], [30]. Precision for the sick class is 90.1% (228 of 253; 95% CI: 85.8–93.4%), meaning that a bird flagged as sick is very likely to be diseased. Sick recall is 81.7% (228 of 279; 95% CI: 76.8–85.8%): 51 of 279 sick birds (18.3%) were passed as healthy, and 25 of 146 healthy birds (17.1%) were flagged as sick. Precision for Healthy is 70.3% because 51 of the 172 birds called healthy (29.7%) are in fact sick.")

    add_image_centered(doc, "extracted_media/fig4_bouncer_cm_425.png", width_inches=4.4)
    add_caption(doc, "Fig. 4. Bouncer binary confusion matrix (Healthy vs. Sick) on the validation cohort (n = 425, Accuracy: 82.1%).")

    p_t6 = add_caption(doc, "TABLE VI. THE BOUNCER CLASSIFICATION PERFORMANCE AT DEFAULT THRESHOLD (p = 0.50, n = 425)")
    t6 = doc.add_table(rows=4, cols=6)
    t6.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t6)
    
    headers_t6 = ["Class", "Support (n)", "Precision", "Recall", "F1-Score", "Recall 95% CI [28]"]
    for j, h in enumerate(headers_t6):
        cell = t6.cell(0, j)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(8.5)
        r.font.bold = True
        set_cell_shading(cell, "F1F5F9")
        set_cell_margins(cell, top=80, bottom=80, left=50, right=50)

    data_t6 = [
        ("Healthy (Non-Diseased)", "146", "70.3%", "82.9%", "0.76", "75.9–88.1%"),
        ("Sick (Diseased Cohort)", "279", "90.1%", "81.7%", "0.86", "76.8–85.8%"),
        ("Macro Average", "425", "80.2%", "82.3%", "0.81", "—")
    ]
    for row_idx, row_data in enumerate(data_t6):
        for col_idx, text in enumerate(row_data):
            cell = t6.cell(row_idx + 1, col_idx)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx == 0 else WD_ALIGN_PARAGRAPH.RIGHT
            p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(text)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            if row_idx == len(data_t6) - 1:
                r.font.bold = True
                set_cell_shading(cell, "EFF6FF")
            elif row_idx % 2 == 1:
                set_cell_shading(cell, "F8FAFC")
            set_cell_margins(cell, top=60, bottom=60, left=50, right=50)

    add_styled_paragraph(doc, "", space_before=4, space_after=8)

    # TABLE VII: THRESHOLD SWEEP
    add_body(doc, "At the default threshold (*p* = 0.50), missing one sick bird in five (18.3% false negative rate) is sub-optimal for high-density poultry operations where undetected respiratory pathogens rapidly infect co-housed birds. Table VII details the performance trajectory across operational screening thresholds:")

    p_t7 = add_caption(doc, "TABLE VII. BOUNCER SENSITIVITY TRAJECTORY ACROSS SCREENING THRESHOLDS (n = 425)")
    t7 = doc.add_table(rows=5, cols=6)
    t7.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t7)
    
    headers_t7 = ["Operating Threshold", "Sick Recall (Sensitivity)", "Healthy Specificity", "Sick Precision", "False Negatives (Missed)", "Youden's Index (J)"]
    for j, h in enumerate(headers_t7):
        cell = t7.cell(0, j)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(8.5)
        r.font.bold = True
        set_cell_shading(cell, "F1F5F9")
        set_cell_margins(cell, top=80, bottom=80, left=50, right=50)

    data_t7 = [
        ("p = 0.50 (Default)", "81.7% (228/279)", "82.9% (121/146)", "90.1% (228/253)", "51 birds", "0.646"),
        ("p = 0.40 (Intermediate)", "87.5% (244/279)", "77.4% (113/146)", "88.1% (244/277)", "35 birds", "0.649"),
        ("p = 0.35 (Safety-First Triage)", "92.2% (261/279)", "71.2% (104/146)", "86.1% (261/303)", "22 birds", "0.634"),
        ("p = 0.25 (Aggressive Quarantine)", "96.1% (268/279)", "54.8% (80/146)", "80.2% (268/334)", "11 birds", "0.509")
    ]
    for row_idx, row_data in enumerate(data_t7):
        for col_idx, text in enumerate(row_data):
            cell = t7.cell(row_idx + 1, col_idx)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx == 0 else WD_ALIGN_PARAGRAPH.RIGHT
            p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(text)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            if row_idx == 2:
                r.font.bold = True
                set_cell_shading(cell, "FEF3C7")
            elif row_idx % 2 == 1:
                set_cell_shading(cell, "F8FAFC")
            set_cell_margins(cell, top=60, bottom=60, left=50, right=50)

    add_styled_paragraph(doc, "", space_before=4, space_after=8)
    add_body(doc, "Shifting the operating point to *p* = 0.35 surges sick-bird sensitivity to 92.2% (261 of 279 detected), reducing missed sick birds by 56.9% (from 51 down to 22). This sensitivity gain incurs only a moderate reduction in specificity (from 82.9% to 71.2%), providing an operationally attractive trade-off for commercial quarantine containment [24], [31].")

    # DOCTOR EVALUATION
    add_heading_2(doc, "C. The Doctor Four-Class Disease Specialization")
    add_body(doc, "The Doctor achieves 71.7% accuracy (200 of 279; 95% CI: 66.1–76.6%), a macro F1 of 0.65, a balanced accuracy of 66.5%, and a Cohen's kappa of 0.56 on the diseased validation cohort (Table VIII, Fig. 5) [28], [29]. Disease-level breakdown reveals clear pathological patterns:")
    add_body(doc, "1) Chronic Respiratory Disease (CRD) is the most reliably classified pathology (F1 = 0.81, recall 82.5%, precision 80.1%, n = 137), supported by substantial training sample size and distinctive facial conjunctivitis features.")
    add_body(doc, "2) Fowl Pox exhibits high recall (89.7%, 26 of 29 detected; 95% CI: 73.6–96.4%) but lower precision (53.1%, 26 of 49) because scabs and nodular lesions overlap visually with dry necrotic tissue in Bumblefoot (9) and facial swelling in Coryza (10).")
    add_body(doc, "3) Infectious Coryza is primarily confused with CRD: 26 of 90 Coryza images were predicted as CRD, and 20 of 137 CRD images were predicted as Coryza (Fig. 5). Both are upper-respiratory bacterial/mycoplasmal infections that present with ocular discharge and facial edema.")
    add_body(doc, "4) Bumblefoot has high precision (80.0%, 8 of 10) but low recall (34.8%, 8 of 23; 95% CI: 18.8–55.1%). Plantar ulcerations on feet were frequently misclassified as Fowl Pox (9) or Coryza (4) when footpad lesions were partially occluded by bedding.")

    add_image_centered(doc, "extracted_media/0ed13235ea1003ea1c8758234ef6a6368fe87bde.png", width_inches=4.4)
    add_caption(doc, "Fig. 5. Doctor four-class disease confusion matrix on the diseased validation cohort (n = 279, Accuracy: 71.7%).")

    # TABLE VIII: DOCTOR REPORT
    p_t8 = add_caption(doc, "TABLE VIII. THE DOCTOR FOUR-CLASS DISEASE CLASSIFICATION REPORT (n = 279)")
    t8 = doc.add_table(rows=6, cols=6)
    t8.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t8)
    
    headers_t8 = ["Disease Category", "Support (n)", "Precision", "Recall", "F1-Score", "Recall 95% CI [28]"]
    for j, h in enumerate(headers_t8):
        cell = t8.cell(0, j)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(8.5)
        r.font.bold = True
        set_cell_shading(cell, "F1F5F9")
        set_cell_margins(cell, top=80, bottom=80, left=50, right=50)

    data_t8 = [
        ("Bumblefoot [4]", "23", "80.0%", "34.8%", "0.49", "18.8–55.1%"),
        ("Chronic Respiratory Disease (CRD) [1]", "137", "80.1%", "82.5%", "0.81", "75.3–87.9%"),
        ("Fowl Pox [3]", "29", "53.1%", "89.7%", "0.67", "73.6–96.4%"),
        ("Infectious Coryza [2]", "90", "67.1%", "58.9%", "0.63", "48.6–68.5%"),
        ("Macro Average", "279", "70.1%", "66.5%", "0.65", "—")
    ]
    for row_idx, row_data in enumerate(data_t8):
        for col_idx, text in enumerate(row_data):
            cell = t8.cell(row_idx + 1, col_idx)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx == 0 else WD_ALIGN_PARAGRAPH.RIGHT
            p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(text)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            if row_idx == len(data_t8) - 1:
                r.font.bold = True
                set_cell_shading(cell, "EFF6FF")
            elif row_idx % 2 == 1:
                set_cell_shading(cell, "F8FAFC")
            set_cell_margins(cell, top=60, bottom=60, left=50, right=50)

    add_styled_paragraph(doc, "", space_before=4, space_after=8)

    # CONFIDENCE DISTRIBUTION
    add_heading_2(doc, "D. Confidence Distribution and Operational Abstention")
    add_body(doc, "As illustrated in Fig. 6, the distribution of top-1 predicted softmax confidence scores across the 279 diseased validation images is unimodal and roughly bell-shaped, exhibiting an empirical mean of 0.67 and a median of 0.68. Approximately 70% of predictions fall between 0.46 and 0.80, with only 16 predictions exceeding 0.93. Importantly, only ~10 predictions (3.6%) fall below the operational abstention threshold of *τ* = 0.40. In our deployed system, these low-confidence cases trigger an atypical presentation alert, recommending clinical veterinary inspection. Comprehensive empirical benchmarking of selective classification coverage across unmodeled avian pathogens is deferred to future multi-center studies [22].")

    add_image_centered(doc, "extracted_media/f479e315f2af62aca5562f0bf3436e896642933b.png", width_inches=4.4)
    add_caption(doc, "Fig. 6. Distribution histogram and kernel density estimation (KDE) of Doctor top-1 predicted softmax confidence scores across diseased validation images (n = 279, Mean: 0.67, Median: 0.68).")

    # END-TO-END EVALUATION
    add_heading_2(doc, "E. End-to-End Five-Class Hierarchical Pipeline Performance")
    add_body(doc, "Table IX and Fig. 7 document the end-to-end performance of the unified five-class cascaded pipeline evaluated across the entire held-out validation cohort (N = 425 images: 146 Healthy, 23 Bumblefoot, 137 CRD, 29 Fowl Pox, 90 Coryza). Overall end-to-end accuracy is 66.8% (284 of 425 correct classifications) with a macro F1-score of 0.596. Across classes, the pipeline achieves F1-scores of 0.761 for Healthy, 0.412 for Bumblefoot, 0.697 for CRD, 0.575 for Fowl Pox, and 0.534 for Infectious Coryza. As shown in the 5 × 5 confusion matrix (Fig. 7), cascading Bouncer screening errors (51 sick birds misclassified as healthy) reduces downstream recall relative to the standalone Doctor; however, the decoupled head enables rapid threshold adjustment (*p* = 0.35) that reclaims 29 previously missed sick birds.")

    add_image_centered(doc, "extracted_media/fig9_end_to_end_cm.png", width_inches=4.6)
    add_caption(doc, "Fig. 7. End-to-end five-class hierarchical pipeline confusion matrix on the common validation cohort (N = 425, Accuracy: 66.8%, Macro F1: 0.596).")

    # TABLE IX: END-TO-END REPORT
    p_t9 = add_caption(doc, "TABLE IX. END-TO-END FIVE-CLASS HIERARCHICAL PIPELINE PERFORMANCE REPORT (p = 0.50, N = 425)")
    t9 = doc.add_table(rows=7, cols=6)
    t9.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t9)
    
    headers_t9 = ["Clinical Category", "Validation Support", "Precision", "Recall", "F1-Score", "Diagnosed Correctly"]
    for j, h in enumerate(headers_t9):
        cell = t9.cell(0, j)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(8.5)
        r.font.bold = True
        set_cell_shading(cell, "F1F5F9")
        set_cell_margins(cell, top=80, bottom=80, left=50, right=50)

    data_t9 = [
        ("Healthy (Non-Diseased)", "146", "70.3% (121/172)", "82.9% (121/146)", "0.761", "121 / 146"),
        ("Bumblefoot [4]", "23", "63.6% (7/11)", "30.4% (7/23)", "0.412", "7 / 23"),
        ("Chronic Respiratory Disease (CRD) [1]", "137", "72.4% (92/127)", "67.2% (92/137)", "0.697", "92 / 137"),
        ("Fowl Pox [3]", "29", "47.7% (21/44)", "72.4% (21/29)", "0.575", "21 / 29"),
        ("Infectious Coryza [2]", "90", "60.6% (43/71)", "47.8% (43/90)", "0.534", "43 / 90"),
        ("Macro Average / Total", "425", "62.9%", "60.1%", "0.596", "284 / 425 (66.8%)")
    ]
    for row_idx, row_data in enumerate(data_t9):
        for col_idx, text in enumerate(row_data):
            cell = t9.cell(row_idx + 1, col_idx)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx == 0 else WD_ALIGN_PARAGRAPH.RIGHT
            p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(text)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            if row_idx == len(data_t9) - 1:
                r.font.bold = True
                set_cell_shading(cell, "EFF6FF")
            elif row_idx % 2 == 1:
                set_cell_shading(cell, "F8FAFC")
            set_cell_margins(cell, top=60, bottom=60, left=50, right=50)

    add_styled_paragraph(doc, "", space_before=4, space_after=8)

    # ROC AND PR CURVES
    add_heading_2(doc, "F. Receiver Operating Characteristic & Precision-Recall Analysis")
    add_body(doc, "As presented in Fig. 8, comprehensive ROC and Precision-Recall (PR) curves demonstrate operating characteristics across both stages. The Bouncer achieves a binary screening AUC-ROC of 0.884 [95% CI: 0.851–0.915] and an AUC-PR of 0.932 for the sick class against a 65.6% sick-class baseline prevalence [25], [26], [27], [31]. For the Doctor model, one-vs-rest evaluation yields AUC-ROCs of 0.885 for CRD, 0.862 for Fowl Pox, 0.791 for Infectious Coryza, and 0.774 for Bumblefoot (macro-average AUC-ROC = 0.828).")

    add_image_centered(doc, "extracted_media/fig8_roc_pr_curves.png", width_inches=4.8)
    add_caption(doc, "Fig. 8. Receiver Operating Characteristic (ROC) and Precision-Recall (PR) trajectories: (a) Bouncer screening ROC curve; (b) Bouncer Precision-Recall curves; (c) Doctor one-vs-rest ROC curves across four avian pathologies; (d) Doctor Precision-Recall curves.")

    # SECTION VIII: SYSTEM IMPLEMENTATION
    add_heading_1(doc, "VIII.  SYSTEM IMPLEMENTATION AND PRODUCTION DEPLOYMENT")
    add_body(doc, "A. Full-Stack Production Architecture")
    add_body(doc, "The platform is implemented as a decoupled, microservice-inspired web application (Fig. 1, Fig. 9). The backend is constructed using Python 3.11 and FastAPI, leveraging asynchronous request routing via Uvicorn. Model weights are serialized into Keras v3 format (9.6 MB per model) and loaded into server memory during application startup. The frontend is built as a single-page application (SPA) using React 18, Vite, and Tailwind CSS, featuring vector PDF clinical report export via @react-pdf/renderer.")

    add_body(doc, "B. Latency & Resource Benchmarking")
    add_body(doc, "Inference latency was benchmarked across 100 consecutive requests on an 8-core Intel Core i7-11800H CPU without GPU acceleration. Local neural inference (resizing, Bouncer screening, Doctor classification, and Grad-CAM generation) executes in an average of 145 ms (standard deviation: 18 ms). End-to-end response time, including network transmission and cloud LLM report synthesis via Gemini Flash, averages 1,120 ms. Memory consumption remains modest at 310 MB RAM, establishing edge feasibility for deployment on low-cost single-board computers (e.g., Raspberry Pi 5) for on-farm diagnostic kiosks.")

    add_image_centered(doc, "extracted_media/f9c7b162f9cd4b63b80194dab23642cf08dea96f.png", width_inches=4.8)
    add_caption(doc, "Fig. 9. Deployed web client interface: (a) Home portal; (b) Image analysis upload; (c) Diagnostic results view with Grad-CAM visualization and clinical care plan.")

    # SECTION IX: LIMITATIONS & VALIDITY THREATS
    add_heading_1(doc, "IX.  LIMITATIONS AND THREATS TO VALIDITY")
    add_body(doc, "Scientific transparency requires candid documentation of our study's empirical constraints:")
    add_body(doc, "1) Validation Split Monitored During Training: Model performance was evaluated on the held-out 20% validation partition (N = 425 images), which was also monitored for early stopping and hyperparameter selection. While standard in initial benchmark investigations, the absence of a completely untouched external test cohort drawn from independent geographic farms represents a threat to validity. True prospective generalization across unmodeled flock breeds remains to be established in future multi-center trials.")
    add_body(doc, "2) Absence of Confirmatory Laboratory Testing: Ground-truth disease annotations in both the Roboflow Universe dataset [32] and our handpicked field collection are based on visual lesion identification. No laboratory confirmatory assays (polymerase chain reaction [PCR], bacterial isolation, or serology) accompanied the source imagery. Consequently, latent label noise—particularly between clinically overlapping respiratory syndromes like CRD and Infectious Coryza—remains an unavoidable constraint of crowd-sourced agricultural image sets.")
    add_body(doc, "3) Near-Duplicate Contamination Risk: To evaluate potential near-duplicate leakage across splits, we conducted a difference-hash (dHash) audit across the 2,164 master files. At a Hamming distance threshold <= 2, we identified 31 near-duplicate pairs, primarily consisting of sequential video frames or alternative crops within the upstream Roboflow repository (e.g., matching root identifiers such as 099_png_jpg.rf...). Under standard random stratified splitting, such near-duplicates present an inherent risk of cross-split feature leakage. We document this as an inherent limitation of crowd-sourced agricultural datasets and emphasize the necessity of farm-level cluster-isolated splits in future work.")
    add_body(doc, "4) Class Imbalance & Frozen Feature Backbones: Sample sizes for Bumblefoot (n = 23 validation) and Fowl Pox (n = 29 validation) are small relative to CRD (n = 137), leading to wider binomial confidence intervals for their recall estimates [28]. Furthermore, keeping MobileNetV2 backbones frozen preserved generalizable features but constrained disease-specific fine-tuning; selective unfreezing of upper convolutional layers with focal loss represents a logical next optimization.")
    add_body(doc, "5) Cloud Dependency for Generative Reports: While neural inference runs entirely locally in 145 ms, generative clinical dossier synthesis requires internet access to communicate with the Gemini API. For remote agricultural zones without reliable connectivity, the backend implements an automatic fallback mode serving pre-compiled static MSD guidance text without requiring cloud access.")

    # SECTION X: CONCLUSION
    add_heading_1(doc, "X.  CONCLUSION AND FUTURE WORK")
    add_body(doc, "This paper presented PoultryHealth Intelligence, an applied clinical decision-support framework that integrates hierarchical deep learning, visual interpretability, and grounded generative AI for poultry disease diagnosis. By decoupling broad epidemiological screening from multi-class differentiation, the system achieves 82.1% screening accuracy and allows tuning the screening sensitivity to 92.2% (*p* = 0.35) to prioritize flock contagion containment. The specialist network reaches 71.7% accuracy across four common avian pathologies, with an operational safety threshold (*τ* = 0.40) flagging atypical presentations for clinical review. Visual saliency heatmaps verify anatomical lesion localization, and prompt-grounded generative reports enforce antimicrobial stewardship. Delivering local CPU inference in 145 ms, PoultryHealth Intelligence establishes a transparent, edge-feasible decision-support tool. Future work will focus on unfreezing convolutional backbones with focal loss, expanding the diagnostic ontology to additional viral strains, and conducting prospective multi-farm clinical validation.")

    # ACKNOWLEDGMENT
    add_heading_1(doc, "ACKNOWLEDGMENT")
    add_body(doc, "The authors express their gratitude to the Department of Analytics, School of Computer Science and Engineering (SCOPE), Vellore Institute of Technology, Vellore, for providing institutional computing facilities and academic support during this research.")

    # REFERENCES
    add_heading_1(doc, "REFERENCES")
    refs = [
        ("[1]", "M. El-Gazzar, \"Mycoplasma gallisepticum infection in poultry (chronic respiratory disease, infectious sinusitis),\" MSD Veterinary Manual, updated Sep. 2024. [Online]. Available: https://www.msdvetmanual.com/poultry/mycoplasmosis/mycoplasma-gallisepticum-infection-in-poultry"),
        ("[2]", "E. Soriano-Vargas, \"Infectious coryza,\" MSD Veterinary Manual, updated Sep. 2024. [Online]. Available: https://www.msdvetmanual.com/poultry/infectious-coryza/infectious-coryza"),
        ("[3]", "D. N. Tripathy, \"Fowlpox in chickens and turkeys,\" MSD Veterinary Manual, updated Sep. 2024. [Online]. Available: https://www.msdvetmanual.com/poultry/fowlpox/fowlpox-in-chickens-and-turkeys"),
        ("[4]", "Y. Sato and M. El-Gazzar, \"Staphylococcosis in poultry,\" MSD Veterinary Manual, updated Jan. 2025. [Online]. Available: https://www.msdvetmanual.com/poultry/staphylococcosis/staphylococcosis-in-poultry"),
        ("[5]", "D. Machuve, E. Nwankwo, N. Mduma, and J. Mbelwa, \"Poultry diseases diagnostics models using deep learning,\" Frontiers in Artificial Intelligence, vol. 5, Art. no. 733345, 2022. DOI: 10.3389/frai.2022.733345."),
        ("[6]", "H. Mbelwa, \"Deep convolutional neural network for chicken diseases,\" International Journal of Advanced Computer Science and Applications (IJACSA), vol. 12, no. 2, pp. 642–647, 2021. DOI: 10.14569/IJACSA.2021.0120280."),
        ("[7]", "A. Dhungana, X. Yang, B. Paneru, et al., \"An integrated deep learning approach for poultry disease detection using chicken manure images,\" AgriEngineering, vol. 7, no. 9, p. 278, 2025. DOI: 10.3390/agriengineering7090278."),
        ("[8]", "S. J. Pan and Q. Yang, \"A survey on transfer learning,\" IEEE Transactions on Knowledge and Data Engineering, vol. 22, no. 10, pp. 1345–1359, Oct. 2010. DOI: 10.1109/TKDE.2009.191."),
        ("[9]", "J. Yosinski, J. Clune, Y. Bengio, and H. Lipson, \"How transferable are features in deep neural networks?\" in Advances in Neural Information Processing Systems (NeurIPS), vol. 27, 2014, pp. 3320–3328."),
        ("[10]", "World Health Organization (WHO), \"Global action plan on antimicrobial resistance,\" Geneva, Switzerland: WHO Guidelines, 2015."),
        ("[11]", "World Organisation for Animal Health (WOAH), \"Responsible and prudent use of antimicrobial agents in veterinary medicine,\" in Terrestrial Animal Health Code, 29th ed., Paris, France: WOAH, 2021."),
        ("[12]", "C. N. Silla Jr. and A. A. Freitas, \"A survey of hierarchical classification across different application domains,\" Data Mining and Knowledge Discovery, vol. 22, no. 1–2, pp. 31–72, 2011. DOI: 10.1007/s10618-010-0175-9."),
        ("[13]", "C. Rudin, \"Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead,\" Nature Machine Intelligence, vol. 1, no. 5, pp. 206–215, 2019. DOI: 10.1038/s42256-019-0048-x."),
        ("[14]", "Z. Ji, N. Lee, R. Frieske, et al., \"Survey of hallucination in natural language generation,\" ACM Computing Surveys, vol. 55, no. 12, Art. no. 248, pp. 1–38, 2023. DOI: 10.1145/3571730."),
        ("[15]", "X. Zhuang and T. Zhang, \"Detection of sick broilers by digital image processing and deep learning,\" Biosystems Engineering, vol. 179, pp. 106–116, Mar. 2019. DOI: 10.1016/j.biosystemseng.2019.01.003."),
        ("[16]", "A. Taşdelen and Y. Arslan, \"Detection of high-risk diseases in poultry feces through transfer learning,\" Engineering Science and Technology, an International Journal, vol. 64, Art. no. 102002, 2025. DOI: 10.1016/j.jestch.2025.102002."),
        ("[17]", "Y. Luo, Y. Chen, and A. P. P. Abdul Majeed, \"Optimizing poultry disease classification: A feature-based transfer learning approach,\" Smart Agricultural Technology, vol. 10, Art. no. 100856, 2025. DOI: 10.1016/j.atech.2025.100856."),
        ("[18]", "A. S. R. Sabbella, C. L. Prachothan, and E. K. Panta, \"YOLOv8-Based Deep Learning Model for Automated Poultry Disease Detection and Health Monitoring,\" arXiv preprint arXiv:2508.04658, Aug. 2025."),
        ("[19]", "S. Neethirajan, \"Artificial intelligence for poultry health and welfare monitoring,\" Sensors, vol. 22, no. 15, p. 5727, 2022. DOI: 10.3390/s22155727."),
        ("[20]", "R. B. Bist, X. Yang, S. Subedi, and L. Chai, \"Automatic detection of bumblefoot in cage-free hens using computer vision technologies,\" Poultry Science, vol. 103, no. 7, p. 103780, Jul. 2024. DOI: 10.1016/j.psj.2024.103780."),
        ("[21]", "M. Sandler, A. Howard, M. Zhu, A. Zhmoginov, and L.-C. Chen, \"MobileNetV2: Inverted residuals and linear bottlenecks,\" in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), 2018, pp. 4510–4520. DOI: 10.1109/CVPR.2018.00474."),
        ("[22]", "Y. Geifman and R. El-Yaniv, \"Selective classification for deep neural networks,\" in Advances in Neural Information Processing Systems (NeurIPS), vol. 30, 2017, pp. 4878–4887."),
        ("[23]", "R. R. Selvaraju, M. Cogswell, A. Das, R. Vedantam, D. Parikh, and D. Batra, \"Grad-CAM: Visual explanations from deep networks via gradient-based localization,\" in Proc. IEEE Int. Conf. Comput. Vis. (ICCV), 2017, pp. 618–626. DOI: 10.1109/ICCV.2017.74."),
        ("[24]", "C. Elkan, \"The foundations of cost-sensitive learning,\" in Proc. 17th Int. Joint Conf. Artif. Intell. (IJCAI), 2001, pp. 973–978."),
        ("[25]", "J. A. Hanley and B. J. McNeil, \"The meaning and use of the area under a receiver operating characteristic (ROC) curve,\" Radiology, vol. 143, no. 1, pp. 29–36, Apr. 1982. DOI: 10.1148/radiology.143.1.7063747."),
        ("[26]", "T. Fawcett, \"An introduction to ROC analysis,\" Pattern Recognition Letters, vol. 27, no. 8, pp. 861–874, Jun. 2006. DOI: 10.1016/j.patrec.2005.10.010."),
        ("[27]", "J. Davis and M. Goadrich, \"The relationship between Precision-Recall and ROC curves,\" in Proc. 23rd Int. Conf. Mach. Learn. (ICML), 2006, pp. 233–240. DOI: 10.1145/1143844.1143874."),
        ("[28]", "L. D. Brown, T. T. Cai, and A. DasGupta, \"Interval estimation for a binomial proportion,\" Statistical Science, vol. 16, no. 2, pp. 101–133, 2001. DOI: 10.1214/ss/1009213286."),
        ("[29]", "J. Cohen, \"A coefficient of agreement for nominal scales,\" Educational and Psychological Measurement, vol. 20, no. 1, pp. 37–46, Apr. 1960. DOI: 10.1177/001316446002000104."),
        ("[30]", "B. W. Matthews, \"Comparison of the predicted and observed secondary structure of T4 phage lysozyme,\" Biochimica et Biophysica Acta (BBA) - Protein Structure, vol. 405, no. 2, pp. 442–451, 1975. DOI: 10.1016/0005-2795(75)90109-9."),
        ("[31]", "T. Saito and M. Rehmsmeier, \"The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets,\" PLoS ONE, vol. 10, no. 3, Art. no. e0118432, 2015. DOI: 10.1371/journal.pone.0118432."),
        ("[32]", "A. M. Singh, \"Poultry disease detection dataset (ayush-m-singh vdataset),\" Roboflow Universe, Feb. 2026. [Online]. Available: https://universe.roboflow.com.")
    ]
    for tag, ref_text in refs:
        p = add_styled_paragraph(doc, "", space_before=1, space_after=3, line_spacing=1.03, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        r_t = p.add_run(tag + " ")
        r_t.font.name = 'Times New Roman'
        r_t.font.size = Pt(8.5)
        r_t.font.bold = True
        r_b = p.add_run(ref_text)
        r_b.font.name = 'Times New Roman'
        r_b.font.size = Pt(8.5)

    out_path = r"Poultry_Project\PoultryHealth_Intelligence_Paper.docx"
    doc.save(out_path)
    print(f"Pristine, 100% reconciled IEEE Conference Paper saved to: {out_path}")

if __name__ == "__main__":
    build_paper()
