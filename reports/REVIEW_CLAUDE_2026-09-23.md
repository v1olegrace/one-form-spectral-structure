# Revisão independente das correções v0.3 e implementação — 23 de setembro de 2026

Revisor e implementador: Claude. Duas fases, deliberadamente separadas neste
documento:

- **Fase 1 (somente leitura).** Revisão das correções v0.3, sem executar nada.
  Os resultados de execução citados como evidência da v0.3 foram produzidos por
  **Codex**, não por mim, e estão marcados como tal.
- **Fase 2 (implementação).** Correção dos achados A1–A4, mais o que apareceu
  durante a implementação. Os números da v0.3a foram medidos por mim, nesta
  máquina, com os comandos listados no fim.

Nenhum enunciado científico, teorema, hipótese ou valor do artigo foi alterado.
As fontes em `paper/` não foram tocadas: os 6 hashes de fonte e o hash do PDF
registrados em `output/data/canonical_pdf_qa.json` continuam idênticos, logo o
PDF canônico v0.3 segue válido e não foi recompilado.

---

## A0 — Dois agentes escreveram nesta árvore de trabalho

Durante a Fase 1 e o início da Fase 2, um segundo processo de agente editou o
mesmo workspace não comitado. Evidência: `DECISIONS.md` (22:03:52) e
`ROADMAP_CIENTIFICO.md` (22:04:34) apareceram como modificados sem que eu os
tocasse, e `reports/VERIFICATION_CLAUDE_2026-09-23.md` (22:07:07) foi criado por
outro agente — ele descreve o meu próprio trabalho em andamento como "de Codex"
e registra a suíte em 136 testes coletados, um estado intermediário meu. No
momento em que escrevo, nenhum processo Python está ativo.

Consequências práticas, e por que isto vem primeiro:

- Uma discrepância que eu quase reportei na Fase 1 (contagem de pytest 120
  versus 121) era artefato de leitura de uma árvore em mutação, não um erro do
  relatório. Reli os quatro locais e todos diziam 121, consistentemente.
- Os arquivos do outro agente foram **preservados**, não revertidos:
  `DECISIONS.md`, `ROADMAP_CIENTIFICO.md` e
  `reports/VERIFICATION_CLAUDE_2026-09-23.md`. A entrada D6 do `DECISIONS.md`
  (recuo da frase "H3 é estritamente mais forte que positividade de reflexão")
  é coerente com o artigo atual e não conflita com nada aqui.
- Este relatório usa nome distinto (`REVIEW_`, não `VERIFICATION_`) para não
  sobrescrever o dele.
- **Os dois relatórios usam numerações de achado incompatíveis.** O A3 dele não
  é o meu A3, e ele registra "A1 pode ter sido resolvido por Codex" quando o A1
  foi resolvido por mim, nesta sessão. Não tente reconciliar as duas listas como
  se fossem um único esquema: leia cada relatório com a sua própria numeração.
- **Recomendação:** não rodar dois agentes com permissão de escrita no mesmo
  workspace não comitado. Contagens e referências `arquivo:linha` produzidas
  nessas condições têm carimbo de tempo, não valor de estado.

---

## Achados confirmados e o que foi feito

### A1 — MÉDIA · O filtro era auxiliar local de um script; três módulos irmãos emitiam limites sem guarda

**Diagnóstico (Fase 1).** As condições necessárias finitas viviam em
`falsification_suite.py`. Não havia equivalente em:

| Módulo | Feixe | Defeito |
|---|---|---|
| `laplace_geometry.hankel_bound` | Laplace (H₁,H₀) | segunda função homônima, sem filtro; é a do caminho canônico de certificação e escreve `laplace_geometry_certification.json` |
| `extended_analysis.pencil` / `sampled_checks` | Hausdorff amostrado | sem filtro, e `bound = -mp.log(L)/h` sem verificar L ∈ (0,1] |
| `analysis.localizing_bound` | Stieltjes (H₀,H₁) | float64 sem guarda de condicionamento |

Quatro textos descreviam o filtro como propriedade "da rotina de limite" ou "do
pipeline": `reports/AUDIT_REMEDIATION_2026-09-23.md`, `CHANGELOG_PAPER.md`,
`README.md` e `paper/paper.tex`. A afirmação era verdadeira de uma das duas
funções chamadas `hankel_bound`.

Exposição real era limitada — a medida em `laplace_geometry` é a densidade Dirac
de um laço, genuinamente positiva; `mp.cholesky` levanta exceção se H₀ não for
numericamente definida positiva; e `check("E(ii) B_K >= M_*")` reprovaria um
valor corrompido. Era defeito de guarda e de documentação, não evidência de
número errado nos artefatos.

**Correção.** Extraí o filtro para `reproducibility/moment_conditions.py`
(`moment_gate`, `validate_request`, `mass_from_log_ratio`,
`conditioning_digits`). Os quatro módulos o importam. A extração é preservadora
de comportamento: os 33 testes de `test_measure_and_hierarchy.py` passaram sem
alteração, com as mesmas cinco cadeias de status que eles verificam.

Um ponto de projeto que não era opcional: **as duas orientações de feixe são
opostas.** No feixe de Laplace o denominador é H₀; no de Stieltjes é H₁. Só o
denominador pode receber a recusa estrita por quase-singularidade — a outra
matriz precisa da condição permissiva (semidefinida), porque uma medida positiva
legítima com átomo em zero torna o localizador singular. Reusar o filtro
ingenuamente em `analysis.py` protegeria a matriz errada, silenciosamente. Por
isso `moment_gate` exige que o chamador declare `strict_shift`, e há teste
discriminante para isso.

`extended_analysis` ganhou também o filtro sobre as amostras e a guarda de
domínio: o limite nominal agora passa por `mass_from_log_ratio`, e a variante
robusta converte a recusa em "sem limite explícito"
(`refused_no_valid_ratio`) em vez de propagar exceção.

**Verificação.** O filtro **passa** em todas as ordens efetivamente reportadas,
sem ajuste de guarda nem redução de faixa de K: Laplace K = 0..5 a r = 1 e 3 com
80 dps, Hausdorff K = 0..5 com 60 dps, Stieltjes K = 0..5 com 120 dps, todos
`CHECKED_COMPATIBLE`. Isso torna a frase de `paper/paper.tex` ("the bound
routine repeats these checks on its actual input") verdadeira sem editar o
artigo — motivo pelo qual não houve recompilação.

### A2 — MÉDIA-BAIXA · O verificador ligava o que estava presente, não que nada faltava

**Diagnóstico.** `verify_one_loop_output.py` ligava apenas
`unique_raw_integrals`. Não havia asserção sobre o contador de avaliações, nem
sobre a cobertura de `comparison.json`, nem sobre `len(certificates)`, nem sobre
os índices de certificado. Remover uma linha de `comparison.json` junto com seu
contador passava por todas as asserções e o verificador imprimia `PASS`.

**Correção.** Bloco de cardinalidade e completude: todo contador de
`summary.json` é recomputado; a tabela de comparação precisa ser exatamente o
produto cartesiano datasets × graus × cortes; `len(certificates) == 2·len(rows)`;
e os índices usados precisam ser uma **bijeção** sobre os certificados
armazenados. Também passei a exigir que cada conjunto tenha checagens
independentes em todos os índices de amostra e que nenhuma delas esteja marcada
como fora do envelope. O resultado da verificação expõe
`comparison_table_complete` e `certificate_index_bijection`.

**Testes discriminantes** (`tests/test_one_loop_verifier.py`, 21 no total):
linha removida com contador ajustado; combinação duplicada preservando a
cardinalidade (que uma checagem só de comprimento não pega); dois índices
apontando para o mesmo certificado; certificado removido; e 11 casos
parametrizados incrementando cada contador de proveniência. Todos falham na
versão anterior.

### A3 — BAIXA · Feixe em precisão dupla publicado, sem requisito medido

**Diagnóstico.** `paper/paper.tex` diz que limites de Hankel de alta ordem não
devem ser reportados em precisão dupla, e o `README` dizia que "o pipeline
detecta colapso de posto". `analysis.localizing_bound` calculava K = 0..5 em
float64 via `scipy.linalg.eigh`, sem guarda, e publicava
`localizing_bounds.csv` e a figura correspondente. Mitigação já existente: não é
o caminho do artigo canônico, como `output/README.md` explicita.

**Correção proporcional.** O cálculo passou a 120 dps com momentos em mpmath
(`dirac_moment_mp`, mesma forma fechada), com o filtro na orientação correta e
com a rota float64 preservada **apenas para medir o próprio erro**
(`localizing_bound_float64`). Cada linha do CSV registra `gate_status`,
`denominator_digits_required`, `working_dps` e
`float64_relative_difference`. As checagens perderam a folga de 1e-10, que não
era mais necessária.

**Resultado medido, e ele corrige a minha própria suspeita:** o feixe de
Stieltjes precisa de 1 a 13 dígitos em K = 0..5, e a diferença da rota float64 é
no máximo 5,9e-12. Ou seja, **a precisão dupla era adequada ali** — float64 tem
~16 dígitos e o requisito é 13. Não havia número errado publicado. O que havia
era um requisito não medido e nenhum caminho de recusa; agora há os dois. Isso
não enfraquece a afirmação do artigo sobre o feixe de Laplace, onde o modelo de
faixa dinâmica larga precisa de ~86 dígitos: são feixes diferentes.

### A4 — BAIXA · Os contadores de proveniência tinham nome mais largo do que o que contavam

**Diagnóstico.** `raw_integral_evaluations` contava só as chamadas a
`certify_sample`. Ficavam fora as 12 integrais de benchmark de `certify_weight`
e as 40 checagens independentes em mpmath. "40 avaliações de integrais" podia
ser lido como o total de quadraturas.

**Correção.** Renomeados para `source_enclosure_evaluations` (40) e
`distinct_source_enclosures` (28); acrescentados
`weight_benchmark_evaluations` (12), `weight_benchmark_integrals` (12),
`distinct_weight_benchmarks` (12) e `independent_quadrature_checks` (40); e um
campo `counter_scope` dizendo em texto que nenhum contador é o total de
quadraturas. `CONFIG` **não** foi tocado, de propósito:
`configuration_sha256 = b4b178b9…` continua o mesmo, então nada que dependa dele
precisou ser reescrito.

### Extra (encontrado na implementação) · `data/claims_matrix.csv`, linha C5

A reivindicação C5 dizia "deterministic error propagation giving **certified**
upper bounds" mas citava como evidência apenas `extended_analysis.py`, cujos
resultados são `CHECKED` (mpmath, sem enclosure). Os limites de fato
`CERTIFIED` vêm de `run_one_loop_certificates.sampled_gap_bound`, que usa
aritmética racional exata sobre envelopes Arb. Corrigi na fonte geradora
(`scripts/build_audit_tables.py`, a tabela é regenerada) para nomear os dois
caminhos com seus status distintos e registrar que o Teorema G só está provado
no rascunho Quarto não canônico.

---

## O que revi e está correto (Fase 1, sem execução)

Registro aqui o que verifiquei por leitura ou derivação à mão, para que não seja
re-auditado sem motivo.

- **Alinhamento de índices do filtro.** Para `a` de comprimento 2K+2, G2 usa
  K′ = (len−1)//2 = K e G3 usa K″ = (len−2)//2 = K — exatamente as entradas de
  H₀ e H₁ do limite reportado. Para n_max ímpar, G2 e G3 juntas consomem todos
  os momentos.
- **Taxonomia das recusas.** G1/G2/G3 violados → `CHECKED_INCOMPATIBLE`;
  quase-singular ou precisão insuficiente → `UNRESOLVED_RANK_OR_PRECISION` com
  "not a refutation of H3". A guarda é unilateral: só converte aceitação em
  recusa, nunca autovalor negativo em aceitação.
- **Guarda `-O` é real, não no-op.** `if not __debug__: raise RuntimeError`, com
  teste que lança subprocesso `python -O` e exige saída não zero. O defeito
  comum (`assert __debug__`) está ausente.
- **Deduplicação preserva a ligação.** `sample_input_key` cobre kind, radius,
  mass, coupling², charge, t_max, bits e tolerance_goal, e é formada **depois**
  de cada campo ser verificado contra a configuração e de radius = r0 + j·spacing
  — logo um registro corrompido não deduplica de forma autoconsistente. A
  comparação de reintegração roda em **toda** ocorrência, não só na primeira.
- **Aritmética dos contadores.** 2 modelos × 2 raios × 3 ruídos = 12 conjuntos;
  12 × 4 graus × 3 cortes = 144 linhas; 2 certificados por linha = 288; raios
  {1,…,3.25} ∪ {2,…,4.25} com h = 1/4 coincidem em 6 pontos → 14 distintos por
  modelo → 28 de 40.
- **Direção do limite é a relevante para WGC.** Γ, B_K e `sampled_gap_bound`
  produzem limites **superiores** para M\*. λ_min de (H₁,H₀) é mínimo de ⟨x⟩
  sobre reponderações de grau K, logo ≥ inf supp; com y = e^{−hx},
  num/den ≤ e^{−hM\*}, então −log(ℓ_inf)/h ≥ M\*.
- **Cadeia WGC** (`paper/paper.tex`, seção da obstrução): algebricamente válida
  com as hipóteses enunciadas, e η > τ+ε torna a raiz real. O texto declara que
  não é derivação da conjectura e avisa sobre calibrar η ou κ após ver o
  espectro.
- **Teto de uma espécie** (`paper/appendix.tex`): correto. f(u)² = 1 − 3u²/4 −
  u³/4 expandindo (1+u/2)²(1−u), logo 0 ≤ f ≤ 1 em [0,1]; e
  r²∫₀^∞ x e^{−rx}dx = 1. O prefator g_R²q²/6π² coincide com `dnu_density`.
- **Teorema C e Teorema E**: provas corretas, incluindo a janela ε/4, o uso de
  Carleman apenas para determinação, e dω = (1+x)e^{−rx}dν dominando os dois
  integrandos do quociente de Rayleigh. A ressalva H₀ ≻ 0 ⟺ ao menos K+1 pontos
  de suporte está no enunciado.
- **Lei de borda**: verifiquei os coeficientes por conta própria. Expandindo
  dν/dx da densidade de Dirac em t = x−2m: 1 − 5t/(24m) + 77t²/(384m²), logo
  β = −5/(24m), γ = 77/(384m²), βp = −5/(16m) e
  2γp(p+1) − β²p² = 1155/768m² − 225/2304m² = 45/(32m²), exatamente o publicado.
  `extended_analysis.symbolic_checks` prova o mesmo em SymPy.
- **Números adversariais**, reproduzidos à mão: a₃ = e^{−1} − 4e^{−2} =
  −0,17346 e det H₀ = −0,024894, reescalados a −0,4715 e −0,1839; para o
  contraexemplo do localizador, 0,855λ² − 1,341λ − 0,09 = 0 dá
  λ_min = −0,0644645, o valor que a rotina antiga devolveria; e
  r = log(Γ(3/2)/10^{−12}) − 1,5·log(1+r) → 22,758.
- **`interval_bounds.envelope_bound` não era um quarto sítio sem guarda**: o
  Cholesky ali só **escolhe** o vetor de teste, sua falha devolve
  `(None, None)`, a desigualdade emitida é uniforme em v, e os resultados são
  rotulados `CHECKED`.

---

## Limitações remanescentes e o que não foi corrigido

1. **Redução automática de posto continua não implementada.** A recusa
   `UNRESOLVED_RANK_OR_PRECISION` é o comportamento correto, não a solução.
   Implementá-la é acréscimo de funcionalidade, fora do escopo desta revisão.
2. **O verificador valida a configuração declarada, não uma pré-registrada.**
   `verify()` não compara `configuration.json` com a constante `CONFIG`; uma
   execução com `CONFIG` alterado se autoverifica. Está divulgado (o `README`
   nega pré-registro com data externa confiável) e não é defeito de código, mas
   permanece verdadeiro.
3. **`sampled_gap_bound` escolhe o vetor de teste em float64** sobre pontos
   médios. A validade não é afetada — o certificado é racional exato e qualquer
   v é admissível — mas a **qualidade** do limite depende de um passo sem
   guarda; as 24 linhas `NO_BOUND` de 144 podem refletir isso em parte.
4. **Não verificado por mim**: a inspeção visual das 12 páginas do PDF (feita
   por Codex; não a repeti porque o PDF é bit a bit o mesmo) e a execução de CI
   remoto, que continua sem acontecer. Revisão humana por especialista continua
   não realizada.
5. **Coleta de testes na raiz.** `python -m pytest` na raiz falha por colisão de
   nomes com a cópia não rastreada em `laplace/`. Use `python -m pytest tests -q`.
   Não mexi em `laplace/`, que é diretório preexistente a preservar.
6. **Assinatura de `extended_analysis.pencil` mudou** (4 para 5 valores de
   retorno, o quinto sendo o diagnóstico do filtro). Os dois chamadores no
   repositório foram atualizados e a suíte está verde; conferi por busca que não
   há chamador fora de `reproducibility/` e `tests/`, inclusive em `manuscript/`
   e na cópia não rastreada em `laplace/`. Registro aqui porque essa cópia não é
   exercitada por teste algum.

Os dois auxiliares citados como evidência, `tmp/check_qa_hashes.py` e
`tmp/prove_guards_discriminate.py`, são rascunho reproduzível em diretório não
versionado, não entregáveis. Nenhum dos dois escreve no repositório.

Fora dos achados acima, não encontrei outra falha demonstrável nas correções
v0.3. **Isto não é certificação da teoria.** H3 geral permanece não provada, as
recusas do filtro seguem sendo condições necessárias finitas, e os limites
continuam condicionais a uma medida positiva.

---

## Próxima obrigação científica concreta

Dentro da obrigação já aberta "derivar H3 além da ordem líder" há uma rota
autocontida, e ela **muda o que se deve provar**. Registro como **proposta,
derivada por mim e não verificada no repositório** — não é teorema e não altera
o escopo científico do artigo.

Expandindo a própria `eq:expansion` do apêndice uma ordem além, o coeficiente
redutível em O(g_R⁶) de 𝒢 − g_R²/Q² é

    g_R⁶ · Q² · [∫ ρ_J(s) ds / (s(s+Q²))]².

Essa função vale 0 em Q² = 0, tem derivada +A² > 0 ali (A = ∫ρ_J/s² ds, finito
porque ρ_J ~ (s−4m²)^{1/2}) e decai como 1/Q² — logo tem máximo interior. Mas
toda função ∫dσ/(Q²+s) com σ ≥ 0 e suporte em [s\*,∞), s\* > 0, é estritamente
decrescente e positiva em Q² = 0. **Portanto o coeficiente O(g_R⁶) redutível não
é, ele mesmo, da forma de H3 com medida positiva.**

O caso exatamente solúvel ρ_J = Z δ(s−s₀) mostra por quê. Com c = g_R²Z/s₀ ∈
(0,1), o núcleo ressomado dá exatamente

    𝒢 = g_R²/Q² + [g_R² c/(1−c)] / (Q² + s₀/(1−c)),

isto é dσ = [g_R²c/(1−c)]·δ_{s₀/(1−c)} ≥ 0: H3 vale a **todas** as ordens da
cadeia de bolhas, mas o polo **se move** com o acoplamento. Expandir em g_R a s
fixo produz coeficientes distribucionais de sinal alternado. (Conferi que o
termo O(c²) dessa forma fechada reproduz exatamente
g_R⁶Z²Q²/(s₀²(s₀+Q²)²).)

Consequência para a agenda: a obrigação **não** é "mostrar dσ₂ ≥ 0" — isso é
impossível por construção. É **mostrar que a resposta estática ressomada
𝒢 = g_R²/(Q²[1−g_R²Π̄(Q²)]) permanece na classe de Stieltjes, com o
deslocamento de limiar e a condição g_R²Π̄(Q²) < 1 explicitamente controlados**
no domínio de Q² usado. É pergunta de classe de Nevanlinna, sem novo insumo de
teoria de campos, e casa com a alternativa que o próprio relatório de remediação
oferece ("restringir o domínio de aplicação com uma hipótese controlada"), já
que o Check 3 do apêndice observa que g²_eff cresce no ultravioleta. Escopo:
vale para a parte **redutível**; a contribuição irredutível de dois laços é
objeto separado e pode cancelar parcialmente. Efeito colateral a registrar:
`M_STAR = 2m` e o s\* da hipótese de gap são objetos de ordem líder, e o exemplo
acima mostra o limiar subindo com o acoplamento.

---

## Prova de que as guardas discriminam

Testes que passam nas duas versões não valem nada. Rodei uma sonda somente
leitura (`tmp/prove_guards_discriminate.py`, não versionada, não modifica o
repositório) reconstruindo localmente a aritmética sem filtro e o conjunto de
asserções da v0.3. Saída literal:

```
1. laplace_geometry.hankel_bound WITHOUT the gate (the v0.3 code path)
   ungated result : B_1 = -0.064464504   <-- a negative 'mass'
   det H0 = 0.855 > 0, det H1 = -0.09 < 0
   gated result   : refused -> No bound: G3 violated: H_1 has a negative eigenvalue at K=1

2. verify_one_loop_output WITHOUT the completeness block
   tampered: dropped 1 of 144 comparison rows and fixed the counter
   v0.3 assertion set (only the distinct-source count): PASSES -> tampering undetected
   v0.3a verifier : refused -> Comparison table is incomplete
   tampered: duplicated one combination, 144 rows preserved
   a length-only check (len(certificates) == 2*len(rows)) still holds: True
   v0.3a verifier : refused -> Comparison table is incomplete
```

O primeiro bloco reproduz exatamente o valor −0,0644645 que o artigo cita como
o que a rotina antiga devolveria — e mostra que a segunda função homônima o
devolvia de fato. O segundo mostra que a remoção de uma linha com o contador
ajustado **passava** pelo conjunto de asserções da v0.3, e que a duplicação de
combinação sobrevive a uma checagem só de comprimento.

## Comandos executados por mim (v0.3a) e resultados

Ambiente: Windows 11, Python 3.13.7, mpmath 1.3.0, NumPy 2.3.5, SciPy 1.15.3,
SymPy 1.13.1, python-flint 0.9.0, Tectonic 0.17.0 portátil em
`tmp/tools/tectonic-0.17.0/` no PATH.

| Comando | Resultado |
|---|---|
| `python -m pytest tests -q` (Tectonic no PATH) | **169 aprovados, nenhum omitido** |
| `python -m pytest tests/test_bound_guards.py -q` | 32 aprovados |
| `python -m pytest tests/test_one_loop_verifier.py -q` | 21 aprovados |
| `python -m pytest tests/test_measure_and_hierarchy.py -q` | 33 aprovados (inalterados após a extração) |
| `python make.py numerics` (duas vezes) | exit 0; os quatro SVG byte a byte idênticos entre as duas execuções |
| `python make.py audit` | exit 0 |
| `python reproducibility/laplace_geometry.py` | todas aprovadas; filtro `CHECKED_COMPATIBLE` em K = 0..5 a r = 1 e 3 |
| `python reproducibility/extended_analysis.py` | 70 verificações, todas aprovadas |
| `python reproducibility/analysis.py` | exit 0; dígitos exigidos 1..13; pior desvio float64 5,9e-12 |
| `python make.py certified` | exit 0; 40/28/12/12/12/40, 144 linhas, 288 certificados, 113 com limite inferior positivo, 24 `NO_BOUND`; `configuration_sha256` = `b4b178b9…` inalterado |
| `python reproducibility/verify_one_loop_output.py --reintegrate --no-write` | `PASS`; 28/28 amostras, 12/12 benchmarks, cardinalidades, produto cartesiano e bijeção de índices |
| hashes de `paper/` e do PDF vs `canonical_pdf_qa.json` | 6/6 fontes e o PDF idênticos; sem recompilação |

Não houve commit, push, reset, checkout destrutivo, limpeza recursiva nem
publicação. `base_cientifica/`, `laplace/` e `reports/memoria_viole_2026-09-14/`
foram preservados, assim como os arquivos do outro agente citados em A0.
