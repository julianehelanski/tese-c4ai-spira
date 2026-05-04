# Análise de rede textual — Capítulo 1

> Análise de rede textual (*text network analysis*, Paranyushkin 2019)
> aplicada ao arquivo `ex_cap1 - 2026-05-04T155948.717.tex`. O texto foi limpo de comandos LaTeX,
> citações e notas de rodapé foram reincorporadas; janela deslizante de
> 4 *tokens* com pesos decrescentes pela distância (3-2-1). Comunidades
> detectadas por Louvain ponderado. Esta versão acrescenta duas métricas
> *informativas* que não dependem da frequência bruta: **PageRank** dos
> nós e **NPMI** das arestas. As métricas baseadas em frequência são
> mantidas em paralelo, para comparação.

## 1. Resumo quantitativo
- Tokens significativos: **15,555**
- Grafo bruto: **3429** nós · **24012** arestas
- Grafo analítico (top 180 nós, peso ≥ 2, maior componente): **180** nós · **2115** arestas
- Tópicos detectados (Louvain): **6**

## 2. Conceitos mais influentes (degree ponderado · *baseline* frequentista)
| # | termo | grau ponderado |
|---|-------|----------------|
| 1 | `pesquisa` | 661 |
| 2 | `ciencia` | 633 |
| 3 | `rede` | 619 |
| 4 | `claude` | 567 |
| 5 | `pesquisador` | 541 |
| 6 | `modelo` | 538 |
| 7 | `composicao` | 455 |
| 8 | `humano` | 418 |
| 9 | `objeto` | 391 |
| 10 | `inteligencia` | 390 |
| 11 | `artificial` | 380 |
| 12 | `campo` | 380 |
| 13 | `etnografia` | 358 |
| 14 | `metodo` | 330 |
| 15 | `sociais` | 304 |
| 16 | `escrita` | 290 |
| 17 | `construcao` | 280 |
| 18 | `tecnico` | 278 |
| 19 | `latour` | 275 |
| 20 | `pratica` | 257 |
| 21 | `agencia` | 241 |
| 22 | `dado` | 241 |
| 23 | `conhecimento` | 227 |
| 24 | `letramento` | 226 |
| 25 | `cientista` | 226 |
| 26 | `actante` | 222 |
| 27 | `parte` | 221 |
| 28 | `existencia` | 213 |
| 29 | `ator` | 201 |
| 30 | `maquina` | 199 |

## 3. Conceitos mais influentes (PageRank · centralidade na rede)
PageRank pondera a importância de um nó pela importância dos seus
vizinhos. Termos pouco frequentes mas bem posicionados na rede sobem;
termos frequentes mas perifericamente conectados descem.

| # | termo | PageRank |
|---|-------|----------|
| 1 | `pesquisa` | 0.0242 |
| 2 | `rede` | 0.0229 |
| 3 | `ciencia` | 0.0227 |
| 4 | `claude` | 0.0201 |
| 5 | `pesquisador` | 0.0198 |
| 6 | `modelo` | 0.0197 |
| 7 | `composicao` | 0.0162 |
| 8 | `humano` | 0.0158 |
| 9 | `campo` | 0.0147 |
| 10 | `objeto` | 0.0146 |
| 11 | `etnografia` | 0.0135 |
| 12 | `metodo` | 0.0134 |
| 13 | `inteligencia` | 0.0131 |
| 14 | `artificial` | 0.0128 |
| 15 | `sociais` | 0.0111 |
| 16 | `latour` | 0.0110 |
| 17 | `tecnico` | 0.0104 |
| 18 | `escrita` | 0.0104 |
| 19 | `construcao` | 0.0102 |
| 20 | `pratica` | 0.0099 |
| 21 | `agencia` | 0.0093 |
| 22 | `dado` | 0.0092 |
| 23 | `conhecimento` | 0.0088 |
| 24 | `actante` | 0.0087 |
| 25 | `cientista` | 0.0086 |
| 26 | `letramento` | 0.0085 |
| 27 | `existencia` | 0.0084 |
| 28 | `parte` | 0.0081 |
| 29 | `maquina` | 0.0079 |
| 30 | `ator` | 0.0077 |

## 4. Termos mais subvalorizados pela frequência (degree → PageRank)
Diferença de posição (rank por degree) − (rank por PageRank). Valor
positivo = o termo é *mais central na rede* do que sugere sua frequência.

| # | termo | degree-rank | pagerank-rank | salto |
|---|-------|-------------|----------------|-------|
| 1 | `operam` | 120 | 98 | +22 |
| 2 | `trata` | 99 | 86 | +13 |
| 3 | `conceito` | 109 | 96 | +13 |
| 4 | `registro` | 146 | 134 | +12 |
| 5 | `operacao` | 148 | 136 | +12 |
| 6 | `alienacao` | 116 | 106 | +10 |
| 7 | `corporacao` | 106 | 99 | +7 |
| 8 | `teorico` | 127 | 120 | +7 |
| 9 | `propoe` | 161 | 154 | +7 |
| 10 | `relacao` | 69 | 63 | +6 |
| 11 | `faire` | 83 | 77 | +6 |
| 12 | `ausencia` | 123 | 117 | +6 |
| 13 | `teria` | 150 | 144 | +6 |
| 14 | `problema` | 85 | 80 | +5 |
| 15 | `escolha` | 113 | 108 | +5 |

## 5. Pontes conceituais (betweenness — termos que costuram tópicos)
| # | termo | betweenness |
|---|-------|-------------|
| 1 | `ciencia` | 0.2223 |
| 2 | `pesquisa` | 0.1849 |
| 3 | `claude` | 0.1821 |
| 4 | `rede` | 0.1451 |
| 5 | `pesquisador` | 0.1358 |
| 6 | `objeto` | 0.0953 |
| 7 | `modelo` | 0.0913 |
| 8 | `humano` | 0.0783 |
| 9 | `campo` | 0.0620 |
| 10 | `composicao` | 0.0611 |
| 11 | `latour` | 0.0494 |
| 12 | `etnografia` | 0.0485 |
| 13 | `dado` | 0.0481 |
| 14 | `sociais` | 0.0349 |
| 15 | `centro` | 0.0321 |
| 16 | `metodo` | 0.0299 |
| 17 | `pratica` | 0.0280 |
| 18 | `tecnologia` | 0.0260 |
| 19 | `inteligencia` | 0.0235 |
| 20 | `acao` | 0.0231 |

## 6. Pares de termos com associação mais surpreendente (NPMI)
NPMI mede *quão surpreendente* é a co-ocorrência de duas palavras dadas
suas frequências individuais. Diferente do peso bruto, ele faz aparecer
pares semanticamente fortes mesmo quando os termos co-ocorrem poucas
vezes.

| # | termo A | termo B | NPMI | co-ocorr. (peso) |
|---|---------|---------|------|------------------|
| 1 | `inteligencia` | `artificial` | 0.847 | 185 |
| 2 | `existencias` | `parciais` | 0.839 | 84 |
| 3 | `existencia` | `parcial` | 0.767 | 64 |
| 4 | `teoria` | `ator` | 0.739 | 60 |
| 5 | `agencia` | `distribuida` | 0.699 | 58 |
| 6 | `tecnico` | `letramento` | 0.676 | 80 |
| 7 | `ausencia` | `presenca` | 0.634 | 23 |
| 8 | `ontologia` | `multiplicidade` | 0.601 | 23 |
| 9 | `visivel` | `tornava` | 0.598 | 16 |
| 10 | `alienacao` | `simondon` | 0.586 | 14 |
| 11 | `tecnica` | `alienacao` | 0.581 | 24 |
| 12 | `cientista` | `computacao` | 0.580 | 38 |
| 13 | `computacional` | `infraestrutura` | 0.574 | 24 |
| 14 | `resultados` | `produzem` | 0.565 | 16 |
| 15 | `mediacoes` | `tecnicas` | 0.552 | 18 |
| 16 | `modelo` | `linguagem` | 0.547 | 84 |
| 17 | `escrita` | `parte` | 0.539 | 42 |
| 18 | `acao` | `responsabilidade` | 0.538 | 18 |
| 19 | `sociais` | `cientista` | 0.525 | 50 |
| 20 | `faire` | `acao` | 0.517 | 20 |
| 21 | `condicoes` | `possibilidade` | 0.516 | 12 |
| 22 | `visivel` | `tornou` | 0.508 | 12 |
| 23 | `treinamento` | `dado` | 0.505 | 28 |
| 24 | `escrita` | `claude` | 0.503 | 74 |
| 25 | `ciencia` | `sociais` | 0.503 | 100 |

## 7. Tópicos latentes (comunidades Louvain)
- **Tópico 1** (40 termos): rede, latour, agencia, ator, distribuida, associacao
- **Tópico 2** (35 termos): pesquisa, inteligencia, artificial, etnografia, tecnico, pratica
- **Tópico 3** (34 termos): claude, pesquisador, modelo, composicao, objeto, escrita
- **Tópico 4** (31 termos): ciencia, sociais, construcao, dado, cientista, laboratorio
- **Tópico 5** (26 termos): humano, metodo, existencia, maquina, parcial, existencias
- **Tópico 6** (14 termos): campo, diagrama, tecnica, visivel, tornava, alienacao

## 8. Lacunas estruturais (pares de tópicos fracamente conectados)
Lacunas estruturais sinalizam *espaços de ideia* pouco articulados no
texto — candidatos a aprofundamento argumentativo.

- Lacuna entre **Tópico 4** [ciencia, sociais, construcao] e **Tópico 5** [humano, metodo, existencia] — densidade ponderada de ligação = 0.2965
- Lacuna entre **Tópico 1** [rede, latour, agencia] e **Tópico 4** [ciencia, sociais, construcao] — densidade ponderada de ligação = 0.3363
- Lacuna entre **Tópico 1** [rede, latour, agencia] e **Tópico 2** [pesquisa, inteligencia, artificial] — densidade ponderada de ligação = 0.3471
- Lacuna entre **Tópico 1** [rede, latour, agencia] e **Tópico 5** [humano, metodo, existencia] — densidade ponderada de ligação = 0.4250
- Lacuna entre **Tópico 2** [pesquisa, inteligencia, artificial] e **Tópico 5** [humano, metodo, existencia] — densidade ponderada de ligação = 0.4527
- Lacuna entre **Tópico 1** [rede, latour, agencia] e **Tópico 3** [claude, pesquisador, modelo] — densidade ponderada de ligação = 0.4904

## 9. Leitura interpretativa

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

## 10. Arquivos gerados
**Visões frequentistas (mantidas)**
- `infranodus_cap1_network.png` — rede completa, tamanho por degree.
- `infranodus_cap1_focus.png` — núcleo (top-100, peso ≥ 3).

**Visões informativas (novas)**
- `infranodus_cap1_pmi.png` — rede completa, tamanho por **PageRank**,
  arestas filtradas por **NPMI ≥ 0,20**.
- `infranodus_cap1_focus_pmi.png` — núcleo, NPMI ≥ 0,25.

**Dados**
- `infranodus_cap1_metrics.json` — métricas brutas (degree, betweenness,
  PageRank, NPMI, comunidades, lacunas).
- `infranodus_cap1.gexf` / `infranodus_cap1_focus.gexf` — grafos para Gephi
  já com `community`, `frequency`, `degree_weighted`, `betweenness`,
  `pagerank` (nós) e `weight`, `npmi` (arestas).
- `infranodus_cap1_nodes.csv` / `infranodus_cap1_edges.csv` (e `_focus_*`)
  — fallback em planilha; CSVs trazem todas as colunas acima.

## 11. Como abrir no Gephi
1. Instale Gephi (≥ 0.10): https://gephi.org/users/download/
2. `File → Open…` → selecione `infranodus_cap1.gexf` (ou `_focus.gexf`).
3. No painel **Appearance**: já vem com cor por `community` e tamanho por
   `degree_weighted` (embutidos via atributos `viz`). Ajuste se quiser.
4. Em **Layout**: aplique *ForceAtlas 2* (ative *Prevent Overlap* e
   *Dissuade Hubs*) por ~30 s; ou *Fruchterman-Reingold* para algo mais rápido.
5. Em **Statistics**: rode *Modularity* e *Average Path Length* se quiser
   recalcular comunidades dentro do Gephi (resultados serão semelhantes).
6. Em **Preview**: ative *Node Labels*, escolha fonte e exporte para PDF/SVG.
