"""Assemble an editorial revision from existing manuscript and recorded evidence.

No scientific code is imported or executed. The previous revision is read only.
"""
from pathlib import Path

M = Path(__file__).resolve().parent
OLD = M.parent / 'manuscript_after_v1.3'
old = (OLD / 'main.tex').read_text()
def between(start, stop):
    return old.split(start, 1)[1].split(stop, 1)[0]

preamble = r'''\documentclass[11pt,twocolumn]{article}
\usepackage[a4paper,margin=0.60in,columnsep=0.25in]{geometry}
\usepackage{amsmath,amssymb,booktabs,graphicx,array}
\usepackage[hidelinks]{hyperref}
\usepackage{xurl}
\hypersetup{pdftitle={AFTER: Digital Twins for Cyberattack and Recovery Monitoring in Industrial Robots},pdfauthor={Muhammad Usman}}
\DeclareMathSizes{10}{10}{8}{6}
% Use cached class resources with a 10/11pt body and compact journal headings.
\makeatletter
\renewcommand{\normalsize}{\@setfontsize\normalsize{10}{11}\abovedisplayskip8pt plus2pt minus3pt\belowdisplayskip8pt plus2pt minus3pt\abovedisplayshortskip0pt plus3pt\belowdisplayshortskip5pt plus3pt minus3pt}
\renewcommand\section{\@startsection{section}{1}{\z@}{-2.5ex plus -1ex minus -.2ex}{1.2ex plus .2ex}{\normalfont\large\bfseries\raggedright}}
\renewcommand\subsection{\@startsection{subsection}{2}{\z@}{-2ex plus -.5ex minus -.2ex}{.8ex plus .2ex}{\normalfont\normalsize\bfseries\raggedright}}
\renewcommand\subsubsection{\@startsection{subsubsection}{3}{\z@}{-1.8ex plus -.5ex minus -.2ex}{.6ex plus .2ex}{\normalfont\normalsize\itshape\raggedright}}
\makeatother
\setlength{\emergencystretch}{2em}
\raggedbottom
\setlength{\textfloatsep}{11pt plus 2pt minus 2pt}
\setlength{\dbltextfloatsep}{12pt plus 2pt minus 2pt}
\setlength{\floatsep}{10pt plus 2pt minus 2pt}
\renewcommand{\topfraction}{0.9}
\renewcommand{\dbltopfraction}{0.9}
\setcounter{dbltopnumber}{4}\setcounter{totalnumber}{6}
\renewcommand{\textfraction}{0.07}
\renewcommand{\floatpagefraction}{0.8}
\renewcommand{\dblfloatpagefraction}{0.8}
\newtheorem{proposition}{Proposition}
\newenvironment{proof}{\par\noindent\textit{Proof.}\ }{\hfill\textit{Q.E.D.}\par}
\title{AFTER: Digital Twins for Cyberattack and Recovery Monitoring in Industrial Robots}
\author{Muhammad Usman\\[3pt]\normalsize COMSATS University Islamabad, Sahiwal Campus, Pakistan}
\date{}
\begin{document}
\makeatletter
\twocolumn[\begin{@twocolumnfalse}
\vspace{-12pt}\maketitle\vspace{-12pt}
\begin{abstract}
'''
abstract = between('\\begin{abstract}', '\\end{abstract}').strip()
intro = between('\\section{Introduction}', '\\section{Related work}')
intro = intro.replace('The contributions supported', r'''The comparison separates three questions. Can clean commissioning improve reference accuracy across the declared mismatch conditions? Does the improved reference reduce benign alarms while retaining evidence through sustained corruption? Which component, if any, explains that benefit? These questions require different measurements: normal prediction error, the complete alarm trajectory, and matched component removals. A single F1 value cannot answer all three.

The contributions supported''')
intro += r'''
The remainder of the paper separates these decisions. Section~\ref{sec:literature} positions the study in prior work. Sections~\ref{sec:methods}--\ref{sec:comparators} define the model, experiments, metrics and comparison methods. Section~\ref{sec:results} reports the complete outcomes; Sections~\ref{sec:discussion} and~\ref{sec:conclusion} interpret their scope. The appendices retain uncertainty derivations, earlier results and source identities within this article.
'''
related = between('\\section{Related work}', '\\section{Proposed reference and alarm model}')
related = related.replace('\\paragraph{Limitations relevant to this comparison.}', '\\subsection{Limitations and unresolved comparison requirements}')
main = preamble + abstract + r'''
\end{abstract}
\noindent\textbf{Keywords:} digital twins; industrial robots; anomaly detection; recovery monitoring; system identification; model mismatch.
\vspace{12pt}
\end{@twocolumnfalse}]
\makeatother
\section{Introduction}
''' + intro + '\n\\section{Literature Review}\\label{sec:literature}\n' + related
for name in ['methods', 'experiments', 'metrics', 'comparators', 'results', 'discussion']:
    main += '\n\\input{sections/' + name + '}\n'
conclusion = between('\\section{Conclusion}', '\\section*{Declarations}')
main += '\n\\section{Conclusion}\\label{sec:conclusion}\n' + conclusion
main += r'''
\section*{Declarations}
\paragraph{Funding and competing interests.} No funding or competing interests were declared.
\paragraph{Data and code availability.} Versioned code, configurations, results and a reproducibility inventory are retained locally. No public repository release is claimed. Third-party data remain subject to provider terms; Appendix~\ref{app:provenance} records source identifiers and hashes. All supporting material discussed here is incorporated in this article.
\paragraph{AI assistance and author review.} OpenAI Codex assisted with literature searches, code, experiment execution, analysis, writing and editing. The named author must review the scientific claims and approve the manuscript before submission. No completed human-contribution attestation or independent human review is asserted here.
\appendix
\input{sections/uncertainty}
\input{sections/earlier_results}
\input{sections/provenance}
\begingroup\raggedright
\input{references}
\endgroup
\end{document}
'''
(M/'main.tex').write_text(main)
print('Assembled one manuscript; no separate supplement.')
