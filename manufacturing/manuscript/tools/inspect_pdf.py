"""Render pages and collect structural evidence; human/model visual review is separate."""
from pathlib import Path
import hashlib,json,re,subprocess,sys
from PIL import Image,ImageOps,ImageDraw
from pypdf import PdfReader
P=Path(__file__).resolve().parents[2]
pdf=P/'output/pdf/correction-evidence-casper-study.pdf';tmp=P/'tmp/pdfs';tmp.mkdir(exist_ok=True,parents=True)
reader=PdfReader(pdf)
page_records=[]
for n,page in enumerate(reader.pages,1):
 text=page.extract_text();(tmp/f'page-{n:02}.txt').write_text(text)
 assert text and len(text.strip())>80,('empty/nearly empty page',n)
 assert '\ufffd' not in text,('replacement glyph',n)
 page_records.append({'page':n,'text_characters':len(text),'width_pt':float(page.mediabox.width),'height_pt':float(page.mediabox.height),'annotations':len(page.get('/Annots',[]).get_object() if hasattr(page.get('/Annots',[]),'get_object') else page.get('/Annots',[]))})
full='\n'.join((p.extract_text() or '') for p in reader.pages)
normalized=' '.join(full.split())
for phrase in ['Muhammad Usman','Haiqa Mushtaq','References','0.017292','0.016603','0.8805','342,559','Author confirmation pending']:
 assert phrase in normalized,('Missing required text',phrase)
assert not re.search(r'\[\?\?\]|\b(?:Table|Figure|Equation)\s+\?\?',full),'Unresolved reference in extracted text'
for old in list(tmp.glob('render-*.png'))+list(tmp.glob('contact-*.png')):old.unlink()
subprocess.run(['pdftoppm','-r','120','-png',str(pdf),str(tmp/'render')],check=True,capture_output=True)
images=sorted(tmp.glob('render-*.png'));assert len(images)==len(reader.pages)
for start in range(0,len(images),4):
 sheets=Image.new('RGB',(1500,2160),'#dddddd');draw=ImageDraw.Draw(sheets)
 for j,p in enumerate(images[start:start+4]):
  im=Image.open(p).convert('RGB');im.thumbnail((730,1035))
  x=(j%2)*750+(750-im.width)//2;y=(j//2)*1080+32
  sheets.paste(im,(x,y));draw.text(((j%2)*750+20,(j//2)*1080+10),f'Page {start+j+1}',fill='black')
 sheets.save(tmp/f'contact-{start+1:02}-{min(start+4,len(images)):02}.png')
report={'kind':'pdf_structure_and_render_check','pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'page_count':len(reader.pages),'pages':page_records,'metadata':{str(k):str(v) for k,v in (reader.metadata or {}).items()},'required_text':'present','unresolved_reference_patterns':'absent','replacement_glyph':'absent','pages_rendered':len(images),'visual_review':'Pending separate inspection; this script does not certify layout.'}
(P/'local/pdf_build_v0.1/pdf_structure.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'pages':len(reader.pages),'characters':len(full),'rendered':len(images),'contact_sheets':len(list(tmp.glob('contact-*.png')))}))
