"""Build a journal .dotm file from a config dict (no Word needed).

A .dotm is a zip file with XML inside. We write the XML ourselves.
Usage:
    from app.journals.ebtekar import EBTEKAR
    build_template(EBTEKAR, "Ebtekar.dotm")
"""

import itertools
import zipfile
from xml.sax.saxutils import escape, quoteattr

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
        '<w:style w:type="character" w:styleId="PlaceholderText">'
        '<w:name w:val="Placeholder Text"/><w:uiPriority w:val="99"/><w:semiHidden/>'
        '<w:rPr><w:color w:val="808080"/></w:rPr></w:style>'
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
def run_xml(text, rtl=True, bold=False, italic=False, placeholder=False):
    """One text run. rtl=True marks the text as right-to-left (Persian)."""
    rpr = ""
    if placeholder:
        rpr += '<w:rStyle w:val="PlaceholderText"/>'
    if bold:
        rpr += "<w:b/><w:bCs/>"
    if italic:
        rpr += "<w:i/><w:iCs/>"
    if rtl:
        rpr += "<w:rtl/>"
    rpr = f"<w:rPr>{rpr}</w:rPr>" if rpr else ""
    return f'<w:r>{rpr}<w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


def sdt_pr(c, rtl, ids):
    """Properties of a content control: alias, tag, id, lock, placeholder."""
    pr = "<w:rPr><w:rtl/></w:rPr>" if rtl else ""
    pr += (f'<w:alias w:val={quoteattr(c["alias"])}/><w:tag w:val={quoteattr(c["tag"])}/>'
           f'<w:id w:val="{next(ids)}"/>')
    if c.get("locked"):
        pr += '<w:lock w:val="sdtLocked"/>'
    pr += "<w:showingPlcHdr/>" if c.get("placeholder", True) else "<w:text/>"
    return f"<w:sdtPr>{pr}</w:sdtPr>"


def control_xml(c, rtl, ids):
    """An inline content control (inside a paragraph)."""
    run = run_xml(c["text"], rtl, placeholder=c.get("placeholder", True))
    return f"<w:sdt>{sdt_pr(c, rtl, ids)}<w:sdtContent>{run}</w:sdtContent></w:sdt>"


def paragraph_xml(style_id, parts, opts, ids):
    """One paragraph. parts = text, a dict, or a list of them."""
    opts = opts or {}
    rtl = opts.get("rtl", True)
    if isinstance(parts, (str, dict)):
        parts = [parts]

    ppr = f'<w:pStyle w:val="{style_id}"/>'
    if opts.get("page_break"):
        ppr += "<w:pageBreakBefore/>"
    if opts.get("border_top"):
        ppr += ('<w:pBdr><w:top w:val="single" w:sz="4" w:space="1" '
                'w:color="auto"/></w:pBdr>')
    if rtl:
        ppr += "<w:bidi/>"
    if "before" in opts:
        ppr += f'<w:spacing w:before="{pt_to_twips(opts["before"])}"/>'
    if "align" in opts:
        ppr += f'<w:jc w:val="{ALIGN[opts["align"]]}"/>'

    # a block control wraps the whole paragraph
    if len(parts) == 1 and isinstance(parts[0], dict) and parts[0].get("block"):
        c = parts[0]
        run = run_xml(c["text"], rtl, placeholder=True)
        return (f"<w:sdt>{sdt_pr(c, rtl, ids)}<w:sdtContent>"
                f"<w:p><w:pPr>{ppr}</w:pPr>{run}</w:p></w:sdtContent></w:sdt>")

    out = ""
    for part in parts:
        if isinstance(part, str):
            out += run_xml(part, rtl) if part else ""
        elif "tag" in part:
            out += control_xml(part, rtl, ids)
        else:  # plain text with options: bold, italic, bookmark
            run = run_xml(part["text"], rtl, part.get("bold"), part.get("italic"))
            if "bookmark" in part:
                n = next(ids)
                run = (f'<w:bookmarkStart w:id="{n}" w:name="{part["bookmark"]}"/>'
                       f'{run}<w:bookmarkEnd w:id="{n}"/>')
            out += run
    return f"<w:p><w:pPr>{ppr}</w:pPr>{out}</w:p>"


def table_xml(t, ids):
    """A borderless layout table. cells = one list of paragraphs per column."""
    widths = [cm_to_twips(w) for w in t["widths_cm"]]
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    cells = ""
    for w, paragraphs in zip(widths, t["cells"]):
        content = "".join(paragraph_xml(*item[:2], item[2] if len(item) > 2 else None, ids)
                          for item in paragraphs) or "<w:p/>"
        cells += f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/></w:tcPr>{content}</w:tc>'
    return ('<w:tbl><w:tblPr><w:bidiVisual/><w:tblW w:w="0" w:type="auto"/>'
            '<w:tblCellMar><w:left w:w="10" w:type="dxa"/>'
            '<w:right w:w="10" w:type="dxa"/></w:tblCellMar></w:tblPr>'
            f'<w:tblGrid>{grid}</w:tblGrid><w:tr>{cells}</w:tr></w:tbl>')


def skeleton_xml(cfg):
    ids = itertools.count(1700001)  # every control needs its own number
    out = ""
    for item in cfg.get("skeleton", []):
        if isinstance(item, dict):
            out += table_xml(item["table"], ids)
        else:
            out += paragraph_xml(item[0], item[1], item[2] if len(item) > 2 else None, ids)
    return out


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
    body = skeleton_xml(cfg)
    if not body:  # no skeleton: one empty paragraph
        body = ('<w:p><w:pPr><w:pStyle w:val="BodyNegar"/><w:bidi/>'
                '<w:ind w:firstLine="0"/></w:pPr></w:p>')
    return f"{XML_HEAD}<w:document {ROOT_ATTRS}><w:body>{body}{sect}</w:body></w:document>"


def settings_xml(cfg):
    odd_even = "<w:evenAndOddHeaders/>" if cfg["page"]["even_odd_headers"] else ""
    compat = ('<w:compat><w:compatSetting w:name="compatibilityMode" '
              'w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat>')
    return (f'{XML_HEAD}<w:settings {ROOT_ATTRS}><w:zoom w:percent="100"/>'
            f'<w:defaultTabStop w:val="720"/>{odd_even}{compat}</w:settings>')


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
    print("Saved:", build_template(EBTEKAR, "Ebtekar_generated.dotx"))
