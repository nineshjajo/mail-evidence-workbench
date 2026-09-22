from email import policy
from email.message import EmailMessage
from email.parser import BytesParser
from email.utils import getaddresses

from .models import Message


def _body(message: EmailMessage, content_type: str) -> str:
    chunks: list[str] = []
    for part in message.walk():
        if part.get_content_type() != content_type:
            continue
        try:
            content = part.get_content()
        except (LookupError, UnicodeDecodeError):
            payload = part.get_payload(decode=True) or b""
            content = payload.decode("utf-8", errors="replace") if isinstance(payload, bytes) else str(payload)
        if isinstance(content, str):
            chunks.append(content)
    return "\n".join(chunks)


def parse_message(raw: bytes) -> Message:
    message = BytesParser(policy=policy.default).parsebytes(raw)
    text = _body(message, "text/plain")
    html = _body(message, "text/html")
    from .evidence import extract_indicators

    indicators = extract_indicators("\n".join((message.get("Subject", ""), text, html)))
    recipients = tuple(address for _, address in getaddresses(message.get_all("To", [])) if address)
    attachments = tuple(
        part.get_filename() or "unnamed-attachment"
        for part in message.walk()
        if part.get_content_disposition() == "attachment"
    )
    return Message(
        sender=message.get("From", ""),
        recipients=recipients,
        subject=message.get("Subject", ""),
        text=text,
        html=html,
        authentication_results=tuple(message.get_all("Authentication-Results", [])),
        urls=indicators["urls"],
        domains=indicators["domains"],
        ips=indicators["ips"],
        hashes=indicators["hashes"],
        attachments=attachments,
    )
