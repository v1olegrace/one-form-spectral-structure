# Registro de decisões

Decisões de escopo e de submissão, com a etapa do
[`ROADMAP_CIENTIFICO.md`](ROADMAP_CIENTIFICO.md) que as produziu. Cada entrada
diz o que foi decidido, com que evidência, e o que ainda pode revertê-la.

---

## D1 — Qual texto é a primeira submissão (etapa E1.4)

**Data:** 21/09/2026 · **Status:** PROVISÓRIA até o fim de E2

### Decisão

**Paper 1 é o texto físico**, `paper/paper.tex` ("Spectral structure of
approximate one-form symmetry breaking"). Ele absorve do rascunho
*Finite-data certificates* **apenas a Proposição 1** (subtrações locais não
alteram o perfil exterior), porque o passo 3 do esboço E2.1 depende dela.

**Paper 2 é o texto matemático**, a ser montado a partir do restante do
rascunho: ambiguidade de amostras finitas, localização com peso mínimo,
certificados de Bernstein e o teorema de filtros polinomiais.

A repartição completa, claim a claim, está em
[`data/manuscript_comparison.csv`](data/manuscript_comparison.csv): 24 claims,
cada um aparecendo exatamente uma vez, 15 para o paper 1 e 9 para o paper 2.
Nenhum claim foi descartado nesta etapa.

### Por que esta repartição

O corte não é por dificuldade, é por **dependência do observável**. A coluna
`class` da matriz separa os claims em PHYSICS (9) — valem por causa do
observável de quebra de simetria de 1-forma — e MATH (15) — valem para
qualquer transformada de Laplace positiva.

A Proposição 1 é a única do rascunho classificada como PHYSICS: ela fala do
campo exterior de uma fonte pontual, e é exatamente o que autoriza subtrações
UV sem perturbar a região r > 0. Sem ela, E2 não fecha.

O restante do rascunho é mais forte justamente onde o paper 1 é mais fraco,
mas por caminhos que não são físicos:

- A **Proposição 2** exibe duas medidas positivas com bordas diferentes e os
  mesmos N primeiros momentos, em aritmética racional exata. É a versão
  afiada do Teorema H. Os dois **não se fundem**: H delimita o alcance dos
  claims físicos e fica no paper 1; P2 é a testemunha construtiva e vai para
  o paper 2, com referência cruzada.
- A **Proposição 3** é a face conversa de H — H diz que não há cota inferior
  *sem* hipótese de peso mínimo, P3 fornece a cota *com* ela.
- O alvo **W(m; r₀)** continua definido quando M = 0, ou seja, exatamente
  onde a Hipótese H2 do paper 1 falha. É a reformulação mais útil do rascunho
  e não pertence a um artigo cuja premissa é o gap.

### O que pode reverter D1

E2 pode reverter. Se a Proposição P-E2 for provada (critério E2(a)), a
Hipótese 3 vira teorema no regime de sonda linear e o paper 1 fica
substancialmente mais forte — a decisão se confirma. Se sair um contraexemplo
(critério E2(b)), o conteúdo físico defensável encolhe e pode passar a fazer
sentido submeter primeiro o texto matemático, que não depende de H3.

Por isso D1 é provisória, conforme o próprio roadmap: "E1 é **provisória** até
o fim de E2".

### Veredictos de novidade

A matriz **não** repete nem contradiz os veredictos de
`data/claims_matrix.csv`. Novidade e precedência são objeto da etapa E3; aqui
só se decidiu destino.

---

## D2 — E1.1 não pode ser cumprida como especificada

**Data:** 21/09/2026 · **Status:** BLOQUEIO REGISTRADO

A tarefa E1.1 pede recuperar o `.tex` do rascunho *Finite-data certificates* e
versioná-lo em `drafts/finite_data/`. **O `.tex` nunca foi entregue.**

`base_cientifica/certificados_espectrais_2026-09-21/manifesto_fontes.json`
registra, para as duas fontes, `"original_code_package_received": false`. Uma
busca por `*.tex` em toda a árvore devolve apenas o paper canônico, a cópia no
pacote `laplace/` e a cópia arquivada em `reports/memoria_viole_2026-09-14/`.
Nenhum deles é o rascunho.

**Fonte autoritativa, na falta do `.tex`:**

| Item | Valor |
|---|---|
| Arquivo | `base_cientifica/certificados_espectrais_2026-09-21/fontes/paper_draft.pdf` |
| SHA-256 | `69b634b07a5ffa6466d29eff99e54baec002f5dc32b8b9d74faea33b2c088ef4` |
| Páginas | 7 |
| Produtor | pdfTeX-1.40.25 (logo, um `.tex` existiu na máquina do autor) |
| Extração | `extracoes/paper_draft.txt` |

`drafts/finite_data/` **não foi criado**: o PDF já está arquivado com manifesto
e SHA-256, e um diretório contendo apenas um aviso de que a fonte não está lá
seria pior que a sua ausência.

**Consequência para E1.2.** A matriz foi montada lendo o PDF e a extração. O
manifesto classifica a extração como auxiliar (`"formula_fidelity": "extraction
is auxiliary; mathematical expressions checked against renders"`). Os
enunciados na matriz são, portanto, **transcrições conferidas contra o render**,
não cópias de fonte LaTeX. Antes de reaproveitar qualquer fórmula do paper 2
em texto submetido, o `.tex` precisa ser recuperado com o autor.

---

## D3 — Discrepância entre o README e o paper canônico

**Data:** 21/09/2026 · **Status:** ABERTA, a resolver em E3/E5

O claim ledger do `README.md` lista **C5** ("derivative-free sampled hierarchy
with error envelope") como claim do paper 1. Ele não está no texto canônico.

Verificado por busca literal em `paper/paper.tex` (546 linhas) e
`paper/appendix.tex` (150 linhas): nenhuma ocorrência de `sampl`, `Hausdorff`,
`Mellin`, `sandwich` ou `two-radius`. Os Teoremas F e G e a ponte de Mellin
(C6) existem apenas no rascunho pt-BR em `manuscript/`, e estão marcados como
`paper1_ptbr_draft_only` na matriz.

Ou o README anuncia um claim que o texto não sustenta, ou os teoremas precisam
ser importados para o `.tex`. A matriz aponta os três para o paper 2, porque a
Proposição 4 do rascunho faz o mesmo trabalho que C5 com certificados exatos.
**Enquanto isso não se resolve, o README está à frente do manuscrito.**

---

## D4 — A tag `paper-v0.2` não foi criada

**Data:** 21/09/2026 · **Status:** PENDENTE de ambiente com LaTeX

A etapa E0 foi integrada nesta árvore (commit `db159ed`), aplicando os dois
patches do pacote `laplace/`. O pacote foi cortado de um histórico que este
repositório não compartilha — o commit-pai `79be9cd` não existe aqui — então
os patches foram aplicados com `--3way`. Todos os trechos entraram limpos.

**Verificado neste ambiente:**

- `reproducibility/figure_data.py --check` reproduz todos os números citados na
  Seção 7: r× = 22.7583, a₃ = −0.1735, det H₀ = −0.0249, reescalados −0.4715 e
  −0.1839.
- `pytest`: 86 passaram, 1 pulado. A suíte de alta precisão (`mpmath`), que o
  README do pacote declara não ter sido reexecutada no ambiente v0.2, **passa
  aqui**.

**Não verificado:** o build limpo do PDF. `pdflatex` e `bibtex` não existem
nesta máquina, `tests/test_paper_build.py` é pulado por esse motivo, e
`paper/paper.pdf` não foi gerado.

A regra 4 do roadmap exige build limpo para encerrar etapa. A tag
`paper-v0.2` fica **deliberadamente não criada** até que `python make.py pdf`
rode num ambiente com LaTeX.
