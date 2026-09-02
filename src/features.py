"""
OpenType feature generator for Om Sans.
Defines GPOS kerning pairs and GSUB feature definitions.
"""

def generate_fea():
    fea = """
languagesystem DFLT dflt;
languagesystem latn dflt;

# Kerning pairs (GPOS)
feature kern {
    # Capital / Capital
    pos A V -65;
    pos A W -55;
    pos A T -70;
    pos A Y -75;
    pos T A -70;
    pos V A -65;
    pos W A -55;
    pos Y A -75;
    pos L T -60;
    pos L V -50;
    pos L W -40;
    pos L Y -60;
    pos P A -50;
    pos F A -40;

    # Capital / Lowercase
    pos T a -60;
    pos T e -60;
    pos T o -60;
    pos T u -50;
    pos T y -55;
    pos V a -55;
    pos V e -55;
    pos V o -55;
    pos W a -45;
    pos W e -45;
    pos W o -45;
    pos Y a -65;
    pos Y e -65;
    pos Y o -65;
    pos F a -45;
    pos F e -40;
    pos F o -45;
    pos P a -30;
    pos P e -30;
    pos P o -30;

    # Lowercase / Lowercase
    pos v o -25;
    pos w o -20;
    pos y o -25;
    pos r a -20;
    pos r e -20;
    pos r o -25;

    # Punctuation kerning
    pos T period -70;
    pos T comma -70;
    pos V period -65;
    pos V comma -65;
    pos W period -55;
    pos W comma -55;
    pos Y period -70;
    pos Y comma -70;
    pos F period -60;
    pos F comma -60;
    pos P period -60;
    pos P comma -60;
} kern;
"""
    return fea
