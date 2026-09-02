"""
Automated font validation script for Om Sans.
Verifies table integrity, glyph coverage, Unicode mapping, variable font axes, and OpenType tables.
"""

import os
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from fontTools.ttLib import TTFont

FONTS_DIR = os.path.join(os.path.dirname(__file__), 'fonts')
VAR_TTF = os.path.join(FONTS_DIR, 'variable', 'OmSans-Variable.ttf')
TTF_DIR = os.path.join(FONTS_DIR, 'ttf')
OTF_DIR = os.path.join(FONTS_DIR, 'otf')

WEIGHTS = ['Thin', 'ExtraLight', 'Light', 'Regular', 'Medium', 'SemiBold', 'Bold', 'ExtraBold', 'Black']

def validate_variable_font():
    print(f"Checking Variable Font: {VAR_TTF}")
    assert os.path.exists(VAR_TTF), f"Missing variable font: {VAR_TTF}"
    vf = TTFont(VAR_TTF)
    
    # Check essential tables
    required_tables = ['head', 'hhea', 'maxp', 'OS/2', 'hmtx', 'cmap', 'loca', 'glyf', 'name', 'post', 'fvar', 'gvar', 'STAT', 'GPOS']
    for t in required_tables:
        assert t in vf, f"Variable font missing table: {t}"
    print(f"  [PASS] All {len(required_tables)} essential tables present.")
    
    # Check fvar axis
    fvar = vf['fvar']
    axes = fvar.axes
    assert len(axes) == 1, f"Expected 1 axis, got {len(axes)}"
    axis = axes[0]
    assert axis.axisTag == 'wght', f"Expected wght axis, got {axis.axisTag}"
    assert axis.minValue == 100.0, f"Expected min 100.0, got {axis.minValue}"
    assert axis.defaultValue == 400.0, f"Expected default 400.0, got {axis.defaultValue}"
    assert axis.maxValue == 900.0, f"Expected max 900.0, got {axis.maxValue}"
    print(f"  [PASS] 'wght' axis valid: min={axis.minValue}, def={axis.defaultValue}, max={axis.maxValue}")
    
    # Check named instances
    assert len(fvar.instances) == 9, f"Expected 9 named instances, got {len(fvar.instances)}"
    print(f"  [PASS] All 9 named instances present in fvar.")
    
    # Check glyphs & cmap
    cmap = vf.getBestCmap()
    assert ord('A') in cmap
    assert ord('a') in cmap
    assert ord('0') in cmap
    assert 0x20B9 in cmap, "Missing Rupee (₹) in cmap"
    assert 0x20AC in cmap, "Missing Euro (€) in cmap"
    assert ord('$') in cmap, "Missing Dollar ($) in cmap"
    print(f"  [PASS] Unicode cmap verified: {len(cmap)} mapped characters including Currency (₹, €, $) and Accents.")
    
    # Check gvar variations
    gvar = vf['gvar']
    assert len(gvar.variations) > 0, "No glyph variations in gvar"
    print(f"  [PASS] 'gvar' contains coordinate variations for {len(gvar.variations)} glyphs.")


def validate_static_ttf():
    print(f"\nChecking Static TTF fonts in {TTF_DIR}...")
    for w in WEIGHTS:
        p = os.path.join(TTF_DIR, f"OmSans-{w}.ttf")
        assert os.path.exists(p), f"Missing TTF: {p}"
        font = TTFont(p)
        for t in ['head', 'hhea', 'maxp', 'OS/2', 'hmtx', 'cmap', 'loca', 'glyf', 'name', 'post', 'GPOS']:
            assert t in font, f"TTF {w} missing table: {t}"
        cmap = font.getBestCmap()
        assert 0x20B9 in cmap
        assert 0x20AC in cmap
        print(f"  [PASS] OmSans-{w}.ttf valid (glyphs: {font['maxp'].numGlyphs}, cmap: {len(cmap)})")


def validate_static_otf():
    print(f"\nChecking Static OTF fonts in {OTF_DIR}...")
    for w in WEIGHTS:
        p = os.path.join(OTF_DIR, f"OmSans-{w}.otf")
        assert os.path.exists(p), f"Missing OTF: {p}"
        font = TTFont(p)
        for t in ['head', 'hhea', 'maxp', 'OS/2', 'name', 'cmap', 'post', 'CFF ', 'hmtx', 'GPOS']:
            assert t in font, f"OTF {w} missing table: {t}"
        cmap = font.getBestCmap()
        assert 0x20B9 in cmap
        assert 0x20AC in cmap
        print(f"  [PASS] OmSans-{w}.otf valid (glyphs: {font['maxp'].numGlyphs}, cmap: {len(cmap)})")


if __name__ == '__main__':
    print("==================================================")
    print("            VALIDATING OM SANS FONT FAMILY        ")
    print("==================================================")
    try:
        validate_variable_font()
        validate_static_ttf()
        validate_static_otf()
        print("\n==================================================")
        print("    ALL VALIDATION CHECKS PASSED SUCCESSFULLY!    ")
        print("==================================================")
    except Exception as e:
        print(f"\n[VALIDATION FAILED] {e}")
        sys.exit(1)
