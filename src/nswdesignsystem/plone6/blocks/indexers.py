from html2text import HTML2Text
from plone.restapi.behaviors import IBlocks
from plone.restapi.interfaces import IBlockSearchableText
from zope.component import adapter
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest


html2text_extractor = HTML2Text()
# Remove the extra characters from formatted text
html2text_extractor.emphasis_mark = ""
html2text_extractor.strong_mark = ""
html2text_extractor.ul_item_mark = ""


def get_rich_text_data(rich_text_field):
    data = (
        rich_text_field
        if isinstance(rich_text_field, str)
        else rich_text_field.get("data", "")
    )
    return html2text_extractor.handle(data)


def extract_card(block_data):
    title = block_data.get("title", "")
    description = get_rich_text_data(block_data.get("description", ""))

    return f"{title} {description}"


def extract_content_block(block_data):
    title = block_data.get("title", "")
    description = get_rich_text_data(block_data.get("description", ""))

    return f"{title} {description}"


def extract_announcement_bar(block_data):
    return f"{get_rich_text_data(block_data.get('body', ''))}"


def extract_callout(block_data):
    title = block_data.get("title", "")
    contents = get_rich_text_data(block_data.get("contents", ""))

    return f"{title} {contents}"


def extract_link_list(block_data):
    titles = []
    for link in block_data.get("links", []):
        link_info = link.get("url", {})
        if not link_info:
            continue
        link_info_data = link_info[0]
        if not isinstance(link_info_data, dict):
            continue
        title = link_info_data.get("title")
        if title:
            titles.append(title)
    return " ".join(titles)


def extract_column_data(block_data):
    data = []

    for column in block_data.get("columns", []):
        extractor = BLOCK_TYPE_EXTRACTOR_MAPPING[column["@type"]]
        if not extractor:
            continue
        data.append(extractor(column))

    return " ".join(data)


BLOCK_TYPE_EXTRACTOR_MAPPING = {
    "__grid": extract_column_data,
    "contentBlockGrid": extract_column_data,
    "card": extract_card,
    "contentBlock": extract_content_block,
    "nsw_announcementBar": extract_announcement_bar,
    "callout": extract_callout,
    "nsw_inPageAlert": extract_announcement_bar,
    "nsw_linkList": extract_link_list,
}


@implementer(IBlockSearchableText)
@adapter(IBlocks, IBrowserRequest)
class NSWSearchableText:
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, block_value):
        extractor = BLOCK_TYPE_EXTRACTOR_MAPPING[block_value["@type"]]
        if not extractor:
            return ""
        return extractor(block_value)


@implementer(IBlockSearchableText)
@adapter(IBlocks, IBrowserRequest)
class HeroSearchableText:
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, block_value):
        title = block_value.get("title", "")
        description = block_value.get("description", "")
        return f"{title} {description}"
