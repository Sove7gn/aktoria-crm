"""Copy the CRM page into index.html for GitHub Pages.

python build.py <path to aktoria-crm.html>

The claude.ai artifact is a page body without a document skeleton; GitHub Pages needs a full HTML document.
Off claude.ai the page reads the Google Sheet published to the web (view only).
"""
import sys
from pathlib import Path

src = Path(sys.argv[1]).read_text(encoding="utf-8")
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="robots" content="noindex">\n')
(Path(__file__).parent / "index.html").write_text(head + src + "\n</html>\n", encoding="utf-8")
print("index.html written")
