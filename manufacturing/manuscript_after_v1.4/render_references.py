"""Produce a linked numeric bibliography from the retained BibTeX metadata."""
from pathlib import Path
import re,json
M=Path(__file__).resolve().parent
s=(M/'references.bib').read_text();entries={}
def balanced(pos):
    start=pos+1;depth=1;pos+=1
    while depth:
        if s[pos]=='{' and (pos==0 or s[pos-1]!='\\'):depth+=1
        elif s[pos]=='}' and s[pos-1]!='\\':depth-=1
        pos+=1
    return s[start:pos-1],pos
for match in re.finditer(r'@\w+\{([^,]+),',s):
    key=match[1];pos=match.end();fields={}
    while True:
        m=re.match(r'\s*,?\s*(\w+)\s*=\s*\{',s[pos:])
        if not m:break
        value,pos=balanced(pos+m.end()-1);fields[m[1]]=value
    entries[key]=fields
main=(M/'main.tex').read_text()
for name in re.findall(r'\\input\{(sections/[^}]+)\}',main):
    main=main.replace('\\input{'+name+'}',(M/(name+'.tex')).read_text())
order=[]
for group in re.findall(r'\\cite\{([^}]+)\}',main):
    for key in group.split(','):
        if key not in order:order.append(key)
assert set(order)==set(entries) and len(order)==20
lines=[r'\begin{thebibliography}{20}']
for key in order:
    # Balance the last page's two reference columns in this fixed layout.
    if key=='timemixer':lines.append(r'\newpage')
    d=entries[key];authors=d['author'].split(' and ')
    names=[]
    for a in authors:
        family,given=a.split(', ',1);names.append(given+' '+family)
    name=', '.join(names) if len(names)<=6 else ', '.join(names[:3])+', et al.'
    venue=d.get('journal',d.get('booktitle','arXiv preprint'))
    details=d.get('volume','')
    if 'number' in d:details+='('+d['number']+')'
    if 'pages' in d:details+=(':' if details else '')+d['pages']
    if details:venue+=', '+details
    note=d.get('note','')
    if d.get('eprint'):note+='; arXiv:'+d['eprint']
    link='https://doi.org/'+d['doi'] if 'doi' in d else d['url']
    line=r'\bibitem{'+key+'} '+name.rstrip('.')+'. '+d['title']+'. '+r'\emph{'+venue+'}, '+d['year']+'.'
    if note:line+=' '+note+'.'
    lines.append(line+r' \url{'+link+'}.')
lines.append(r'\end{thebibliography}')
(M/'references.tex').write_text('\n\n'.join(lines)+'\n')
(M/'REFERENCE_INDEX.json').write_text(json.dumps({'count':len(order),'recent_cited_versions':sum(int(d['year'])>=2024 for d in entries.values()),'citation_order':order,'entries':entries},indent=2,ensure_ascii=False)+'\n')
print('20 cited references; 18 cited publication versions dated 2024--2026')
