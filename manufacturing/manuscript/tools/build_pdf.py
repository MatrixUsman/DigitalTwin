"""Rebuild the manuscript with the locally pinned compiler; offline by default."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,shutil,subprocess,sys
M=Path(__file__).resolve().parents[1];P=M.parent
LOCAL=P/'local/pdf_build_v0.1';BUILD=LOCAL/'build';OUTPUT=P/'output/pdf/correction-evidence-casper-study.pdf'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--allow-resource-downloads',action='store_true',help='Allow compiler resource downloads; never upload manuscript content.');args=ap.parse_args()
 binary=LOCAL/'bin/tectonic'
 if not binary.is_file():raise SystemExit('Missing local Tectonic binary. See PDF_BUILD_REPORT.md for the verified release and installation scope.')
 release=json.loads((LOCAL/'tectonic_release.json').read_text());asset=next(x for x in release['assets'] if x['name']=='tectonic-0.17.0-aarch64-apple-darwin.tar.gz')
 if 'sha256:'+sha(LOCAL/'tectonic.tar.gz')!=asset['digest']:raise SystemExit('Compiler archive digest differs from the recorded publisher digest.')
 subprocess.run([sys.executable,str(M/'tools/build_assets.py'),'--check'],check=True)
 BUILD.mkdir(parents=True,exist_ok=True);OUTPUT.parent.mkdir(parents=True,exist_ok=True)
 env=dict(os.environ);env['TECTONIC_CACHE_DIR']=str(LOCAL/'cache')
 command=[str(binary),'--untrusted','--keep-logs','--keep-intermediates','--outdir',str(BUILD)]
 if not args.allow_resource_downloads:command.append('--only-cached')
 command.append('main.tex')
 source_paths=sorted(list(M.glob('*.tex'))+list((M/'sections').glob('*.tex'))+list((M/'generated').glob('*.tex'))+list((M/'figures').glob('*.tex')))
 source_hashes={str(p.relative_to(M)):sha(p) for p in source_paths}
 started=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (LOCAL/'build.stdout.log').open('w') as log:
  result=subprocess.run(command,cwd=M,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=300)
 if result.returncode:raise SystemExit('Compilation failed; see local/pdf_build_v0.1/build.stdout.log. Previous final PDF preserved.')
 pdf=BUILD/'main.pdf'
 if not pdf.is_file() or pdf.read_bytes()[:5]!=b'%PDF-':raise SystemExit('No valid PDF signature; final output preserved.')
 if source_hashes!={str(p.relative_to(M)):sha(p) for p in source_paths}:raise SystemExit('Sources changed during compilation; output not accepted.')
 shutil.copyfile(pdf,OUTPUT)
 receipt={'kind':'manuscript_pdf_build','started_at_utc':started,'completed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':command,'cwd':str(M),'compiler_version':subprocess.check_output([str(binary),'--version'],text=True).strip(),'compiler_sha256':sha(binary),'publisher_archive_sha256':asset['digest'],'cache':env['TECTONIC_CACHE_DIR'],'offline':not args.allow_resource_downloads,'shell_escape_enabled':False,'sources':source_hashes,'sources_unchanged_during_build':True,'pdf':{'path':str(OUTPUT.relative_to(P)),'bytes':OUTPUT.stat().st_size,'sha256':sha(OUTPUT)},'models_run':False,'raw_data_opened':False,'visual_review':'Separate page inspection required for each changed PDF.'}
 (LOCAL/'build_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt['pdf']))
if __name__=='__main__':main()
