from lxml import etree

def xml_to_dict(elem):
    d = {}
    # Attributes
    for k, v in elem.attrib.items():
        d[f"@{k}"] = v

    # Children
    for child in elem:
        child_dict = xml_to_dict(child)
        d.setdefault(child.tag, [])
        d[child.tag].append(child_dict)

    # Text
    text = (elem.text or "").strip()
    if text:
        d["#text"] = text

    return d

def parse_xml(raw: bytes):
    root = etree.fromstring(raw)
    return [xml_to_dict(root)]
