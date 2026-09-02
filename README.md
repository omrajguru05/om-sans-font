# Om Sans Variable

**Om Sans** is an original geometric sans-serif typeface I created featuring pure circular geometry, balanced optical weights, a generous x-height, and open apertures.

It is engineered to perform seamlessly as both a **display typeface** (commanding, balanced headlines in Bold and Black, refined elegance in Thin and Light) and a **body typeface** (comfortable reading texture, generous counters, and optical clarity in Regular and Medium).

---

## Background and Update

A while ago, I posted [this tweet on X](https://x.com/NotOmRajguru/status/2095193668454055936?s=20):

> *"Google just launched Gemini 3.8 Flash, so I gave it one job: create an entire variable font for me from scratch.*  
> *Will report back once it's done."*

### Update: Reporting Back

Here is the completed font family. **Om Sans Variable** is a fully functional, mathematically validated, production-ready typeface:
- **Variable Font** (`OmSans-Variable.ttf` and `OmSans[wght].ttf`) featuring a continuous weight axis from 100 (Thin) to 900 (Black).
- **9 Static TrueType Fonts (`.ttf`)** covering standard typographic weights.
- **9 Static OpenType Fonts (`.otf`)** with native Type 2 CFF cubic Bézier outlines for print design, Figma, and Adobe Creative Cloud.
- **Webfont Formats (`.woff2`)** for modern, high-performance web deployment.
- **OpenType Kerning (`GPOS`)** and custom-crafted glyphs including an Indian Rupee (`₹` U+20B9) designed specifically to match the font's geometric proportions.

---

## Author and Profiles

- **Personal Website**: [omrajguru.com](https://omrajguru.com)
- **Projects**: [projects.omrajguru.com](https://projects.omrajguru.com)
- **X (Twitter)**: [@NotOmRajguru](https://x.com/NotOmRajguru)

---

## Repository Structure

```
om-sans-font/
├── fonts/
│   ├── variable/
│   │   ├── OmSans-Variable.ttf       # Variable TrueType font (wght 100–900)
│   │   ├── OmSans[wght].ttf          # Google Fonts axis bracket naming
│   │   └── OmSans-Variable.woff2     # Compressed variable webfont
│   ├── ttf/                          # 9 Static TrueType font files
│   │   ├── OmSans-Thin.ttf           (Weight 100)
│   │   ├── OmSans-ExtraLight.ttf     (Weight 200)
│   │   ├── OmSans-Light.ttf          (Weight 300)
│   │   ├── OmSans-Regular.ttf        (Weight 400)
│   │   ├── OmSans-Medium.ttf         (Weight 500)
│   │   ├── OmSans-SemiBold.ttf       (Weight 600)
│   │   ├── OmSans-Bold.ttf           (Weight 700)
│   │   ├── OmSans-ExtraBold.ttf      (Weight 800)
│   │   └── OmSans-Black.ttf          (Weight 900)
│   ├── otf/                          # 9 Static OpenType CFF font files
│   │   ├── OmSans-Thin.otf
│   │   ├── OmSans-ExtraLight.otf
│   │   ├── OmSans-Light.otf
│   │   ├── OmSans-Regular.otf
│   │   ├── OmSans-Medium.otf
│   │   ├── OmSans-SemiBold.otf
│   │   ├── OmSans-Bold.otf
│   │   ├── OmSans-ExtraBold.otf
│   │   └── OmSans-Black.otf
│   └── woff2/                        # Static WOFF2 webfonts (all 9 weights)
├── src/                              # Base geometric font sources
│   └── base_geom.ttf                 # Base variable geometric font master
├── build_fonts.py                    # Font compilation pipeline
├── validate_fonts.py                 # Automated OpenType table validation suite
├── requirements.txt                  # Python dependencies (fonttools, brotli)
├── LICENSE                           # SIL Open Font License 1.1
└── README.md
```

---

## Typographic Specifications

| Parameter | Value | Details |
| :--- | :--- | :--- |
| **Units Per Em (UPM)** | 1000 | Standard high-resolution grid |
| **Cap Height** | 700 | Classic proportional height for capitals |
| **x-Height** | 520 | Tall, generous x-height for enhanced screen legibility |
| **Ascender** | 750 | Subtle rise above cap height |
| **Descender** | -250 | Deep enough for clear descenders ('g', 'j', 'p', 'q', 'y') |
| **Typo Line Gap** | 100 | Comfortable default line spacing |
| **Weight Axis** | 100 to 900 | Full continuous range from Thin (100) to Black (900) |
| **Character Count** | 416 glyphs | Full Latin Extended, diacritics, currency, punctuation, tabular figures |

---

## Design Characteristics

1. **Geometric Precision**:
   - Pure circular forms on 'O', 'o', and lining zero ('0').
   - Broad circular sweeps on 'C' and 'G' with generous apertures.
   - Modern 'G' crossbar meeting the vertical centerline cleanly without a bottom spur.
   - Single-story lowercase 'a' and single-story 'g'.
   - Circular dots (tittles) on 'i', 'j', exclamation, and question marks.
2. **Screen and Editorial Clarity**:
   - Generous 520-unit x-height ensuring crisp legibility down to 11px–14px body text.
   - Wide inner counters preventing blur across high-density and standard displays.
3. **Indian Rupee (`₹`) and Global Currencies**:
   - Custom-crafted Indian Rupee (`₹` U+20B9) matching the exact angle, curvature, and stem thickness of Om Sans.
   - Full currency set: Dollar (`$`), Euro (`€`), Rupee (`₹`), Pound (`£`), and Yen (`¥`).
4. **OpenType Kerning (`GPOS`)**:
   - Precision kerning pairs across uppercase, lowercase, numbers, and punctuation (`AV`, `AW`, `AT`, `Ta`, `To`, `Va`, `Vo`, `Wa`, `We`, `Yo`, etc.).

---

## Installation

### macOS (Recommended)
1. Open [`fonts/variable/`](fonts/variable/) or [`fonts/otf/`](fonts/otf/).
2. Double-click the font file (e.g. `OmSans-Variable.ttf` or any static `.otf` file).
3. In the preview window, click **Install Font**.
4. The font is registered in **Font Book** and immediately accessible across macOS applications (Figma, Sketch, Adobe Creative Cloud, Keynote, Pages, etc.).

### Windows
1. Open the [`fonts/ttf/`](fonts/ttf/) or [`fonts/variable/`](fonts/variable/) folder.
2. Select the font files, right-click, and choose **Install** or **Install for all users**.
3. Om Sans will immediately appear in your font menu across all applications.

### Linux
1. Copy the desired font files to `~/.local/share/fonts/` or `/usr/local/share/fonts/`.
2. Run `fc-cache -f -v` to refresh the font cache.

### Web CSS Usage
```css
@font-face {
  font-family: 'Om Sans Variable';
  src: url('/fonts/variable/OmSans-Variable.woff2') format('woff2-variations'),
       url('/fonts/variable/OmSans-Variable.ttf') format('truetype');
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
}

/* Body Text */
body {
  font-family: 'Om Sans Variable', -apple-system, sans-serif;
  font-variation-settings: 'wght' 400; /* Regular */
  font-size: 16px;
  line-height: 1.5;
}

/* Display Titles */
h1 {
  font-family: 'Om Sans Variable', -apple-system, sans-serif;
  font-variation-settings: 'wght' 800; /* ExtraBold */
  letter-spacing: -0.02em;
}
```

---

## Building and Validating From Source

Requirements: Python 3.10+ and `fonttools`.

```bash
# Set up virtual environment
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt

# Compile all font formats (Variable TTF, Static TTF, Static OTF, WOFF2)
.venv/Scripts/python build_fonts.py

# Run automated validation suite
.venv/Scripts/python validate_fonts.py
```

---

## License

This font family is released under the [SIL Open Font License, Version 1.1](LICENSE). You are free to use it in personal, commercial, digital, or print projects.