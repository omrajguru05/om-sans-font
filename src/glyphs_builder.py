"""
Glyphs builder for Om Sans.
Defines parametric glyph geometry for weights 100 to 900.
Strictly preserves contour count and point sequence across weights for seamless variable interpolation.
"""

import math
from src.path_utils import Path, GlyphSpec

def get_metrics_for_weight(weight):
    """
    Compute typographic dimensions for a given weight (100 to 900).
    UPM = 1000, CapHeight = 700, xHeight = 520, Ascender = 750, Descender = -200.
    """
    # Stem thickness calibration:
    # 100: 24 (Thin)
    # 400: 84 (Regular)
    # 900: 224 (Black)
    if weight <= 400:
        t = (weight - 100) / 300.0
        stem = 24.0 + t * (84.0 - 24.0)
    else:
        t = (weight - 400) / 500.0
        stem = 84.0 + t * (224.0 - 84.0)
        
    stem_h = stem * 0.90 # horizontal stems slightly lighter for optical balance
    overshoot = 12.0 + (stem - 24.0) * 0.05
    
    return {
        'weight': weight,
        'stem': stem,
        'stem_h': stem_h,
        'cap_h': 700.0,
        'x_h': 520.0,
        'asc': 750.0,
        'desc': -200.0,
        'ov': overshoot,
        'lsb_cap': max(45.0, 75.0 - stem * 0.12),
        'lsb_low': max(40.0, 68.0 - stem * 0.12)
    }


def build_all_glyphs(weight):
    """
    Build all GlyphSpec objects for the given weight.
    Returns a dictionary mapping glyph_name -> GlyphSpec.
    """
    m = get_metrics_for_weight(weight)
    stem = m['stem']
    stem_h = m['stem_h']
    cap_h = m['cap_h']
    x_h = m['x_h']
    asc = m['asc']
    desc = m['desc']
    ov = m['ov']
    
    glyphs = {}

    def add_glyph(spec):
        glyphs[spec.name] = spec
        return spec

    # -------------------------------------------------------------
    # .notdef
    # -------------------------------------------------------------
    p_notdef = Path()
    w_notdef = 500.0
    p_notdef.rect(60.0, 0.0, w_notdef - 120.0, cap_h)
    p_notdef.rect(60.0 + stem, stem, w_notdef - 120.0 - 2*stem, cap_h - 2*stem)
    add_glyph(GlyphSpec('.notdef', None, w_notdef, 60.0, [p_notdef]))

    # -------------------------------------------------------------
    # space
    # -------------------------------------------------------------
    w_space = 280.0 + stem * 0.2
    add_glyph(GlyphSpec('space', 0x0020, w_space, 0.0, [Path()]))

    # -------------------------------------------------------------
    # UPPERCASE A-Z
    # -------------------------------------------------------------
    
    # --- A ---
    w_A = 680.0 + stem * 0.5
    lsb_A = 50.0
    rsb_A = w_A - 50.0
    cx_A = w_A / 2.0
    y_bar_top = 270.0
    y_bar_bot = y_bar_top - stem_h
    
    p_A_out = Path()
    # Outer contour
    p_A_out.move_to(lsb_A, 0.0)
    p_A_out.line_to(cx_A - stem * 0.3, cap_h)
    p_A_out.line_to(cx_A + stem * 0.3, cap_h)
    p_A_out.line_to(rsb_A, 0.0)
    p_A_out.line_to(rsb_A - stem * 1.1, 0.0)
    # Right inner diagonal up to bar bottom
    t_r_bot = y_bar_bot / cap_h
    xr_bot = (rsb_A - stem * 1.1) + t_r_bot * (cx_A - (rsb_A - stem * 1.1))
    p_A_out.line_to(xr_bot, y_bar_bot)
    # Crossbar bottom
    t_l_bot = y_bar_bot / cap_h
    xl_bot = (lsb_A + stem * 1.1) + t_l_bot * (cx_A - (lsb_A + stem * 1.1))
    p_A_out.line_to(xl_bot, y_bar_bot)
    # Left inner diagonal down to baseline
    p_A_out.line_to(lsb_A + stem * 1.1, 0.0)
    p_A_out.close()
    
    # Inner triangle counter
    t_l_top = y_bar_top / cap_h
    xl_top = (lsb_A + stem * 1.1) + t_l_top * (cx_A - (lsb_A + stem * 1.1))
    t_r_top = y_bar_top / cap_h
    xr_top = (rsb_A - stem * 1.1) + t_r_top * (cx_A - (rsb_A - stem * 1.1))
    p_A_in = Path()
    p_A_in.move_to(xl_top, y_bar_top)
    p_A_in.line_to(xr_top, y_bar_top)
    p_A_in.line_to(cx_A, cap_h - stem_h * 1.1)
    p_A_in.close()
    add_glyph(GlyphSpec('A', 0x0041, w_A, lsb_A, [p_A_out, p_A_in]))

    # --- B ---
    w_B = 620.0 + stem * 0.4
    lsb_B = 80.0
    waist_B = 360.0
    p_B_out = Path()
    p_B_out.move_to(lsb_B, 0.0)
    p_B_out.line_to(lsb_B, cap_h)
    p_B_out.line_to(w_B - 140.0, cap_h)
    p_B_out.arc_to(w_B - 140.0, (cap_h + waist_B)/2.0, 140.0 - lsb_B*0.4, (cap_h - waist_B)/2.0, 90, -90, clockwise=True, steps=4)
    p_B_out.line_to(w_B - 120.0, waist_B)
    p_B_out.arc_to(w_B - 120.0, waist_B/2.0, 150.0 - lsb_B*0.4, waist_B/2.0, 90, -90, clockwise=True, steps=4)
    p_B_out.line_to(lsb_B, 0.0)
    p_B_out.close()
    
    # Top counter (counter-clockwise)
    p_B_top = Path()
    p_B_top.move_to(lsb_B + stem, waist_B + stem_h*0.5)
    p_B_top.line_to(lsb_B + stem, cap_h - stem_h)
    p_B_top.line_to(w_B - 160.0, cap_h - stem_h)
    p_B_top.arc_to(w_B - 160.0, (cap_h + waist_B)/2.0, max(10.0, 140.0 - lsb_B*0.4 - stem), (cap_h - waist_B)/2.0 - stem_h, 90, -90, clockwise=False, steps=4)
    p_B_top.close()
    
    # Bottom counter (counter-clockwise)
    p_B_bot = Path()
    p_B_bot.move_to(lsb_B + stem, stem_h)
    p_B_bot.line_to(lsb_B + stem, waist_B - stem_h*0.5)
    p_B_bot.line_to(w_B - 140.0, waist_B - stem_h*0.5)
    p_B_bot.arc_to(w_B - 140.0, waist_B/2.0, max(10.0, 150.0 - lsb_B*0.4 - stem), waist_B/2.0 - stem_h, 90, -90, clockwise=False, steps=4)
    p_B_bot.close()
    add_glyph(GlyphSpec('B', 0x0042, w_B, lsb_B, [p_B_out, p_B_top, p_B_bot]))

    # --- C (Pure Circular Arc, Clean Terminals) ---
    w_C = 720.0 + stem * 0.4
    cx_C = w_C / 2.0 + 10.0
    cy_C = cap_h / 2.0
    rx_C = (w_C - 100.0) / 2.0
    ry_C = (cap_h + 2*ov) / 2.0
    ang_cut = 42.0
    
    p_C = Path()
    # Outer arc from top terminal clockwise around back to bottom terminal
    a_top = 90.0 - ang_cut
    a_bot = 270.0 + ang_cut
    x_out_top = cx_C + rx_C * math.cos(math.radians(a_top))
    y_out_top = cy_C + ry_C * math.sin(math.radians(a_top))
    p_C.move_to(x_out_top, y_out_top)
    p_C.arc_to(cx_C, cy_C, rx_C, ry_C, a_top, a_bot, clockwise=True, steps=6)
    
    # Bottom flat terminal inward
    x_in_bot = cx_C + (rx_C - stem) * math.cos(math.radians(a_bot))
    y_in_bot = cy_C + (ry_C - stem_h) * math.sin(math.radians(a_bot))
    p_C.line_to(x_in_bot, y_in_bot)
    
    # Inner arc counter-clockwise back to top terminal
    p_C.arc_to(cx_C, cy_C, rx_C - stem, ry_C - stem_h, a_bot, a_top, clockwise=False, steps=6)
    p_C.close()
    add_glyph(GlyphSpec('C', 0x0043, w_C, 60.0, [p_C]))

    # --- D ---
    w_D = 720.0 + stem * 0.4
    lsb_D = 80.0
    p_D_out = Path()
    p_D_out.move_to(lsb_D, 0.0)
    p_D_out.line_to(lsb_D, cap_h)
    p_D_out.line_to(w_D - 280.0, cap_h)
    p_D_out.arc_to(w_D - 280.0, cap_h/2.0, 240.0, cap_h/2.0, 90, -90, clockwise=True, steps=4)
    p_D_out.line_to(lsb_D, 0.0)
    p_D_out.close()
    
    p_D_in = Path()
    p_D_in.move_to(lsb_D + stem, stem_h)
    p_D_in.line_to(lsb_D + stem, cap_h - stem_h)
    p_D_in.line_to(w_D - 280.0, cap_h - stem_h)
    p_D_in.arc_to(w_D - 280.0, cap_h/2.0, max(10.0, 240.0 - stem), cap_h/2.0 - stem_h, 90, -90, clockwise=False, steps=4)
    p_D_in.close()
    add_glyph(GlyphSpec('D', 0x0044, w_D, lsb_D, [p_D_out, p_D_in]))

    # --- E ---
    w_E = 600.0 + stem * 0.3
    lsb_E = 80.0
    p_E = Path()
    p_E.move_to(lsb_E, 0.0)
    p_E.line_to(lsb_E, cap_h)
    p_E.line_to(w_E - 60.0, cap_h)
    p_E.line_to(w_E - 60.0, cap_h - stem_h)
    p_E.line_to(lsb_E + stem, cap_h - stem_h)
    p_E.line_to(lsb_E + stem, 350.0 + stem_h/2.0)
    p_E.line_to(w_E - 100.0, 350.0 + stem_h/2.0)
    p_E.line_to(w_E - 100.0, 350.0 - stem_h/2.0)
    p_E.line_to(lsb_E + stem, 350.0 - stem_h/2.0)
    p_E.line_to(lsb_E + stem, stem_h)
    p_E.line_to(w_E - 50.0, stem_h)
    p_E.line_to(w_E - 50.0, 0.0)
    p_E.close()
    add_glyph(GlyphSpec('E', 0x0045, w_E, lsb_E, [p_E]))

    # --- F ---
    w_F = 570.0 + stem * 0.3
    lsb_F = 80.0
    p_F = Path()
    p_F.move_to(lsb_F, 0.0)
    p_F.line_to(lsb_F, cap_h)
    p_F.line_to(w_F - 50.0, cap_h)
    p_F.line_to(w_F - 50.0, cap_h - stem_h)
    p_F.line_to(lsb_F + stem, cap_h - stem_h)
    p_F.line_to(lsb_F + stem, 360.0 + stem_h/2.0)
    p_F.line_to(w_F - 90.0, 360.0 + stem_h/2.0)
    p_F.line_to(w_F - 90.0, 360.0 - stem_h/2.0)
    p_F.line_to(lsb_F + stem, 360.0 - stem_h/2.0)
    p_F.line_to(lsb_F + stem, 0.0)
    p_F.close()
    add_glyph(GlyphSpec('F', 0x0046, w_F, lsb_F, [p_F]))

    # --- G (Clean Circular Sweep, Horizontal Inset Bar, No Spur) ---
    w_G = 760.0 + stem * 0.4
    cx_G = w_G / 2.0 + 10.0
    cy_G = cap_h / 2.0
    rx_G = (w_G - 100.0) / 2.0
    ry_G = (cap_h + 2*ov) / 2.0
    y_bar_G = 330.0
    
    p_G = Path()
    # Outer arc starting at top terminal
    x_out_top_G = cx_G + rx_G * math.cos(math.radians(a_top))
    y_out_top_G = cy_G + ry_G * math.sin(math.radians(a_top))
    p_G.move_to(x_out_top_G, y_out_top_G)
    p_G.arc_to(cx_G, cy_G, rx_G, ry_G, a_top, 0, clockwise=True, steps=6)
    # Straight up to crossbar
    p_G.line_to(cx_G + rx_G, y_bar_G)
    p_G.line_to(cx_G - 20.0, y_bar_G)
    p_G.line_to(cx_G - 20.0, y_bar_G - stem_h)
    p_G.line_to(cx_G + rx_G - stem, y_bar_G - stem_h)
    # Inner arc counter-clockwise back to top terminal
    p_G.arc_to(cx_G, cy_G, rx_G - stem, ry_G - stem_h, 0, a_top, clockwise=False, steps=6)
    p_G.close()
    add_glyph(GlyphSpec('G', 0x0047, w_G, 60.0, [p_G]))

    # --- H ---
    w_H = 720.0 + stem * 0.4
    lsb_H = 80.0
    rsb_H = w_H - 80.0
    p_H = Path()
    p_H.move_to(lsb_H, 0.0)
    p_H.line_to(lsb_H, cap_h)
    p_H.line_to(lsb_H + stem, cap_h)
    p_H.line_to(lsb_H + stem, 350.0 + stem_h/2.0)
    p_H.line_to(rsb_H - stem, 350.0 + stem_h/2.0)
    p_H.line_to(rsb_H - stem, cap_h)
    p_H.line_to(rsb_H, cap_h)
    p_H.line_to(rsb_H, 0.0)
    p_H.line_to(rsb_H - stem, 0.0)
    p_H.line_to(rsb_H - stem, 350.0 - stem_h/2.0)
    p_H.line_to(lsb_H + stem, 350.0 - stem_h/2.0)
    p_H.line_to(lsb_H + stem, 0.0)
    p_H.close()
    add_glyph(GlyphSpec('H', 0x0048, w_H, lsb_H, [p_H]))

    # --- I ---
    w_I = 260.0 + stem * 0.8
    lsb_I = (w_I - stem) / 2.0
    p_I = Path()
    p_I.rect(lsb_I, 0.0, stem, cap_h)
    add_glyph(GlyphSpec('I', 0x0049, w_I, lsb_I, [p_I]))

    # --- J ---
    w_J = 480.0 + stem * 0.3
    lsb_J = 60.0
    p_J = Path()
    p_J.move_to(w_J - 80.0 - stem, cap_h)
    p_J.line_to(w_J - 80.0, cap_h)
    p_J.line_to(w_J - 80.0, 160.0)
    p_J.arc_to(w_J - 80.0 - 140.0, 160.0, 140.0, 160.0 + ov, 0, -180, clockwise=True, steps=4)
    p_J.line_to(lsb_J, 180.0)
    p_J.line_to(lsb_J + stem, 180.0)
    p_J.line_to(lsb_J + stem, 160.0)
    p_J.arc_to(w_J - 80.0 - 140.0, 160.0, max(10.0, 140.0 - stem), 160.0 + ov - stem_h, 180, 0, clockwise=False, steps=4)
    p_J.close()
    add_glyph(GlyphSpec('J', 0x004A, w_J, lsb_J, [p_J]))

    # --- K ---
    w_K = 650.0 + stem * 0.4
    lsb_K = 80.0
    p_K = Path()
    p_K.move_to(lsb_K, 0.0)
    p_K.line_to(lsb_K, cap_h)
    p_K.line_to(lsb_K + stem, cap_h)
    # To diagonal junction
    p_K.line_to(lsb_K + stem, 390.0)
    p_K.line_to(w_K - 100.0, cap_h)
    p_K.line_to(w_K - 100.0 + stem*1.1, cap_h)
    p_K.line_to(lsb_K + stem + 60.0, 310.0)
    p_K.line_to(w_K - 70.0 + stem*1.1, 0.0)
    p_K.line_to(w_K - 70.0, 0.0)
    p_K.line_to(lsb_K + stem, 250.0)
    p_K.line_to(lsb_K + stem, 0.0)
    p_K.close()
    add_glyph(GlyphSpec('K', 0x004B, w_K, lsb_K, [p_K]))

    # --- L ---
    w_L = 520.0 + stem * 0.3
    lsb_L = 80.0
    p_L = Path()
    p_L.move_to(lsb_L, 0.0)
    p_L.line_to(lsb_L, cap_h)
    p_L.line_to(lsb_L + stem, cap_h)
    p_L.line_to(lsb_L + stem, stem_h)
    p_L.line_to(w_L - 60.0, stem_h)
    p_L.line_to(w_L - 60.0, 0.0)
    p_L.close()
    add_glyph(GlyphSpec('L', 0x004C, w_L, lsb_L, [p_L]))

    # --- M (Geometric modern: Verticals + Diagonals touching baseline) ---
    w_M = 820.0 + stem * 0.5
    lsb_M = 70.0
    rsb_M = w_M - 70.0
    cx_M = w_M / 2.0
    p_M = Path()
    p_M.move_to(lsb_M, 0.0)
    p_M.line_to(lsb_M, cap_h)
    p_M.line_to(lsb_M + stem*0.9, cap_h)
    p_M.line_to(cx_M, 160.0)
    p_M.line_to(rsb_M - stem*0.9, cap_h)
    p_M.line_to(rsb_M, cap_h)
    p_M.line_to(rsb_M, 0.0)
    p_M.line_to(rsb_M - stem, 0.0)
    p_M.line_to(rsb_M - stem, cap_h - 180.0)
    p_M.line_to(cx_M, 40.0)
    p_M.line_to(lsb_M + stem, cap_h - 180.0)
    p_M.line_to(lsb_M + stem, 0.0)
    p_M.close()
    add_glyph(GlyphSpec('M', 0x004D, w_M, lsb_M, [p_M]))

    # --- N ---
    w_N = 720.0 + stem * 0.4
    lsb_N = 80.0
    rsb_N = w_N - 80.0
    p_N = Path()
    p_N.move_to(lsb_N, 0.0)
    p_N.line_to(lsb_N, cap_h)
    p_N.line_to(lsb_N + stem*0.9, cap_h)
    p_N.line_to(rsb_N - stem, 120.0)
    p_N.line_to(rsb_N - stem, cap_h)
    p_N.line_to(rsb_N, cap_h)
    p_N.line_to(rsb_N, 0.0)
    p_N.line_to(rsb_N - stem*0.9, 0.0)
    p_N.line_to(lsb_N + stem, cap_h - 120.0)
    p_N.line_to(lsb_N + stem, 0.0)
    p_N.close()
    add_glyph(GlyphSpec('N', 0x004E, w_N, lsb_N, [p_N]))

    # --- O (Pure Geometric Circle) ---
    w_O = 780.0 + stem * 0.4
    cx_O = w_O / 2.0
    cy_O = cap_h / 2.0
    rx_O = (w_O - 90.0) / 2.0
    ry_O = (cap_h + 2*ov) / 2.0
    p_O = Path()
    p_O.donut(cx_O, cy_O, rx_O, ry_O, max(10.0, rx_O - stem), max(10.0, ry_O - stem_h))
    add_glyph(GlyphSpec('O', 0x004F, w_O, 45.0, [p_O]))

    # --- P ---
    w_P = 620.0 + stem * 0.3
    lsb_P = 80.0
    y_mid_P = 280.0
    p_P_out = Path()
    p_P_out.move_to(lsb_P, 0.0)
    p_P_out.line_to(lsb_P, cap_h)
    p_P_out.line_to(w_P - 180.0, cap_h)
    p_P_out.arc_to(w_P - 180.0, (cap_h + y_mid_P)/2.0, 140.0, (cap_h - y_mid_P)/2.0, 90, -90, clockwise=True, steps=4)
    p_P_out.line_to(lsb_P + stem, y_mid_P)
    p_P_out.line_to(lsb_P + stem, 0.0)
    p_P_out.close()
    
    p_P_in = Path()
    p_P_in.move_to(lsb_P + stem, y_mid_P + stem_h)
    p_P_in.line_to(lsb_P + stem, cap_h - stem_h)
    p_P_in.line_to(w_P - 180.0, cap_h - stem_h)
    p_P_in.arc_to(w_P - 180.0, (cap_h + y_mid_P)/2.0, max(10.0, 140.0 - stem), (cap_h - y_mid_P)/2.0 - stem_h, 90, -90, clockwise=False, steps=4)
    p_P_in.close()
    add_glyph(GlyphSpec('P', 0x0050, w_P, lsb_P, [p_P_out, p_P_in]))

    # --- Q (Circular O with sleek diagonal tail) ---
    w_Q = w_O
    p_Q_bowl = Path()
    p_Q_bowl.donut(cx_O, cy_O, rx_O, ry_O, max(10.0, rx_O - stem), max(10.0, ry_O - stem_h))
    p_Q_tail = Path()
    # Sleek diagonal tail
    tail_x0 = cx_O + 60.0
    tail_y0 = 120.0
    tail_x1 = w_Q - 20.0
    tail_y1 = -60.0
    p_Q_tail.move_to(tail_x0, tail_y0)
    p_Q_tail.line_to(tail_x0 + stem, tail_y0)
    p_Q_tail.line_to(tail_x1, tail_y1)
    p_Q_tail.line_to(tail_x1 - stem*1.2, tail_y1)
    p_Q_tail.close()
    add_glyph(GlyphSpec('Q', 0x0051, w_Q, 45.0, [p_Q_bowl, p_Q_tail]))

    # --- R ---
    w_R = 650.0 + stem * 0.4
    lsb_R = 80.0
    p_R_out = Path()
    p_R_out.move_to(lsb_R, 0.0)
    p_R_out.line_to(lsb_R, cap_h)
    p_R_out.line_to(w_R - 180.0, cap_h)
    p_R_out.arc_to(w_R - 180.0, (cap_h + y_mid_P)/2.0, 140.0, (cap_h - y_mid_P)/2.0, 90, -90, clockwise=True, steps=4)
    p_R_out.line_to(lsb_R + stem + 20.0, y_mid_P)
    p_R_out.line_to(w_R - 80.0, 0.0)
    p_R_out.line_to(w_R - 80.0 - stem*1.1, 0.0)
    p_R_out.line_to(lsb_R + stem, y_mid_P)
    p_R_out.line_to(lsb_R + stem, 0.0)
    p_R_out.close()
    
    p_R_in = Path()
    p_R_in.move_to(lsb_R + stem, y_mid_P + stem_h)
    p_R_in.line_to(lsb_R + stem, cap_h - stem_h)
    p_R_in.line_to(w_R - 180.0, cap_h - stem_h)
    p_R_in.arc_to(w_R - 180.0, (cap_h + y_mid_P)/2.0, max(10.0, 140.0 - stem), (cap_h - y_mid_P)/2.0 - stem_h, 90, -90, clockwise=False, steps=4)
    p_R_in.close()
    add_glyph(GlyphSpec('R', 0x0052, w_R, lsb_R, [p_R_out, p_R_in]))

    # --- S (Geometric Modern S with open terminals) ---
    w_S = 600.0 + stem * 0.3
    lsb_S = 70.0
    rsb_S = w_S - 70.0
    cx_S = w_S / 2.0
    p_S = Path()
    # Outer continuous ribbon
    p_S.move_to(rsb_S - 30.0, cap_h - 130.0)
    p_S.arc_to(cx_S, cap_h - 170.0, (w_S - 140.0)/2.0, 170.0 + ov, 30, 180, clockwise=False, steps=4)
    p_S.arc_to(cx_S, 170.0, (w_S - 140.0)/2.0, 170.0 + ov, 0, -150, clockwise=True, steps=4)
    p_S.line_to(lsb_S + 30.0, 130.0)
    # Inner sweep
    p_S.arc_to(cx_S, 170.0, max(10.0, (w_S - 140.0)/2.0 - stem), max(10.0, 170.0 + ov - stem_h), -150, 0, clockwise=False, steps=4)
    p_S.arc_to(cx_S, cap_h - 170.0, max(10.0, (w_S - 140.0)/2.0 - stem), max(10.0, 170.0 + ov - stem_h), 180, 30, clockwise=True, steps=4)
    p_S.close()
    add_glyph(GlyphSpec('S', 0x0053, w_S, lsb_S, [p_S]))

    # --- T ---
    w_T = 620.0 + stem * 0.3
    cx_T = w_T / 2.0
    p_T = Path()
    p_T.move_to(cx_T - stem/2.0, 0.0)
    p_T.line_to(cx_T - stem/2.0, cap_h - stem_h)
    p_T.line_to(40.0, cap_h - stem_h)
    p_T.line_to(40.0, cap_h)
    p_T.line_to(w_T - 40.0, cap_h)
    p_T.line_to(w_T - 40.0, cap_h - stem_h)
    p_T.line_to(cx_T + stem/2.0, cap_h - stem_h)
    p_T.line_to(cx_T + stem/2.0, 0.0)
    p_T.close()
    add_glyph(GlyphSpec('T', 0x0054, w_T, 40.0, [p_T]))

    # --- U ---
    w_U = 720.0 + stem * 0.4
    lsb_U = 80.0
    rsb_U = w_U - 80.0
    cx_U = w_U / 2.0
    p_U = Path()
    p_U.move_to(lsb_U, cap_h)
    p_U.line_to(lsb_U + stem, cap_h)
    p_U.line_to(lsb_U + stem, 220.0)
    p_U.arc_to(cx_U, 220.0, max(10.0, (w_U - 160.0)/2.0 - stem), max(10.0, 220.0 + ov - stem_h), 180, 0, clockwise=True, steps=4)
    p_U.line_to(rsb_U - stem, cap_h)
    p_U.line_to(rsb_U, cap_h)
    p_U.line_to(rsb_U, 220.0)
    p_U.arc_to(cx_U, 220.0, (w_U - 160.0)/2.0, 220.0 + ov, 0, -180, clockwise=True, steps=4)
    p_U.line_to(lsb_U, cap_h)
    p_U.close()
    add_glyph(GlyphSpec('U', 0x0055, w_U, lsb_U, [p_U]))

    # --- V ---
    w_V = 680.0 + stem * 0.4
    lsb_V = 40.0
    rsb_V = w_V - 40.0
    cx_V = w_V / 2.0
    p_V = Path()
    p_V.move_to(lsb_V, cap_h)
    p_V.line_to(lsb_V + stem*1.1, cap_h)
    p_V.line_to(cx_V, stem_h*0.8)
    p_V.line_to(rsb_V - stem*1.1, cap_h)
    p_V.line_to(rsb_V, cap_h)
    p_V.line_to(cx_V + stem*0.3, 0.0)
    p_V.line_to(cx_V - stem*0.3, 0.0)
    p_V.close()
    add_glyph(GlyphSpec('V', 0x0056, w_V, lsb_V, [p_V]))

    # --- W ---
    w_W = 960.0 + stem * 0.6
    lsb_W = 40.0
    rsb_W = w_W - 40.0
    p_W = Path()
    p_W.move_to(lsb_W, cap_h)
    p_W.line_to(lsb_W + stem*0.9, cap_h)
    p_W.line_to(lsb_W + 200.0, 0.0)
    p_W.line_to(lsb_W + 200.0 + stem*0.8, 0.0)
    p_W.line_to(w_W / 2.0, cap_h - 160.0)
    p_W.line_to(rsb_W - 200.0 - stem*0.8, 0.0)
    p_W.line_to(rsb_W - 200.0, 0.0)
    p_W.line_to(rsb_W - stem*0.9, cap_h)
    p_W.line_to(rsb_W, cap_h)
    p_W.line_to(rsb_W - 190.0, 0.0)
    p_W.line_to(w_W / 2.0, cap_h - 220.0)
    p_W.line_to(lsb_W + 190.0, 0.0)
    p_W.close()
    add_glyph(GlyphSpec('W', 0x0057, w_W, lsb_W, [p_W]))

    # --- X ---
    w_X = 640.0 + stem * 0.4
    lsb_X = 50.0
    rsb_X = w_X - 50.0
    p_X = Path()
    p_X.move_to(lsb_X, cap_h)
    p_X.line_to(lsb_X + stem*1.1, cap_h)
    p_X.line_to(rsb_X, 0.0)
    p_X.line_to(rsb_X - stem*1.1, 0.0)
    p_X.close()
    p_X2 = Path()
    p_X2.move_to(rsb_X - stem*1.1, cap_h)
    p_X2.line_to(rsb_X, cap_h)
    p_X2.line_to(lsb_X + stem*1.1, 0.0)
    p_X2.line_to(lsb_X, 0.0)
    p_X2.close()
    add_glyph(GlyphSpec('X', 0x0058, w_X, lsb_X, [p_X, p_X2]))

    # --- Y ---
    w_Y = 640.0 + stem * 0.4
    lsb_Y = 50.0
    rsb_Y = w_Y - 50.0
    cx_Y = w_Y / 2.0
    p_Y = Path()
    p_Y.move_to(lsb_Y, cap_h)
    p_Y.line_to(lsb_Y + stem*1.1, cap_h)
    p_Y.line_to(cx_Y, 300.0)
    p_Y.line_to(cx_Y, 0.0)
    p_Y.line_to(cx_Y + stem, 0.0)
    p_Y.line_to(cx_Y + stem, 300.0)
    p_Y.line_to(rsb_Y, cap_h)
    p_Y.line_to(rsb_Y - stem*1.1, cap_h)
    p_Y.line_to(cx_Y + stem/2.0, 320.0)
    p_Y.close()
    add_glyph(GlyphSpec('Y', 0x0059, w_Y, lsb_Y, [p_Y]))

    # --- Z ---
    w_Z = 600.0 + stem * 0.3
    lsb_Z = 60.0
    rsb_Z = w_Z - 60.0
    p_Z = Path()
    p_Z.move_to(lsb_Z, cap_h)
    p_Z.line_to(rsb_Z, cap_h)
    p_Z.line_to(rsb_Z, cap_h - stem_h)
    p_Z.line_to(lsb_Z + stem*1.2, stem_h)
    p_Z.line_to(rsb_Z, stem_h)
    p_Z.line_to(rsb_Z, 0.0)
    p_Z.line_to(lsb_Z, 0.0)
    p_Z.line_to(lsb_Z, stem_h)
    p_Z.line_to(rsb_Z - stem*1.2, cap_h - stem_h)
    p_Z.line_to(lsb_Z, cap_h - stem_h)
    p_Z.close()
    add_glyph(GlyphSpec('Z', 0x005A, w_Z, lsb_Z, [p_Z]))

    # -------------------------------------------------------------
    # LOWERCASE a-z
    # -------------------------------------------------------------

    # --- a (Single-Story Circular Bowl with Right Vertical Stem) ---
    w_a = 600.0 + stem * 0.4
    rsb_a = w_a - 60.0
    cx_a = (rsb_a - stem) / 2.0 + 30.0
    cy_a = x_h / 2.0
    rx_a = (rsb_a - stem - 40.0) / 2.0
    ry_a = (x_h + 2*ov) / 2.0
    
    p_a_stem = Path()
    # Right vertical stem with circular bowl merge
    p_a_stem.move_to(rsb_a - stem, 0.0)
    p_a_stem.line_to(rsb_a, 0.0)
    p_a_stem.line_to(rsb_a, x_h)
    p_a_stem.line_to(rsb_a - stem, x_h)
    p_a_stem.close()
    
    p_a_bowl = Path()
    p_a_bowl.donut(cx_a, cy_a, rx_a, ry_a, max(10.0, rx_a - stem), max(10.0, ry_a - stem_h))
    add_glyph(GlyphSpec('a', 0x0061, w_a, 50.0, [p_a_bowl, p_a_stem]))

    # --- b ---
    w_b = 620.0 + stem * 0.4
    lsb_b = 60.0
    cx_b = (w_b + lsb_b + stem) / 2.0 - 20.0
    cy_b = x_h / 2.0
    rx_b = (w_b - lsb_b - stem - 30.0) / 2.0
    ry_b = (x_h + 2*ov) / 2.0
    
    p_b_stem = Path()
    p_b_stem.rect(lsb_b, 0.0, stem, asc)
    p_b_bowl = Path()
    p_b_bowl.donut(cx_b, cy_b, rx_b, ry_b, max(10.0, rx_b - stem), max(10.0, ry_b - stem_h))
    add_glyph(GlyphSpec('b', 0x0062, w_b, lsb_b, [p_b_stem, p_b_bowl]))

    # --- c (Circular arc with open aperture) ---
    w_c = 540.0 + stem * 0.3
    cx_c = w_c / 2.0 + 5.0
    cy_c = x_h / 2.0
    rx_c = (w_c - 80.0) / 2.0
    ry_c = (x_h + 2*ov) / 2.0
    a_c = 44.0
    
    p_c = Path()
    x_c_top = cx_c + rx_c * math.cos(math.radians(90.0 - a_c))
    y_c_top = cy_c + ry_c * math.sin(math.radians(90.0 - a_c))
    p_c.move_to(x_c_top, y_c_top)
    p_c.arc_to(cx_c, cy_c, rx_c, ry_c, 90.0 - a_c, 270.0 + a_c, clockwise=True, steps=6)
    x_c_bot_in = cx_c + (rx_c - stem) * math.cos(math.radians(270.0 + a_c))
    y_c_bot_in = cy_c + (ry_c - stem_h) * math.sin(math.radians(270.0 + a_c))
    p_c.line_to(x_c_bot_in, y_c_bot_in)
    p_c.arc_to(cx_c, cy_c, rx_c - stem, ry_c - stem_h, 270.0 + a_c, 90.0 - a_c, clockwise=False, steps=6)
    p_c.close()
    add_glyph(GlyphSpec('c', 0x0063, w_c, 50.0, [p_c]))

    # --- d ---
    w_d = 620.0 + stem * 0.4
    rsb_d = w_d - 60.0
    cx_d = (rsb_d - stem + 50.0) / 2.0
    cy_d = x_h / 2.0
    rx_d = (rsb_d - stem - 50.0) / 2.0
    ry_d = (x_h + 2*ov) / 2.0
    
    p_d_stem = Path()
    p_d_stem.rect(rsb_d - stem, 0.0, stem, asc)
    p_d_bowl = Path()
    p_d_bowl.donut(cx_d, cy_d, rx_d, ry_d, max(10.0, rx_d - stem), max(10.0, ry_d - stem_h))
    add_glyph(GlyphSpec('d', 0x0064, w_d, 50.0, [p_d_bowl, p_d_stem]))

    # --- e (Horizontal Crossbar, Circular Upper Bowl, Open Lower Curve) ---
    w_e = 580.0 + stem * 0.35
    cx_e = w_e / 2.0
    cy_e = x_h / 2.0
    rx_e = (w_e - 80.0) / 2.0
    ry_e = (x_h + 2*ov) / 2.0
    y_bar_e = 260.0
    
    p_e_out = Path()
    # Outer curve starting from bar right end, curving over top to bottom terminal
    p_e_out.move_to(cx_e + rx_e, y_bar_e)
    p_e_out.arc_to(cx_e, cy_e, rx_e, ry_e, 0, 310, clockwise=False, steps=6)
    # Bottom terminal flat inward
    x_e_bot_in = cx_e + (rx_e - stem) * math.cos(math.radians(310.0))
    y_e_bot_in = cy_e + (ry_e - stem_h) * math.sin(math.radians(310.0))
    p_e_out.line_to(x_e_bot_in, y_e_bot_in)
    # Inner lower curve back to bar
    p_e_out.arc_to(cx_e, cy_e, rx_e - stem, ry_e - stem_h, 310.0, 180.0, clockwise=True, steps=4)
    p_e_out.line_to(cx_e + rx_e, y_bar_e - stem_h)
    p_e_out.close()
    
    # Top eye counter
    p_e_eye = Path()
    p_e_eye.move_to(cx_e - rx_e + stem, y_bar_e)
    p_e_eye.arc_to(cx_e, cy_e, max(10.0, rx_e - stem), max(10.0, ry_e - stem_h), 180, 0, clockwise=False, steps=4)
    p_e_eye.line_to(cx_e - rx_e + stem, y_bar_e)
    p_e_eye.close()
    add_glyph(GlyphSpec('e', 0x0065, w_e, 50.0, [p_e_out, p_e_eye]))

    # --- f ---
    w_f = 350.0 + stem * 0.3
    cx_f = 120.0
    p_f = Path()
    p_f.move_to(cx_f, 0.0)
    p_f.line_to(cx_f + stem, 0.0)
    p_f.line_to(cx_f + stem, asc - 140.0)
    p_f.arc_to(cx_f + stem + 70.0, asc - 140.0, 70.0, 140.0, 180, 45, clockwise=False, steps=3)
    p_f.line_to(w_f - 30.0, asc - 10.0)
    p_f.arc_to(cx_f + stem + 70.0, asc - 140.0, max(10.0, 70.0 - stem), max(10.0, 140.0 - stem_h), 45, 180, clockwise=True, steps=3)
    p_f.line_to(cx_f, 0.0)
    p_f.close()
    
    p_f_bar = Path()
    p_f_bar.rect(40.0, x_h - stem_h, w_f - 60.0, stem_h)
    add_glyph(GlyphSpec('f', 0x0066, w_f, 40.0, [p_f, p_f_bar]))

    # --- g (Modern single-story circular bowl + descending hook) ---
    w_g = 600.0 + stem * 0.4
    rsb_g = w_g - 60.0
    cx_g = (rsb_g - stem + 50.0) / 2.0
    cy_g = x_h / 2.0
    rx_g = (rsb_g - stem - 50.0) / 2.0
    ry_g = (x_h + 2*ov) / 2.0
    
    p_g_bowl = Path()
    p_g_bowl.donut(cx_g, cy_g, rx_g, ry_g, max(10.0, rx_g - stem), max(10.0, ry_g - stem_h))
    
    p_g_tail = Path()
    p_g_tail.move_to(rsb_g - stem, x_h)
    p_g_tail.line_to(rsb_g, x_h)
    p_g_tail.line_to(rsb_g, -60.0)
    p_g_tail.arc_to(rsb_g - 140.0, -60.0, 140.0, 140.0 - desc*0.1, 0, -160, clockwise=True, steps=4)
    p_g_tail.line_to(w_g - 260.0, -190.0)
    p_g_tail.arc_to(rsb_g - 140.0, -60.0, max(10.0, 140.0 - stem), max(10.0, 140.0 - desc*0.1 - stem_h), -160, 0, clockwise=False, steps=4)
    p_g_tail.close()
    add_glyph(GlyphSpec('g', 0x0067, w_g, 50.0, [p_g_bowl, p_g_tail]))

    # --- h ---
    w_h = 600.0 + stem * 0.4
    lsb_h = 60.0
    rsb_h = w_h - 60.0
    p_h_stem = Path()
    p_h_stem.rect(lsb_h, 0.0, stem, asc)
    
    p_h_arch = Path()
    p_h_arch.move_to(lsb_h + stem, x_h - 160.0)
    p_h_arch.arc_to((lsb_h + stem + rsb_h)/2.0, x_h - 160.0, (rsb_h - (lsb_h + stem))/2.0, 160.0 + ov, 180, 0, clockwise=False, steps=4)
    p_h_arch.line_to(rsb_h, 0.0)
    p_h_arch.line_to(rsb_h - stem, 0.0)
    p_h_arch.line_to(rsb_h - stem, x_h - 160.0)
    p_h_arch.arc_to((lsb_h + stem + rsb_h)/2.0, x_h - 160.0, max(10.0, (rsb_h - (lsb_h + stem))/2.0 - stem), max(10.0, 160.0 + ov - stem_h), 0, 180, clockwise=True, steps=4)
    p_h_arch.close()
    add_glyph(GlyphSpec('h', 0x0068, w_h, lsb_h, [p_h_stem, p_h_arch]))

    # --- i (Clean stem + Circular Dot) ---
    w_i = 250.0 + stem * 0.8
    lsb_i = (w_i - stem) / 2.0
    p_i_stem = Path()
    p_i_stem.rect(lsb_i, 0.0, stem, x_h)
    p_i_dot = Path()
    r_dot = max(18.0, stem * 0.6)
    p_i_dot.circle(w_i / 2.0, 650.0, r_dot)
    add_glyph(GlyphSpec('i', 0x0069, w_i, lsb_i, [p_i_stem, p_i_dot]))

    # --- j ---
    w_j = 270.0 + stem * 0.7
    rsb_j = w_j - 60.0
    p_j_stem = Path()
    p_j_stem.move_to(rsb_j - stem, x_h)
    p_j_stem.line_to(rsb_j, x_h)
    p_j_stem.line_to(rsb_j, -60.0)
    p_j_stem.arc_to(rsb_j - 110.0, -60.0, 110.0, 140.0, 0, -180, clockwise=True, steps=4)
    p_j_stem.line_to(rsb_j - 220.0, -40.0)
    p_j_stem.line_to(rsb_j - 220.0 + stem, -40.0)
    p_j_stem.arc_to(rsb_j - 110.0, -60.0, max(10.0, 110.0 - stem), max(10.0, 140.0 - stem_h), -180, 0, clockwise=False, steps=4)
    p_j_stem.close()
    p_j_dot = Path()
    p_j_dot.circle(rsb_j - stem/2.0, 650.0, r_dot)
    add_glyph(GlyphSpec('j', 0x006A, w_j, 40.0, [p_j_stem, p_j_dot]))

    # --- k ---
    w_k = 540.0 + stem * 0.35
    lsb_k = 60.0
    p_k_stem = Path()
    p_k_stem.rect(lsb_k, 0.0, stem, asc)
    p_k_diag = Path()
    p_k_diag.move_to(lsb_k + stem, 220.0)
    p_k_diag.line_to(w_k - 70.0, x_h)
    p_k_diag.line_to(w_k - 70.0 + stem*1.1, x_h)
    p_k_diag.line_to(lsb_k + stem + 40.0, 160.0)
    p_k_diag.line_to(w_k - 50.0 + stem*1.1, 0.0)
    p_k_diag.line_to(w_k - 50.0, 0.0)
    p_k_diag.line_to(lsb_k + stem, 110.0)
    p_k_diag.close()
    add_glyph(GlyphSpec('k', 0x006B, w_k, lsb_k, [p_k_stem, p_k_diag]))

    # --- l ---
    w_l = 250.0 + stem * 0.8
    lsb_l = (w_l - stem) / 2.0
    p_l = Path()
    p_l.rect(lsb_l, 0.0, stem, asc)
    add_glyph(GlyphSpec('l', 0x006C, w_l, lsb_l, [p_l]))

    # --- m ---
    w_m = 920.0 + stem * 1.0
    lsb_m = 60.0
    col_w = (w_m - 2*lsb_m) / 2.0
    p_m_stem = Path()
    p_m_stem.rect(lsb_m, 0.0, stem, x_h)
    
    rx_m_in = max(10.0, (col_w - 2*stem) / 2.0)
    ry_m_in = max(10.0, 150.0 + ov - stem_h)
    cx_m1 = lsb_m + stem + (col_w - stem)/2.0
    
    p_m_arch1 = Path()
    p_m_arch1.move_to(lsb_m + stem, x_h - 150.0)
    p_m_arch1.arc_to(cx_m1, x_h - 150.0, (col_w - stem)/2.0, 150.0 + ov, 180, 0, clockwise=False, steps=4)
    p_m_arch1.line_to(lsb_m + col_w, 0.0)
    p_m_arch1.line_to(lsb_m + col_w - stem, 0.0)
    p_m_arch1.line_to(lsb_m + col_w - stem, x_h - 150.0)
    p_m_arch1.arc_to(cx_m1, x_h - 150.0, rx_m_in, ry_m_in, 0, 180, clockwise=True, steps=4)
    p_m_arch1.close()
    
    cx_m2 = lsb_m + col_w + (col_w - stem)/2.0
    p_m_arch2 = Path()
    p_m_arch2.move_to(lsb_m + col_w, x_h - 150.0)
    p_m_arch2.arc_to(cx_m2, x_h - 150.0, (col_w - stem)/2.0, 150.0 + ov, 180, 0, clockwise=False, steps=4)
    p_m_arch2.line_to(lsb_m + col_w*2.0, 0.0)
    p_m_arch2.line_to(lsb_m + col_w*2.0 - stem, 0.0)
    p_m_arch2.line_to(lsb_m + col_w*2.0 - stem, x_h - 150.0)
    p_m_arch2.arc_to(cx_m2, x_h - 150.0, rx_m_in, ry_m_in, 0, 180, clockwise=True, steps=4)
    p_m_arch2.close()
    add_glyph(GlyphSpec('m', 0x006D, w_m, lsb_m, [p_m_stem, p_m_arch1, p_m_arch2]))

    # --- n ---
    w_n = 600.0 + stem * 0.4
    lsb_n = 60.0
    rsb_n = w_n - 60.0
    p_n_stem = Path()
    p_n_stem.rect(lsb_n, 0.0, stem, x_h)
    p_n_arch = Path()
    p_n_arch.move_to(lsb_n + stem, x_h - 160.0)
    p_n_arch.arc_to((lsb_n + stem + rsb_n)/2.0, x_h - 160.0, (rsb_n - (lsb_n + stem))/2.0, 160.0 + ov, 180, 0, clockwise=False, steps=4)
    p_n_arch.line_to(rsb_n, 0.0)
    p_n_arch.line_to(rsb_n - stem, 0.0)
    p_n_arch.line_to(rsb_n - stem, x_h - 160.0)
    p_n_arch.arc_to((lsb_n + stem + rsb_n)/2.0, x_h - 160.0, max(10.0, (rsb_n - (lsb_n + stem))/2.0 - stem), max(10.0, 160.0 + ov - stem_h), 0, 180, clockwise=True, steps=4)
    p_n_arch.close()
    add_glyph(GlyphSpec('n', 0x006E, w_n, lsb_n, [p_n_stem, p_n_arch]))

    # --- o (Geometric Circle) ---
    w_o = 600.0 + stem * 0.4
    cx_o = w_o / 2.0
    cy_o = x_h / 2.0
    rx_o = (w_o - 80.0) / 2.0
    ry_o = (x_h + 2*ov) / 2.0
    p_o = Path()
    p_o.donut(cx_o, cy_o, rx_o, ry_o, max(10.0, rx_o - stem), max(10.0, ry_o - stem_h))
    add_glyph(GlyphSpec('o', 0x006F, w_o, 40.0, [p_o]))

    # --- p ---
    w_p = 620.0 + stem * 0.4
    lsb_p = 60.0
    p_p_stem = Path()
    p_p_stem.rect(lsb_p, desc, stem, x_h - desc)
    p_p_bowl = Path()
    cx_p = (w_p + lsb_p + stem) / 2.0 - 20.0
    cy_p = x_h / 2.0
    rx_p = (w_p - lsb_p - stem - 30.0) / 2.0
    ry_p = (x_h + 2*ov) / 2.0
    p_p_bowl.donut(cx_p, cy_p, rx_p, ry_p, max(10.0, rx_p - stem), max(10.0, ry_p - stem_h))
    add_glyph(GlyphSpec('p', 0x0070, w_p, lsb_p, [p_p_stem, p_p_bowl]))

    # --- q ---
    w_q = 620.0 + stem * 0.4
    rsb_q = w_q - 60.0
    p_q_stem = Path()
    p_q_stem.rect(rsb_q - stem, desc, stem, x_h - desc)
    p_q_bowl = Path()
    cx_q = (rsb_q - stem + 50.0) / 2.0
    cy_q = x_h / 2.0
    rx_q = (rsb_q - stem - 50.0) / 2.0
    ry_q = (x_h + 2*ov) / 2.0
    p_q_bowl.donut(cx_q, cy_q, rx_q, ry_q, max(10.0, rx_q - stem), max(10.0, ry_q - stem_h))
    add_glyph(GlyphSpec('q', 0x0071, w_q, 50.0, [p_q_bowl, p_q_stem]))

    # --- r ---
    w_r = 400.0 + stem * 0.3
    lsb_r = 60.0
    p_r_stem = Path()
    p_r_stem.rect(lsb_r, 0.0, stem, x_h)
    p_r_arch = Path()
    p_r_arch.move_to(lsb_r + stem, x_h - 150.0)
    p_r_arch.arc_to(lsb_r + stem + 90.0, x_h - 150.0, 90.0, 150.0 + ov, 180, 45, clockwise=False, steps=3)
    p_r_arch.line_to(w_r - 20.0, x_h - 60.0)
    p_r_arch.arc_to(lsb_r + stem + 90.0, x_h - 150.0, max(10.0, 90.0 - stem), max(10.0, 150.0 + ov - stem_h), 45, 180, clockwise=True, steps=3)
    p_r_arch.close()
    add_glyph(GlyphSpec('r', 0x0072, w_r, lsb_r, [p_r_stem, p_r_arch]))

    # --- s ---
    w_s = 500.0 + stem * 0.3
    lsb_s = 60.0
    rsb_s = w_s - 60.0
    cx_s = w_s / 2.0
    p_s = Path()
    p_s.move_to(rsb_s - 20.0, x_h - 100.0)
    p_s.arc_to(cx_s, x_h - 130.0, (w_s - 120.0)/2.0, 130.0 + ov, 30, 180, clockwise=False, steps=4)
    p_s.arc_to(cx_s, 130.0, (w_s - 120.0)/2.0, 130.0 + ov, 0, -150, clockwise=True, steps=4)
    p_s.line_to(lsb_s + 20.0, 100.0)
    p_s.arc_to(cx_s, 130.0, max(10.0, (w_s - 120.0)/2.0 - stem), max(10.0, 130.0 + ov - stem_h), -150, 0, clockwise=False, steps=4)
    p_s.arc_to(cx_s, x_h - 130.0, max(10.0, (w_s - 120.0)/2.0 - stem), max(10.0, 130.0 + ov - stem_h), 180, 30, clockwise=True, steps=4)
    p_s.close()
    add_glyph(GlyphSpec('s', 0x0073, w_s, lsb_s, [p_s]))

    # --- t (Straight stem with curved bottom hook, crossbar at x-height) ---
    w_t = 360.0 + stem * 0.3
    cx_t = 110.0
    p_t = Path()
    p_t.move_to(cx_t, 650.0)
    p_t.line_to(cx_t + stem, 650.0)
    p_t.line_to(cx_t + stem, 120.0)
    p_t.arc_to(cx_t + stem + 70.0, 120.0, 70.0, 120.0 + ov, 180, 270, clockwise=True, steps=2)
    p_t.line_to(w_t - 30.0, 0.0)
    p_t.line_to(w_t - 30.0, stem_h)
    p_t.line_to(cx_t + stem + 70.0, stem_h)
    p_t.arc_to(cx_t + stem + 70.0, 120.0, max(10.0, 70.0 - stem), max(10.0, 120.0 + ov - stem_h), 270, 180, clockwise=False, steps=2)
    p_t.line_to(cx_t, 650.0)
    p_t.close()
    
    p_t_bar = Path()
    p_t_bar.rect(40.0, x_h - stem_h, w_t - 60.0, stem_h)
    add_glyph(GlyphSpec('t', 0x0074, w_t, 40.0, [p_t, p_t_bar]))

    # --- u ---
    w_u = 600.0 + stem * 0.4
    lsb_u = 60.0
    rsb_u = w_u - 60.0
    cx_u = w_u / 2.0
    p_u = Path()
    p_u.move_to(lsb_u, x_h)
    p_u.line_to(lsb_u + stem, x_h)
    p_u.line_to(lsb_u + stem, 160.0)
    p_u.arc_to(cx_u, 160.0, max(10.0, (w_u - 120.0)/2.0 - stem), max(10.0, 160.0 + ov - stem_h), 180, 0, clockwise=True, steps=4)
    p_u.line_to(rsb_u - stem, x_h)
    p_u.line_to(rsb_u, x_h)
    p_u.line_to(rsb_u, 160.0)
    p_u.arc_to(cx_u, 160.0, (w_u - 120.0)/2.0, 160.0 + ov, 0, -180, clockwise=True, steps=4)
    p_u.line_to(lsb_u, x_h)
    p_u.close()
    add_glyph(GlyphSpec('u', 0x0075, w_u, lsb_u, [p_u]))

    # --- v ---
    w_v = 560.0 + stem * 0.35
    lsb_v = 30.0
    rsb_v = w_v - 30.0
    cx_v = w_v / 2.0
    p_v = Path()
    p_v.move_to(lsb_v, x_h)
    p_v.line_to(lsb_v + stem*1.1, x_h)
    p_v.line_to(cx_v, stem_h*0.8)
    p_v.line_to(rsb_v - stem*1.1, x_h)
    p_v.line_to(rsb_v, x_h)
    p_v.line_to(cx_v + stem*0.3, 0.0)
    p_v.line_to(cx_v - stem*0.3, 0.0)
    p_v.close()
    add_glyph(GlyphSpec('v', 0x0076, w_v, lsb_v, [p_v]))

    # --- w ---
    w_w = 820.0 + stem * 0.5
    lsb_w = 30.0
    rsb_w = w_w - 30.0
    p_w = Path()
    p_w.move_to(lsb_w, x_h)
    p_w.line_to(lsb_w + stem*0.9, x_h)
    p_w.line_to(lsb_w + 170.0, 0.0)
    p_w.line_to(lsb_w + 170.0 + stem*0.8, 0.0)
    p_w.line_to(w_w / 2.0, x_h - 130.0)
    p_w.line_to(rsb_w - 170.0 - stem*0.8, 0.0)
    p_w.line_to(rsb_w - 170.0, 0.0)
    p_w.line_to(rsb_w - stem*0.9, x_h)
    p_w.line_to(rsb_w, x_h)
    p_w.line_to(rsb_w - 160.0, 0.0)
    p_w.line_to(w_w / 2.0, x_h - 180.0)
    p_w.line_to(lsb_w + 160.0, 0.0)
    p_w.close()
    add_glyph(GlyphSpec('w', 0x0077, w_w, lsb_w, [p_w]))

    # --- x ---
    w_x = 540.0 + stem * 0.35
    lsb_x = 40.0
    rsb_x = w_x - 40.0
    p_x1 = Path()
    p_x1.move_to(lsb_x, x_h)
    p_x1.line_to(lsb_x + stem*1.1, x_h)
    p_x1.line_to(rsb_x, 0.0)
    p_x1.line_to(rsb_x - stem*1.1, 0.0)
    p_x1.close()
    p_x2 = Path()
    p_x2.move_to(rsb_x - stem*1.1, x_h)
    p_x2.line_to(rsb_x, x_h)
    p_x2.line_to(lsb_x + stem*1.1, 0.0)
    p_x2.line_to(lsb_x, 0.0)
    p_x2.close()
    add_glyph(GlyphSpec('x', 0x0078, w_x, lsb_x, [p_x1, p_x2]))

    # --- y ---
    w_y = 560.0 + stem * 0.35
    lsb_y = 30.0
    rsb_y = w_y - 30.0
    cx_y = w_y / 2.0
    p_y = Path()
    p_y.move_to(lsb_y, x_h)
    p_y.line_to(lsb_y + stem*1.1, x_h)
    p_y.line_to(cx_y, 160.0)
    p_y.line_to(lsb_y + 40.0, desc + 40.0)
    p_y.arc_to(lsb_y + 80.0, desc + 40.0, 40.0, 40.0, 180, 270, clockwise=True, steps=2)
    p_y.line_to(cx_y, desc)
    p_y.line_to(rsb_y, x_h)
    p_y.line_to(rsb_y - stem*1.1, x_h)
    p_y.line_to(cx_y + stem*0.3, 160.0)
    p_y.close()
    add_glyph(GlyphSpec('y', 0x0079, w_y, lsb_y, [p_y]))

    # --- z ---
    w_z = 500.0 + stem * 0.3
    lsb_z = 50.0
    rsb_z = w_z - 50.0
    p_z = Path()
    p_z.move_to(lsb_z, x_h)
    p_z.line_to(rsb_z, x_h)
    p_z.line_to(rsb_z, x_h - stem_h)
    p_z.line_to(lsb_z + stem*1.2, stem_h)
    p_z.line_to(rsb_z, stem_h)
    p_z.line_to(rsb_z, 0.0)
    p_z.line_to(lsb_z, 0.0)
    p_z.line_to(lsb_z, stem_h)
    p_z.line_to(rsb_z - stem*1.2, x_h - stem_h)
    p_z.line_to(lsb_z, x_h - stem_h)
    p_z.close()
    add_glyph(GlyphSpec('z', 0x007A, w_z, lsb_z, [p_z]))

    # -------------------------------------------------------------
    # FIGURES 0-9 (Lining Modern Proportional)
    # -------------------------------------------------------------

    # --- zero ---
    w_0 = 640.0 + stem * 0.4
    cx_0 = w_0 / 2.0
    cy_0 = cap_h / 2.0
    rx_0 = (w_0 - 80.0) / 2.0
    ry_0 = (cap_h + 2*ov) / 2.0
    p_0 = Path()
    p_0.donut(cx_0, cy_0, rx_0, ry_0, max(10.0, rx_0 - stem), max(10.0, ry_0 - stem_h))
    add_glyph(GlyphSpec('zero', 0x0030, w_0, 40.0, [p_0]))

    # --- one ---
    w_1 = 440.0 + stem * 0.3
    cx_1 = w_1 / 2.0 + 20.0
    p_1 = Path()
    p_1.move_to(cx_1 - stem/2.0, 0.0)
    p_1.line_to(cx_1 + stem/2.0, 0.0)
    p_1.line_to(cx_1 + stem/2.0, cap_h)
    p_1.line_to(cx_1 - 130.0, cap_h - 110.0)
    p_1.line_to(cx_1 - 130.0 + stem*0.8, cap_h - 110.0)
    p_1.line_to(cx_1 - stem/2.0, cap_h - 40.0)
    p_1.close()
    add_glyph(GlyphSpec('one', 0x0031, w_1, 60.0, [p_1]))

    # --- two ---
    w_2 = 580.0 + stem * 0.35
    lsb_2 = 60.0
    rsb_2 = w_2 - 60.0
    p_2 = Path()
    p_2.move_to(lsb_2 + 20.0, cap_h - 140.0)
    p_2.arc_to(w_2 / 2.0, cap_h - 170.0, (w_2 - 120.0)/2.0, 170.0 + ov, 150, 0, clockwise=False, steps=4)
    p_2.line_to(lsb_2, stem_h)
    p_2.line_to(rsb_2, stem_h)
    p_2.line_to(rsb_2, 0.0)
    p_2.line_to(lsb_2, 0.0)
    p_2.line_to(lsb_2, stem_h*1.2)
    p_2.line_to(rsb_2 - stem*1.3, cap_h - 220.0)
    p_2.arc_to(w_2 / 2.0, cap_h - 170.0, max(10.0, (w_2 - 120.0)/2.0 - stem), max(10.0, 170.0 + ov - stem_h), 0, 150, clockwise=True, steps=4)
    p_2.close()
    add_glyph(GlyphSpec('two', 0x0032, w_2, lsb_2, [p_2]))

    # --- three ---
    w_3 = 580.0 + stem * 0.35
    lsb_3 = 60.0
    rsb_3 = w_3 - 60.0
    cx_3 = w_3 / 2.0
    y_m3 = 360.0
    p_3 = Path()
    p_3.move_to(lsb_3 + 30.0, cap_h - 120.0)
    p_3.arc_to(cx_3, (cap_h + y_m3)/2.0, (w_3 - 120.0)/2.0, (cap_h - y_m3)/2.0 + ov, 140, -40, clockwise=False, steps=4)
    p_3.arc_to(cx_3, y_m3/2.0, (w_3 - 120.0)/2.0, y_m3/2.0 + ov, 40, -140, clockwise=False, steps=4)
    p_3.line_to(lsb_3 + 30.0, 100.0)
    p_3.arc_to(cx_3, y_m3/2.0, max(10.0, (w_3 - 120.0)/2.0 - stem), max(10.0, y_m3/2.0 + ov - stem_h), -140, 40, clockwise=True, steps=4)
    p_3.arc_to(cx_3, (cap_h + y_m3)/2.0, max(10.0, (w_3 - 120.0)/2.0 - stem), max(10.0, (cap_h - y_m3)/2.0 + ov - stem_h), -40, 140, clockwise=True, steps=4)
    p_3.close()
    add_glyph(GlyphSpec('three', 0x0033, w_3, lsb_3, [p_3]))

    # --- four ---
    w_4 = 600.0 + stem * 0.35
    lsb_4 = 50.0
    rsb_4 = w_4 - 50.0
    p_4_frame = Path()
    p_4_frame.move_to(rsb_4 - 100.0 - stem, 0.0)
    p_4_frame.line_to(rsb_4 - 100.0, 0.0)
    p_4_frame.line_to(rsb_4 - 100.0, 200.0)
    p_4_frame.line_to(rsb_4, 200.0)
    p_4_frame.line_to(rsb_4, 200.0 + stem_h)
    p_4_frame.line_to(rsb_4 - 100.0, 200.0 + stem_h)
    p_4_frame.line_to(rsb_4 - 100.0, cap_h)
    p_4_frame.line_to(rsb_4 - 100.0 - stem, cap_h)
    p_4_frame.line_to(lsb_4, 200.0 + stem_h)
    p_4_frame.line_to(lsb_4, 200.0)
    p_4_frame.line_to(rsb_4 - 100.0 - stem, 200.0)
    p_4_frame.close()
    
    p_4_in = Path()
    p_4_in.move_to(lsb_4 + stem*1.4, 200.0 + stem_h)
    p_4_in.line_to(rsb_4 - 100.0 - stem, cap_h - stem*1.6)
    p_4_in.line_to(rsb_4 - 100.0 - stem, 200.0 + stem_h)
    p_4_in.close()
    add_glyph(GlyphSpec('four', 0x0034, w_4, lsb_4, [p_4_frame, p_4_in]))

    # --- five ---
    w_5 = 580.0 + stem * 0.35
    lsb_5 = 60.0
    rsb_5 = w_5 - 60.0
    cx_5 = w_5 / 2.0
    p_5 = Path()
    p_5.move_to(lsb_5, cap_h)
    p_5.line_to(rsb_5, cap_h)
    p_5.line_to(rsb_5, cap_h - stem_h)
    p_5.line_to(lsb_5 + stem, cap_h - stem_h)
    p_5.line_to(lsb_5 + stem, 360.0)
    p_5.arc_to(cx_5, 190.0, (w_5 - 120.0)/2.0, 190.0 + ov, 90, -140, clockwise=True, steps=5)
    p_5.line_to(lsb_5 + 30.0, 80.0)
    p_5.arc_to(cx_5, 190.0, max(10.0, (w_5 - 120.0)/2.0 - stem), max(10.0, 190.0 + ov - stem_h), -140, 90, clockwise=False, steps=5)
    p_5.line_to(lsb_5, 360.0)
    p_5.close()
    add_glyph(GlyphSpec('five', 0x0035, w_5, lsb_5, [p_5]))

    # --- six ---
    w_6 = 620.0 + stem * 0.4
    cx_6 = w_6 / 2.0
    cy_6 = 220.0
    rx_6 = (w_6 - 80.0) / 2.0
    ry_6 = (440.0 + 2*ov) / 2.0
    p_6_bowl = Path()
    p_6_bowl.donut(cx_6, cy_6, rx_6, ry_6, max(10.0, rx_6 - stem), max(10.0, ry_6 - stem_h))
    p_6_spine = Path()
    p_6_spine.move_to(cx_6 - rx_6 + stem, 220.0)
    p_6_spine.arc_to(cx_6, 460.0, rx_6, 240.0 + ov, 180, 45, clockwise=False, steps=4)
    p_6_spine.line_to(w_6 - 60.0, cap_h - 40.0)
    p_6_spine.arc_to(cx_6, 460.0, max(10.0, rx_6 - stem), max(10.0, 240.0 + ov - stem_h), 45, 180, clockwise=True, steps=4)
    p_6_spine.close()
    add_glyph(GlyphSpec('six', 0x0036, w_6, 40.0, [p_6_bowl, p_6_spine]))

    # --- seven ---
    w_7 = 580.0 + stem * 0.35
    lsb_7 = 60.0
    rsb_7 = w_7 - 60.0
    p_7 = Path()
    p_7.move_to(lsb_7, cap_h)
    p_7.line_to(rsb_7, cap_h)
    p_7.line_to(lsb_7 + 100.0, 0.0)
    p_7.line_to(lsb_7 + 100.0 - stem*1.1, 0.0)
    p_7.line_to(rsb_7 - stem*1.2, cap_h - stem_h)
    p_7.line_to(lsb_7, cap_h - stem_h)
    p_7.close()
    add_glyph(GlyphSpec('seven', 0x0037, w_7, lsb_7, [p_7]))

    # --- eight ---
    w_8 = 600.0 + stem * 0.4
    cx_8 = w_8 / 2.0
    cy_8_bot = 200.0
    cy_8_top = cap_h - 180.0
    rx_8_bot = (w_8 - 80.0) / 2.0
    ry_8_bot = (400.0 + 2*ov) / 2.0
    rx_8_top = rx_8_bot * 0.90
    ry_8_top = (360.0 + 2*ov) / 2.0
    p_8_bot = Path()
    p_8_bot.donut(cx_8, cy_8_bot, rx_8_bot, ry_8_bot, max(10.0, rx_8_bot - stem), max(10.0, ry_8_bot - stem_h))
    p_8_top = Path()
    p_8_top.donut(cx_8, cy_8_top, rx_8_top, ry_8_top, max(10.0, rx_8_top - stem), max(10.0, ry_8_top - stem_h))
    add_glyph(GlyphSpec('eight', 0x0038, w_8, 40.0, [p_8_bot, p_8_top]))

    # --- nine ---
    w_9 = 620.0 + stem * 0.4
    cx_9 = w_9 / 2.0
    cy_9 = cap_h - 220.0
    rx_9 = (w_9 - 80.0) / 2.0
    ry_9 = (440.0 + 2*ov) / 2.0
    p_9_bowl = Path()
    p_9_bowl.donut(cx_9, cy_9, rx_9, ry_9, max(10.0, rx_9 - stem), max(10.0, ry_9 - stem_h))
    p_9_spine = Path()
    p_9_spine.move_to(cx_9 + rx_9 - stem, cy_9)
    p_9_spine.arc_to(cx_9, 240.0, rx_9, 240.0 + ov, 0, -135, clockwise=True, steps=4)
    p_9_spine.line_to(60.0, 40.0)
    p_9_spine.arc_to(cx_9, 240.0, max(10.0, rx_9 - stem), max(10.0, 240.0 + ov - stem_h), -135, 0, clockwise=False, steps=4)
    p_9_spine.close()
    add_glyph(GlyphSpec('nine', 0x0039, w_9, 40.0, [p_9_bowl, p_9_spine]))

    # -------------------------------------------------------------
    # PUNCTUATION & SYMBOLS
    # -------------------------------------------------------------

    # --- period (Clean Circular Dot) ---
    w_period = 260.0 + stem * 0.4
    r_dot_base = max(20.0, stem * 0.6)
    p_period = Path()
    p_period.circle(w_period / 2.0, r_dot_base, r_dot_base)
    add_glyph(GlyphSpec('period', 0x002E, w_period, w_period/2.0 - r_dot_base, [p_period]))

    # --- comma ---
    w_comma = w_period
    p_comma = Path()
    p_comma.circle(w_comma / 2.0, r_dot_base, r_dot_base)
    p_comma_tail = Path()
    p_comma_tail.move_to(w_comma / 2.0 + r_dot_base*0.8, r_dot_base)
    p_comma_tail.line_to(w_comma / 2.0 - r_dot_base*0.8, -60.0)
    p_comma_tail.line_to(w_comma / 2.0 - r_dot_base*0.2, -60.0)
    p_comma_tail.line_to(w_comma / 2.0 + r_dot_base*0.8, 0.0)
    p_comma_tail.close()
    add_glyph(GlyphSpec('comma', 0x002C, w_comma, 40.0, [p_comma, p_comma_tail]))

    # --- colon ---
    w_colon = w_period
    p_colon1 = Path()
    p_colon1.circle(w_colon / 2.0, r_dot_base, r_dot_base)
    p_colon2 = Path()
    p_colon2.circle(w_colon / 2.0, x_h - r_dot_base, r_dot_base)
    add_glyph(GlyphSpec('colon', 0x003A, w_colon, 40.0, [p_colon1, p_colon2]))

    # --- semicolon ---
    w_semi = w_period
    p_semi_top = Path()
    p_semi_top.circle(w_semi / 2.0, x_h - r_dot_base, r_dot_base)
    p_semi_bot = Path()
    p_semi_bot.circle(w_semi / 2.0, r_dot_base, r_dot_base)
    p_semi_tail = Path()
    p_semi_tail.move_to(w_semi / 2.0 + r_dot_base*0.8, r_dot_base)
    p_semi_tail.line_to(w_semi / 2.0 - r_dot_base*0.8, -60.0)
    p_semi_tail.line_to(w_semi / 2.0 - r_dot_base*0.2, -60.0)
    p_semi_tail.line_to(w_semi / 2.0 + r_dot_base*0.8, 0.0)
    p_semi_tail.close()
    add_glyph(GlyphSpec('semicolon', 0x003B, w_semi, 40.0, [p_semi_top, p_semi_bot, p_semi_tail]))

    # --- exclam ---
    w_exclam = 280.0 + stem * 0.4
    cx_ex = w_exclam / 2.0
    p_ex_bar = Path()
    p_ex_bar.move_to(cx_ex - stem/2.0, cap_h)
    p_ex_bar.line_to(cx_ex + stem/2.0, cap_h)
    p_ex_bar.line_to(cx_ex + stem*0.35, 180.0)
    p_ex_bar.line_to(cx_ex - stem*0.35, 180.0)
    p_ex_bar.close()
    p_ex_dot = Path()
    p_ex_dot.circle(cx_ex, r_dot_base, r_dot_base)
    add_glyph(GlyphSpec('exclam', 0x0021, w_exclam, cx_ex - stem/2.0, [p_ex_bar, p_ex_dot]))

    # --- question ---
    w_q = 500.0 + stem * 0.3
    cx_q = w_q / 2.0
    p_q_hook = Path()
    p_q_hook.move_to(cx_q - 130.0, cap_h - 130.0)
    p_q_hook.arc_to(cx_q, cap_h - 170.0, 140.0, 170.0 + ov, 150, 0, clockwise=False, steps=4)
    p_q_hook.line_to(cx_q + stem/2.0, 200.0)
    p_q_hook.line_to(cx_q - stem/2.0, 200.0)
    p_q_hook.line_to(cx_q - stem/2.0, cap_h - 220.0)
    p_q_hook.arc_to(cx_q, cap_h - 170.0, max(10.0, 140.0 - stem), max(10.0, 170.0 + ov - stem_h), 0, 150, clockwise=True, steps=4)
    p_q_hook.close()
    p_q_dot = Path()
    p_q_dot.circle(cx_q, r_dot_base, r_dot_base)
    add_glyph(GlyphSpec('question', 0x003F, w_q, 60.0, [p_q_hook, p_q_dot]))

    # --- hyphen ---
    w_hyph = 360.0 + stem * 0.3
    p_hyph = Path()
    p_hyph.rect(60.0, 260.0 - stem_h/2.0, w_hyph - 120.0, stem_h)
    add_glyph(GlyphSpec('hyphen', 0x002D, w_hyph, 60.0, [p_hyph]))

    # --- endash ---
    w_endash = 540.0 + stem * 0.3
    p_endash = Path()
    p_endash.rect(60.0, 260.0 - stem_h/2.0, w_endash - 120.0, stem_h)
    add_glyph(GlyphSpec('endash', 0x2013, w_endash, 60.0, [p_endash]))

    # --- emdash ---
    w_emdash = 840.0 + stem * 0.4
    p_emdash = Path()
    p_emdash.rect(50.0, 260.0 - stem_h/2.0, w_emdash - 100.0, stem_h)
    add_glyph(GlyphSpec('emdash', 0x2014, w_emdash, 50.0, [p_emdash]))

    # --- underscore ---
    w_under = 540.0 + stem * 0.3
    p_under = Path()
    p_under.rect(30.0, -120.0, w_under - 60.0, stem_h)
    add_glyph(GlyphSpec('underscore', 0x005F, w_under, 30.0, [p_under]))

    # --- slash ---
    w_slash = 460.0 + stem * 0.3
    p_slash = Path()
    p_slash.move_to(50.0, -80.0)
    p_slash.line_to(50.0 + stem*1.1, -80.0)
    p_slash.line_to(w_slash - 50.0, cap_h + 80.0)
    p_slash.line_to(w_slash - 50.0 - stem*1.1, cap_h + 80.0)
    p_slash.close()
    add_glyph(GlyphSpec('slash', 0x002F, w_slash, 50.0, [p_slash]))

    # --- backslash ---
    w_bslash = w_slash
    p_bslash = Path()
    p_bslash.move_to(50.0, cap_h + 80.0)
    p_bslash.line_to(50.0 + stem*1.1, cap_h + 80.0)
    p_bslash.line_to(w_bslash - 50.0, -80.0)
    p_bslash.line_to(w_bslash - 50.0 - stem*1.1, -80.0)
    p_bslash.close()
    add_glyph(GlyphSpec('backslash', 0x005C, w_bslash, 50.0, [p_bslash]))

    # --- bar ---
    w_bar = 260.0 + stem * 0.4
    p_bar = Path()
    p_bar.rect(w_bar/2.0 - stem/2.0, -140.0, stem, cap_h + 280.0)
    add_glyph(GlyphSpec('bar', 0x007C, w_bar, w_bar/2.0 - stem/2.0, [p_bar]))

    # --- parenleft ---
    w_paren = 360.0 + stem * 0.3
    cx_pl = w_paren - 40.0
    cy_pl = 250.0
    rx_pl = 200.0
    ry_pl = 450.0
    p_pl = Path()
    p_pl.move_to(cx_pl, cy_pl + ry_pl)
    p_pl.arc_to(cx_pl, cy_pl, rx_pl, ry_pl, 90, 270, clockwise=False, steps=4)
    p_pl.line_to(cx_pl, cy_pl - ry_pl)
    p_pl.arc_to(cx_pl, cy_pl, max(10.0, rx_pl - stem), max(10.0, ry_pl - stem_h), 270, 90, clockwise=True, steps=4)
    p_pl.close()
    add_glyph(GlyphSpec('parenleft', 0x0028, w_paren, 50.0, [p_pl]))

    # --- parenright ---
    w_pr = w_paren
    cx_pr = 40.0
    p_pr = Path()
    p_pr.move_to(cx_pr, cy_pl + ry_pl)
    p_pr.arc_to(cx_pr, cy_pl, rx_pl, ry_pl, 90, -90, clockwise=True, steps=4)
    p_pr.line_to(cx_pr, cy_pl - ry_pl)
    p_pr.arc_to(cx_pr, cy_pl, max(10.0, rx_pl - stem), max(10.0, ry_pl - stem_h), -90, 90, clockwise=False, steps=4)
    p_pr.close()
    add_glyph(GlyphSpec('parenright', 0x0029, w_pr, 50.0, [p_pr]))

    # --- bracketleft ---
    w_brk = 340.0 + stem * 0.3
    lsb_brk = 70.0
    p_bl = Path()
    p_bl.rect(lsb_brk, -100.0, stem, cap_h + 200.0)
    p_bl_top = Path()
    p_bl_top.rect(lsb_brk, cap_h + 100.0 - stem_h, 150.0, stem_h)
    p_bl_bot = Path()
    p_bl_bot.rect(lsb_brk, -100.0, 150.0, stem_h)
    add_glyph(GlyphSpec('bracketleft', 0x005B, w_brk, lsb_brk, [p_bl, p_bl_top, p_bl_bot]))

    # --- bracketright ---
    w_brkr = w_brk
    rsb_brkr = w_brkr - 70.0
    p_br = Path()
    p_br.rect(rsb_brkr - stem, -100.0, stem, cap_h + 200.0)
    p_br_top = Path()
    p_br_top.rect(rsb_brkr - 150.0, cap_h + 100.0 - stem_h, 150.0, stem_h)
    p_br_bot = Path()
    p_br_bot.rect(rsb_brkr - 150.0, -100.0, 150.0, stem_h)
    add_glyph(GlyphSpec('bracketright', 0x005D, w_brkr, rsb_brkr - 150.0, [p_br, p_br_top, p_br_bot]))

    # --- braceleft ---
    w_brace = 380.0 + stem * 0.3
    cx_brc = w_brace - 60.0
    p_bcl = Path()
    p_bcl.move_to(cx_brc, cap_h + 80.0)
    p_bcl.line_to(cx_brc - 100.0, cap_h + 80.0)
    p_bcl.line_to(cx_brc - 100.0, 370.0)
    p_bcl.line_to(cx_brc - 160.0, 300.0)
    p_bcl.line_to(cx_brc - 100.0, 230.0)
    p_bcl.line_to(cx_brc - 100.0, -80.0)
    p_bcl.line_to(cx_brc, -80.0)
    p_bcl.line_to(cx_brc, -80.0 + stem_h)
    p_bcl.line_to(cx_brc - 100.0 + stem, -80.0 + stem_h)
    p_bcl.line_to(cx_brc - 100.0 + stem, 220.0)
    p_bcl.line_to(cx_brc - 160.0 + stem*1.4, 300.0)
    p_bcl.line_to(cx_brc - 100.0 + stem, 380.0)
    p_bcl.line_to(cx_brc - 100.0 + stem, cap_h + 80.0 - stem_h)
    p_bcl.line_to(cx_brc, cap_h + 80.0 - stem_h)
    p_bcl.close()
    add_glyph(GlyphSpec('braceleft', 0x007B, w_brace, 50.0, [p_bcl]))

    # --- braceright ---
    w_brcr = w_brace
    cx_brcr = 60.0
    p_bcr = Path()
    p_bcr.move_to(cx_brcr, cap_h + 80.0)
    p_bcr.line_to(cx_brcr + 100.0, cap_h + 80.0)
    p_bcr.line_to(cx_brcr + 100.0, 370.0)
    p_bcr.line_to(cx_brcr + 160.0, 300.0)
    p_bcr.line_to(cx_brcr + 100.0, 230.0)
    p_bcr.line_to(cx_brcr + 100.0, -80.0)
    p_bcr.line_to(cx_brcr, -80.0)
    p_bcr.line_to(cx_brcr, -80.0 + stem_h)
    p_bcr.line_to(cx_brcr + 100.0 - stem, -80.0 + stem_h)
    p_bcr.line_to(cx_brcr + 100.0 - stem, 220.0)
    p_bcr.line_to(cx_brcr + 160.0 - stem*1.4, 300.0)
    p_bcr.line_to(cx_brcr + 100.0 - stem, 380.0)
    p_bcr.line_to(cx_brcr + 100.0 - stem, cap_h + 80.0 - stem_h)
    p_bcr.line_to(cx_brcr, cap_h + 80.0 - stem_h)
    p_bcr.close()
    add_glyph(GlyphSpec('braceright', 0x007D, w_brcr, 60.0, [p_bcr]))

    # --- quotesingle ---
    w_qs = 240.0 + stem * 0.4
    p_qs = Path()
    p_qs.rect(w_qs/2.0 - stem/2.0, cap_h - 220.0, stem, 220.0)
    add_glyph(GlyphSpec('quotesingle', 0x0027, w_qs, w_qs/2.0 - stem/2.0, [p_qs]))

    # --- quotedbl ---
    w_qd = 380.0 + stem * 0.6
    p_qd1 = Path()
    p_qd1.rect(w_qd/2.0 - stem*1.1, cap_h - 220.0, stem, 220.0)
    p_qd2 = Path()
    p_qd2.rect(w_qd/2.0 + stem*0.1, cap_h - 220.0, stem, 220.0)
    add_glyph(GlyphSpec('quotedbl', 0x0022, w_qd, 60.0, [p_qd1, p_qd2]))

    # --- quoteleft / quoteright ---
    p_ql = Path()
    p_ql.circle(w_qs/2.0, cap_h - 100.0, r_dot_base)
    p_ql_tail = Path()
    p_ql_tail.move_to(w_qs/2.0 - r_dot_base*0.8, cap_h - 100.0)
    p_ql_tail.line_to(w_qs/2.0 + r_dot_base*0.8, cap_h - 190.0)
    p_ql_tail.line_to(w_qs/2.0 + r_dot_base*0.2, cap_h - 190.0)
    p_ql_tail.line_to(w_qs/2.0 - r_dot_base*0.8, cap_h - 140.0)
    p_ql_tail.close()
    add_glyph(GlyphSpec('quoteleft', 0x2018, w_qs, 40.0, [p_ql, p_ql_tail]))

    p_qr = Path()
    p_qr.circle(w_qs/2.0, cap_h - 100.0, r_dot_base)
    p_qr_tail = Path()
    p_qr_tail.move_to(w_qs/2.0 + r_dot_base*0.8, cap_h - 100.0)
    p_qr_tail.line_to(w_qs/2.0 - r_dot_base*0.8, cap_h - 190.0)
    p_qr_tail.line_to(w_qs/2.0 - r_dot_base*0.2, cap_h - 190.0)
    p_qr_tail.line_to(w_qs/2.0 + r_dot_base*0.8, cap_h - 140.0)
    p_qr_tail.close()
    add_glyph(GlyphSpec('quoteright', 0x2019, w_qs, 40.0, [p_qr, p_qr_tail]))

    # --- plus ---
    w_plus = 560.0 + stem * 0.4
    cx_plu = w_plus / 2.0
    cy_plu = 280.0
    p_plus_h = Path()
    p_plus_h.rect(80.0, cy_plu - stem_h/2.0, w_plus - 160.0, stem_h)
    p_plus_v = Path()
    p_plus_v.rect(cx_plu - stem/2.0, cy_plu - (w_plus - 160.0)/2.0, stem, w_plus - 160.0)
    add_glyph(GlyphSpec('plus', 0x002B, w_plus, 80.0, [p_plus_h, p_plus_v]))

    # --- equal ---
    w_eq = 560.0 + stem * 0.4
    p_eq1 = Path()
    p_eq1.rect(80.0, 360.0 - stem_h/2.0, w_eq - 160.0, stem_h)
    p_eq2 = Path()
    p_eq2.rect(80.0, 200.0 - stem_h/2.0, w_eq - 160.0, stem_h)
    add_glyph(GlyphSpec('equal', 0x003D, w_eq, 80.0, [p_eq1, p_eq2]))

    # --- less / greater ---
    w_lt = 540.0 + stem * 0.35
    p_lt = Path()
    p_lt.move_to(w_lt - 80.0, 460.0)
    p_lt.line_to(80.0, 280.0)
    p_lt.line_to(w_lt - 80.0, 100.0)
    p_lt.line_to(w_lt - 80.0 - stem*1.1, 100.0)
    p_lt.line_to(80.0 + stem*1.4, 280.0)
    p_lt.line_to(w_lt - 80.0 - stem*1.1, 460.0)
    p_lt.close()
    add_glyph(GlyphSpec('less', 0x003C, w_lt, 80.0, [p_lt]))

    p_gt = Path()
    p_gt.move_to(80.0, 460.0)
    p_gt.line_to(w_lt - 80.0, 280.0)
    p_gt.line_to(80.0, 100.0)
    p_gt.line_to(80.0 + stem*1.1, 100.0)
    p_gt.line_to(w_lt - 80.0 - stem*1.4, 280.0)
    p_gt.line_to(80.0 + stem*1.1, 460.0)
    p_gt.close()
    add_glyph(GlyphSpec('greater', 0x003E, w_lt, 80.0, [p_gt]))

    # --- at (@) ---
    w_at = 820.0 + stem * 0.5
    cx_at = w_at / 2.0
    cy_at = x_h / 2.0
    p_at_out = Path()
    p_at_out.donut(cx_at, cy_at, (w_at - 80.0)/2.0, (x_h + 240.0)/2.0, max(10.0, (w_at - 80.0)/2.0 - stem), max(10.0, (x_h + 240.0)/2.0 - stem_h))
    p_at_in = Path()
    p_at_in.circle(cx_at, cy_at, max(10.0, (w_at - 320.0)/2.0 - stem))
    add_glyph(GlyphSpec('at', 0x0040, w_at, 40.0, [p_at_out, p_at_in]))

    # --- numbersign (#) ---
    w_hash = 600.0 + stem * 0.4
    p_h1 = Path()
    p_h1.rect(50.0, 420.0 - stem_h/2.0, w_hash - 100.0, stem_h)
    p_h2 = Path()
    p_h2.rect(50.0, 220.0 - stem_h/2.0, w_hash - 100.0, stem_h)
    p_v1 = Path()
    p_v1.rect(w_hash/2.0 - 100.0 - stem/2.0, 60.0, stem, 520.0)
    p_v2 = Path()
    p_v2.rect(w_hash/2.0 + 100.0 - stem/2.0, 60.0, stem, 520.0)
    add_glyph(GlyphSpec('numbersign', 0x0023, w_hash, 50.0, [p_h1, p_h2, p_v1, p_v2]))

    # --- percent (%) ---
    w_pct = 780.0 + stem * 0.4
    p_pct_sl = Path()
    p_pct_sl.move_to(100.0, 60.0)
    p_pct_sl.line_to(100.0 + stem*1.1, 60.0)
    p_pct_sl.line_to(w_pct - 100.0, cap_h - 60.0)
    p_pct_sl.line_to(w_pct - 100.0 - stem*1.1, cap_h - 60.0)
    p_pct_sl.close()
    r_pct = 70.0
    p_pct1 = Path()
    p_pct1.donut(220.0, cap_h - 150.0, r_pct, r_pct, max(10.0, r_pct - stem*0.8), max(10.0, r_pct - stem_h*0.8))
    p_pct2 = Path()
    p_pct2.donut(w_pct - 220.0, 150.0, r_pct, r_pct, max(10.0, r_pct - stem*0.8), max(10.0, r_pct - stem_h*0.8))
    add_glyph(GlyphSpec('percent', 0x0025, w_pct, 60.0, [p_pct_sl, p_pct1, p_pct2]))

    # --- ampersand (&) ---
    w_amp = 680.0 + stem * 0.4
    cx_amp = w_amp / 2.0
    p_amp = Path()
    p_amp.circle(cx_amp, 180.0, 180.0)
    p_amp2 = Path()
    p_amp2.circle(cx_amp - 20.0, cap_h - 200.0, 140.0)
    add_glyph(GlyphSpec('ampersand', 0x0026, w_amp, 50.0, [p_amp, p_amp2]))

    # --- asterisk (*) ---
    w_ast = 440.0 + stem * 0.3
    cx_ast = w_ast / 2.0
    cy_ast = cap_h - 180.0
    r_ast = 130.0
    p_ast1 = Path()
    p_ast1.rect(cx_ast - stem/2.0, cy_ast - r_ast, stem, 2*r_ast)
    p_ast2 = Path()
    p_ast2.rect(cx_ast - r_ast, cy_ast - stem_h/2.0, 2*r_ast, stem_h)
    add_glyph(GlyphSpec('asterisk', 0x002A, w_ast, cx_ast - r_ast, [p_ast1, p_ast2]))

    # -------------------------------------------------------------
    # CURRENCY (₹ Rupee, € Euro, $ Dollar, £ Pound, ¥ Yen)
    # -------------------------------------------------------------

    # --- Indian Rupee (₹) - Special Signature for Om Sans! ---
    w_rup = 640.0 + stem * 0.4
    lsb_rup = 70.0
    rsb_rup = w_rup - 70.0
    p_rup_bar1 = Path()
    p_rup_bar1.rect(lsb_rup, cap_h - stem_h, rsb_rup - lsb_rup, stem_h)
    p_rup_bar2 = Path()
    p_rup_bar2.rect(lsb_rup, cap_h - stem_h*2.5, rsb_rup - lsb_rup, stem_h)
    
    p_rup_stem = Path()
    p_rup_stem.rect(lsb_rup + 40.0, 260.0, stem, cap_h - 260.0)
    
    # Upper loop
    p_rup_loop = Path()
    p_rup_loop.move_to(lsb_rup + 40.0 + stem, cap_h - stem_h*2.5)
    p_rup_loop.arc_to(lsb_rup + 40.0 + 130.0, 420.0, 130.0, 100.0, 90, -90, clockwise=True, steps=4)
    p_rup_loop.line_to(lsb_rup + 40.0, 320.0)
    p_rup_loop.line_to(lsb_rup + 40.0, 320.0 + stem_h)
    p_rup_loop.line_to(lsb_rup + 40.0 + 130.0, 320.0 + stem_h)
    p_rup_loop.arc_to(lsb_rup + 40.0 + 130.0, 420.0, max(10.0, 130.0 - stem), max(10.0, 100.0 - stem_h), -90, 90, clockwise=False, steps=4)
    p_rup_loop.close()
    
    # Diagonal leg down to baseline
    p_rup_leg = Path()
    p_rup_leg.move_to(lsb_rup + 120.0, 320.0)
    p_rup_leg.line_to(rsb_rup, 0.0)
    p_rup_leg.line_to(rsb_rup - stem*1.2, 0.0)
    p_rup_leg.line_to(lsb_rup + 40.0, 280.0)
    p_rup_leg.close()
    add_glyph(GlyphSpec('rupee', 0x20B9, w_rup, lsb_rup, [p_rup_bar1, p_rup_bar2, p_rup_stem, p_rup_loop, p_rup_leg]))

    # --- euro (€) ---
    w_eur = 720.0 + stem * 0.4
    p_eur_c = Path()
    # C arc
    cx_eur = w_eur/2.0 + 20.0
    cy_eur = cap_h/2.0
    rx_eur = (w_eur - 100.0)/2.0
    ry_eur = (cap_h + 2*ov)/2.0
    x_eur_start = cx_eur + rx_eur * math.cos(math.radians(45))
    y_eur_start = cy_eur + ry_eur * math.sin(math.radians(45))
    p_eur_c.move_to(x_eur_start, y_eur_start)
    p_eur_c.arc_to(cx_eur, cy_eur, rx_eur, ry_eur, 45, 315, clockwise=True, steps=6)
    p_eur_c.line_to(cx_eur + (rx_eur - stem)*math.cos(math.radians(315)), cy_eur + (ry_eur - stem_h)*math.sin(math.radians(315)))
    p_eur_c.arc_to(cx_eur, cy_eur, rx_eur - stem, ry_eur - stem_h, 315, 45, clockwise=False, steps=6)
    p_eur_c.close()
    p_eur_b1 = Path()
    p_eur_b1.rect(50.0, 390.0 - stem_h/2.0, w_eur*0.6, stem_h)
    p_eur_b2 = Path()
    p_eur_b2.rect(50.0, 290.0 - stem_h/2.0, w_eur*0.6, stem_h)
    add_glyph(GlyphSpec('euro', 0x20AC, w_eur, 50.0, [p_eur_c, p_eur_b1, p_eur_b2]))

    # --- dollar ($) ---
    w_dol = 600.0 + stem * 0.3
    # S curve + vertical bar
    p_dol_s = Path()
    cx_dol = w_dol / 2.0
    p_dol_s.move_to(w_dol - 90.0, cap_h - 130.0)
    p_dol_s.arc_to(cx_dol, cap_h - 170.0, (w_dol - 140.0)/2.0, 170.0 + ov, 30, 180, clockwise=False, steps=4)
    p_dol_s.arc_to(cx_dol, 170.0, (w_dol - 140.0)/2.0, 170.0 + ov, 0, -150, clockwise=True, steps=4)
    p_dol_s.line_to(90.0, 130.0)
    p_dol_s.arc_to(cx_dol, 170.0, max(10.0, (w_dol - 140.0)/2.0 - stem), max(10.0, 170.0 + ov - stem_h), -150, 0, clockwise=False, steps=4)
    p_dol_s.arc_to(cx_dol, cap_h - 170.0, max(10.0, (w_dol - 140.0)/2.0 - stem), max(10.0, 170.0 + ov - stem_h), 180, 30, clockwise=True, steps=4)
    p_dol_s.close()
    p_dol_v = Path()
    p_dol_v.rect(cx_dol - stem*0.4, -60.0, stem*0.8, cap_h + 120.0)
    add_glyph(GlyphSpec('dollar', 0x0024, w_dol, 50.0, [p_dol_s, p_dol_v]))

    # --- sterling (£) ---
    w_ster = 600.0 + stem * 0.35
    p_ster = Path()
    p_ster.rect(80.0, 0.0, w_ster - 160.0, stem_h)
    p_ster_b = Path()
    p_ster_b.rect(60.0, 270.0, 220.0, stem_h)
    add_glyph(GlyphSpec('sterling', 0x00A3, w_ster, 60.0, [p_ster, p_ster_b]))

    # --- yen (¥) ---
    w_yen = 640.0 + stem * 0.4
    cx_yen = w_yen / 2.0
    p_yen_v = Path()
    p_yen_v.move_to(50.0, cap_h)
    p_yen_v.line_to(50.0 + stem*1.1, cap_h)
    p_yen_v.line_to(cx_yen, 340.0)
    p_yen_v.line_to(cx_yen, 0.0)
    p_yen_v.line_to(cx_yen + stem, 0.0)
    p_yen_v.line_to(cx_yen + stem, 340.0)
    p_yen_v.line_to(w_yen - 50.0, cap_h)
    p_yen_v.line_to(w_yen - 50.0 - stem*1.1, cap_h)
    p_yen_v.line_to(cx_yen + stem/2.0, 360.0)
    p_yen_v.close()
    p_yen_b1 = Path()
    p_yen_b1.rect(120.0, 300.0 - stem_h/2.0, w_yen - 240.0, stem_h)
    p_yen_b2 = Path()
    p_yen_b2.rect(120.0, 200.0 - stem_h/2.0, w_yen - 240.0, stem_h)
    add_glyph(GlyphSpec('yen', 0x00A5, w_yen, 50.0, [p_yen_v, p_yen_b1, p_yen_b2]))

    # -------------------------------------------------------------
    # TYPOGRAPHIC SYMBOLS (bullet, ellipsis, copyright, etc.)
    # -------------------------------------------------------------
    
    # --- bullet (•) ---
    w_bul = 360.0 + stem * 0.4
    p_bul = Path()
    p_bul.circle(w_bul / 2.0, 280.0, max(24.0, stem * 0.7))
    add_glyph(GlyphSpec('bullet', 0x2022, w_bul, w_bul/2.0 - 30.0, [p_bul]))

    # --- ellipsis (…) ---
    w_ell = w_period * 3.0
    p_ell1 = Path()
    p_ell1.circle(w_period / 2.0, r_dot_base, r_dot_base)
    p_ell2 = Path()
    p_ell2.circle(w_period * 1.5, r_dot_base, r_dot_base)
    p_ell3 = Path()
    p_ell3.circle(w_period * 2.5, r_dot_base, r_dot_base)
    add_glyph(GlyphSpec('ellipsis', 0x2026, w_ell, w_period/2.0 - r_dot_base, [p_ell1, p_ell2, p_ell3]))

    # --- copyright (©) ---
    w_copy = 800.0 + stem * 0.4
    p_copy_o = Path()
    p_copy_o.donut(w_copy/2.0, cap_h/2.0, (w_copy - 80.0)/2.0, cap_h/2.0 + ov, max(10.0, (w_copy - 80.0)/2.0 - stem*0.8), max(10.0, cap_h/2.0 + ov - stem_h*0.8))
    p_copy_c = Path()
    p_copy_c.circle(w_copy/2.0, cap_h/2.0, 160.0)
    add_glyph(GlyphSpec('copyright', 0x00A9, w_copy, 40.0, [p_copy_o, p_copy_c]))

    # --- registered (®) ---
    w_reg = 800.0 + stem * 0.4
    p_reg_o = Path()
    p_reg_o.donut(w_reg/2.0, cap_h/2.0, (w_reg - 80.0)/2.0, cap_h/2.0 + ov, max(10.0, (w_reg - 80.0)/2.0 - stem*0.8), max(10.0, cap_h/2.0 + ov - stem_h*0.8))
    p_reg_r = Path()
    p_reg_r.circle(w_reg/2.0, cap_h/2.0, 160.0)
    add_glyph(GlyphSpec('registered', 0x00AE, w_reg, 40.0, [p_reg_o, p_reg_r]))

    # --- trademark (™) ---
    w_tm = 860.0 + stem * 0.4
    p_tm1 = Path()
    p_tm1.rect(60.0, cap_h - 200.0, 300.0, 200.0)
    p_tm2 = Path()
    p_tm2.rect(400.0, cap_h - 200.0, 400.0, 200.0)
    add_glyph(GlyphSpec('trademark', 0x2122, w_tm, 60.0, [p_tm1, p_tm2]))

    # --- degree (°) ---
    w_deg = 360.0 + stem * 0.3
    p_deg = Path()
    p_deg.donut(w_deg / 2.0, cap_h - 100.0, 80.0, 80.0, max(10.0, 80.0 - stem*0.8), max(10.0, 80.0 - stem_h*0.8))
    add_glyph(GlyphSpec('degree', 0x00B0, w_deg, w_deg/2.0 - 80.0, [p_deg]))

    # -------------------------------------------------------------
    # DIACRITICS / ACCENTS & ACCENTED CHARACTERS
    # -------------------------------------------------------------
    
    # Helper to generate an accent path
    def make_accent(acc_type, cx, y_base):
        p = Path()
        if acc_type == 'acute':
            p.move_to(cx - 50.0, y_base)
            p.line_to(cx + 40.0, y_base + 120.0)
            p.line_to(cx + 40.0 + stem*0.8, y_base + 120.0)
            p.line_to(cx - 50.0 + stem*0.8, y_base)
            p.close()
        elif acc_type == 'grave':
            p.move_to(cx + 50.0, y_base)
            p.line_to(cx - 40.0, y_base + 120.0)
            p.line_to(cx - 40.0 - stem*0.8, y_base + 120.0)
            p.line_to(cx + 50.0 - stem*0.8, y_base)
            p.close()
        elif acc_type == 'circumflex':
            p.move_to(cx - 80.0, y_base)
            p.line_to(cx, y_base + 100.0)
            p.line_to(cx + 80.0, y_base)
            p.line_to(cx + 80.0 - stem*0.8, y_base)
            p.line_to(cx, y_base + 100.0 - stem_h*0.9)
            p.line_to(cx - 80.0 + stem*0.8, y_base)
            p.close()
        elif acc_type == 'tilde':
            p.rect(cx - 70.0, y_base + 30.0, 140.0, stem_h*0.9)
        elif acc_type == 'dieresis':
            r = max(14.0, stem * 0.45)
            p.circle(cx - 50.0, y_base + 50.0, r)
            p2 = Path()
            p2.circle(cx + 50.0, y_base + 50.0, r)
            return [p, p2]
        elif acc_type == 'ring':
            r = 45.0
            p.donut(cx, y_base + 60.0, r, r, max(8.0, r - stem*0.7), max(8.0, r - stem_h*0.7))
        return [p]

    # Add accented latin letters by combining base glyph paths with accent paths
    accent_defs = [
        # Uppercase
        ('Agrave', 0x00C0, 'A', 'grave', cap_h + 20.0),
        ('Aacute', 0x00C1, 'A', 'acute', cap_h + 20.0),
        ('Acircumflex', 0x00C2, 'A', 'circumflex', cap_h + 20.0),
        ('Atilde', 0x00C3, 'A', 'tilde', cap_h + 20.0),
        ('Adieresis', 0x00C4, 'A', 'dieresis', cap_h + 20.0),
        ('Aring', 0x00C5, 'A', 'ring', cap_h + 20.0),
        ('Egrave', 0x00C8, 'E', 'grave', cap_h + 20.0),
        ('Eacute', 0x00C9, 'E', 'acute', cap_h + 20.0),
        ('Ecircumflex', 0x00CA, 'E', 'circumflex', cap_h + 20.0),
        ('Edieresis', 0x00CB, 'E', 'dieresis', cap_h + 20.0),
        ('Igrave', 0x00CC, 'I', 'grave', cap_h + 20.0),
        ('Iacute', 0x00CD, 'I', 'acute', cap_h + 20.0),
        ('Icircumflex', 0x00CE, 'I', 'circumflex', cap_h + 20.0),
        ('Idieresis', 0x00CF, 'I', 'dieresis', cap_h + 20.0),
        ('Ntilde', 0x00D1, 'N', 'tilde', cap_h + 20.0),
        ('Ograve', 0x00D2, 'O', 'grave', cap_h + 20.0),
        ('Oacute', 0x00D3, 'O', 'acute', cap_h + 20.0),
        ('Ocircumflex', 0x00D4, 'O', 'circumflex', cap_h + 20.0),
        ('Otilde', 0x00D5, 'O', 'tilde', cap_h + 20.0),
        ('Odieresis', 0x00D6, 'O', 'dieresis', cap_h + 20.0),
        ('Ugrave', 0x00D9, 'U', 'grave', cap_h + 20.0),
        ('Uacute', 0x00DA, 'U', 'acute', cap_h + 20.0),
        ('Ucircumflex', 0x00DB, 'U', 'circumflex', cap_h + 20.0),
        ('Udieresis', 0x00DC, 'U', 'dieresis', cap_h + 20.0),
        ('Yacute', 0x00DD, 'Y', 'acute', cap_h + 20.0),
        # Lowercase
        ('agrave', 0x00E0, 'a', 'grave', x_h + 20.0),
        ('aacute', 0x00E1, 'a', 'acute', x_h + 20.0),
        ('acircumflex', 0x00E2, 'a', 'circumflex', x_h + 20.0),
        ('atilde', 0x00E3, 'a', 'tilde', x_h + 20.0),
        ('adieresis', 0x00E4, 'a', 'dieresis', x_h + 20.0),
        ('aring', 0x00E5, 'a', 'ring', x_h + 20.0),
        ('egrave', 0x00E8, 'e', 'grave', x_h + 20.0),
        ('eacute', 0x00E9, 'e', 'acute', x_h + 20.0),
        ('ecircumflex', 0x00EA, 'e', 'circumflex', x_h + 20.0),
        ('edieresis', 0x00EB, 'e', 'dieresis', x_h + 20.0),
        ('igrave', 0x00EC, 'l', 'grave', x_h + 20.0),
        ('iacute', 0x00ED, 'l', 'acute', x_h + 20.0),
        ('icircumflex', 0x00EE, 'l', 'circumflex', x_h + 20.0),
        ('idieresis', 0x00EF, 'l', 'dieresis', x_h + 20.0),
        ('ntilde', 0x00F1, 'n', 'tilde', x_h + 20.0),
        ('ograve', 0x00F2, 'o', 'grave', x_h + 20.0),
        ('oacute', 0x00F3, 'o', 'acute', x_h + 20.0),
        ('ocircumflex', 0x00F4, 'o', 'circumflex', x_h + 20.0),
        ('otilde', 0x00F5, 'o', 'tilde', x_h + 20.0),
        ('odieresis', 0x00F6, 'o', 'dieresis', x_h + 20.0),
        ('ugrave', 0x00F9, 'u', 'grave', x_h + 20.0),
        ('uacute', 0x00FA, 'u', 'acute', x_h + 20.0),
        ('ucircumflex', 0x00FB, 'u', 'circumflex', x_h + 20.0),
        ('udieresis', 0x00FC, 'u', 'dieresis', x_h + 20.0),
        ('yacute', 0x00FD, 'y', 'acute', x_h + 20.0),
    ]

    for (name, ucode, base_name, acc_type, y_base) in accent_defs:
        base_g = glyphs[base_name]
        cx_acc = base_g.advance_width / 2.0
        acc_paths = make_accent(acc_type, cx_acc, y_base)
        combined_paths = list(base_g.paths) + acc_paths
        add_glyph(GlyphSpec(name, ucode, base_g.advance_width, base_g.lsb, combined_paths))

    # --- germandbls (ß) ---
    w_ss = 600.0 + stem * 0.4
    p_ss = Path()
    p_ss.rect(70.0, 0.0, stem, asc)
    p_ss_lobe = Path()
    p_ss_lobe.circle(w_ss/2.0, 300.0, 180.0)
    add_glyph(GlyphSpec('germandbls', 0x00DF, w_ss, 70.0, [p_ss, p_ss_lobe]))

    return glyphs
