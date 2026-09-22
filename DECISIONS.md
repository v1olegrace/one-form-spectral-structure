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
[`data/manuscript_comparison.csv`](data/manuscript_comparison.csv): 29 claims,
cada um aparecendo exatamente uma vez, 20 para o paper 1 e 9 para o paper 2.
Nenhum claim foi descartado nesta etapa.

### Como os claims foram enumerados

Não basta varrer ambientes `\begin{theorem}`. O paper canônico enuncia
resultados em **três** formas, e as três foram varridas:

1. ambientes numerados — `thm:A`, `thm:C`, `thm:E`, `thm:H`, as cinco
   hipóteses e a `definition` do perfil;
2. `\paragraph{...}` dentro das seções 2 e 6 — é onde vivem a monotonicidade
   completa, a não-equivalência com H3, o modo de falha *gapless* e os regimes
   excluídos;
3. o apêndice, cujos parágrafos provam C e E e enunciam a lei de borda.

Cinco claims (`P1-S0`, `P1-DEF`, `P1-S1`, `P1-S2`, `P1-S3`) aparecem na matriz
e **não constam nem de `claims_matrix.csv` nem de `theorem_status.csv`**. O
mais importante deles é `P1-S2`, "the first threshold need not be charged": o
modo de falha em QED completa, anunciado no TL;DR do README como um dos três
limites explícitos do paper, mas que não tinha linha própria em nenhum registro
anterior.

### Por que esta repartição

O corte não é por dificuldade, é por **dependência do observável**. A coluna
`class` da matriz separa os claims em PHYSICS (13) — valem por causa do
observável de quebra de simetria de 1-forma — e MATH (16) — valem para
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

Verificado em duas passadas sobre `paper/paper.tex` (546 linhas) e
`paper/appendix.tex` (150 linhas). Por vocabulário: nenhuma ocorrência de
`sampl`, `Hausdorff`, `Mellin`, `sandwich` ou `two-radius`. E, porque um texto
pode enunciar o claim sem usar essas palavras, também por conteúdo: nenhuma
ocorrência de `b_j`, `envelope`, `equally spaced`, `derivative-free` ou
`r+jh`. A ausência é do claim, não só do termo. Os Teoremas F e G e a ponte de Mellin
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

---

## D5 — Obrigações de prova da P-E2 (auditoria externa de 22/09/2026)

**Data:** 22/09/2026 · **Status:** ABERTA, condiciona E2.3a/b

Uma auditoria independente do repositório levantou três pontos contra o
enunciado da P-E2 no roadmap. Os três foram conferidos aqui. Não são
contraexemplos à H3: são passos que o enunciado atual assume sem provar.

**O1 — Polo de Coulomb.** A P-E2 afirma que (W), (B) e (L) dão
𝒢 = Z/Q² + ∫dσ/(Q²+s) + P. Não dão: um campo de Proca livre satisfaz as três
condições e não tem polo em Q² = 0 (q∞ = 0, e δ nem está definido). O
**paper** já está correto nesse ponto, porque a H2 postula explicitamente
"a Coulomb pole of residue g_R² > 0". A lacuna está no **roadmap**. A P-E2
precisa de uma hipótese explícita (C) de fase de Coulomb, com resíduo positivo
e q∞ ≠ 0. A alternativa é enunciar o teorema espectral geral e, à parte, o
corolário para o perfil.

**O2 — Do correlator ao observável.** A positividade de ⟨FF⟩ precisa ser
transportada até o coeficiente quadrático do laço de Wilson. Isso envolve a
projeção tensorial, o sinal da medida, os termos de contato, a renormalização
do perímetro e o limite T → ∞. Um fato já verificado simbolicamente ajuda: no
limite estático, ⟨E_iE_j⟩ ∝ Q_iQ_j D_E(Q²) é **longitudinal**, e o escalar
visto pelo potencial é Q² D_E(Q²). A estrutura transversal está em ⟨B_iB_j⟩.
O brief do Codex dizia o contrário e foi corrigido.

**O3 — Subtrações versus H3.** A H3 do paper é **não subtraída**, com
∫dσ/(μ₀²+s) < ∞. A P-E2 admite subtrações e um polinômio P(Q²). A tensão é
menor do que o roadmap sugere. O passo 3 de E2.1 diz que "∫ρ/(s+μ²)
diverge", mas isso vale para a densidade de corrente ρ_J, não para σ. A uma
volta, dσ = g⁴ρ_J ds/s, e com ρ_J → constante a integral
∫dσ/(μ₀²+s) ~ ∫ds/s² **converge**: nessa ordem a H3 não subtraída vale.
Subtrações só se tornam necessárias se σ crescer mais que isso. É o caso do
exemplo matemático da Proposição 1 do rascunho (dσ = ½ds), que diverge
logaritmicamente. **A verificar na nota E2:** se a forma ressomada preserva
essa convergência, e o que a Proposição 1 acrescenta fisicamente além dela.

**Consequência para E2.3b.** A classificação tensorial deve partir do
correlator mais geral compatível com Poincaré, paridade e antissimetria, e só
então impor Bianchi, tratando p² = 0 e os termos de contato separadamente.
Verificar Bianchi num tensor construído a partir de F = dA é tautológico e não
conta como prova.

**Verificação complementar feita nesta data.**
`verify_one_loop_output.py --reintegrate` passou. Reintegrou com Arb as quatro
chaves (tipo, r₀), e com elas **todas as 28 integrais de amostra distintas** —
os três datasets de cada chave diferem só no ruído, que é aplicado depois da
integração —, além dos benchmarks diretos de peso. O `source_pairs_reintegrated: 0`
da execução anterior refletia só a ausência da flag.
