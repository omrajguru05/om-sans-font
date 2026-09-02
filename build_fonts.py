"""
Build script for Om Sans Variable and complete static TTF & OTF family.
Compiles:
  - Variable TTF with wght axis (100 to 900): OmSans-Variable.ttf and OmSans[wght].ttf
  - 9 Static TTF fonts: OmSans-Thin.ttf through OmSans-Black.ttf
  - 9 Static OTF fonts: OmSans-Thin.otf through OmSans-Black.otf
  - WOFF2 web fonts: OmSans-Variable.woff2 and static woff2 files
"""

import os
import shutil
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.designspaceLib import DesignSpaceDocument, AxisDescriptor, SourceDescriptor, InstanceDescriptor
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.ttLib import TTFont
from fontTools.misc.timeTools import timestampNow
import fontTools.varLib as varLib

from src.glyphs_builder import build_all_glyphs
from src.features import generate_fea

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
FONTS_DIR = os.path.join(BASE_DIR, 'fonts')
FONTS_VAR = os.path.join(FONTS_DIR, 'variable')
FONTS_TTF = os.path.join(FONTS_DIR, 'ttf')
FONTS_OTF = os.path.join(FONTS_DIR, 'otf')
FONTS_WOFF2 = os.path.join(FONTS_DIR, 'woff2')
MASTERS_DIR = os.path.join(BASE_DIR, '.masters_build')


def ensure_dirs():
    for d in [FONTS_VAR, FONTS_TTF, FONTS_OTF, FONTS_WOFF2, MASTERS_DIR]:
        os.makedirs(d, exist_ok=True)


def safe_save(font_obj, out_path):
    """Safely save a font, retrying if Windows/OneDrive temporarily locks the file."""
    import time
    for attempt in range(6):
        try:
            if os.path.exists(out_path):
                try:
                    os.remove(out_path)
                except OSError:
                    pass
            font_obj.save(out_path)
            return out_path
        except OSError:
            time.sleep(0.4)
    tmp_path = out_path + ".tmp"
    font_obj.save(tmp_path)
    shutil.move(tmp_path, out_path)
    return out_path


def build_single_ttf(weight, style_name, out_path, is_master=False):
    """Build a static TrueType (.ttf) font file."""
    glyphs_dict = build_all_glyphs(weight)
    glyph_order = ['.notdef', 'space'] + [k for k in glyphs_dict.keys() if k not in ('.notdef', 'space')]
    
    fb = FontBuilder(unitsPerEm=1000, isTTF=True)
    fb.setupGlyphOrder(glyph_order)
    
    # Character map
    cmap = {}
    for name, spec in glyphs_dict.items():
        if spec.unicode_val is not None:
            cmap[spec.unicode_val] = name
    fb.setupCharacterMap(cmap)
    
    # Glyphs & Horizontal Metrics
    tt_glyphs = {}
    h_metrics = {}
    for name in glyph_order:
        spec = glyphs_dict[name]
        pen = TTGlyphPen(None)
        for p in spec.paths:
            p.draw_to_tt_pen(pen)
        tt_glyphs[name] = pen.glyph()
        h_metrics[name] = (spec.advance_width, spec.lsb)
        
    fb.setupGlyf(tt_glyphs)
    fb.setupHorizontalMetrics(h_metrics)
    fb.setupHorizontalHeader(ascent=900, descent=-250, lineGap=100)
    
    is_bold = (weight >= 700)
    fs_selection = 0x0020 if is_bold else 0x0040
    mac_style = 0x01 if is_bold else 0x00
    now = timestampNow()
    fb.setupHead(macStyle=mac_style, created=now, modified=now)
    fb.setupOS2(
        sTypoAscender=750,
        sTypoDescender=-250,
        sTypoLineGap=100,
        usWinAscent=900,
        usWinDescent=250,
        sxHeight=520,
        sCapHeight=700,
        usWeightClass=weight,
        fsSelection=fs_selection
    )
    
    # OpenType names
    ps_name = f"OmSans-{style_name}"
    full_name = f"Om Sans {style_name}"
    
    if style_name in ('Regular', 'Bold'):
        family_name = "Om Sans"
        subfamily_name = style_name
    else:
        family_name = f"Om Sans {style_name}"
        subfamily_name = "Regular"
        
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
    
    # Add GPOS kerning features
    try:
        fea = generate_fea()
        addOpenTypeFeaturesFromString(fb.font, fea)
    except Exception as e:
        print(f"  [Warning] Feature compilation note for {style_name}: {e}")
        
    safe_save(fb, out_path)
    return out_path


def build_single_otf(weight, style_name, out_path):
    """Build a static OpenType-CFF (.otf) font file."""
    glyphs_dict = build_all_glyphs(weight)
    glyph_order = ['.notdef', 'space'] + [k for k in glyphs_dict.keys() if k not in ('.notdef', 'space')]
    
    fb = FontBuilder(unitsPerEm=1000, isTTF=False)
    fb.setupGlyphOrder(glyph_order)
    
    # Character map
    cmap = {}
    for name, spec in glyphs_dict.items():
        if spec.unicode_val is not None:
            cmap[spec.unicode_val] = name
    fb.setupCharacterMap(cmap)
    
    # CFF CharStrings & Horizontal Metrics
    charstrings = {}
    h_metrics = {}
    for name in glyph_order:
        spec = glyphs_dict[name]
        t2pen = T2CharStringPen(spec.advance_width, None)
        for p in spec.paths:
            p.draw_to_t2_pen(t2pen)
        charstrings[name] = t2pen.getCharString()
        h_metrics[name] = (spec.advance_width, spec.lsb)
        
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
    fb.setupHorizontalMetrics(h_metrics)
    fb.setupHorizontalHeader(ascent=900, descent=-250, lineGap=100)
    
    is_bold = (weight >= 700)
    fs_selection = 0x0020 if is_bold else 0x0040
    mac_style = 0x01 if is_bold else 0x00
    now = timestampNow()
    fb.setupHead(macStyle=mac_style, created=now, modified=now)
    fb.setupOS2(
        sTypoAscender=750,
        sTypoDescender=-250,
        sTypoLineGap=100,
        usWinAscent=900,
        usWinDescent=250,
        sxHeight=520,
        sCapHeight=700,
        usWeightClass=weight,
        fsSelection=fs_selection
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
    
    try:
        fea = generate_fea()
        addOpenTypeFeaturesFromString(fb.font, fea)
    except Exception as e:
        print(f"  [Warning] Feature compilation note for {style_name}: {e}")
        
    safe_save(fb, out_path)
    return out_path


def build_variable_font(master_paths, out_path):
    """Build the variable TTF with full weight axis (100-900) using varLib."""
    doc = DesignSpaceDocument()
    
    axis = AxisDescriptor()
    axis.name = "Weight"
    axis.tag = "wght"
    axis.minimum = 100
    axis.default = 400
    axis.maximum = 900
    doc.addAxis(axis)
    
    for weight, path in master_paths.items():
        s = SourceDescriptor()
        s.path = path
        s.location = {"Weight": weight}
        doc.addSource(s)
        
    for weight, style_name in WEIGHTS:
        inst = InstanceDescriptor()
        inst.name = f"Om Sans {style_name}"
        inst.styleName = style_name
        inst.location = {"Weight": weight}
        doc.addInstance(inst)
        
    ds_path = os.path.join(MASTERS_DIR, "OmSans.designspace")
    doc.write(ds_path)
    
    vf, _, _ = varLib.build(ds_path)
    
    # Update Variable Font Name Table
    name_table = vf['name']
    name_table.setName("Om Sans Variable", 1, 3, 1, 0x409)
    name_table.setName("Regular", 2, 3, 1, 0x409)
    name_table.setName("1.000;OMSF;OmSans-Variable", 3, 3, 1, 0x409)
    name_table.setName("Om Sans Variable", 4, 3, 1, 0x409)
    name_table.setName("Version 1.000", 5, 3, 1, 0x409)
    name_table.setName("OmSans-Variable", 6, 3, 1, 0x409)
    name_table.setName("Om Rajguru", 9, 3, 1, 0x409)
    name_table.setName("Om Sans", 16, 3, 1, 0x409)
    name_table.setName("Regular", 17, 3, 1, 0x409)
    name_table.setName("https://omrajguru.com", 11, 3, 1, 0x409)
    name_table.setName("https://x.com/NotOmRajguru", 12, 3, 1, 0x409)
    
    # Add GPOS kerning
    try:
        fea = generate_fea()
        addOpenTypeFeaturesFromString(vf, fea)
    except Exception as e:
        print(f"  [Warning] Variable font feature compilation: {e}")
        
    safe_save(vf, out_path)
    return out_path


def make_woff2(font_path, out_path):
    """Convert any TTF/OTF font to compressed WOFF2 format."""
    font = TTFont(font_path)
    font.flavor = "woff2"
    safe_save(font, out_path)
    return out_path


def main():
    print("=========================================================")
    print("         BUILDING OM SANS VARIABLE & STATIC FONTS        ")
    print("=========================================================")
    ensure_dirs()
    
    # Step 1: Build masters (100, 400, 900)
    print("\n[1/5] Building interpolation masters (Thin 100, Regular 400, Black 900)...")
    master_paths = {}
    for weight, name in [(100, 'Thin'), (400, 'Regular'), (900, 'Black')]:
        p = os.path.join(MASTERS_DIR, f"master_{weight}.ttf")
        build_single_ttf(weight, name, p, is_master=True)
        master_paths[weight] = p
        print(f"  -> Master {weight} ({name}) generated.")
        
    # Step 2: Build Variable Font
    print("\n[2/5] Compiling Om Sans Variable TrueType Font (wght 100-900)...")
    var_ttf_path = os.path.join(FONTS_VAR, "OmSans-Variable.ttf")
    build_variable_font(master_paths, var_ttf_path)
    print(f"  -> Generated: {var_ttf_path}")
    
    # Also save with Google Fonts axis bracket convention OmSans[wght].ttf
    var_bracket_path = os.path.join(FONTS_VAR, "OmSans[wght].ttf")
    shutil.copy2(var_ttf_path, var_bracket_path)
    print(f"  -> Generated: {var_bracket_path}")
    
    # Generate Variable WOFF2
    var_woff2_path = os.path.join(FONTS_VAR, "OmSans-Variable.woff2")
    make_woff2(var_ttf_path, var_woff2_path)
    print(f"  -> Generated: {var_woff2_path}")
    
    # Step 3: Build 9 Static TTF files
    print("\n[3/5] Building all 9 Static TTF fonts...")
    for weight, name in WEIGHTS:
        ttf_path = os.path.join(FONTS_TTF, f"OmSans-{name}.ttf")
        build_single_ttf(weight, name, ttf_path)
        print(f"  -> TTF: OmSans-{name}.ttf (Weight {weight})")
        
    # Step 4: Build 9 Static OTF files
    print("\n[4/5] Building all 9 Static OTF (CFF) fonts...")
    for weight, name in WEIGHTS:
        otf_path = os.path.join(FONTS_OTF, f"OmSans-{name}.otf")
        build_single_otf(weight, name, otf_path)
        print(f"  -> OTF: OmSans-{name}.otf (Weight {weight})")
        
    # Step 5: Webfont generation (WOFF2)
    print("\n[5/5] Generating WOFF2 webfonts...")
    for weight, name in WEIGHTS:
        src_ttf = os.path.join(FONTS_TTF, f"OmSans-{name}.ttf")
        dest_woff2 = os.path.join(FONTS_WOFF2, f"OmSans-{name}.woff2")
        make_woff2(src_ttf, dest_woff2)
        
    # Clean up temporary masters build directory
    shutil.rmtree(MASTERS_DIR, ignore_errors=True)
        
    print("\n=========================================================")
    print("           OM SANS FONT GENERATION COMPLETE!             ")
    print("=========================================================")
    print(f"Variable Fonts : {FONTS_VAR}")
    print(f"Static TTF (9) : {FONTS_TTF}")
    print(f"Static OTF (9) : {FONTS_OTF}")
    print(f"Webfonts WOFF2 : {FONTS_WOFF2}")


if __name__ == "__main__":
    main()
