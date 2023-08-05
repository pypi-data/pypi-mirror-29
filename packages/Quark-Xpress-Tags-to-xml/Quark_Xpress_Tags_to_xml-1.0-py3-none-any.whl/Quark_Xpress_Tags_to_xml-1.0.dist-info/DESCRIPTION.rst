
Convert Quark Xpress tagged text (Tags, xtags) to XML.

This module is intended as a pre-processing step in the conversion of
Quark Xpress tagged text to (semantic) HTML; as such it does not
attempt to convert every single tag to XML, but only those that are
relevant to the production of semantic, HTML5-compliant HTML. 

This means that Paragraph and Character style sheet definitions are
ignored; we only care about the apllied style sheet names. It also
means that import character attributes like <i> and <b>, but ignore 
tags related to print typesseting only (tracking, kerning,
baseline shift, etc.) by default , though they can be turned on.

The module doen't actually produced XML but an Element Tree, in case 
you'd like to do further processing on the tree itself before
serialising it with lxml.etree.tostring(). The serialised XML can
then be turned to HTML with e.g. BeautifulSoup for postprocessing
(for example, mapping Quark paragraph stylesheet to CSS classes, 
character tags and stylesheets to semantic HTML tags, rolling up
indented quotes to <blockquote>, etc.)

Outputs UTF-8.

Usage:

>>> frpm quark_tagged_text import get_encoding, to_xml
>>> from lxml.etree import to_tring
>>> encoding = get_encoding(<source file>)
>>> with open(<source file>, encoding=encoding) as tagged_text:
>>>     element_tree = to_xml(tagged_text) 
>>> serialised_xml = tostring(element_tree, encoding='utf-8')


