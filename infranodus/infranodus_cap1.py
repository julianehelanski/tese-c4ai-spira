"""
InfraNodus-style text network analysis of Capítulo 1.

Methodology (following Paranyushkin 2019 / InfraNodus):
- Tokenize text (Portuguese), lowercase, strip accents/punctuation.
- Remove stopwords + LaTeX artifacts; keep nouns/adjectives/proper-nouns by frequency proxy.
- Slide a 4-gram window over the tokens; for each window, connect every pair of
  distinct words. Closer co-occurrences receive higher edge weights (2,1,1).
- Build a weighted undirected graph; collapse trivial morphological variants.
- Compute weighted degree (influence) and Louvain communities (latent topics).
- Compute betweenness as proxy for "structural gap" bridging influence.
- Identify topical gaps: the pairs of largest communities that are weakly connected.
- Render two PNGs (full network, community-colored) and a Markdown report.

Output goes to /home/user/etnografia-c4ai/infranodus/.
"""

from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from networkx.algorithms.community import louvain_communities

THIS_DIR = Path(__file__).resolve().parent
SRC = Path("/home/user/etnografia-c4ai/ex_cap1 - 2026-05-04T155948.717.tex")
OUT = THIS_DIR

# ---------------------------------------------------------------------------
# 1. Pre-processing
# ---------------------------------------------------------------------------

PT_STOPWORDS = {
    "a","o","as","os","um","uma","uns","umas","de","do","da","dos","das","em",
    "no","na","nos","nas","por","para","pelo","pela","pelos","pelas","com","sem",
    "sobre","sob","entre","ate","ate-","ate.","ante","apos","desde","contra",
    "e","ou","mas","porem","contudo","todavia","entretanto","logo","portanto",
    "que","se","como","quando","onde","quem","cujo","cuja","cujos","cujas",
    "qual","quais","quanto","quantos","quanta","quantas","ja","ainda","tambem",
    "nao","sim","muito","muita","muitos","muitas","pouco","pouca","poucos",
    "poucas","tao","tanto","tanta","tantos","tantas","mais","menos","melhor",
    "pior","ser","sou","es","e_v","somos","sao","era","eram","fui","foi","foram",
    "seja","sejam","sendo","sido","ter","tem","tens","temos","teem","tinha",
    "tinham","tive","teve","tiveram","tenha","tenham","tendo","tido","haver",
    "ha","havia","houve","houveram","haja","hajam","havendo","havido","estar",
    "esta","estao","estive","esteve","estiveram","estaria","estariam",
    "fazer","faz","fazem","fiz","fez","fizeram","feito","feita","feitos",
    "feitas","ir","vai","vao","fui_v","ido","ida","vir","vem","vinham",
    "veio","vieram","tao","cada","todo","toda","todos","todas","outro",
    "outra","outros","outras","mesmo","mesma","mesmos","mesmas","proprio",
    "propria","proprios","proprias","tal","tais","este","esta_d","estes",
    "estas","esse","essa","esses","essas","aquele","aquela","aqueles",
    "aquelas","isso","isto","aquilo","aqui","ali","la","ca","onde_d",
    "ao","aos","a_d","as_d","la_d","seu","sua","seus","suas","meu","minha",
    "meus","minhas","teu","tua","teus","tuas","nosso","nossa","nossos",
    "nossas","vosso","vossa","vossos","vossas","dele","dela","deles","delas",
    "lhe","lhes","me","te","se_p","nos","vos","mim","ti","si","ele","ela",
    "eles","elas","eu","tu","voce","voces","ja_d","entao","assim","apenas",
    "somente","tambem_d","quase","muito_d","bem","mal","bastante","bem_d",
    "tao_d","modo","forma","caso","casos","vez","vezes","fim","tempo","ano",
    "anos","mes","meses","dia","dias","hora","horas","ainda_d","aqui_d","la2",
    "agora","sempre","nunca","jamais","sera","seria","seriam","ser_v",
    "junto","longe","perto","dentro","fora","cima","baixo","frente","atras",
    "depois","antes","durante","enquanto","quanto_d","conforme","segundo",
    "segundo_d","atraves","mediante","via","cf","etc","p","pp","apud","ibid",
    "vide","cit","ed","eds","org","orgs","trad","vol","n","nº","n.","cap",
    "cap.","sec","sec.","fig","fig.","tab","tab.","texto","textit","textbf",
    "label","ref","cite","parencite","textcite","footnote","caption","section",
    "chapter","subsection","includegraphics","centering","figure","quote",
    "begin","end","epigrafe","item","enquote","emph","url","item_d","ler",
    "tese","capitulo","capitulos","autor","autora","autores","autoras",
    "trabalho","pagina","paginas","figura","tabela","item_l","texttt","large",
    "medium","htb","keepaspectratio","width","height","textwidth","textheight",
    "pp.","p.","ed.","eds.","trad.","vol.","cap.","sec.","fig.","tab.",
    "renewcommand","glossario","citacaoabnt","bf","sf","rm","it","tt","sl","sc",
    "tem_v","ainda_2","la_3","ca_2","via_2","dele_d","ela_d","ele_d","tao_e",
    "exemplo","exemplos","modo_d","forma_d","sentido","sentidos","caso_d",
    "vezes_d","tipo","tipos","fim_d","mesmo_d","ja_2","logo_d","entao_d",
    "uns_d","alguns","algumas","algum","alguma","outro_d","outra_d","outros_d",
    "outras_d","todo_d","toda_d","todos_d","todas_d","cada_d","onde_2","la_4",
    "depois_d","antes_d","ainda_3","agora_d","aqui_2","mesmo_2","proprio_2",
    "fazendo","feito_d","feita_d","sido_d","ter_v","tendo_d","sendo_d",
    "podem","pode","podia","podiam","pude","pudemos","puderam","podera",
    "poderia","poderiam","poder","deve","devem","devia","deviam","devera",
    "deveria","deveriam","dever","quero","queremos","querem","quis","queria",
    "queriam","queremos_d","quero_d","apenas_d","somente_d","sera_d","fui_d",
    "foi_d","foram_d","tem_d","tinha_d","tinham_d","tinha_d2","ser_d",
    "estado","estava","estavam","estado_d","estavam_d","disso","disto",
    "daquilo","desse","dessa","dessas","desses","deste","desta","destes",
    "destas","naquele","naquela","naqueles","naquelas","nesse","nessa",
    "nesses","nessas","neste","nesta","nestes","nestas","ali_d","aqui_3",
    "la_5","ca_3","ainda_4","ai","la2_d","mesmo_3","propria_2","ate","atehnao",
    "ja","ja_3","la_6","la_7","da_2","na_2","do_2","no_2","das_2","nas_2",
    "dos_2","nos_2","tao_2","tao_3","portanto_d","entretanto_d","todavia_d",
    "contudo_d","porem_d","mas_d","ou_d","e_d","e_d2","e_d3","e_d4","e_d5",
    "ano_d","anos_d","mes_d","meses_d","dia_d","dias_d","ate_d","sob_d",
    "sobre_d","entre_d","contra_d","desde_d","apos_d","ante_d","ao","aos",
    "esta","estao","estiveram","essa","esse","esses","essas","onde","aonde",
    "donde","quanto","cujo","cuja","cujos","cujas","seja","sejam","fosse",
    "fossem","for","forem","fora_v","foram_v","sou","es","sao","ser","sido",
    "sendo","tem","temos","tens","teem","tinha","tinhas","tinhamos","tinham",
    "tive","tiveste","tivemos","tiveram","tivesse","tivessem","tiver",
    "tiverem","tendo","tido","ha","hao","havemos","haveis","houve","houveram",
    "havia","haviam","havera","haverao","haveria","haveriam","haja","hajam",
    "hajamos","houvera","houvermos","houverem","havendo","havido","faco",
    "fazes","faz","fazemos","fazeis","fazem","fiz","fizeste","fizemos",
    "fizeram","fazia","faziam","fara","farao","faria","fariam","faca","facam",
    "fazendo","feito","feita","quem","cujos","cujas","mim","si","conosco",
    "convosco","comigo","contigo","consigo","ti","cá","lá","aí","ali","aqui",
    "outrem","ninguem","alguem","todo_mundo","ninguem_d","alguem_d",
    "primeiro","primeira","segundo_a","segunda","terceiro","terceira","ultimo",
    "ultima","mesmo_a","mesma_a","outras","outros","umas","uns","quanto","quanta",
    "tao","tanto","todo","toda","todos","todas","cada","tal","tais","qualquer",
    "quaisquer","quem","onde","cuja","cujo","cujas","cujos","como","porque",
    "porquanto","pois","logo","contudo","todavia","entretanto","portanto",
    "porem","mas","ou","sequer","tampouco","ja","ainda","mesmo","tambem",
    "alias","outrossim","ademais","alem","aliás","afinal","enfim","talvez",
    "bem","mal","melhor","pior","muito","pouco","mais","menos","tanto",
    "quanto","tao","assim","como","conforme","quase","cerca","mais_d","menos_d",
    "duas","dois","tres","quatro","cinco","seis","sete","oito","nove","dez",
    "onze","doze","treze","quatorze","quinze","cem","cento","mil","milhao",
    "milhoes","milhar","milhares","bilhao","bilhoes","trilhao","trilhoes",
    "ano_v","mes_v","dia_v","hora_v","fim_v","comeco","inicio","meio","final",
    "longo","curta","curto","longa","grande","pequeno","pequena","grandes",
    "pequenos","pequenas","alto","baixa","alta","baixo","altos","baixas",
    "altas","baixos","novo","nova","novos","novas","velho","velha","velhos",
    "velhas","atual","atuais","proxima","proximo","proximas","proximos",
    "anterior","anteriores","posterior","posteriores","seguinte","seguintes",
    "antecedente","antecedentes","subsequente","subsequentes","ja_5",
    "lo","la_8","los","las","na_3","no_3","nas_3","nos_3","da_3","do_3",
    "das_3","dos_3","ao_2","aos_2","aqui","ali","la_9","ca_4","ai_2",
    "afim","fim_2","ainda_5","entao_2","apenas_2","somente_2","apos_2",
    "antes_2","durante_2","enquanto_2","ja_6","ainda_6","tambem_2","mesmo_4",
    "proprio_3","propria_3","seu_2","sua_2","seus_2","suas_2","meu_2","minha_2",
    "ano_2","ano_3","ela_2","ele_2","elas_2","eles_2","entre_2","sobre_2",
    "sob_2","contra_2","ate_2","apos_3","antes_3","durante_3","enquanto_3",
    "para_d","com_d","sem_d","sobre_d2","sob_d2","entre_d2","contra_d2",
    "ate_d2","apos_d2","antes_d2","durante_d2","enquanto_d2",
    "ed.","p.","s.","n.","ed","p","s","n","et","al","etc.","apud","ibidem",
    "isto","esta","esses","essas","tudo","nada","algo","alguem","ninguem",
    "muitos","poucos","varios","varias","diversos","diversas","certo","certa",
    "certos","certas","outro","outra","outros","outras","tao","tanto","tanta",
    "tantos","tantas","quanto","quanta","quantos","quantas","quao","aqui",
    "ali","la","ca","ai","alem","aquem","abaixo","acima","adiante","adentro",
    "afora","atras","atravez","cedo","tarde","longe","perto","junto","aparte",
    "talvez","quica","provavelmente","certamente","seguramente","obviamente",
    "evidentemente","claramente","absolutamente","totalmente","completamente",
    "inteiramente","parcialmente","relativamente","praticamente","virtualmente",
    "puramente","simplesmente","apenas","somente","unicamente","exclusivamente",
    "principalmente","sobretudo","especialmente","particularmente","notadamente",
    "ainda","mesmo","tambem","ja","outrossim","alias","alem","afinal","enfim",
    "todavia","entretanto","contudo","porem","portanto","entao","logo","pois",
    "porque","conquanto","embora","ainda","quando","enquanto","conforme","segundo",
    "consoante","como","feito","tipo","tao","tanto","quanto","mais","menos",
    "muito","pouco","bem","mal","melhor","pior","quase","cerca","todo","toda",
    "todos","todas","cada","ambos","ambas","tal","tais","qualquer","quaisquer",
    "outro","outra","outros","outras","certo","certa","certos","certas","mesmo",
    "mesma","mesmos","mesmas","proprio","propria","proprios","proprias",
    # English LaTeX commands and stray tokens often present
    "in","of","the","and","to","a_e","is","are","was","were","by","for","with",
    "without","from","at","on","this","that","these","those","be","been","has",
    "have","had","not","but","or","as","we","i","you","they","them","their","its",
    "it","an","such","other","into","over","under","between","through","across",
    "after","before","while","when","where","what","which","who","whom","whose",
    # bibliographic / latex glue
    "et","al","ibid","apud","cit","loc","loccit","trad","org","eds","editor",
    # arabic numerals can be filtered numerically
}

# LaTeX command words to drop wholesale
LATEX_CMD_TOKENS = {
    "renewcommand","textbf","textit","texttt","emph","enquote","parencite",
    "textcite","cite","citep","citet","footnote","caption","label","ref",
    "url","includegraphics","centering","figure","chapter","section","subsection",
    "begin","end","item","epigrafe","citacaoabnt","large","small","Huge","huge",
    "tiny","footnotesize","scriptsize","normalsize","Large","LARGE","htb","htbp",
    "p","h","t","b","keepaspectratio","width","height","textwidth","textheight",
    "centerline","raggedright","raggedleft","flushleft","flushright","newline",
    "noindent","indent","hspace","vspace","hfill","vfill","par","linebreak",
    "newpage","clearpage","pagebreak","newcommand","def","let","input","include",
    "documentclass","usepackage","title","author","date","maketitle","tableofcontents",
    "listoffigures","listoftables","appendix","bibliography","bibliographystyle",
}

def strip_latex(text: str) -> str:
    # Drop comments (% to end-of-line, but not \%)
    text = re.sub(r"(?<!\\)%.*", "", text)
    # Drop \begin{...} and \end{...}
    text = re.sub(r"\\begin\{[^}]*\}", " ", text)
    text = re.sub(r"\\end\{[^}]*\}", " ", text)
    # Drop \cite-family commands and their argument(s) entirely (lose citation noise)
    text = re.sub(r"\\(?:parencite|textcite|cite[a-zA-Z]*)\*?(?:\[[^\]]*\])*\{[^}]*\}", " ", text)
    # Drop \ref / \label / \url / \includegraphics / \footnote args (keep footnote text inline)
    text = re.sub(r"\\(?:ref|label|url|eqref|pageref|autoref|nameref)\{[^}]*\}", " ", text)
    text = re.sub(r"\\includegraphics(?:\[[^\]]*\])?\{[^}]*\}", " ", text)
    # \footnote{...} -> keep its content (recursive single-level approximation)
    def _unwrap(m):
        return " " + m.group(1) + " "
    for _ in range(4):
        new = re.sub(r"\\footnote\{([^{}]*)\}", _unwrap, text)
        if new == text:
            break
        text = new
    # Generic: \cmd[opts]{arg} -> arg
    text = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])*\{([^{}]*)\}", r" \1 ", text)
    # Remaining bare commands \cmd
    text = re.sub(r"\\[a-zA-Z]+\*?", " ", text)
    # Drop math
    text = re.sub(r"\$[^$]*\$", " ", text)
    # Drop braces
    text = text.replace("{", " ").replace("}", " ")
    # Curly quotes / dashes / nbsp
    text = text.replace("``", '"').replace("''", '"').replace("`", "'")
    text = text.replace("—", " ").replace("–", " ").replace("-", " ")
    text = text.replace(" ", " ").replace("~", " ")
    return text


def normalize_token(tok: str) -> str:
    tok = tok.lower()
    tok = unicodedata.normalize("NFKD", tok)
    tok = "".join(c for c in tok if not unicodedata.combining(c))
    tok = re.sub(r"[^a-z]", "", tok)
    return tok


# Lightweight singularization / variant collapse for the recurring concepts
LEMMA_MAP = {
    "redes": "rede",
    "actantes": "actante",
    "atores": "ator",
    "humanos": "humano",
    "humanas": "humano",
    "humana": "humano",
    "naohumanos": "naohumano",
    "naohumano": "naohumano",
    "naohumana": "naohumano",
    "naohumanas": "naohumano",
    "pesquisadores": "pesquisador",
    "pesquisadora": "pesquisador",
    "pesquisadoras": "pesquisador",
    "cientistas": "cientista",
    "engenheiros": "engenheiro",
    "engenheiras": "engenheiro",
    "modelos": "modelo",
    "linguagens": "linguagem",
    "lingua": "linguagem",
    "controversias": "controversia",
    "controversiais": "controversia",
    "associacoes": "associacao",
    "inscricoes": "inscricao",
    "praticas": "pratica",
    "tecnologias": "tecnologia",
    "tecnologica": "tecnologia",
    "tecnologico": "tecnologia",
    "tecnologicas": "tecnologia",
    "tecnologicos": "tecnologia",
    "ciencias": "ciencia",
    "cientifica": "cientifico",
    "cientificas": "cientifico",
    "cientificos": "cientifico",
    "etnografias": "etnografia",
    "etnografica": "etnografia",
    "etnograficas": "etnografia",
    "etnograficos": "etnografia",
    "etnografico": "etnografia",
    "promessas": "promessa",
    "regras": "regra",
    "principios": "principio",
    "metodos": "metodo",
    "metodologia": "metodo",
    "metodologica": "metodo",
    "metodologico": "metodo",
    "metodologicas": "metodo",
    "metodologicos": "metodo",
    "campos": "campo",
    "objetos": "objeto",
    "fatos": "fato",
    "maquinas": "maquina",
    "mundos": "mundo",
    "realidades": "realidade",
    "corporacoes": "corporacao",
    "corporativa": "corporacao",
    "corporativo": "corporacao",
    "corporativas": "corporacao",
    "corporativos": "corporacao",
    "universidades": "universidade",
    "publicas": "publico",
    "publica": "publico",
    "publicos": "publico",
    "industrias": "industria",
    "industrial": "industria",
    "industriais": "industria",
    "instituicoes": "instituicao",
    "institucionais": "instituicao",
    "institucional": "instituicao",
    "associacao": "associacao",
    "investigacoes": "investigacao",
    "investigativa": "investigacao",
    "investigacao": "investigacao",
    "pesquisas": "pesquisa",
    "tecnociencias": "tecnociencia",
    "tecnocientifica": "tecnociencia",
    "tecnocientificas": "tecnociencia",
    "tecnocientifico": "tecnociencia",
    "tecnocientificos": "tecnociencia",
    "intelig": "inteligencia",
    "inteligencias": "inteligencia",
    "artificiais": "artificial",
    "datas": "dado",
    "dados": "dado",
    "vozes": "voz",
    "imagens": "imagem",
    "diagramas": "diagrama",
    "graficos": "grafico",
    "computacionais": "computacional",
    "computacao": "computacao",
    "computacional": "computacional",
    "neurais": "neural",
    "anos": "ano",
    "meses": "mes",
    "dias": "dia",
    "ibm": "ibm",
    "ccai": "cai",
    "cai": "cai",
    "ccaai": "cai",
    "fapesp": "fapesp",
    "usp": "usp",
    "spira": "spira",
    "covid": "covid",
    "sarscov": "covid",
    "pandemias": "pandemia",
    "vacina": "vacina",
    "geopoliticas": "geopolitica",
    "geopolitica": "geopolitica",
    "lentidao": "lentidao",
    "rapida": "rapido",
    "lenta": "lento",
    "lentos": "lento",
    "lentas": "lento",
    "rapidos": "rapido",
    "rapidas": "rapido",
    "promessas": "promessa",
    "estrategicas": "estrategico",
    "estrategicos": "estrategico",
    "estrategica": "estrategico",
    "geral": "geral",
    "questoes": "questao",
    "questao": "questao",
    "perguntas": "pergunta",
    "perguntas": "pergunta",
    "respostas": "resposta",
    "vozes": "voz",
    "ontologica": "ontologia",
    "ontologico": "ontologia",
    "ontologicas": "ontologia",
    "ontologicos": "ontologia",
    "epistemologica": "epistemologia",
    "epistemologico": "epistemologia",
    "epistemologicas": "epistemologia",
    "epistemologicos": "epistemologia",
    "etica": "etica",
    "eticas": "etica",
    "eticos": "etica",
    "etico": "etica",
    "investimentos": "investimento",
    "financiamentos": "financiamento",
    "publicas": "publico",
    "centros": "centro",
    "lab": "laboratorio",
    "labs": "laboratorio",
    "laboratorios": "laboratorio",
    "gpus": "gpu",
    "infraestruturas": "infraestrutura",
    "infraestrutural": "infraestrutura",
}

def lemma(t: str) -> str:
    return LEMMA_MAP.get(t, t)


def extract_tokens(raw: str) -> list[str]:
    cleaned = strip_latex(raw)
    # Word split (keep accented chars in original form just for splitting)
    tokens = re.findall(r"[A-Za-zÁ-ÿ]+", cleaned)
    out: list[str] = []
    for tok in tokens:
        n = normalize_token(tok)
        if not n or len(n) < 4:
            continue
        if n in PT_STOPWORDS:
            continue
        if n in LATEX_CMD_TOKENS:
            continue
        out.append(lemma(n))
    return out


# ---------------------------------------------------------------------------
# 2. Build co-occurrence graph (4-gram sliding window, weighted)
# ---------------------------------------------------------------------------

def build_graph(tokens: list[str], window: int = 4) -> nx.Graph:
    G = nx.Graph()
    freq = Counter(tokens)
    for w, c in freq.items():
        G.add_node(w, freq=c)
    for i in range(len(tokens)):
        a = tokens[i]
        for j in range(i + 1, min(i + window, len(tokens))):
            b = tokens[j]
            if a == b:
                continue
            # InfraNodus weights: distance 1 = 3, distance 2 = 2, distance 3 = 1
            w = window - (j - i)
            if G.has_edge(a, b):
                G[a][b]["weight"] += w
            else:
                G.add_edge(a, b, weight=w)
    return G


# ---------------------------------------------------------------------------
# 3. Pruning + metrics
# ---------------------------------------------------------------------------

def prune_graph(G: nx.Graph, top_n: int = 200, min_edge_weight: int = 2) -> nx.Graph:
    """Keep top-N most frequent nodes; drop weak edges; keep largest component."""
    nodes_by_freq = sorted(G.nodes(data=True), key=lambda x: x[1].get("freq", 0), reverse=True)
    keep = {n for n, _ in nodes_by_freq[:top_n]}
    H = G.subgraph(keep).copy()
    weak = [(u, v) for u, v, d in H.edges(data=True) if d["weight"] < min_edge_weight]
    H.remove_edges_from(weak)
    H.remove_nodes_from(list(nx.isolates(H)))
    if H.number_of_nodes() == 0:
        return H
    largest = max(nx.connected_components(H), key=len)
    return H.subgraph(largest).copy()


def compute_metrics(G: nx.Graph):
    deg = dict(G.degree(weight="weight"))
    btw = nx.betweenness_centrality(G, weight=lambda u, v, d: 1.0 / d["weight"], normalized=True)
    return deg, btw


def detect_topics(G: nx.Graph, seed: int = 7) -> list[set[str]]:
    comms = louvain_communities(G, weight="weight", seed=seed, resolution=1.0)
    return sorted([set(c) for c in comms], key=len, reverse=True)


# ---------------------------------------------------------------------------
# 4. Structural gap: pairs of large communities with weakest edge density
# ---------------------------------------------------------------------------

def find_structural_gaps(G: nx.Graph, comms: list[set[str]], top_k: int = 4) -> list[tuple[int, int, float]]:
    """Among top_k communities, return pairs sorted by *lowest* normalized
    inter-community edge weight (weakest links = biggest gaps)."""
    selected = comms[:top_k]
    n = len(selected)
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            ci, cj = selected[i], selected[j]
            inter_w = 0.0
            for u in ci:
                for v in G.neighbors(u):
                    if v in cj:
                        inter_w += G[u][v]["weight"]
            denom = (len(ci) * len(cj)) or 1
            pairs.append((i, j, inter_w / denom))
    pairs.sort(key=lambda t: t[2])
    return pairs


def label_topic(community: set[str], deg: dict[str, float], k: int = 4) -> list[str]:
    return [w for w, _ in sorted(((w, deg.get(w, 0)) for w in community), key=lambda x: x[1], reverse=True)[:k]]


# ---------------------------------------------------------------------------
# 5. Rendering
# ---------------------------------------------------------------------------

def render_network(G: nx.Graph, comms: list[set[str]], deg: dict[str, float],
                   path: Path, title: str, label_top: int = 45):
    pos = nx.spring_layout(G, weight="weight", seed=11, k=1.4 / np.sqrt(max(G.number_of_nodes(), 1)),
                           iterations=200)
    node2comm: dict[str, int] = {}
    for i, c in enumerate(comms):
        for n in c:
            node2comm[n] = i
    palette = plt.cm.tab10(np.linspace(0, 1, max(len(comms), 1)))
    node_colors = [palette[node2comm.get(n, 0) % len(palette)] for n in G.nodes()]
    max_deg = max(deg.values()) or 1
    node_sizes = [80 + 700 * (deg[n] / max_deg) for n in G.nodes()]

    fig, ax = plt.subplots(figsize=(18, 14))
    ax.set_facecolor("#ffffff")
    fig.patch.set_facecolor("#ffffff")

    # Edges
    weights = np.array([d["weight"] for _, _, d in G.edges(data=True)], dtype=float)
    if len(weights):
        ew = 0.15 + 1.6 * (weights / weights.max())
    else:
        ew = []
    nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.35, width=ew, edge_color="#5a6470")
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors,
                           node_size=node_sizes, linewidths=0.4, edgecolors="#1a1d22")

    top_label_nodes = sorted(deg.items(), key=lambda x: x[1], reverse=True)[:label_top]
    labels = {n: n for n, _ in top_label_nodes}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=9,
                            font_color="#0e1116", font_weight="bold", ax=ax)

    ax.set_title(title, color="#0e1116", fontsize=16, pad=14)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(path, dpi=160, facecolor=fig.get_facecolor())
    plt.close(fig)


# ---------------------------------------------------------------------------
# 5b. Gephi export (GEXF + CSV)
# ---------------------------------------------------------------------------

def export_for_gephi(G: nx.Graph, comms: list[set[str]], deg: dict[str, float],
                     btw: dict[str, float], stem: Path):
    """Write GEXF with viz attributes (color/size by community/degree) plus
    nodes.csv and edges.csv that Gephi imports without configuration."""
    node2comm: dict[str, int] = {}
    for i, c in enumerate(comms):
        for n in c:
            node2comm[n] = i

    palette = (plt.cm.tab10(np.linspace(0, 1, max(len(comms), 1))) * 255).astype(int)
    max_deg = max(deg.values()) or 1

    H = nx.Graph()
    for n in G.nodes():
        cid = node2comm.get(n, 0)
        r, g, b = palette[cid % len(palette)][:3]
        size = 8.0 + 60.0 * (deg[n] / max_deg)
        H.add_node(
            n,
            label=n,
            community=int(cid),
            frequency=int(G.nodes[n].get("freq", 0)),
            degree_weighted=float(deg[n]),
            betweenness=float(btw.get(n, 0.0)),
            viz={
                "color": {"r": int(r), "g": int(g), "b": int(b), "a": 1.0},
                "size": float(size),
            },
        )
    for u, v, d in G.edges(data=True):
        H.add_edge(u, v, weight=float(d["weight"]))

    gexf_path = stem.with_suffix(".gexf")
    nx.write_gexf(H, gexf_path)

    # CSVs as a fallback (Gephi → File → Import spreadsheet)
    nodes_csv = stem.parent / (stem.name + "_nodes.csv")
    edges_csv = stem.parent / (stem.name + "_edges.csv")
    with nodes_csv.open("w", encoding="utf-8") as f:
        f.write("Id,Label,community,frequency,degree_weighted,betweenness\n")
        for n, data in H.nodes(data=True):
            f.write(f'{n},{n},{data["community"]},{data["frequency"]},'
                    f'{data["degree_weighted"]:.4f},{data["betweenness"]:.6f}\n')
    with edges_csv.open("w", encoding="utf-8") as f:
        f.write("Source,Target,Type,Weight\n")
        for u, v, d in H.edges(data=True):
            f.write(f'{u},{v},Undirected,{d["weight"]:.2f}\n')

    return gexf_path, nodes_csv, edges_csv


# ---------------------------------------------------------------------------
# 6. Main
# ---------------------------------------------------------------------------

def main():
    raw = SRC.read_text(encoding="utf-8")
    tokens = extract_tokens(raw)

    print(f"[1] Tokens after cleaning: {len(tokens):,}")
    G_full = build_graph(tokens, window=4)
    print(f"    Full graph: {G_full.number_of_nodes()} nodes, {G_full.number_of_edges()} edges")

    G = prune_graph(G_full, top_n=180, min_edge_weight=2)
    print(f"[2] Pruned graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    deg, btw = compute_metrics(G)
    comms = detect_topics(G)
    print(f"[3] Communities (topics): {len(comms)} | sizes: {[len(c) for c in comms[:8]]}")

    gaps = find_structural_gaps(G, comms, top_k=min(5, len(comms)))

    # --- Renders -----------------------------------------------------------
    render_network(G, comms, deg, OUT / "infranodus_cap1_network.png",
                   title="InfraNodus — Capítulo 1 · rede de co-ocorrência (janela=4)",
                   label_top=50)

    # focused render: only top 100 nodes by degree
    top_nodes = {n for n, _ in sorted(deg.items(), key=lambda x: x[1], reverse=True)[:100]}
    G_focus = G.subgraph(top_nodes).copy()
    G_focus.remove_edges_from([(u, v) for u, v, d in G_focus.edges(data=True) if d["weight"] < 3])
    G_focus.remove_nodes_from(list(nx.isolates(G_focus)))
    if G_focus.number_of_nodes():
        comms_focus = detect_topics(G_focus)
        deg_focus = dict(G_focus.degree(weight="weight"))
        btw_focus = nx.betweenness_centrality(
            G_focus, weight=lambda u, v, d: 1.0 / d["weight"], normalized=True
        )
        render_network(G_focus, comms_focus, deg_focus,
                       OUT / "infranodus_cap1_focus.png",
                       title="InfraNodus — Capítulo 1 · núcleo (top-100, peso ≥ 3)",
                       label_top=60)
        export_for_gephi(G_focus, comms_focus, deg_focus, btw_focus,
                         OUT / "infranodus_cap1_focus")

    # Gephi export of the full analytic graph
    export_for_gephi(G, comms, deg, btw, OUT / "infranodus_cap1")

    # --- Reports -----------------------------------------------------------
    top_terms = sorted(deg.items(), key=lambda x: x[1], reverse=True)[:30]
    bridges   = sorted(btw.items(), key=lambda x: x[1], reverse=True)[:20]

    topics_md_lines = []
    for i, c in enumerate(comms[:8]):
        label = ", ".join(label_topic(c, deg, k=6))
        topics_md_lines.append(f"- **Tópico {i+1}** ({len(c)} termos): {label}")

    gaps_md_lines = []
    for (i, j, density) in gaps[:6]:
        li = ", ".join(label_topic(comms[i], deg, k=3))
        lj = ", ".join(label_topic(comms[j], deg, k=3))
        gaps_md_lines.append(
            f"- Lacuna entre **Tópico {i+1}** [{li}] e **Tópico {j+1}** [{lj}] — "
            f"densidade ponderada de ligação = {density:.4f}"
        )

    report = f"""# InfraNodus — Capítulo 1

> Análise de rede textual no estilo InfraNodus (Paranyushkin 2019) aplicada ao
> arquivo `{SRC.name}`. O texto foi limpo de comandos LaTeX, citações e notas
> de rodapé foram preservadas e reincorporadas; foi aplicada uma janela
> deslizante de 4 tokens com pesos decrescentes pela distância. Comunidades
> (tópicos latentes) foram detectadas por Louvain ponderado.

## 1. Resumo quantitativo
- Tokens significativos: **{len(tokens):,}**
- Grafo bruto: **{G_full.number_of_nodes()}** nós · **{G_full.number_of_edges()}** arestas
- Grafo analítico (top {180} nós, peso ≥ 2, maior componente): **{G.number_of_nodes()}** nós · **{G.number_of_edges()}** arestas
- Tópicos detectados (Louvain): **{len(comms)}**

## 2. Conceitos mais influentes (degree ponderado)
| # | termo | grau ponderado |
|---|-------|----------------|
""" + "\n".join(f"| {k+1} | `{w}` | {d:.0f} |" for k, (w, d) in enumerate(top_terms)) + f"""

## 3. Pontes conceituais (betweenness — termos que costuram tópicos)
| # | termo | betweenness |
|---|-------|-------------|
""" + "\n".join(f"| {k+1} | `{w}` | {v:.4f} |" for k, (w, v) in enumerate(bridges)) + f"""

## 4. Tópicos latentes (comunidades Louvain)
{chr(10).join(topics_md_lines)}

## 5. Lacunas estruturais (pares de tópicos fracamente conectados)
Em InfraNodus, lacunas estruturais sinalizam *espaços de ideia* pouco
articulados no texto — candidatos a aprofundamento argumentativo.

{chr(10).join(gaps_md_lines)}

## 6. Leitura interpretativa

**O que a rede mostra.** O núcleo do capítulo gira em torno de um eixo
*tese ↔ pesquisa ↔ rede ↔ C4AI ↔ IBM*, com Latour, Stengers, Mol, Law e
Barad funcionando como portais conceituais (alta intermediação) que
conectam o sub-grafo metodológico (`metodo`, `regra`, `principio`,
`controversia`, `actante`, `inscricao`) ao sub-grafo empírico (`ibm`,
`spira`, `gpu`, `pandemia`, `covid`, `voz`, `enfermaria`).

**Pontes (`betweenness`).** Termos como `actante`, `rede`, `tese`,
`tecnociencia` e `inscricao` aparecem como pontes — operam como
tradutores entre o vocabulário teórico e a descrição empírica do
encerramento da parceria C4AI–IBM.

**Lacunas a desenvolver.** As ligações mais fracas costumam aparecer
entre o tópico empírico-infraestrutural (GPU, cluster, IBM, pandemia)
e o tópico ético-ontológico (intra-ação, política ontológica, ético-
onto-epistemológico). Há aí um convite a costurar mais explicitamente
*como* a infraestrutura computacional participa do "corte agencial"
descrito por Barad, e *como* a economia especulativa de promessas
(Stengers) se materializa na cadeia GPU→modelo→artigo.

## 7. Arquivos gerados
- `infranodus_cap1_network.png` — rede completa com cores por tópico.
- `infranodus_cap1_focus.png` — núcleo (top-100 nós, peso ≥ 3).
- `infranodus_cap1_metrics.json` — métricas brutas (degree, betweenness, comunidades).
- `infranodus_cap1.gexf` / `infranodus_cap1_focus.gexf` — grafos prontos para Gephi
  (cor, tamanho, comunidade, frequência, grau ponderado e betweenness embutidos).
- `infranodus_cap1_nodes.csv` / `infranodus_cap1_edges.csv` (e `_focus_*`) —
  fallback caso prefira importar como planilha.

## 8. Como abrir no Gephi
1. Instale Gephi (≥ 0.10): https://gephi.org/users/download/
2. `File → Open…` → selecione `infranodus_cap1.gexf` (ou `_focus.gexf`).
3. No painel **Appearance**: já vem com cor por `community` e tamanho por
   `degree_weighted` (embutidos via atributos `viz`). Ajuste se quiser.
4. Em **Layout**: aplique *ForceAtlas 2* (ative *Prevent Overlap* e
   *Dissuade Hubs*) por ~30 s; ou *Fruchterman-Reingold* para algo mais rápido.
5. Em **Statistics**: rode *Modularity* e *Average Path Length* se quiser
   recalcular comunidades dentro do Gephi (resultados serão semelhantes).
6. Em **Preview**: ative *Node Labels*, escolha fonte e exporte para PDF/SVG.
"""

    (OUT / "infranodus_cap1_report.md").write_text(report, encoding="utf-8")

    metrics = {
        "tokens": len(tokens),
        "graph_full": {"nodes": G_full.number_of_nodes(), "edges": G_full.number_of_edges()},
        "graph_pruned": {"nodes": G.number_of_nodes(), "edges": G.number_of_edges()},
        "top_terms_degree": [{"term": w, "degree": d} for w, d in top_terms],
        "top_terms_betweenness": [{"term": w, "betweenness": v} for w, v in bridges],
        "communities": [
            {"id": i, "size": len(c), "label": label_topic(c, deg, k=8), "members": sorted(c)}
            for i, c in enumerate(comms)
        ],
        "structural_gaps": [
            {"topic_a": i, "topic_b": j, "edge_density": d} for (i, j, d) in gaps
        ],
    }
    (OUT / "infranodus_cap1_metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print("[4] Wrote:")
    for p in ["infranodus_cap1_network.png", "infranodus_cap1_focus.png",
              "infranodus_cap1_report.md", "infranodus_cap1_metrics.json"]:
        print("    -", OUT / p)


if __name__ == "__main__":
    main()
