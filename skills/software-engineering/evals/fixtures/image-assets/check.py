from pathlib import Path
from html.parser import HTMLParser
class Check(HTMLParser):
 def handle_starttag(self, tag, attrs):
  if tag == "img":
   src = dict(attrs).get("src")
   assert src and Path(src).is_file(), src
Check().feed(Path("index.html").read_text())
print("local image references valid")
