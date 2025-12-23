import re
import unicodedata

def sanitize_filename(name: str) -> str:
    """Remove acentos e caracteres especiais para salvar arquivos PDF."""
    # Normaliza unicode (ex: ã -> a)
    nfkd_form = unicodedata.normalize('NFKD', name)
    only_ascii = nfkd_form.encode('ASCII', 'ignore').decode('utf-8')
    # Remove tudo que não for letra, número, traço ou underline
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', only_ascii)

def format_currency(value: float) -> str:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")