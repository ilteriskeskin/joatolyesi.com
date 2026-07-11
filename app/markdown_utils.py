"""Blog gövdesi: markdown -> temizlenmiş HTML. nh3 (ammonia) XSS'i süpürür."""

import markdown as md
import nh3

ALLOWED_TAGS = {
    "p", "br", "strong", "em", "blockquote", "code", "pre",
    "h2", "h3", "ul", "ol", "li", "hr", "a",
}
ALLOWED_ATTRS = {"a": {"href", "title"}}


def render_markdown(text: str) -> str:
    html = md.markdown(text, extensions=["nl2br", "sane_lists"])
    return nh3.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        link_rel="nofollow noopener",
        url_schemes={"http", "https", "mailto"},
    )


def markdown_excerpt(text: str, length: int = 220) -> str:
    """Liste görünümü için düz metin özet: HTML'e çevirip tüm etiketleri soy."""
    plain = nh3.clean(md.markdown(text), tags=set())
    plain = " ".join(plain.split())
    return plain[:length] + ("…" if len(plain) > length else "")
