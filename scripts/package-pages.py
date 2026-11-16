"""Build a dependency-free Pages artifact; use content-hashed offline cache versions."""
from pathlib import Path
import hashlib,re,shutil
root=Path(__file__).resolve().parent.parent
out=root/'_site'
if out.exists():shutil.rmtree(out)
out.mkdir()
assets=['index.html','style.css','core.js','app.js','backup.js','sound.js','sessions.js','cooking.js','ingredient-editor.js','updates.js','manifest.webmanifest','jszip.min.js','icon-192.png','icon-512.png']
digest=hashlib.sha256()
for name in assets:
 data=(root/name).read_bytes();digest.update(name.encode()+b'\0'+data);shutil.copyfile(root/name,out/name)
worker=(root/'sw.js').read_text();digest.update(worker.encode())
worker=re.sub(r"const CACHE='[^']+';", "const CACHE='ria-happy-cookbook-"+digest.hexdigest()[:16]+"';",worker,count=1)
(out/'sw.js').write_text(worker)
(out/'.nojekyll').touch()
print('Prepared Pages artifact with release cache',digest.hexdigest()[:16])
