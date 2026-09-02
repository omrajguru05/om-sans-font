"""
Build script for Om Sans Variable and complete static TTF, OTF & WOFF2 family.
Compiles:
  - Variable TTF with wght axis (100 to 900): OmSans-Variable.ttf and OmSans[wght].ttf
  - Variable WOFF2: OmSans-Variable.woff2
  - 9 Static TTF fonts: OmSans-Thin.ttf through OmSans-Black.ttf
  - 9 Static OTF (CFF) fonts: OmSans-Thin.otf through OmSans-Black.otf
  - 9 Static WOFF2 web fonts: OmSans-Thin.woff2 through OmSans-Black.woff2
"""

import os
import shutil
import time
from fontTools.ttLib import TTFont
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.varLib.instancer import instantiateVariableFont, OverlapMode
from fontTools.misc.timeTools import timestampNow

WEIGHTS = [
    (100, 'Thin'),
    (200, 'ExtraLight'),
    (300, 'Light'),
    (400, 'Regular'),
    (500, 'Medium'),
    (600, 'SemiBold'),
    (700, 'Bold'),
    (800, 'ExtraBold'),
    (900, 'Black'),
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_BASE_TTF = os.path.join(BASE_DIR, 'src', 'base_geom.ttf')
FONTS_DIR = os.path.join(BASE_DIR, 'fonts')
FONTS_VAR = os.path.join(FONTS_DIR, 'variable')
FONTS_TTF = os.path.join(FONTS_DIR, 'ttf')
FONTS_OTF = os.path.join(FONTS_DIR, 'otf')
FONTS_WOFF2 = os.path.join(FONTS_DIR, 'woff2')


def ensure_dirs():
    """Ensure all export directories exist."""
    for d in (FONTS_VAR, FONTS_TTF, FONTS_OTF, FONTS_WOFF2):
        os.makedirs(d, exist_ok=True)


def safe_save(font_obj, out_path):
    """Safely save font, handling Windows file locking."""
    for _ in range(5):
        try:
            font_obj.save(out_path)
            return out_path
        except OSError:
            time.sleep(0.3)
    tmp_path = out_path + ".tmp"
    font_obj.save(tmp_path)
    shutil.move(tmp_path, out_path)
    return out_path


def set_overlap_flags(font):
    """
    Set OVERLAP_SIMPLE flag (0x0040) on all simple TrueType glyphs.
    Ensures DirectWrite and Windows GDI render contours with non-zero winding rule.
    """
    if 'glyf' in font:
        glyf = font['glyf']
        for name in font.getGlyphOrder():
            g = glyf[name]
            if g.numberOfContours > 0 and hasattr(g, 'flags'):
                g.flags = [flag | 0x0040 for flag in g.flags]


def make_woff2(font_path, out_path):
    """Convert font to compressed WOFF2 webfont."""
    font = TTFont(font_path)
    font.flavor = "woff2"
    safe_save(font, out_path)
    return out_path


def build_variable_font():
    """Build Om Sans Variable font with updated metadata and non-zero overlap flags."""
    vf = TTFont(SRC_BASE_TTF)
    name_table = vf['name']
    name_table.names = []

    records = [
        (0, "Copyright 2026 The Om Sans Project Authors (https://omrajguru.com)"),
        (1, "Om Sans Variable"),
        (2, "Regular"),
        (3, "1.000;OMSF;OmSans-Variable"),
        (4, "Om Sans Variable"),
        (5, "Version 1.000"),
        (6, "OmSans-Variable"),
        (8, "Om Rajguru"),
        (9, "Om Rajguru"),
        (11, "https://omrajguru.com"),
        (12, "https://x.com/NotOmRajguru"),
        (13, "This Font Software is licensed under the SIL Open Font License, Version 1.1."),
        (14, "https://scripts.sil.org/OFL"),
        (16, "Om Sans"),
        (17, "Regular"),
        (25, "Om Sans"),
    ]
    for n_id, s in records:
        name_table.setName(s, n_id, 3, 1, 0x409)
        name_table.setName(s, n_id, 1, 0, 0)

    # Ensure Indian Rupee (₹) is in cmap
    for table in vf['cmap'].tables:
        if table.isUnicode():
            table.cmap[0x20B9] = table.cmap.get(0xA4, 'currency')

    set_overlap_flags(vf)

    var_ttf_path = os.path.join(FONTS_VAR, "OmSans-Variable.ttf")
    safe_save(vf, var_ttf_path)

    var_bracket_path = os.path.join(FONTS_VAR, "OmSans[wght].ttf")
    shutil.copy2(var_ttf_path, var_bracket_path)

    var_woff2_path = os.path.join(FONTS_VAR, "OmSans-Variable.woff2")
    make_woff2(var_ttf_path, var_woff2_path)

    return var_ttf_path


def build_static_ttf(base_vf, weight, style_name):
    """Instantiate static TrueType font with pristine non-overlapping geometry."""
    inst = instantiateVariableFont(base_vf, {'wght': weight}, overlap=OverlapMode.KEEP_AND_SET_FLAGS)
    # Ensure Indian Rupee (₹) is in cmap
    for table in inst['cmap'].tables:
        if table.isUnicode():
            table.cmap[0x20B9] = table.cmap.get(0xA4, 'currency')

    set_overlap_flags(inst)

    ps_name = f"OmSans-{style_name}"
    full_name = f"Om Sans {style_name}"

    if style_name in ('Regular', 'Bold'):
        family_name = "Om Sans"
        subfamily_name = style_name
    else:
        family_name = f"Om Sans {style_name}"
        subfamily_name = "Regular"

    name_table = inst['name']
    name_table.names = []
    records = [
        (0, "Copyright 2026 The Om Sans Project Authors (https://omrajguru.com)"),
        (1, family_name),
        (2, subfamily_name),
        (3, f"1.000;OMSF;{ps_name}"),
        (4, full_name),
        (5, "Version 1.000"),
        (6, ps_name),
        (8, "Om Rajguru"),
        (9, "Om Rajguru"),
        (11, "https://omrajguru.com"),
        (12, "https://x.com/NotOmRajguru"),
        (13, "This Font Software is licensed under the SIL Open Font License, Version 1.1."),
        (14, "https://scripts.sil.org/OFL"),
        (16, "Om Sans"),
        (17, style_name),
    ]
    for n_id, s in records:
        name_table.setName(s, n_id, 3, 1, 0x409)
        name_table.setName(s, n_id, 1, 0, 0)

    out_path = os.path.join(FONTS_TTF, f"OmSans-{style_name}.ttf")
    safe_save(inst, out_path)
    return inst, out_path


def build_static_otf(inst_ttf, weight, style_name):
    """Build static OpenType-CFF (.otf) font from instantiated TTF."""
    glyph_order = inst_ttf.getGlyphOrder()
    glyph_set = inst_ttf.getGlyphSet()

    fb = FontBuilder(unitsPerEm=inst_ttf['head'].unitsPerEm, isTTF=False)
    fb.setupGlyphOrder(glyph_order)
    fb.setupCharacterMap(inst_ttf.getBestCmap())

    charstrings = {}
    for name in glyph_order:
        g = glyph_set[name]
        pen = T2CharStringPen(g.width, glyph_set)
        g.draw(pen)
        charstrings[name] = pen.getCharString()

    hmtx = {}
    for name in glyph_order:
        hmtx[name] = inst_ttf['hmtx'][name]

    ps_name = f"OmSans-{style_name}"
    full_name = f"Om Sans {style_name}"
    if style_name in ('Regular', 'Bold'):
        family_name = "Om Sans"
        subfamily_name = style_name
    else:
        family_name = f"Om Sans {style_name}"
        subfamily_name = "Regular"

    cff_info = {
        'FullName': full_name,
        'FamilyName': 'Om Sans',
        'Weight': style_name
    }
    fb.setupCFF(ps_name, cff_info, charstrings, {})
    fb.setupHorizontalMetrics(hmtx)
    fb.setupHorizontalHeader(
        ascent=inst_ttf['hhea'].ascent,
        descent=inst_ttf['hhea'].descent,
        lineGap=inst_ttf['hhea'].lineGap
    )

    is_bold = (weight >= 700)
    mac_style = 0x01 if is_bold else 0x00
    now = timestampNow()
    fb.setupHead(macStyle=mac_style, created=now, modified=now)

    os2 = inst_ttf['OS/2']
    fb.setupOS2(
        sTypoAscender=os2.sTypoAscender,
        sTypoDescender=os2.sTypoDescender,
        sTypoLineGap=os2.sTypoLineGap,
        usWinAscent=os2.usWinAscent,
        usWinDescent=os2.usWinDescent,
        sxHeight=os2.sxHeight,
        sCapHeight=os2.sCapHeight,
        usWeightClass=weight,
        fsSelection=os2.fsSelection
    )

    name_strings = {
        'familyName': family_name,
        'styleName': subfamily_name,
        'uniqueFontIdentifier': f"1.000;OMSF;{ps_name}",
        'fullName': full_name,
        'version': "Version 1.000",
        'psName': ps_name,
        'typographicFamily': "Om Sans",
        'typographicSubfamily': style_name,
        'designer': "Om Rajguru",
        'manufacturer': "Om Rajguru",
        'licenseDescription': "SIL Open Font License, Version 1.1",
        'vendorURL': "https://omrajguru.com",
        'designerURL': "https://x.com/NotOmRajguru"
    }
    fb.setupNameTable(name_strings)
    fb.setupPost()

    if 'GSUB' in inst_ttf:
        fb.font['GSUB'] = inst_ttf['GSUB']
    if 'GPOS' in inst_ttf:
        fb.font['GPOS'] = inst_ttf['GPOS']

    out_path = os.path.join(FONTS_OTF, f"OmSans-{style_name}.otf")
    safe_save(fb, out_path)
    return out_path


def main():
    print("=========================================================")
    print("         BUILDING OM SANS VARIABLE & STATIC FONTS        ")
    print("=========================================================")
    ensure_dirs()

    # Step 1: Build Variable Fonts
    print("\n[1/4] Compiling Om Sans Variable TrueType Font (wght 100-900)...")
    build_variable_font()
    print("  -> Generated OmSans-Variable.ttf, OmSans[wght].ttf, OmSans-Variable.woff2")

    # Step 2: Build Static TTF, OTF, and WOFF2 fonts
    base_vf = TTFont(SRC_BASE_TTF)
    print("\n[2/4] Building all 9 Static TTF fonts...")
    instantiated_fonts = {}
    for weight, name in WEIGHTS:
        inst_ttf, path = build_static_ttf(base_vf, weight, name)
        instantiated_fonts[name] = inst_ttf
        print(f"  -> TTF: OmSans-{name}.ttf (Weight {weight})")

    print("\n[3/4] Building all 9 Static OTF (CFF) fonts...")
    for weight, name in WEIGHTS:
        inst_ttf = instantiated_fonts[name]
        build_static_otf(inst_ttf, weight, name)
        print(f"  -> OTF: OmSans-{name}.otf (Weight {weight})")

    print("\n[4/4] Generating WOFF2 webfonts...")
    for weight, name in WEIGHTS:
        src_ttf = os.path.join(FONTS_TTF, f"OmSans-{name}.ttf")
        dest_woff2 = os.path.join(FONTS_WOFF2, f"OmSans-{name}.woff2")
        make_woff2(src_ttf, dest_woff2)
        print(f"  -> WOFF2: OmSans-{name}.woff2")

    print("\n=========================================================")
    print("           OM SANS FONT GENERATION COMPLETE!             ")
    print("=========================================================")
    print(f"Variable Fonts : {FONTS_VAR}")
    print(f"Static TTF (9) : {FONTS_TTF}")
    print(f"Static OTF (9) : {FONTS_OTF}")
    print(f"Webfonts WOFF2 : {FONTS_WOFF2}")


if __name__ == "__main__":
    main()
