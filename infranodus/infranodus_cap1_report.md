# InfraNodus — Capítulo 1

> Análise de rede textual no estilo InfraNodus (Paranyushkin 2019) aplicada ao
> arquivo `ex_cap1 - 2026-05-04T155948.717.tex`. O texto foi limpo de comandos LaTeX, citações e notas
> de rodapé foram preservadas e reincorporadas; foi aplicada uma janela
> deslizante de 4 tokens com pesos decrescentes pela distância. Comunidades
> (tópicos latentes) foram detectadas por Louvain ponderado.

## 1. Resumo quantitativo
- Tokens significativos: **15,555**
- Grafo bruto: **3429** nós · **24012** arestas
- Grafo analítico (top 180 nós, peso ≥ 2, maior componente): **180** nós · **2115** arestas
- Tópicos detectados (Louvain): **7**

## 2. Conceitos mais influentes (degree ponderado)
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
| 11 | `campo` | 380 |
| 12 | `artificial` | 380 |
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
| 24 | `cientista` | 226 |
| 25 | `letramento` | 226 |
| 26 | `actante` | 222 |
| 27 | `parte` | 221 |
| 28 | `existencia` | 213 |
| 29 | `ator` | 201 |
| 30 | `maquina` | 199 |

## 3. Pontes conceituais (betweenness — termos que costuram tópicos)
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

## 4. Tópicos latentes (comunidades Louvain)
- **Tópico 1** (37 termos): claude, pesquisador, modelo, composicao, objeto, escrita
- **Tópico 2** (33 termos): ciencia, sociais, dado, cientista, laboratorio, social
- **Tópico 3** (33 termos): rede, latour, agencia, ator, distribuida, associacao
- **Tópico 4** (27 termos): pesquisa, etnografia, construcao, pratica, centro, vocabulario
- **Tópico 5** (22 termos): humano, metodo, existencia, maquina, parcial, existencias
- **Tópico 6** (15 termos): campo, diagrama, tecnica, tornou, visivel, tornava
- **Tópico 7** (13 termos): inteligencia, artificial, tecnico, conhecimento, letramento, generativa

## 5. Lacunas estruturais (pares de tópicos fracamente conectados)
Em InfraNodus, lacunas estruturais sinalizam *espaços de ideia* pouco
articulados no texto — candidatos a aprofundamento argumentativo.

- Lacuna entre **Tópico 2** [ciencia, sociais, dado] e **Tópico 5** [humano, metodo, existencia] — densidade ponderada de ligação = 0.2865
- Lacuna entre **Tópico 2** [ciencia, sociais, dado] e **Tópico 3** [rede, latour, agencia] — densidade ponderada de ligação = 0.3471
- Lacuna entre **Tópico 4** [pesquisa, etnografia, construcao] e **Tópico 5** [humano, metodo, existencia] — densidade ponderada de ligação = 0.3788
- Lacuna entre **Tópico 3** [rede, latour, agencia] e **Tópico 4** [pesquisa, etnografia, construcao] — densidade ponderada de ligação = 0.4198
- Lacuna entre **Tópico 1** [claude, pesquisador, modelo] e **Tópico 2** [ciencia, sociais, dado] — densidade ponderada de ligação = 0.4234
- Lacuna entre **Tópico 1** [claude, pesquisador, modelo] e **Tópico 3** [rede, latour, agencia] — densidade ponderada de ligação = 0.4685

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
