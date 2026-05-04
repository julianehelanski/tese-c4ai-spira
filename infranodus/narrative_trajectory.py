"""
Narrative trajectory analysis of capítulo 1.

Three complementary views, all answering questions about *order* and
*flow* rather than aggregate co-occurrence:

  1. Gantt lexical (`trajectory_gantt.png`):
     for each top concept, draws a horizontal life-span from its first
     paragraph to its last; ticks mark every occurrence. Sorted by
     entry order — answers "where does each idea enter and exit?".

  2. Alluvial / Sankey (`trajectory_alluvial.png`):
     splits the chapter into K sequential segments, ranks the top
     concepts per segment, and connects them across adjacent segments
     when they persist — answers "what links to what across the chapter?".

  3. Semantic trajectory (`trajectory_semantic.png`):
     embeds each paragraph with a multilingual sentence-transformer,
     projects to 2D with PCA, draws the path through that space colored
     by reading order — answers "what arc does the chapter trace?".

Reuses tokenization / lemmatization from `infranodus_cap1.py`.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(THIS_DIR))

from infranodus_cap1 import (  # noqa: E402
    LATEX_CMD_TOKENS,
    PT_STOPWORDS,
    SRC,
    lemma,
    normalize_token,
    strip_latex,
)


# ---------------------------------------------------------------------------
# 1. Paragraph extraction (preserves reading order)
# ---------------------------------------------------------------------------

def extract_paragraphs(raw: str, min_chars: int = 120) -> list[str]:
    """Split chapter into paragraphs after LaTeX cleanup, keeping order.

    LaTeX environments like figure/citacaoabnt produce short or empty
    paragraphs after stripping; we filter those out by character length.
    """
    cleaned = strip_latex(raw)
    paras = [p.strip() for p in re.split(r"\n{2,}", cleaned)]
    paras = [re.sub(r"\s+", " ", p) for p in paras]
    return [p for p in paras if len(p) >= min_chars]


def tokenize(text: str) -> list[str]:
    out: list[str] = []
    for tok in re.findall(r"[A-Za-zÁ-ÿ]+", text):
        n = normalize_token(tok)
        if not n or len(n) < 4:
            continue
        if n in PT_STOPWORDS or n in LATEX_CMD_TOKENS:
            continue
        out.append(lemma(n))
    return out


# ---------------------------------------------------------------------------
# 2. Gantt lexical
# ---------------------------------------------------------------------------

def render_gantt(paras: list[str], para_tokens: list[list[str]],
                  top_concepts: list[str], path: Path):
    info = {}
    for c in top_concepts:
        positions = [i for i, ts in enumerate(para_tokens) if c in ts]
        if not positions:
            continue
        info[c] = {
            "first": positions[0],
            "last": positions[-1],
            "all": positions,
            "count": sum(ts.count(c) for ts in para_tokens),
        }

    concepts_sorted = sorted(info.items(), key=lambda kv: kv[1]["first"])

    fig, ax = plt.subplots(figsize=(17, max(8, 0.42 * len(concepts_sorted) + 2)))
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")

    palette = plt.cm.tab20(np.linspace(0, 1, max(len(concepts_sorted), 1)))
    n_paras = len(paras)

    for i, (c, d) in enumerate(concepts_sorted):
        col = palette[i]
        ax.hlines(y=i, xmin=d["first"], xmax=d["last"], colors=col, linewidth=5, alpha=0.45)
        ax.scatter(d["all"], [i] * len(d["all"]), color=col, s=22,
                   edgecolor="#1a1d22", linewidth=0.4, zorder=3)
        ax.text(d["last"] + 0.6, i, f"  {c}  ({d['count']}×)",
                va="center", fontsize=9, color="#0e1116")
        ax.text(d["first"] - 0.6, i, f"¶{d['first']+1}",
                va="center", ha="right", fontsize=8, color="#6b7280")

    ax.set_yticks([])
    ax.set_xlabel("parágrafo (ordem de leitura) →", fontsize=11, color="#0e1116")
    ax.set_xlim(-3, n_paras + 8)
    ax.set_ylim(-1, len(concepts_sorted))
    ax.invert_yaxis()
    ax.set_title(
        "Capítulo 1 · Gantt lexical: entrada, persistência e saída dos conceitos\n"
        "(barra = ‘vida’ do conceito · pontos = ocorrências · ordenado por entrada)",
        fontsize=13, color="#0e1116", pad=12,
    )
    ax.grid(axis="x", alpha=0.2)
    for spine in ("top", "right", "left"):
        ax.spines[spine].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=160, facecolor="#ffffff")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 3. Alluvial / Sankey across K segments
# ---------------------------------------------------------------------------

def render_alluvial(paras: list[str], para_tokens: list[list[str]],
                     path: Path, K: int = 8, top_per_seg: int = 5):
    n = len(paras)
    bounds = [(round(k * n / K), round((k + 1) * n / K)) for k in range(K)]

    seg_counts = []
    for s, e in bounds:
        toks = [t for i in range(s, e) for t in para_tokens[i]]
        seg_counts.append(Counter(toks))
    seg_top = [[w for w, _ in c.most_common(top_per_seg)] for c in seg_counts]

    universe = sorted({c for s in seg_top for c in s})
    cmap = plt.cm.tab20(np.linspace(0, 1, max(len(universe), 1)))
    color = {c: cmap[i] for i, c in enumerate(universe)}

    fig, ax = plt.subplots(figsize=(20, 10))
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")

    box_w, box_h, gap = 0.6, 0.85, 0.18
    col_x = np.arange(K) * 3.4

    boxes = {}
    for k, top in enumerate(seg_top):
        for r, c in enumerate(top):
            y_top = -r * (box_h + gap)
            y_bot = y_top - box_h
            boxes[(k, c)] = (col_x[k], y_top, y_bot)
            ax.add_patch(plt.Rectangle(
                (col_x[k] - box_w / 2, y_bot), box_w, box_h,
                facecolor=color[c], edgecolor="#1a1d22", linewidth=0.7,
            ))
            ax.text(col_x[k], (y_top + y_bot) / 2, c, ha="center", va="center",
                    fontsize=9.5, color="#0e1116", fontweight="bold")

    # Persistence ribbons between adjacent segments
    for k in range(K - 1):
        for c in seg_top[k]:
            if c not in seg_top[k + 1]:
                continue
            x1, y1t, y1b = boxes[(k, c)]
            x2, y2t, y2b = boxes[(k + 1, c)]
            left = x1 + box_w / 2
            right = x2 - box_w / 2
            mid = (left + right) / 2
            poly_x = [left, mid, mid, right, right, mid, mid, left]
            poly_y = [y1t, y1t, y2t, y2t, y2b, y2b, y1b, y1b]
            ax.fill(poly_x, poly_y, color=color[c], alpha=0.22, linewidth=0)

    # Indicate "entrance" (concept appears for first time in a segment) and "exit"
    seen_so_far: set[str] = set()
    for k, top in enumerate(seg_top):
        for c in top:
            if c in seen_so_far:
                continue
            x, yt, yb = boxes[(k, c)]
            ax.plot([x - box_w / 2 - 0.15, x - box_w / 2],
                    [(yt + yb) / 2, (yt + yb) / 2],
                    color=color[c], lw=2)
            ax.plot(x - box_w / 2 - 0.15, (yt + yb) / 2,
                    marker=">", markersize=8, color=color[c])
            seen_so_far.add(c)

    for k in range(K):
        last_seen = {c for c in seg_top[k] if c not in (seg_top[k + 1] if k + 1 < K else [])}
        for c in last_seen:
            x, yt, yb = boxes[(k, c)]
            ax.plot([x + box_w / 2, x + box_w / 2 + 0.15],
                    [(yt + yb) / 2, (yt + yb) / 2],
                    color=color[c], lw=2, alpha=0.6)

    # Segment labels
    for k, (s, e) in enumerate(bounds):
        ax.text(col_x[k], 1.2, f"Seg. {k+1}\n¶{s+1}–{e}",
                ha="center", va="bottom", fontsize=10, color="#374151",
                fontweight="bold")

    ax.set_xlim(col_x[0] - 1.6, col_x[-1] + 1.6)
    y_min = -top_per_seg * (box_h + gap) - 0.4
    ax.set_ylim(y_min, 2.5)
    ax.axis("off")
    ax.set_title(
        f"Capítulo 1 · fluxo de tópicos por segmento (top-{top_per_seg} em {K} segmentos sequenciais)\n"
        "blocos = peso local · faixas = persistência · ▶ = primeira aparição na cadeia",
        fontsize=13, color="#0e1116", pad=14,
    )
    fig.tight_layout()
    fig.savefig(path, dpi=160, facecolor="#ffffff")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 4. Semantic trajectory (paragraph embeddings → PCA 2D)
# ---------------------------------------------------------------------------

def render_semantic_trajectory(paras: list[str], para_tokens: list[list[str]],
                                 path: Path, group_size: int = 5):
    """Embed groups of paragraphs ("moments") and project to 2D.

    Tries the multilingual sentence-transformer first; if the model can't
    be downloaded (offline / blocked), falls back to TF-IDF + Truncated SVD
    (Latent Semantic Analysis), which is a respectable in-corpus embedding
    that captures the same notion of paragraph similarity without external
    weights.

    Paragraphs are grouped into windows of `group_size` to produce a
    smoother trajectory; per-paragraph embeddings of a long chapter tend
    to live in a noisy high-dimensional space whose 2D projection is
    visually overcrowded.
    """
    from sklearn.decomposition import PCA, TruncatedSVD
    from sklearn.feature_extraction.text import TfidfVectorizer

    # Group paragraphs into moments
    n_paras = len(paras)
    moments_text: list[str] = []
    moments_tokens: list[list[str]] = []
    moments_bounds: list[tuple[int, int]] = []
    for s in range(0, n_paras, group_size):
        e = min(s + group_size, n_paras)
        moments_text.append(" ".join(paras[s:e]))
        moments_tokens.append([t for i in range(s, e) for t in para_tokens[i]])
        moments_bounds.append((s, e))

    method = "sentence-transformer (paraphrase-multilingual-MiniLM-L12-v2)"
    try:
        from sentence_transformers import SentenceTransformer
        print("    [embeddings] tentando sentence-transformer ...")
        model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        emb = model.encode(moments_text, show_progress_bar=False, batch_size=16,
                            normalize_embeddings=True)
        pca = PCA(n_components=2)
        coords = pca.fit_transform(emb)
        var_ratio = pca.explained_variance_ratio_
    except Exception as e:
        print(f"    [embeddings] fallback para TF-IDF + LSA ({type(e).__name__})")
        method = "TF-IDF + LSA (Truncated SVD, in-corpus)"
        joined = [" ".join(ts) for ts in moments_tokens]
        vec = TfidfVectorizer(min_df=1, max_df=0.9, ngram_range=(1, 2),
                               sublinear_tf=True)
        X = vec.fit_transform(joined)
        n_components = min(40, X.shape[0] - 1, X.shape[1] - 1)
        svd = TruncatedSVD(n_components=n_components, random_state=7)
        emb = svd.fit_transform(X)
        norms = np.linalg.norm(emb, axis=1, keepdims=True)
        emb = emb / np.maximum(norms, 1e-9)
        pca = PCA(n_components=2)
        coords = pca.fit_transform(emb)
        var_ratio = pca.explained_variance_ratio_

    var1, var2 = var_ratio[0] * 100, var_ratio[1] * 100

    fig, ax = plt.subplots(figsize=(16, 12))
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")

    n = len(coords)
    colors = plt.cm.viridis(np.linspace(0, 1, n))

    # Trajectory arrows
    for i in range(n - 1):
        ax.annotate("", xy=coords[i + 1], xytext=coords[i],
                    arrowprops=dict(arrowstyle="-|>", color=colors[i],
                                     alpha=0.7, lw=1.6,
                                     mutation_scale=14))

    # Points
    ax.scatter(coords[:, 0], coords[:, 1], s=140, c=colors,
                edgecolor="#1a1d22", linewidth=0.6, zorder=3)

    # Label every moment with its dominant term
    for i, (s, e) in enumerate(moments_bounds):
        c = Counter(moments_tokens[i])
        top_term = c.most_common(1)[0][0] if c else "—"
        dx, dy = (10, 10) if i % 2 == 0 else (10, -16)
        ax.annotate(f"¶{s+1}–{e} · {top_term}", coords[i],
                     xytext=(dx, dy), textcoords="offset points",
                     fontsize=8.5, color="#0e1116", fontweight="bold",
                     bbox=dict(boxstyle="round,pad=0.22",
                                facecolor="white", edgecolor="#cbd5e1",
                                linewidth=0.6, alpha=0.92))

    # Start / end markers
    ax.scatter(*coords[0], s=460, marker="*", color="#10b981",
                edgecolor="#0e1116", linewidth=1.5, zorder=4,
                label=f"início · ¶1–{moments_bounds[0][1]}")
    ax.scatter(*coords[-1], s=320, marker="X", color="#ef4444",
                edgecolor="#0e1116", linewidth=1.5, zorder=4,
                label=f"fim · ¶{moments_bounds[-1][0]+1}–{moments_bounds[-1][1]}")

    ax.set_xlabel(f"PC1 ({var1:.1f}% da variância)", fontsize=11, color="#0e1116")
    ax.set_ylabel(f"PC2 ({var2:.1f}% da variância)", fontsize=11, color="#0e1116")
    ax.set_title(
        f"Capítulo 1 · trajetória semântica em {n} momentos (grupos de {group_size} parágrafos)\n"
        f"(embeddings: {method} · projeção PCA 2D · cor = ordem de leitura)",
        fontsize=12, color="#0e1116", pad=12,
    )
    ax.legend(loc="best", frameon=True, framealpha=0.9)
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(path, dpi=160, facecolor="#ffffff")
    plt.close(fig)

    return coords


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    raw = SRC.read_text(encoding="utf-8")
    paras = extract_paragraphs(raw)
    para_tokens = [tokenize(p) for p in paras]
    print(f"[1] Paragraphs extracted: {len(paras)}")
    print(f"    Tokens per paragraph (mean): {np.mean([len(t) for t in para_tokens]):.1f}")

    # Pick concepts to display in the Gantt: top by frequency, but skipping
    # generic ones whose ubiquity drowns the timeline.
    flat = [t for ts in para_tokens for t in ts]
    freq = Counter(flat)
    GANTT_SIZE = 20
    SKIP = {"parte", "modo", "tipo", "questao", "geral", "exemplo",
            "claude"}  # remove if you want the AI-assistant marker visible
    candidates = [w for w, _ in freq.most_common(60) if w not in SKIP]
    top_concepts = candidates[:GANTT_SIZE]

    out = THIS_DIR
    print(f"[2] Rendering Gantt ({len(top_concepts)} concepts) ...")
    render_gantt(paras, para_tokens, top_concepts, out / "trajectory_gantt.png")

    print(f"[3] Rendering alluvial flow (K=8 segments) ...")
    render_alluvial(paras, para_tokens, out / "trajectory_alluvial.png", K=8, top_per_seg=5)

    print(f"[4] Rendering semantic trajectory ...")
    render_semantic_trajectory(paras, para_tokens, out / "trajectory_semantic.png")

    print("[5] Done. Outputs:")
    for n in ["trajectory_gantt.png", "trajectory_alluvial.png", "trajectory_semantic.png"]:
        print("    -", out / n)


if __name__ == "__main__":
    main()
