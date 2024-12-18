\NeedsTeXFormat{LaTeX2e}

\ProvidesClass{unitothesis}[2023/03/19 LaTeX class for BS/MS thesis at fisica.campusnet.unito.it]
\LoadClass[12pt]{article}
\RequirePackage[english]{babel}
\RequirePackage{csquotes}
\RequirePackage[a4paper]{geometry}
\RequirePackage{graphicx} % Required for inserting images
\RequirePackage{amsmath, amssymb}
\RequirePackage{mathtools}
\RequirePackage{physics}
\RequirePackage{siunitx}
\RequirePackage[super]{nth}
\RequirePackage[backend=biber,
                sorting=none]{biblatex}
\addbibresource{bibliography.bib}

\AtBeginDocument{\RenewCommandCopy\qty\SI}
\ExplSyntaxOn
\msg_redirect_name:nnn { siunitx } { physics-pkg } { none }
\ExplSyntaxOff

\RequirePackage{xcolor}
\definecolor{main_dark}{HTML}{072c3d}

\RequirePackage{tikz}
\RequirePackage{tikz-3dplot}
\usetikzlibrary{angles, quotes}
\tikzset{>=latex} % for LaTeX arrow head
\tikzstyle{vector}=[-stealth,myblue,thick,line cap=round]

\usetikzlibrary{quantikz2}

\renewcommand{\H}{\mathcal{H}}
\let\temp\phi
\let\phi\varphi
\let\varphi\temp

\renewcommand{\eqref}[1]{(\ref{#1})}

\RequirePackage{hyperref}
\hypersetup{colorlinks=true,   
            urlcolor=blue,
            linkcolor=black}

\RequirePackage{xifthen}
\RequirePackage{refcount}
\RequirePackage{xstring}

\newcommand{\thesistype}{MSc}

\newcommand\aayear[1]{\renewcommand\@aayear{#1}}
\newcommand\@aayear{\@latex@error{No \noexpand\aayear given}\@ehc}

\newcommand\phdname[1]{\renewcommand\@phdname{#1}}
\newcommand\@phdname{\@latex@error{No \noexpand\phdname given}\@ehc}

\DeclareOption{BSc}{\renewcommand{\thesistype}{BSc}}
\DeclareOption{MSc}{\renewcommand{\thesistype}{MSc}}
\DeclareOption{VO}{\renewcommand{\thesistype}{VO}}
\DeclareOption{PhD}{\renewcommand{\thesistype}{PhD}}
%\DeclareOption{italian}{\PassOptionsToPackage{italian}{babel}\selectlanguage{italian}}
%\DeclareOption{english}{\PassOptionsToPackage{english}{babel}\selectlanguage{english}}
\DeclareOption{italian}{\AtBeginDocument{\selectlanguage{italian}}}
\DeclareOption{english}{\AtBeginDocument{\selectlanguage{english}}}
%\DeclareOption{red}{\renewcommand{\headlinecolor}{\color{slcolor}}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{book}}
\ProcessOptions\relax


\providecommand*{\supervisorname}{Supervisors}
\providecommand*{\cosupervisorname}{Co-Supervisors}
\providecommand*{\CdLname}{BSc programme in Physics}
\providecommand*{\thesistypename}{final project}
\providecommand*{\aaname}{academic year}

\phdname{\iflanguage{italian}{fisica}{physics}}

\newcounter{supervisorsno}
\newcounter{cosupervisorsno}

\newcommand\@supervisors{\@latex@error{No supervisors given}\@ehc}
\NewEnviron{supervisors}{\global\let\@supervisors\BODY}

\newcommand\@cosupervisors{}
\newcommand\@cosupervisorscheck{NOCOSUPERVISORS}
\NewEnviron{cosupervisors}{\global\let\@cosupervisors\BODY\global\let\@cosupervisorscheck\@empty}

\newcommand{\supervisor}[3]{\refstepcounter{supervisorsno}#1 \> #2 #3 \\}

\newcommand{\cosupervisor}[3]{\refstepcounter{cosupervisorsno}#1 \> #2 #3 \\}

\newcommand{\svnon}{}

\newcommand{\cosvnon}{}

\AtBeginDocument{%
    \StrBehind{\getrefbykeydefault{svno}{anchor}{}}{.}[\svnon]
    \StrBehind{\getrefbykeydefault{cosvno}{anchor}{}}{.}[\cosvnon]
    \iflanguage{italian}{%
        \ifthenelse{\equal{\svnon}{1}}{%
            \renewcommand*\supervisorname{Relatore}%
        }{%
            \renewcommand*\supervisorname{Relatrice}%
        }
        \ifthenelse{\equal{\cosvnon}{1}}{%
            \renewcommand*\cosupervisorname{Correlatore}%
        }{%
            \renewcommand*\cosupervisorname{Correlatori}%
        }
        \renewcommand*\aaname{anno accademico}%
        \ifthenelse{\equal{\thesistype}{BSc}}{%
            \renewcommand{\CdLname}{corso di laurea in fisica}%
            \renewcommand{\thesistypename}{elaborato finale}%
        }{\relax}
        \ifthenelse{\equal{\thesistype}{MSc}}{%
            \renewcommand{\CdLname}{corso di laurea magistrale in fisica}%
            \renewcommand{\thesistypename}{elaborato finale}%
        }{\relax}
        \ifthenelse{\equal{\thesistype}{VO}}{%
            \renewcommand{\CdLname}{corso di laurea in fisica}%
            \renewcommand{\thesistypename}{tesi di laurea}%
        }{\relax}
        \ifthenelse{\equal{\thesistype}{PhD}}{%
            \renewcommand{\CdLname}{dottorato di ricerca in \@phdname}%
            \renewcommand{\thesistypename}{tesi di dottorato}%
        }{\relax}
    }{\relax}%
    \iflanguage{english}{%
        \ifthenelse{\equal{\svnon}{1}}{%
            \renewcommand*\supervisorname{Professor}%
        }{%
            \renewcommand*\supervisorname{Professor}%
        }
        \ifthenelse{\equal{\cosvnon}{1}}{%
            \renewcommand*\cosupervisorname{Co-Supervisor}%
        }{%
            \renewcommand*\cosupervisorname{Co-Supervisors}%
        }
        \renewcommand*\aaname{academic year}%
        \ifthenelse{\equal{\thesistype}{BSc}}{%
            \renewcommand{\CdLname}{BSc programme in physics}%
            \renewcommand{\thesistypename}{final project}%
        }{\relax}
        \ifthenelse{\equal{\thesistype}{MSc}}{%
            \renewcommand{\CdLname}{Dynamical Systems}%
            \renewcommand{\thesistypename}{final project}%
        }{\relax}
        \ifthenelse{\equal{\thesistype}{VO}}{%
            \renewcommand{\CdLname}{degree course in physics}%
            \renewcommand{\thesistypename}{degree thesis}%
        }{\relax}
        \ifthenelse{\equal{\thesistype}{PhD}}{%
            \renewcommand{\CdLname}{PhD programme in \@phdname}%
            \renewcommand{\thesistypename}{PhD thesis}%
        }{\relax}
    }{\relax}%
}

\newcommand{\maketitlepage}{%
    \begin{titlepage}
        \begin{center}
            \begin{minipage}[c]{0.45\textwidth}
               \begin{flushleft}
                  \includegraphics[height=0.1\textheight]{Images/logo_unito}
               \end{flushleft}
            \end{minipage}
            \hfill
            \begin{minipage}[c]{0.45\textwidth}
               \begin{flushright}
                  \includegraphics[height=0.1\textheight]{Images/logo_fisica}
               \end{flushright}
            \end{minipage}\\
            \medskip
            {\Large\sc\CdLname}\\
            \hbox to \textwidth{\hrulefill}
            \vspace{3truecm}
            {\large\sc\@author}
            \vfill
            \uppercase{{\LARGE\sc\@title}}
            % \vfill
            % \centerline{\hbox to 4truecm{\hrulefill}}
            % \medskip
            % {\sc\thesistypename}\\
            % \centerline{\hbox to 4truecm{\hrulefill}}
            \vfill
            \begin{flushleft}
                \begin{minipage}{0.4\textwidth}
                    \begin{tabbing}
                        \= Prof. P. Pallino \kill
                        \sc\supervisorname: \> \\
                        \@supervisors
                        \label{svno}%
                        \ifthenelse{\equal{\expandafter\@cosupervisorscheck}{NOCOSUPERVISORS}}{%
                           \relax
                        }{%
                           \medskip\\
                           \cosupervisorname: \> \\
                           \@cosupervisors
                           \label{cosvno}
                        }
                    \end{tabbing}
                \end{minipage}
            \end{flushleft}
            \vfill
            \hbox to \textwidth{\hrulefill}
            {\large\sc\aaname{} \@aayear}
        \end{center}
    \end{titlepage}
}
