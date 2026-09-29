# Passagem de tarefa para Claude — 23 de setembro de 2026

O usuário pediu: "corrija e melhore tudo que achar", depois "continue ate
terminar e passe a tarefa pro claude". Este documento passa o estado concreto
do trabalho para continuidade. Não assuma que os registros históricos sejam
evidência atual nem que um teste aprovado demonstre um teorema físico.

## Fonte de verdade e preservação

- Workspace: `C:\Users\meyy\Downloads\physics of all`.
- Artigo canônico: `paper/paper.tex` e `paper/appendix.tex`, draft v0.3.
- PDF: `output/pdf/spectral_structure_v03.pdf`.
- Relatório atual: `reports/AUDIT_REMEDIATION_2026-09-23.md`.
- `manuscript/` é rascunho Quarto não canônico; `notes/E2b_tensor_classification.tex`
  é nota de pesquisa, não prova concluída de H3.
- Há mudanças locais ainda sem commit. Preserve-as. Não faça reset, checkout
  destrutivo, limpeza, commit, push ou publicação nesta passagem.
- Preserve `base_cientifica/`, `laplace/` e
  `reports/memoria_viole_2026-09-14/`, que já estavam não rastreados antes.
- Não envie mensagens, arquivos ou resultados a terceiros.

## Correções já implementadas

1. `reproducibility/moment_conditions.py` (v0.3a): condições finitas para
   momentos reais/finitos, matriz H0 e localizador H1, compartilhadas por todas
   as rotinas que emitem limite. Singularidade/precisão são recusadas como não
   resolvidas, não como refutação física. Em v0.3 isso era um auxiliar local de
   `falsification_suite.py` e três módulos irmãos não tinham guarda nenhuma.
2. Regressão central: δ1 + e δ2 − e⁹δ10/1000, r=1, dá momentos reescalados
   (1.999,2.99,4.9,8), det H0=.855, det H1=−.09. A antiga resposta negativa
   B1≈−.0644645 agora é recusada.
3. Limitação registrada e testada: δ1+δ2+δ3−10⁻⁶δ4 passa em ordem5, falha em
   ordem7. Aprovação finita se chama `CHECKED_COMPATIBLE`, nunca prova de H3.
4. Artigo: inclusão do suporte versus borda exata, limiar efetivamente acoplado
   versus carregado, gap H2 versus positividade, medida não nula e espectro
   atômico finito foram corrigidos. Hipóteses da implicação gravitacional e
   prova do teto de uma espécie estão explícitas.
5. Certificados: 40 avaliações de amostras-fonte / 28 entradas distintas;
   reintegração por parâmetros completos, comparação de todas as cópias dos
   dados, vínculo com configuração, proteção contra `python -O` e `--no-write`.
6. SVGs estáveis; rótulos CHECKED corrigidos; tabelas de auditoria regeneradas;
   teste de build aceita Tectonic; QA específico do PDF canônico foi acrescentado.
7. v0.3a, da revisão independente (`reports/REVIEW_CLAUDE_2026-09-23.md`):
   guardas unificadas nos quatro feixes, com a orientação estrita declarada pelo
   chamador; `mass_from_log_ratio` recusa razões fora de (0,1]; verificador
   completo (cardinalidades, produto cartesiano, bijeção de índices, todo
   contador recomputado); contadores renomeados para o que contam; feixe de
   Stieltjes a 120 dps com requisito de precisão medido. Nenhum enunciado
   científico mudou e as fontes de `paper/` não foram tocadas.

## Evidência atual

- pytest: **169 aprovados**, nenhum omitido, com Tectonic no PATH (eram 121 em
  v0.3; +32 em `tests/test_bound_guards.py`, +16 no verificador).
- Pipeline numérico aprovado; análise estendida **70 checks**; falsificação 21.
- 12 conjuntos, 144 comparações, 288 certificados e 28 reintegrações distintas,
  mais 12 benchmarks reintegrados e as checagens de completude.
- PDF de 12 páginas, sem avisos LaTeX/BibTeX, overfull ou fontes Type3;
  páginas inspecionadas visualmente por Codex, sem declarar revisão humana.
  Não foi recompilado em v0.3a: os 6 hashes de fonte e o hash do PDF em
  `output/data/canonical_pdf_qa.json` continuam iguais.
- Logs locais: `tmp/all-v03.log`, `tmp/numerics-v03.log`, `tmp/numerics-second.log`.
- QA e hashes: `output/data/canonical_pdf_qa.json`.
- Nenhum CI remoto foi executado; H3 geral não foi provada.
- **Atenção operacional:** dois agentes escreveram nesta árvore não comitada em
  23/09. Não rode dois agentes com escrita no mesmo workspace. Detalhes e
  evidência de mtime no achado A0 do parecer; o instantâneo do outro agente está
  em `reports/VERIFICATION_CLAUDE_2026-09-23.md` e foi preservado.
- Use `python -m pytest tests -q`; na raiz a coleta quebra por colisão de nomes
  com a cópia não rastreada em `laplace/`.

## Primeira tarefa para Claude — CONCLUÍDA em 23/09/2026

A revisão independente foi feita e depois implementada. Parecer completo,
com severidade, arquivo/linha, argumento, correção e o que ficou de fora:
`reports/REVIEW_CLAUDE_2026-09-23.md`. Resumo dos cinco pontos pedidos:

- *Limite inválido contornando as condições*: **sim**, fora de
  `falsification_suite` — três módulos irmãos emitiam limites sem guarda
  (achado A1). Corrigido por filtro compartilhado; nenhum número publicado
  estava errado, era defeito de guarda e de documentação.
- *Incompatibilidade vs posto/precisão vs hipótese física*: correto, e a guarda
  é unilateral. Mantido, agora com teste da orientação estrita.
- *Reintegração e deduplicação*: preservam a ligação. A lacuna era de
  **completude**, não de ligação (A2). Corrigida.
- *Enunciados e implicação WGC*: contêm as hipóteses necessárias. Verifiquei a
  cadeia, o teto de uma espécie, Teoremas C/E/H e a lei de borda (coeficientes
  re-derivados à mão). Nada a corrigir no artigo.
- *Texto que atribui demais à evidência*: quatro frases sobre o filtro e os
  contadores de proveniência (A1, A4). Corrigidas nos textos, não no artigo.

Não repita esta revisão. Se for auditar de novo, comece pelas limitações
remanescentes listadas no parecer (redução de posto, pré-registro da
configuração, vetor de teste em float64, inspeção visual, CI remoto).

## Continuidade científica

H3 além da ordem líder, a ponte ⟨FF⟩ → Wilson loop → kernel estático, termos
de contato/subtrações e isolamento positivo de canais carregados continuam
abertos. Não os resolva por renomeação, numerologia ou testes simbólicos de
dimensão finita. A nota E2b registra lemas e fontes ainda pendentes.

Rota concreta proposta para a primeira delas, no fim do parecer: o coeficiente
redutível O(g_R⁶) **não** é da forma de H3 com medida positiva (anula-se em
Q²=0 e tem máximo interior), e no caso solúvel ρ_J = Zδ(s−s₀) o núcleo
ressomado dá medida positiva com o **polo deslocado** para s₀/(1−c). Logo a
obrigação não é "mostrar dσ₂ ≥ 0" — é mostrar que a resposta ressomada
permanece na classe de Stieltjes, com o deslocamento de limiar e a condição
g_R²Π̄ < 1 controlados. Isso é **proposta, não teorema**; não a promova sem
prova.

Os comandos de validação e a configuração local do compilador estão no
relatório atual. O binário Tectonic está em `tmp/tools/tectonic-0.17.0/`,
sem instalação global; sua origem e digest foram conferidos.

## Sess?o Claude Code criada

ID: `ad31838e-09a3-4f5f-a4b6-83d33c8fb7d7`.

Retomar no PowerShell, a partir deste workspace:

```powershell
& 'C:\Users\meyy\.local\bin\claude.exe' --resume ad31838e-09a3-4f5f-a4b6-83d33c8fb7d7
```

Atualiza??o final de Codex: a compara??o de todas as c?pias foi estendida
tamb?m aos benchmarks diretos de peso. A regress?o adicional passou;
valida??o final: 121 testes, 28 amostras e 12 benchmarks diretos reintegrados.
O registro da primeira revis?o de Claude ? separado da evid?ncia de execu??o
por Codex.

---

## Estado atual — 24 de setembro de 2026

Esta seção **substitui** a resposta que este agente escreveu em 23/09, que
ficou obsoleta: ela dizia "nenhuma correção de código foi aplicada" e listava
achados que o outro agente corrigiu logo depois. Estava no rodapé, lendo-se
como palavra final sem ser.

### Onde o trabalho parou

O outro agente parou em **23/09 às 22:31:11**, tendo como último arquivo
`output/certified_one_loop/summary.json`. Nada foi tocado por ele desde então.
O estado é **consistente**: `python -m pytest tests -q` dá **169 aprovados**,
reexecutado e confirmado em 24/09.

Ordem dos fatos: revisão somente leitura → relatório em
`reports/VERIFICATION_CLAUDE_2026-09-23.md` → (concorrência detectada) → o
outro agente implementou correções e escreveu
`reports/REVIEW_CLAUDE_2026-09-23.md` → regenerou todos os artefatos.

### Os dois relatórios usam numerações incompatíveis

Isto já causou confusão e o próprio `REVIEW_` alerta. Mapa:

| VERIFICATION_ (23/09) | REVIEW_ (23/09) | Situação em 24/09 |
|---|---|---|
| A0 concorrência de dois agentes | A0 (mesmo fenômeno) | encerrada; sem concorrência agora |
| A1 CI referencia arquivo não rastreado | — | **ABERTA e mais grave** (ver abaixo) |
| A2 `pytest` na raiz falha na coleta | limitação 5 | **CORRIGIDA em 24/09** (`pytest.ini`) |
| A3 contagem de 40 sem asserção | A2 + A4 (mais amplos) | superada pelo trabalho do outro agente |
| A4 ponteiro obsoleto no cabeçalho do CI | — | **CORRIGIDA em 24/09** |
| — | A1 três módulos irmãos sem guarda | corrigida por ele; eu havia examinado a função homônima errada |
| — | A3 feixe float64 sem requisito medido | corrigida por ele |
| — | extra: linha C5 de `claims_matrix.csv` | corrigida por ele |

### O que está aberto — obrigação administrativa prioritária

**Quatro arquivos load-bearing continuam não rastreados.** O mais crítico:
`reproducibility/moment_conditions.py` é importado por quatro módulos
**rastreados e modificados** (`analysis`, `extended_analysis`,
`falsification_suite`, `laplace_geometry`). Commitar sem ele quebra o pipeline
inteiro num clone novo. A falha seria **ruidosa, não silenciosa** — o job
`tests` do CI para com `ImportError` —, mas trava a primeira execução.

```
git add reproducibility/moment_conditions.py reproducibility/canonical_pdf_qa.py         tests/test_bound_guards.py tests/test_one_loop_verifier.py         pytest.ini reports/VERIFICATION_CLAUDE_2026-09-23.md         reports/REVIEW_CLAUDE_2026-09-23.md reports/AUDIT_REMEDIATION_2026-09-23.md
```

Decisão do autor. Nenhum agente commitou, fez push ou mexeu no índice.
`base_cientifica/`, `laplace/` e `reports/memoria_viole_2026-09-14/` intactos.

### Correções aplicadas em 24/09

- `pytest.ini` com `testpaths` e `norecursedirs`: `python -m pytest` na raiz
  passou a funcionar. Conferido que raiz e `make.py test` dão **169** iguais.
- Cabeçalho de `.github/workflows/tests.yml`: ponteiro para `FINAL_REPORT.md`
  substituído pela fonte de status corrente, e registrada a dependência dos
  arquivos não rastreados.

### Continuidade científica

A obrigação de fundo não mudou: **H3 além da ordem líder**. O que mudou é a
formulação proposta no fim de `REVIEW_CLAUDE_2026-09-23.md`. Verifiquei a
álgebra dela de forma independente em 24/09, em SymPy, e as três afirmações
**se confirmam** — registro na seção 6 de
`reports/VERIFICATION_CLAUDE_2026-09-23.md`, com duas ressalvas minhas: a
convergência de A precisa dos dois extremos, e a álgebra supõe a polarização
**subtraída**, que não é a não subtração de σ registrada no O3 de `DECISIONS.md`.

Confirmar uma identidade algébrica dentro de uma proposta **não** é endossá-la
como direção de pesquisa, e o caso verificado é um modelo solúvel de um polo.
A proposta continua proposta; H3 continua hipótese; a parte irredutível de dois
laços segue em aberto.
