# Technical Documentation: PoultryHealth Intelligence

**Hierarchical Deep Learning and Grounded Generative AI for Poultry Disease Diagnosis**

*Authors: Ayush M Singh (23BDS0033), Venkata Sriram Topalli (23BE0441), Dr. Dega Nagaraju (Professor Grade 2)*  
*Vellore Institute of Technology (VIT), Vellore, India*

---

## 1. System Overview

**PoultryHealth Intelligence** is a dual-stage computer vision and grounded generative artificial intelligence decision-support platform designed for avian health screening and disease differentiation. The architecture decouples broad epidemiological sickness screening from fine-grained pathological categorization to address the asymmetric cost structure inherent in veterinary diagnostics: missing an actively shedding, highly contagious pathogen introduces severe epidemiological risk to commercial and smallholder flocks.

The platform integrates:
1. **Multimodal Input Gate (Gemini 2.5/3.8 Flash)**: Semantic out-of-distribution (OOD) filter verifying poultry anatomical presence before neural computation.
2. **Binary Screening Network ("The Bouncer")**: Lightweight MobileNetV2 classifier predicting binary sickness probability $p \in [0, 1]$.
3. **Multi-Class Disease Specialist ("The Doctor")**: MobileNetV2 classifier computing conditional probability distribution $\mathbf{q} \in \Delta^3$ across four major avian conditions: Bumblefoot (*Staphylococcus*), Chronic Respiratory Disease (CRD, *Mycoplasma gallisepticum*), Fowl Pox (Avipoxvirus), and Infectious Coryza (*Avibacterium paragallinarum*).
4. **Safety-First Soft Probability Fusion**: Unifies dual-stage outputs into a 5-class simplex with cost-sensitive threshold tuning ($p_{\text{thresh}} = 0.35$ for high-sensitivity triage).
5. **Operational Abstention Protocol**: Maximum Softmax Probability thresholding ($\tau_{\text{open}} = 0.40$) flagging atypical or low-confidence presentations for veterinary review.
6. **Pathological Explainability (Grad-CAM)**: Gradient-weighted class activation mapping targeting the penultimate `out_relu` convolutional feature maps.
7. **Grounded Clinical Report Generation**: Closed-world generative synthesis bounded strictly by an approved veterinary clinical knowledge base aligned with the MSD Veterinary Manual.
8. **Decoupled Production Stack**: High-throughput FastAPI backend with asynchronous request routing, paired with a modern React 18 single-page application and client-side vector PDF dossier rendering.

---

## 2. Repository & Monorepo Architecture

```
Poultry_Project/
├── Master dataset/
│   ├── Handpicked Data/          # 112 cleaned real-world field photographs
│   │   ├── Bumblefoot/           # 23 field images
│   │   ├── Foul Pox/             # 30 field images
│   │   ├── Healthy/              # 19 field images
│   │   ├── Infectious coryza/    # 30 field images
│   │   └── Others/               # 7 non-poultry distractor images (purged)
│   └── Roboflow Dataset/         # 2,031 benchmark images (CC BY 4.0)
│       └── train/                # Bumblefoot (92), coryza (440), crd (673), Fowlpox (114), Healthy (712)
├── Poultry UI And Backend/
│   ├── apps/
│   │   ├── api/                  # Express/Node API proxy layer
│   │   └── web/                  # React 18 + Vite + Tailwind CSS Single-Page Application
│   ├── Poultry_API/              # Core Machine Learning & Inference Microservice
│   │   ├── app.py                # FastAPI application & Grad-CAM pipeline
│   │   ├── poultry_bouncer_final.keras # Serialized Binary Screener (MobileNetV2, 9.6 MB)
│   │   ├── poultry_doctor_final.keras  # Serialized Multi-Class Specialist (MobileNetV2, 9.7 MB)
│   │   └── requirements.txt      # Python runtime dependencies
│   └── TECHNICAL_DOCUMENTATION.md# This comprehensive system specification
├── build_paper.py                # Fully automated script compiling pristine conference paper
├── PoultryHealth_Intelligence_Paper.docx # Reconciled publication-ready conference manuscript
└── PoultryHealth_Intelligence_Paper_ORIGINAL_BACKUP.docx # Preserved pristine backup
```

---

## 3. Mathematical Foundations

### 3.1. Hierarchical Probability Synthesis
Let $\mathbf{x} \in \mathbb{R}^{224 \times 224 \times 3}$ denote an input photograph.
1. The Bouncer outputs the marginal sickness probability:
   $$p = f_B(\mathbf{x}) = P(\text{Sick} \mid \mathbf{x}) \in [0, 1]$$
2. The Doctor outputs the conditional disease distribution:
   $$\mathbf{q} = f_D(\mathbf{x}) = \left[ q_1, q_2, q_3, q_4 \right]^T \in \Delta^3, \quad \sum_{k=1}^4 q_k = 1$$
   where $k \in \{1: \text{Bumblefoot}, 2: \text{CRD}, 3: \text{Fowl Pox}, 4: \text{Infectious Coryza}\}$.
3. Unified 5-class joint probability distribution across $\Omega = \{\text{Healthy}, \text{Bumblefoot}, \text{CRD}, \text{Fowl Pox}, \text{Coryza}\}$:
   $$P(\text{Healthy} \mid \mathbf{x}) = 1 - p$$
   $$P(\text{Disease}_k \mid \mathbf{x}) = p \cdot q_k, \quad \forall k \in \{1, 2, 3, 4\}$$

### 3.2. Cost-Sensitive Triage Formulation
Given misclassification costs $C_{\text{FN}} \gg C_{\text{FP}}$, the Bayesian optimal decision rule assigns $\mathbf{x}$ to the sick cohort if:
$$p \ge p_{\text{thresh}} = \frac{C_{\text{FP}}}{C_{\text{FP}} + C_{\text{FN}}}$$
Setting $p_{\text{thresh}} = 0.35$ reflects a cost ratio $C_{\text{FN}} / C_{\text{FP}} \approx 1.86$, prioritizing sensitivity to prevent contagion propagation.

### 3.3. Gradient-Weighted Class Activation Mapping (Grad-CAM)
Let $y^c$ denote the classification logit for class $c$, and $A^k$ the $k$-th feature map of penultimate layer `out_relu` ($7 \times 7 \times 1280$):
$$\alpha_k^c = \frac{1}{Z} \sum_{i=1}^7 \sum_{j=1}^7 \frac{\partial y^c}{\partial A_{i,j}^k}$$
$$L_{\text{Grad-CAM}}^c = \text{ReLU}\left( \sum_k \alpha_k^c A^k \right)$$

---

## 4. API Specification

### Endpoint: `/analyze`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Payload**: `image` or `file` (JPEG, PNG, WebP)
- **Header**: Optional `x-gemini-api-key` or configured server environment variable.
- **Response Format**: `application/json`
```json
{
  "status": "success",
  "system": "PoultryHealth Intelligence",
  "primary_diagnosis": "CRD",
  "confidence": 76.4,
  "distribution": {
    "Healthy": 7.2,
    "Bumblefoot": 1.4,
    "CRD": 76.4,
    "Fowl Pox": 3.8,
    "Infectious Coryza": 11.2
  },
  "open_set_alert": false,
  "report": "### 📊 DIAGNOSTIC BREAKDOWN\n...",
  "original_image_base64": "data:image/jpeg;base64,...",
  "heatmap_image_base64": "data:image/jpeg;base64,..."
}
```

---

## 5. Security & Responsible Veterinary Use Guidelines

1. **Non-Replacement Clause**: PoultryHealth Intelligence provides algorithmic triage and preliminary decision-support; it is not a replacement for microscopic pathology, bacterial culture, PCR confirmation, or licensed veterinary inspection.
2. **Closed-World Pharmacological Safety**: Prescriptive antibiotic therapy (e.g., tylosin, erythromycin) must strictly be confirmed and overseen by a licensed avian veterinarian.
3. **Zero-Storage Privacy**: Input images and biometric artifacts are processed strictly in-memory and base64-streamed; no farmer proprietary imagery is retained on disk without explicit consent.

---

## 6. Empirical Validation & Benchmark Metrics

### 6.1. Curated Benchmark Distribution
- **Raw Master Corpus**: 2,164 files (2,031 Roboflow Universe + 133 Handpicked).
- **Exclusions Purged**: 7 non-poultry distractor images (cars, cats, dogs in `Others`), 2 exact byte duplicates, and unreadable files = 18 excluded.
- **Cleaned Master Benchmark**: **2,143 images** (2,031 Roboflow Universe, 112 Handpicked).
- **Stratified 80/20 Partition**:
  - **Bouncer Dataset**: 1,718 training images (585 Healthy, 1,133 Sick), **425 validation images** (146 Healthy, 279 Sick).
  - **Doctor Dataset (Diseased only)**: 1,133 training images, **279 validation images** (23 Bumblefoot, 137 CRD, 29 Fowl Pox, 90 Coryza).
  - **Common Validation Cohort**: Exactly $N = 425$ images across all models (146 Healthy, 279 Diseased).

### 6.2. Screening Performance & Threshold Sensitivity (n = 425)
- **Default Threshold ($p = 0.50$)**:
  - Accuracy: **82.1%** (349/425; 95% CI: 78.1–85.5%)
  - Sick Recall (Sensitivity): **81.7%** (228/279)
  - Healthy Specificity: **82.9%** (121/146)
  - Sick Precision: **90.1%** (228/253)
  - Healthy Precision: **70.3%** (121/172)
  - Balanced Accuracy: **82.3%** | Macro F1: **0.81** | MCC: **0.62**
  - False Negatives: **51** missed sick birds
  - Screening AUC-ROC: **0.884** [95% CI: 0.851–0.915]
- **Cost-Sensitive Triage Threshold ($p = 0.35$)**:
  - Sick Recall surges to **92.2%** (261/279)
  - Healthy Specificity: **71.2%** (104/146)
  - Sick Precision: **86.1%** (261/303)
  - False Negatives slashed from 51 down to **22** (a 56.9% reduction in missed sick birds)
  - Youden's Index ($J$): **0.634**

### 6.3. Doctor Four-Class Disease Classification (n = 279)
- **Overall Accuracy**: **71.7%** (200/279; 95% CI: 66.1–76.6%)
- **Macro Average**: Precision **70.1%**, Recall **66.5%**, Macro F1 **0.65**, Cohen's $\kappa$ = **0.56**
- **Per-Class Metrics**:
  - *Bumblefoot* ($n=23$): Recall **34.8%** (8/23), Precision **80.0%** (8/10), F1 = **0.49**
  - *CRD* ($n=137$): Recall **82.5%** (113/137), Precision **80.1%** (113/141), F1 = **0.81** (Note: 20 CRD predicted as Coryza, matching Fig. 5)
  - *Fowl Pox* ($n=29$): Recall **89.7%** (26/29), Precision **53.1%** (26/49), F1 = **0.67**
  - *Infectious Coryza* ($n=90$): Recall **58.9%** (53/90), Precision **67.1%** (53/79), F1 = **0.63**

### 6.4. End-to-End Five-Class Hierarchical Performance (n = 425)
- **Overall Accuracy**: **66.8%** (284/425)
- **Macro F1-Score**: **0.596** (unweighted arithmetic mean of per-class F1s)
- **Per-Class Metrics**:
  - *Healthy*: Precision 70.3%, Recall 82.9%, F1 = **0.761**
  - *Bumblefoot*: Precision 63.6%, Recall 30.4%, F1 = **0.412**
  - *CRD*: Precision 72.4%, Recall 67.2%, F1 = **0.697**
  - *Fowl Pox*: Precision 47.7%, Recall 72.4%, F1 = **0.575**
  - *Infectious Coryza*: Precision 60.6%, Recall 47.8%, F1 = **0.534**
- **5x5 Confusion Matrix**:
  ```
               Predicted: Healthy  Bumblefoot  CRD  FowlPox  Coryza
  Actual Healthy:           121         2       11     5        7    (146)
  Actual Bumblefoot:          4         7        2     7        3    (23)
  Actual CRD:                25         0       92     3       17    (137)
  Actual Fowl Pox:            5         1        1    21        1    (29)
  Actual Coryza:             17         1       21     8       43    (90)
  ```

### 6.5. Operational Confidence & Abstention Safety
- **Confidence Distribution ($n=279$)**: Top-1 softmax confidence scores form a unimodal distribution with a mean of **0.67** and median of **0.68**. Approximately 70% of predictions fall between 0.46 and 0.80, with only 16 predictions exceeding 0.93.
- **Operational Safety Threshold ($\tau_{\text{abstain}} = 0.40$)**: Flags ~10 low-confidence predictions (3.6%) as atypical presentations requiring clinical veterinary consultation. Formal selective classification coverage evaluation is deferred to future work.
- **Clinical Stewardship Grounding**: Generative care reports strictly bounded by Table IV guidelines derived from the MSD Veterinary Manual, adhering to WHO/WOAH antimicrobial stewardship (no unguided antibiotic prescriptions; mandatory veterinary consultation).

### 6.6. Leakage & Near-Duplicate Audit
- **MD5 Byte Audit**: Identified 2 exact duplicate pairs bridging datasets, purged during preprocessing.
- **dHash Perceptual Audit**: Evaluated difference hashes across all 2,164 files. Identified 31 near-duplicate pairs (Hamming distance $\le 2$) originating from sequential video frames within the upstream Roboflow repository. Documented as an acknowledged threat to validity in Section IX.
