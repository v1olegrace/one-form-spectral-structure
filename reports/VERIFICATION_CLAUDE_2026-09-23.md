# Verificação independente por Claude — 23 de setembro de 2026

> ## ⚠ Este documento é um INSTANTÂNEO, não o estado corrente
>
> **Janela de medição:** aproximadamente 21:50–22:05 (horário local) de
> 23/09/2026. Todos os números abaixo eram verdadeiros quando medidos.
>
> **Durante e depois dessa janela, um processo Codex (PID 22900, ativo desde
> 16:38) estava escrevendo neste mesmo workspace.** A árvore de trabalho foi
> mutada por outro agente no meio desta auditoria. Portanto as contagens e as
> referências `arquivo:linha` deste relatório têm **carimbo de tempo, não
> commit**, e não devem ser lidas como descrição do estado atual.
>
> **Já superado no momento em que este aviso foi escrito:** a suíte passou de
> 121 para 136 testes coletados, e `verify_one_loop_output.py` passou a usar
> um esquema novo de `summary.json` (`distinct_source_enclosures`,
> `source_enclosure_evaluations`, `weight_benchmark_integrals`) no lugar de
> `raw_integral_evaluations` / `unique_raw_integrals`. Em consequência,
> **o achado A3 já não se aplica** na forma em que está escrito: a linha 82
> que ele cita não existe mais. **A1 pode ter sido resolvido** por Codex.
> **A2 e A4 são estruturais e provavelmente continuam válidos.**
>
> Para revalidar qualquer item, reexecute contra a árvore atual.

Este registro é **separado** da evidência de execução produzida por Codex em
`reports/AUDIT_REMEDIATION_2026-09-23.md`. Ele não substitui aquele relatório:
reexecuta as verificações de forma independente e relata o que foi observado
nesta sessão, no mesmo workspace e no mesmo ambiente.

Escopo: revisão inicialmente somente leitura das correções de Codex, seguida de
reexecução dos comandos de validação e de atualização da documentação de estado.
Nenhum commit, push, reset, checkout destrutivo ou publicação foi feito. Os
diretórios preexistentes não rastreados `base_cientifica/`, `laplace/` e
`reports/memoria_viole_2026-09-14/` foram preservados. Nada foi enviado a
terceiros.

Nada aqui certifica a teoria. Reexecução bem-sucedida de testes é evidência
sobre o código e sobre a consistência dos dados, não sobre a verdade de H3.

## 1. Reexecução das evidências declaradas

Todas as reexecuções usaram o ambiente descrito no relatório de Codex:
Windows 11, Python 3.13.7, Tectonic 0.17.0 portátil em `tmp/tools/`.

| Verificação declarada por Codex | Comando reexecutado | Resultado observado |
|---|---|---|
| 121 testes aprovados, zero omitidos | `python make.py test` | **121 passed** em 19.70 s, exit 0 — confere |
| Pipeline numérico exit 0 | `python make.py numerics` | exit 0; `all quoted values reproduced` — confere |
| Tabelas de auditoria regeneram limpas | `python make.py audit` | exit 0; 11 linhas em `theorem_status.csv` — confere |
| 12 conjuntos, 144 comparações, 288 certificados | `verify_one_loop_output.py --reintegrate --no-write` | `PASS`, 12 / 144 / 288 — confere |
| 28 amostras distintas reintegradas | idem | `distinct_source_samples_checked: 28`, `source_samples_reintegrated: 28` — confere |
| 12 benchmarks diretos de peso reintegrados | idem | `distinct_weight_benchmarks_checked: 12`, `weight_benchmarks_reintegrated: 12` — confere |
| 40 avaliações / 28 entradas distintas | `output/certified_one_loop/summary.json` | `raw_integral_evaluations: 40`, `unique_raw_integrals: 28` — ambos os campos existem |
| SVG estáveis byte a byte | `git diff --stat` antes e depois de `make.py numerics` | diffstat **idêntico** (29 arquivos, 3732/3360) — confere |
| PDF v0.3 corresponde às fontes atuais | `sha256sum` das 7 entradas de `canonical_pdf_qa.json` | **todos os 7 hashes conferem** |

### Aritmética de proveniência conferida à mão

A contagem 40 / 28 é consistente com a configuração: 2 modelos × 2 raios de
referência = 4 pares (tipo, r₀), × `sample_count` 10 = **40 avaliações**. Com
espaçamento 1/4, os raios de r₀=1 cobrem 1…3.25 e os de r₀=2 cobrem 2…4.25,
com 6 pontos em comum; logo 10+10−6 = 14 por modelo, × 2 modelos = **28
entradas distintas**. Os 12 conjuntos são os 4 pares × 3 níveis de ruído, e o
ruído é aplicado depois da integração — por isso os mesmos 28 insumos servem
aos 12 conjuntos.

### Verificação do PDF canônico

`output/data/canonical_pdf_qa.json` fixa o SHA-256 de `paper/paper.tex`,
`appendix.tex`, `references.bib`, `physofall.bst` e dos dois `.dat`, além do
PDF e do log. Todos os sete valores conferem com o estado atual da árvore de
trabalho, e `paper/figures/` contém exatamente os dois `.dat` inventariados.
Portanto as afirmações do README sobre o PDF (12 páginas, sem avisos, sem
fontes Type 3) descrevem as fontes atualmente presentes, e não uma versão
anterior. A inspeção visual continua sendo de Codex, não revisão humana.

## 2. Achados confirmados

Ordenados por severidade. Nenhum deles invalida os resultados acima.

### A0 — ALTA (processo, não ciência) — Dois agentes escreveram a mesma árvore não commitada, simultaneamente

A passagem de tarefa declara que Codex terminou. **Não terminou.** O processo
`codex` (PID 22900, início 16:38) continuou editando o workspace durante toda
esta auditoria. As datas de modificação, lidas contra o relógio de 22:05:49,
mostram os dois agentes escrevendo com segundos de diferença:

| Horário | Arquivo | Autor |
|---|---|---|
| 22:03:28 | `reproducibility/run_one_loop_certificates.py` | Codex |
| 22:03:33 | `README.md` | Claude |
| 22:03:52 | `DECISIONS.md` | Claude |
| 22:04:08 | `reproducibility/verify_one_loop_output.py` | Codex |
| 22:04:34 | `ROADMAP_CIENTIFICO.md` | Claude |
| 22:04:50 | `HANDOFF_CLAUDE.md` | Claude |
| 22:05:14 | `tests/test_one_loop_verifier.py` | Codex |

**Consequência imediata.** A reexecução da suíte após as edições de
documentação acusou `1 failed, 135 passed` em
`test_dropped_comparison_row_is_refused`. **Isso não é um defeito.** É uma
leitura rasgada de um refatoramento em voo: `verify_one_loop_output.py`
(22:04:08) já exige o esquema novo de `summary.json`, enquanto
`output/certified_one_loop/summary.json` continua em 22:55 de 22/09, com o
esquema antigo. Nenhum dos dois lados está errado; faltou regenerar o
artefato, coisa que o próprio Codex provavelmente faria em seguida.
Registrar essa falha como achado seria um falso positivo.

*Correção mínima:* **é decisão do usuário, não de um agente.** Coordenar ou
encerrar uma das duas sessões antes de qualquer commit. Escritas concorrentes
não atômicas em arquivos compartilhados podem perder atualizações, e nenhum
dos dois agentes consegue detectar sozinho o que o outro sobrescreveu. Esta
sessão parou de editar o repositório ao constatar o fato.

*Nota de escopo:* as quatro edições de documentação desta sessão (`README.md`,
`DECISIONS.md`, `ROADMAP_CIENTIFICO.md`, `HANDOFF_CLAUDE.md`) foram conferidas
às 22:06:42 e continuavam íntegras, com seus marcadores presentes e sem
sobrescrita por Codex. Os arquivos que Codex tocou são disjuntos dos que esta
sessão editou — desta vez, por sorte, não por coordenação.

### A1 — MÉDIA — O workflow de CI referencia um arquivo não rastreado

`.github/workflows/tests.yml:64` adiciona `tests/test_one_loop_verifier.py` ao
job `certified`, mas esse arquivo está **não rastreado** (`??`). O mesmo vale
para `reproducibility/canonical_pdf_qa.py`, citado como comando de reexecução
no relatório de auditoria. Se o workflow for commitado sem que esses dois
arquivos entrem no índice, o job `certified` falha na coleta do pytest —
e falharia por motivo administrativo, não científico.

*Reprodução:* `git ls-files tests/test_one_loop_verifier.py
reproducibility/canonical_pdf_qa.py` retorna vazio.

*Correção mínima:* incluir os dois arquivos no mesmo commit que o workflow.
Decisão do autor; esta sessão não commita.

### A2 — MÉDIA — `python -m pytest` na raiz falha na coleta

Executar `pytest` sem escopo na raiz do repositório aborta com **3 erros de
coleta**: `test_bibliography`, `test_latex_structure` e `test_paper_build`
colidem com cópias homônimas em
`laplace/physics_of_all_v0.2_update/tests/`, que tem `__pycache__` obsoleto.
`make.py test` passa apenas porque restringe a `tests`. Não há `pytest.ini`,
`pyproject.toml` nem `setup.cfg` com `testpaths`.

*Reprodução:* `python -m pytest -q` na raiz → `Interrupted: 3 errors during
collection`.

*Correção mínima:* um `pytest.ini` com `testpaths = tests` e
`norecursedirs = laplace base_cientifica tmp manuscript`. É mudança de
configuração, não de documentação — **não foi aplicada nesta sessão**; está
registrada no README como condição conhecida do ambiente.

### A3 — BAIXA — O verificador não amarra a contagem de 40 avaliações

`verify_one_loop_output.py:82` verifica
`summary['unique_raw_integrals'] == len(source_records)` (as 28), mas nunca
verifica `raw_integral_evaluations`. O número 40 é citado no CHANGELOG, em
`output/README.md` e no relatório de auditoria como proveniência, sem estar
ligado aos dados por nenhuma asserção.

*Correção mínima* (atenção ao invariante correto — não é a soma sobre os 12
conjuntos, que daria 120):

```python
pairs = {(d['kind'], d['r0']) for d in datasets}
assert summary['raw_integral_evaluations'] == len(pairs) * config['sample_count']
```

### A4 — BAIXA — Referência cruzada obsoleta no cabeçalho do CI

O comentário no topo de `.github/workflows/tests.yml` aponta para
`FINAL_REPORT.md` como fonte do status `UNVERIFIED_IN_ENVIRONMENT`. A fonte de
status corrente é o README mais o relatório de auditoria de 23/09;
`FINAL_REPORT.md` é registro histórico. O fato declarado continua correto — o
workflow nunca foi executado —, apenas o ponteiro envelheceu.

## 3. Pontos checados sem achado

Estes são os itens que a passagem de tarefa pediu para examinar. Não encontrei
falha adicional neles. Isso **não** é um atestado de correção da teoria.

- **Contorno do filtro.** `hankel_bound` chama `_moment_gate` nos próprios
  momentos que usa, e o `K` calculado no filtro para cada deslocamento coincide
  com o das matrizes que a rotina de fato constrói. Não localizei caminho de
  chamada que emita um limite sem passar pelas condições finitas. O teste
  `J2 direct bound call cannot bypass gate` cobre exatamente isso.
- **Distinção entre incompatibilidade, posto/precisão e hipótese física.**
  `CHECKED_INCOMPATIBLE`, `UNRESOLVED_RANK_OR_PRECISION` e
  `CHECKED_COMPATIBLE` estão separados, e o caso do átomo único positivo é
  classificado como não resolvido, não como refutação. O guard de precisão
  recusa; não converte autovalor negativo em positivo aceito.
- **Reintegração e deduplicação.** A chave é `sample_input_key`, e toda
  ocorrência repetida é comparada (`Conflicting repeated source enclosure`),
  inclusive entre conjuntos que diferem só no ruído. A dedução das 28 chaves
  confere com a aritmética da seção 1. Os benchmarks diretos de peso passaram
  a ter o mesmo tratamento.
- **Teto de uma espécie (apêndice).** Com u = 4m²/x² e f(u) = (1+u/2)√(1−u),
  vale f(u)² = 1 − 3u²/4 − u³/4, logo 0 ≤ f ≤ 1 em [0,1]. A conta confere.
- **Cadeia da implicação gravitacional.** De R = maxᵢ g_R|qᵢ|M_pl/mᵢ e mᵢ ≤ Λ
  segue g_R²qᵢ² ≤ R²Λ²/M_pl²; somando N termos e aplicando NΛ² ≤ κM_pl²
  obtém-se κR². A cadeia é válida e as hipóteses (espécies leves, aditividade,
  cauda τ, erro ε, margem η > τ+ε) estão enunciadas antes do uso. Continua
  sendo implicação condicional, não prova da WGC.
- **Atribuição de evidência.** Não encontrei, nos documentos correntes, texto
  que chame H3 de provada, que chame o filtro finito de certificado, ou que
  declare revisão humana ou CI como executados.

## 4. Suspeitas não confirmadas

- O guard de precisão em `_moment_gate` usa `100 * (K+1) * eps * scale`. É um
  heurístico de recusa, e o próprio código o declara como tal. Não construí um
  caso em que ele aceite uma medida assinada que deveria recusar, nem um em
  que recuse uma positiva bem condicionada. O comportamento em modelos com
  faixa dinâmica larga não foi mapeado sistematicamente nesta sessão.
- A estabilidade byte a byte dos SVG foi confirmada para **uma** regeneração
  no mesmo ambiente. Não é garantia entre versões de Matplotlib.

## 5. Próxima obrigação científica concreta

Inalterada pela presente revisão, e não resolvível por código: **fechar a ponte
⟨FF⟩ → laço de Wilson → kernel estático da etapa E2.1**, item 2, tratando
explicitamente a projeção tensorial em p² = 0, os termos de contato e as
subtrações, de modo que a Proposição P-E2 deixe de ser conjectura com esboço.
Enquanto isso não for feito com rigor, H3 além da ordem líder permanece
hipótese, e a nota `notes/E2b_tensor_classification.tex` permanece nota de
pesquisa, não prova.

A obrigação administrativa mais próxima é A1: sem os dois arquivos rastreados,
nenhuma execução de CI é sequer possível.

---

# Adendo — 24 de setembro de 2026

Reaberto no dia seguinte, com o Codex **parado** (último arquivo escrito:
`output/certified_one_loop/summary.json`, 23/09 às 22:31:11). Sem concorrência
desta vez. Árvore reexecutada nesta data: **169 testes aprovados**.

## 6. Verificação independente da proposta Stieltjes ressomada

`reports/REVIEW_CLAUDE_2026-09-23.md` encerra com uma proposta, explicitamente
marcada por seu autor como **proposta derivada e não verificada no
repositório**, de que a obrigação científica correta não é provar dσ₂ ≥ 0 — o
que seria impossível por construção — e sim mostrar que a resposta **ressomada**
permanece na classe de Stieltjes. Como isso redirecionaria a agenda de E2,
verifiquei a álgebra de forma independente, em SymPy, antes que alguém construa
em cima dela.

**As três afirmações se confirmam.** Com ρ_J = Z·δ(s−s₀) e c = g_R²Z/s₀ ∈ (0,1):

| Afirmação | Resultado |
|---|---|
| Forma fechada 𝒢 = g_R²/Q² + [g_R²c/(1−c)]/(Q² + s₀/(1−c)) | **CONFIRMADA**, diferença simbólica exatamente 0 |
| Coeficiente O(g_R⁶) = g_R⁶Z²Q²/(s₀²(s₀+Q²)²) | **CONFIRMADA**, diferença exatamente 0 |
| O coeficiente de ordem fixa não é Stieltjes-positivo | **CONFIRMADA** (detalhe abaixo) |

Para a terceira: F(Q²) = Q²·[∫ρ_J/(s(s+Q²))]² tem F(0) = 0, F′(0) = Z²/s₀⁴ que
é exatamente A² com A = ∫ρ_J/s² = Z/s₀², ponto crítico interior em Q² = s₀, e
Q²·F → Z²/s₀², logo F ~ 1/Q². Tem portanto máximo interior. Toda função
∫dσ/(Q²+s) com σ ≥ 0 e suporte em [s\*,∞), s\* > 0, é **positiva** em Q² = 0 e
estritamente decrescente; F(0) = 0 e F cresce no início. Logo F não é dessa
forma. O argumento fecha.

A forma fechada mostra o ponto central: o peso g_R²c/(1−c) é **positivo** para
c ∈ (0,1) e o polo fica em s₀/(1−c) = s₀²/(s₀ − g_R²Z), que **sobe** com o
acoplamento. Isto é, H3 vale a todas as ordens da cadeia de bolhas, e o que
quebra a positividade ordem a ordem é apenas o deslocamento do limiar. As
afirmações 1–2 e a 3 apontam em direções opostas e **ambas são verdadeiras**:
a 3 diz que o coeficiente de ordem fixa não é Stieltjes; a 1 diz que o objeto
ressomado é. É exatamente esse o argumento.

### Duas observações minhas, que o relatório original não faz

1. **A convergência de A tem dois extremos, não um.** O relatório justifica
   A = ∫ρ_J/s² ds < ∞ por ρ_J ~ (s−4m²)^{1/2} perto do limiar — isso cuida do
   extremo **inferior**. O extremo superior também precisa: com ρ_J → constante
   no UV, ∫^∞ ds/s² converge. Os dois convergem, então o passo "derivada
   +A² > 0" se sustenta; mas a justificativa publicada é unilateral.
2. **A álgebra depende da convenção subtraída.** O coeficiente O(g_R⁶) na forma
   citada só decorre se Π̄ for a polarização **subtraída**, com Π̄(0) = 0
   (usei Π̄ = Q²∫ρ_J/(s(s+Q²))). Com a forma não subtraída o termo sai como
   Π̄²/Q², de formato diferente, e as afirmações 1–2 **não** fecham — foi assim
   que errei na primeira tentativa. Isso não conflita com o registro O3 de
   `DECISIONS.md`, que diz que a **H3 do artigo é não subtraída**: ali a não
   subtração é de σ, e aqui a subtração é de Π̄, objetos distintos. Registro
   para que ninguém conflate os dois ao escrever a nota de E2.

**Escopo.** Confirmei uma identidade algébrica dentro de uma proposta. Isso
**não** é endosso da proposta como direção de pesquisa correta, nem prova de
que a resposta ressomada de QED permaneça na classe de Stieltjes — o caso
verificado é um modelo solúvel de um polo. O próprio relatório limita o alcance
à parte **redutível**, e a contribuição irredutível de dois laços permanece
objeto separado, podendo cancelar parcialmente. A proposta continua proposta.
