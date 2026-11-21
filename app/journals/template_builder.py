"""Build a journal .dotm file from a config dict (no Word needed).

A .dotm is a zip file with XML inside. We write the XML ourselves.
Usage:
    from app.journals.ebtekar import EBTEKAR
    build_template(EBTEKAR, "Ebtekar.dotm")
"""

import zipfile
from xml.sax.saxutils import escape

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
ROOT_ATTRS = f'xmlns:w="{W_NS}" xmlns:r="{R_NS}"'
XML_HEAD = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'

ALIGN = {"left": "left", "right": "right", "center": "center", "both": "both"}


# ---------------------------------------------------------------- units
def cm_to_twips(cm):
    return round(cm * 566.929)      # 1 cm = 566.929 twips (1/20 pt)


def pt_to_twips(pt):
    return round(pt * 20)


def half_points(pt):
    return round(pt * 2)            # Word stores font size in half-points


# ---------------------------------------------------------------- styles
def style_xml(style_id, s):
    """One <w:style> element from one dictionary entry."""
    p = []                                         # paragraph properties
    if s.get("keep_next"):
        p.append("<w:keepNext/>")
    if "before" in s or "after" in s:
        attrs = ""
        if "before" in s:
            attrs += f' w:before="{pt_to_twips(s["before"])}"'
        if "after" in s:
            attrs += f' w:after="{pt_to_twips(s["after"])}"'
        p.append(f"<w:spacing{attrs}/>")
    ind = ""
    if "left_cm" in s:
        ind += f' w:left="{cm_to_twips(s["left_cm"])}"'
    if "hanging_cm" in s:
        ind += f' w:hanging="{cm_to_twips(s["hanging_cm"])}"'
    if "first_line_cm" in s:
        ind += f' w:firstLine="{cm_to_twips(s["first_line_cm"])}"'
    if ind:
        p.append(f"<w:ind{ind}/>")
    if "align" in s:
        p.append(f'<w:jc w:val="{ALIGN[s["align"]]}"/>')
    if "outline" in s:
        p.append(f'<w:outlineLvl w:val="{s["outline"]}"/>')

    r = []                                         # run (font) properties
    if "font_cs" in s:
        r.append(f'<w:rFonts w:cs="{escape(s["font_cs"])}"/>')
    if s.get("bold"):
        r.append("<w:b/><w:bCs/>")
    if s.get("italic"):
        r.append("<w:i/><w:iCs/>")
    if "size" in s:
        hp = half_points(s["size"])
        r.append(f'<w:sz w:val="{hp}"/><w:szCs w:val="{hp}"/>')

    out = (f'<w:style w:type="paragraph" w:customStyle="1" w:styleId="{style_id}">'
           f'<w:name w:val="{style_id}"/>')
    if "based_on" in s:
        out += f'<w:basedOn w:val="{s["based_on"]}"/>'
    if "next" in s:
        out += f'<w:next w:val="{s["next"]}"/>'
    out += "<w:qFormat/>"
    if p:
        out += "<w:pPr>" + "".join(p) + "</w:pPr>"
    if r:
        out += "<w:rPr>" + "".join(r) + "</w:rPr>"
    return out + "</w:style>"


def styles_xml(cfg):
    f = cfg["fonts"]
    base = half_points(f["base_size"])
    defaults = (
        "<w:docDefaults><w:rPrDefault><w:rPr>"
        f'<w:rFonts w:ascii="{f["latin"]}" w:eastAsia="{f["latin"]}" '
        f'w:hAnsi="{f["latin"]}" w:cs="{f["complex"]}"/>'
        f'<w:sz w:val="{base}"/><w:szCs w:val="{base}"/>'
        '<w:lang w:val="en-US" w:eastAsia="en-US" w:bidi="fa-IR"/>'
        "</w:rPr></w:rPrDefault><w:pPrDefault/></w:docDefaults>"
    )
    built_in = (
        '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
        '<w:name w:val="Normal"/><w:qFormat/></w:style>'
        '<w:style w:type="paragraph" w:styleId="Header"><w:name w:val="header"/>'
        '<w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="120"/></w:pPr>'
        '<w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="Footer"><w:name w:val="footer"/>'
        '<w:basedOn w:val="Normal"/><w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/>'
        "</w:rPr></w:style>"
    )
    custom = "".join(style_xml(i, s) for i, s in cfg["styles"].items())
    return f"{XML_HEAD}<w:styles {ROOT_ATTRS}>{defaults}{built_in}{custom}</w:styles>"


# ---------------------------------------------------------------- header / footer
def _header_paragraph(text, size, bold=False, border=False):
    hp = half_points(size)
    rpr = f'<w:rPr>{"<w:b/><w:bCs/>" if bold else ""}<w:sz w:val="{hp}"/><w:szCs w:val="{hp}"/><w:rtl/></w:rPr>'
    pbdr = ('<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="1" w:color="000000"/></w:pBdr>'
            if border else "")
    return (f'<w:p><w:pPr><w:pStyle w:val="Header"/>{pbdr}<w:bidi/></w:pPr>'
            f'<w:r>{rpr}<w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>')


def _page_number_paragraph(size):
    hp = half_points(size)
    rpr = f'<w:rPr><w:sz w:val="{hp}"/><w:szCs w:val="{hp}"/></w:rPr>'
    return (f'<w:p><w:pPr><w:pStyle w:val="Footer"/><w:bidi/><w:jc w:val="center"/></w:pPr>'
            f'<w:r>{rpr}<w:fldChar w:fldCharType="begin"/></w:r>'
            f'<w:r>{rpr}<w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
            f'<w:r>{rpr}<w:fldChar w:fldCharType="separate"/></w:r>'
            f'<w:r>{rpr}<w:t>1</w:t></w:r>'
            f'<w:r>{rpr}<w:fldChar w:fldCharType="end"/></w:r></w:p>')


def header_xml(cfg, kind):
    """kind: 'odd' (default), 'even', 'first'. Only odd has text, like the original."""
    h = cfg["header"]
    if kind == "odd":
        body = (_header_paragraph(h["line1"], h["size"], bold=True) +
                _header_paragraph(h["line2"], h["size"], border=h["border"]))
    else:
        body = '<w:p><w:pPr><w:pStyle w:val="Header"/></w:pPr></w:p>'
    return f"{XML_HEAD}<w:hdr {ROOT_ATTRS}>{body}</w:hdr>"


def footer_xml(cfg, kind):
    body = (_page_number_paragraph(cfg["header"]["size"]) if kind != "first"
            else '<w:p><w:pPr><w:pStyle w:val="Footer"/></w:pPr></w:p>')
    return f"{XML_HEAD}<w:ftr {ROOT_ATTRS}>{body}</w:ftr>"


# ---------------------------------------------------------------- document
def document_xml(cfg):
    pg = cfg["page"]
    refs = ('<w:headerReference w:type="even" r:id="rId11"/>'
            '<w:headerReference w:type="default" r:id="rId12"/>'
            '<w:headerReference w:type="first" r:id="rId13"/>'
            '<w:footerReference w:type="even" r:id="rId14"/>'
            '<w:footerReference w:type="default" r:id="rId15"/>'
            '<w:footerReference w:type="first" r:id="rId16"/>')
    sect = (
        f"<w:sectPr>{refs}"
        f'<w:pgSz w:w="{cm_to_twips(pg["width_cm"])}" w:h="{cm_to_twips(pg["height_cm"])}"/>'
        f'<w:pgMar w:top="{cm_to_twips(pg["margin_top"])}" '
        f'w:right="{cm_to_twips(pg["margin_right"])}" '
        f'w:bottom="{cm_to_twips(pg["margin_bottom"])}" '
        f'w:left="{cm_to_twips(pg["margin_left"])}" '
        f'w:header="{cm_to_twips(pg["header_distance"])}" '
        f'w:footer="{cm_to_twips(pg["footer_distance"])}" w:gutter="0"/>'
        + ("<w:titlePg/>" if pg["different_first_page"] else "")
        + ("<w:bidi/>" if pg["rtl"] else "")
        + "</w:sectPr>"
    )
    body = ('<w:p><w:pPr><w:pStyle w:val="BodyNegar"/><w:bidi/>'
            '<w:ind w:firstLine="0"/></w:pPr></w:p>')
    return f"{XML_HEAD}<w:document {ROOT_ATTRS}><w:body>{body}{sect}</w:body></w:document>"


def settings_xml(cfg):
    odd_even = "<w:evenAndOddHeaders/>" if cfg["page"]["even_odd_headers"] else ""
    return (f'{XML_HEAD}<w:settings {ROOT_ATTRS}><w:zoom w:percent="100"/>'
            f'{odd_even}<w:defaultTabStop w:val="720"/></w:settings>')


# ---------------------------------------------------------------- package
CONTENT_TYPES = f"""{XML_HEAD}<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.template.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
{''.join(f'<Override PartName="/word/header{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>' for i in (1, 2, 3))}
{''.join(f'<Override PartName="/word/footer{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>' for i in (1, 2, 3))}
</Types>"""

ROOT_RELS = f"""{XML_HEAD}<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""


def _rel(rid, kind, target):
    return (f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/'
            f'officeDocument/2006/relationships/{kind}" Target="{target}"/>')


DOC_RELS = (f'{XML_HEAD}<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            + _rel("rId1", "styles", "styles.xml")
            + _rel("rId2", "settings", "settings.xml")
            + _rel("rId11", "header", "header1.xml")    # even
            + _rel("rId12", "header", "header2.xml")    # default (odd)
            + _rel("rId13", "header", "header3.xml")    # first
            + _rel("rId14", "footer", "footer1.xml")
            + _rel("rId15", "footer", "footer2.xml")
            + _rel("rId16", "footer", "footer3.xml")
            + "</Relationships>")


def build_template(cfg, output_path):
    """Write a .dotm file made from cfg. Returns output_path."""
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", ROOT_RELS)
        z.writestr("word/_rels/document.xml.rels", DOC_RELS)
        z.writestr("word/document.xml", document_xml(cfg))
        z.writestr("word/styles.xml", styles_xml(cfg))
        z.writestr("word/settings.xml", settings_xml(cfg))
        for n, kind in enumerate(("even", "odd", "first"), start=1):
            z.writestr(f"word/header{n}.xml", header_xml(cfg, kind))
            z.writestr(f"word/footer{n}.xml", footer_xml(cfg, kind))
    return output_path


if __name__ == "__main__":
    from app.journals.ebtekar import EBTEKAR
    print("Saved:", build_template(EBTEKAR, "Ebtekar_generated.dotm"))
