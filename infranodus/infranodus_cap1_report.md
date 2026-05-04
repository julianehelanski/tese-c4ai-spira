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
| 21 | `dado` | 241 |
| 22 | `agencia` | 241 |
| 23 | `conhecimento` | 227 |
| 24 | `letramento` | 226 |
| 25 | `cientista` | 226 |
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
- **Tópico 1** (36 termos): claude, pesquisador, modelo, composicao, objeto, escrita
- **Tópico 2** (33 termos): pesquisa, inteligencia, artificial, etnografia, construcao, tecnico
- **Tópico 3** (32 termos): rede, agencia, ator, diagrama, distribuida, associacao
- **Tópico 4** (31 termos): humano, metodo, latour, existencia, maquina, parcial
- **Tópico 5** (29 termos): ciencia, campo, sociais, dado, conhecimento, cientista
- **Tópico 6** (15 termos): instituicao, cientifico, computacional, sistemas, compreender, infraestrutura
- **Tópico 7** (4 termos): tecnica, alienacao, partir, simondon

## 5. Lacunas estruturais (pares de tópicos fracamente conectados)
Em InfraNodus, lacunas estruturais sinalizam *espaços de ideia* pouco
articulados no texto — candidatos a aprofundamento argumentativo.

- Lacuna entre **Tópico 4** [humano, metodo, latour] e **Tópico 5** [ciencia, campo, sociais] — densidade ponderada de ligação = 0.2714
- Lacuna entre **Tópico 2** [pesquisa, inteligencia, artificial] e **Tópico 3** [rede, agencia, ator] — densidade ponderada de ligação = 0.3608
- Lacuna entre **Tópico 3** [rede, agencia, ator] e **Tópico 5** [ciencia, campo, sociais] — densidade ponderada de ligação = 0.3642
- Lacuna entre **Tópico 2** [pesquisa, inteligencia, artificial] e **Tópico 4** [humano, metodo, latour] — densidade ponderada de ligação = 0.3734
- Lacuna entre **Tópico 1** [claude, pesquisador, modelo] e **Tópico 3** [rede, agencia, ator] — densidade ponderada de ligação = 0.4392
- Lacuna entre **Tópico 3** [rede, agencia, ator] e **Tópico 4** [humano, metodo, latour] — densidade ponderada de ligação = 0.4869

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
