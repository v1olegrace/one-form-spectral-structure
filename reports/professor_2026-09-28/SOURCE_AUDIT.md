# SOURCE_AUDIT — pacote professor, 28/09/2026

Autor: Claude (leitura e redação). Escrita restrita a `reports/professor_2026-09-28/`. Nenhum git add/commit/push.
Sem web. **Python não pôde ser executado nesta sessão (permissão negada)**: `check_numbers.py` foi escrito mas
**não rodou**, e `fig_tiny_atom.csv` **não existe** ainda. Codex deve executar
`python reports/professor_2026-09-28/check_numbers.py` e conferir as saídas contra CONTENT.md.

## 1. O que foi verificado hoje (28/09) e o que é registro histórico

| Item | Tipo de evidência |
|---|---|
| sha256 de `paper/paper.tex`, `paper/appendix.tex`, `paper/figures/hidden_threshold.dat` e `output/pdf/spectral_structure_v03.pdf` iguais aos de `output/data/canonical_pdf_qa.json` | **verificado hoje** (sha256sum) — o PDF v0.3 corresponde às fontes atuais |
| t_× = ln(10¹²) = 27,63; r_× ≈ 22,76 (decomposição 27,63−0,12−4,75); Γ(10,20,22,76,30) = 3,136/3,018/2,532/2,0005; B₀(3)=3,375 | **conferido à mão hoje** |
| ã_n=(1,999;2,99;4,9;8), det H̃₀=0,855, det H̃₁=−0,09, B₁≈−0,0645; a₃(1)=−0,1735 para δ₁−½δ₂ | **conferido à mão hoje** |
| Polo único: 𝒢 = g²/Q² + [g²c/(1−c)]/(Q²+s₀/(1−c)) | **conferido à mão hoje** (frações parciais) |
| Tabela Z₃ de QED (0,9335 / 0,6446 / 0,0022 / −0,083) | conferida à mão via (α/3π)(L−0,28); fonte: nota 24/09 |
| pytest 169, 70 checks, 21 falsificação, 288 certificados, 28 reintegrações, 1,4981/2,4904, B₀..₄(3)→3,108, ≈86 dígitos, ordem 5/7 | **registrado em 22–23/09, NÃO reexecutado** |
| 13 testes de `tests/test_e2_tensor_classification.py` | nomes lidos; **não executados** |

## 2. Inventário de fontes (versão, status, como foi lido)

| Arquivo | Data/mtime | Status | Leitura |
|---|---|---|---|
| `paper/paper.tex` (599 l.) | 23/09 | **canônico v0.3** | integral |
| `paper/appendix.tex` (163 l.) | 22/09 | **canônico v0.3** | integral |
| `notes/H3_attack_2026-09-24.md` (271 l.) | 24/09 | nota de trabalho **mais recente**; não promovida | integral |
| `notes/E2b_tensor_classification.tex` (376 l.) | 22/09 (conteúdo em HEAD `72d6dcc`) | nota de trabalho; não compilada; 3 lemas "to read" | integral |
| `notes/E2_codex_brief.md` | 22/09 | brief corrigido | grep (l. 58–65) |
| `DECISIONS.md` | — | registro de decisões | l. 9–90, 179–275 |
| `ROADMAP_CIENTIFICO.md` | — | plano | l. 135–274 (E2) |
| `HANDOFF_CLAUDE.md` | 23/09 | passagem | l. 1–100 |
| `reports/REVIEW_CLAUDE_2026-09-23.md` | 23/09 | parecer | l. 278–313 |
| `reports/HANKEL_PADE_GEVP_EQUIVALENCE.md` | — | mapa de analogia | integral |
| `reports/WHAT_IS_ACTUALLY_NEW.md` | 11/09 | **histórico** (parcialmente superado) | l. 1–104 |
| `reports/H3_DEEP_DIVE.md` | 11/09 | **histórico** | cabeçalho + grep |
| `reports/AUDIT_REMEDIATION_2026-09-23.md` | 23/09 | relatório | cabeçalho |
| `data/theorem_status.csv` | — | tabela de status | linhas A–L4 |
| `output/README.md` | — | rótulos CERTIFIED/CHECKED | grep |
| `output/data/canonical_pdf_qa.json` | 23/09 | QA do PDF | integral |
| `CHANGELOG_PAPER.md` | — | changelog | l. 1–20 |
| `base_cientifica/.../extracoes/paper_draft.txt` | PDF de 15/09 | rascunho não canônico *Finite-data certificates* (paper 2 por D1) | grep das proposições |
| `base_cientifica/.../manifesto_fontes.json` | 21/09 | manifesto | integral |
| `laplace/README_1.md` | 21/09 | **histórico v0.2** | 12 linhas |
| `reports/memoria_viole_2026-09-14/05_MEMORIA/CONFLITOS.md` | 14/09 | **histórico** | só títulos (CF06 "crossover depende do modelo") |

## 3. Referências usadas no CONTENT (arquivo:linhas) e classificação epistemológica

| Afirmação no pacote | Fonte | Classe |
|---|---|---|
| Def. q(r), δ(r), Φ(r) | `paper/paper.tex:169-174, 191-198` | definição |
| H1–H5 | `paper/paper.tex:213-246`; H3 central e não provada: `:248-257` | hipóteses |
| Teorema A e prova | `paper/paper.tex:261-298` | teorema condicional |
| Ordem líder, Basile–Golmohammadi eq. 13, Uehling | `paper/paper.tex:308-312`; `paper/appendix.tex:20-72` | teorema (dada dispersão) |
| Teoremas C, E, momentos, pencil | `paper/paper.tex:318-356`; provas `paper/appendix.tex:89-144` | teorema (aplicação clássica) |
| Edge law | `paper/paper.tex:358-367`; `paper/appendix.tex:146-163` | teorema |
| CM ≠ H3; filtros finitos; CHECKED | `paper/paper.tex:372-402` | teorema/escopo |
| Primeiro limiar não carregado (multi‑fóton) | `paper/paper.tex:404-411` | limitação |
| Teorema H, t_× | `paper/paper.tex:413-427` | teorema |
| Medida assinada; δ₁+eδ₂−e⁹δ₁₀/1000; ordem 5/7 | `paper/paper.tex:454-471` | contraexemplo |
| Tiny atom, r_×=22,76 ≠ 27,6 | `paper/paper.tex:472-485`, Fig. `:487-522` | contraexemplo + numérico |
| Condicionamento 86 dígitos | `paper/paper.tex:524-527` | numérico registrado |
| Obstrução WGC | `paper/paper.tex:529-563` | teorema condicional |
| O(g⁶) não tem forma H3; polo único | `reports/REVIEW_CLAUDE_2026-09-23.md:284-312` | nota de trabalho (proposta do revisor) |
| Critério Z₃, dualidade SSV, QED, atribuição | `notes/H3_attack_2026-09-24.md:21-90, 135-176` | nota de trabalho |
| Frente 3 colapsa na 2 (sem ordem de laço) | `notes/H3_attack_2026-09-24.md:178-212` | nota de trabalho |
| ⟨E_iE_j⟩ longitudinal; CBF; g²_eff não decrescente | `notes/H3_attack_2026-09-24.md:218-260` | nota de trabalho (verificação simbólica registrada) |
| Proca ⇒ precisa (C) | `notes/H3_attack_2026-09-24.md:121-129`; `DECISIONS.md:187-194`; `notes/E2b...tex:256-261` | contraexemplo ao enunciado P‑E2 |
| P‑E2 conjectura | `ROADMAP_CIENTIFICO.md:154-159`; obrigações `DECISIONS.md:179-219` | conjectura |
| Hipóteses W/B; T; lemas | `notes/E2b_tensor_classification.tex:37-147` | nota de trabalho |
| Setores p=0, massivo, cone | `notes/E2b...tex:158-229` | nota de trabalho, álgebra testada |
| Teorema montado; escopo | `notes/E2b...tex:233-261, 308-325` | nota condicional a 3 lemas |
| Termos locais | `notes/E2b...tex:263-306` | nota de trabalho |
| Tabela de uso de hipóteses; testes | `notes/E2b...tex:327-364`; `tests/test_e2_tensor_classification.py:182-303` | — |
| H3 vs positividade de reflexão desconhecida | `DECISIONS.md:230-275` | estado aberto |
| Estimador vs falsificador | `reports/HANKEL_PADE_GEVP_EQUIVALENCE.md:18-33` | enquadramento |
| Prop. 3 (peso mínimo) | `base_cientifica/.../extracoes/paper_draft.txt:180-186` | rascunho não canônico |
| CERTIFIED vs CHECKED; 288 certificados | `output/README.md:25-30, 102-119` | benchmark, não H3 |

## 4. Erratas e versões superadas (não usar a forma antiga)

| Antigo | Atual | Onde |
|---|---|---|
| "H3 is strictly stronger than reflection positivity" (v0.2; também `H3_DEEP_DIVE.md:75-77`) | relação desconhecida nas duas direções | `DECISIONS.md:230-275`; `paper/paper.tex:118-123` |
| Brief do Codex: ⟨E_iE_j⟩ estático transversal | longitudinal, escalar Q²D(Q²) | `notes/E2_codex_brief.md:58-65`; `DECISIONS.md:196-202` |
| Roadmap E2.1 passo 1: "(B) elimina a dual para p²≠0" | só p²>0; no cone, localidade via CPT | `ROADMAP_CIENTIFICO.md:163-167` vs `:203-209`; `notes/E2b...tex:190-229` |
| P‑E2 sem hipótese de Coulomb | precisa (C), μ({0})>0 | `DECISIONS.md:187-194` |
| Roadmap E2.1 passo 3: "∫ρ/(s+μ²) diverge" | vale para ρ_J, não para σ (a um laço H3 não subtraída converge) | `DECISIONS.md:204-213` |
| `WHAT_IS_ACTUALLY_NEW.md:97-99`: "r_x ≈ log(1/ε)/(M−μ), predicted 22.758" | 22,76 é o crossover do modelo; log(1/ε)/Δm dá 27,6 | `paper/paper.tex:476-480`; CONFLITOS CF06 |
| `WHAT_IS_ACTUALLY_NEW.md` (versão anterior): positividade só confirma em outras áreas | falso; violação de positividade é diagnóstico estabelecido (Loveridge et al. 2022) | `WHAT_IS_ACTUALLY_NEW.md:57-83`; `paper/paper.tex:394-397` |
| Corolário A1 (Stieltjes da polarização) como contribuição | PREVIOUSLY_KNOWN (Raman 2026) | `WHAT_IS_ACTUALLY_NEW.md:12-32` |
| Nota H3: "Planck ⇒ log ≈ 100, Z₃ ≈ 0,93" | a linha 10¹⁹ da tabela é Planck em GeV, não em m_e; Planck/m_e ≈ 2,4×10²² ⇒ L ≈ 101, Z₃ ≈ 0,92 | `notes/H3_attack_2026-09-24.md:84` (erro menor; CONTENT cita só as linhas da tabela) |
| Polo de Landau "em L = 3π/α" | leading log; com densidade completa Z₃=0 em L ≈ 3π/α + 0,28 | `notes/H3_attack_2026-09-24.md:83` (irrelevante na prática) |

## 5. Não lido / lido parcialmente (cobertura real)

- `laplace/Cardoso_Viole_one-form_spectral_v0.2.pdf` e `laplace/physics_of_all_v0.2_update/` (v0.2, histórico): **não lidos**.
- `reports/memoria_viole_2026-09-14/` (65 arquivos): só títulos de `CONFLITOS.md`.
- `base_cientifica/.../fontes/*.pdf`: não abertos; `paper_draft.txt` só por grep; `caminhos_pesquisa.txt` só 40 linhas.
- `manuscript/*.qmd` (onde vivem os Teoremas F e G): **não lidos** — F/G ficaram fora do pacote.
- `FINAL_REPORT.md`, `RED_TEAM_REPORT.md`, `REMEDIATION_LOG.md`, `README.md`, `HANDOFF_CLAUDE.md:101-205`.
- `reports/`: BOOK_ROADMAP, LITERATURE_MAP, PRIORITY_THREATS, SEARCH_SATURATION_REPORT, SOFTWARE_AUDIT,
  UNREAD_HIGH_PRIORITY, VERIFICATION_CLAUDE, AUDIT_REMEDIATION (além do cabeçalho), REVIEW_CLAUDE fora de l. 278–313.
- `data/claims_matrix.csv`, `data/claim_literature_matrix.csv`, `data/literature_audit.csv`, `data/manuscript_comparison.csv`.
- Código em `reproducibility/` e demais testes: não lidos (só nomes de testes E2).
- Nenhuma fonte primária externa (Källén, SSV, Streater–Wightman, Brown–Weisberger) foi lida por mim; as citações a elas
  são as registradas nas notas.

## 6. Questões críticas para o Codex e o usuário

1. **Nenhum problema fatal encontrado** nas afirmações usadas: as implicações do artigo estão corretamente condicionadas, e
   os números conferidos à mão batem.
2. **O maior risco de apresentação** é a p. 4 parecer progresso sobre H3. Ela não é: a classificação é nota não compilada,
   provavelmente clássica, e o passo O2 está intocado.
3. **Critério Z₃** é a coisa nova mais interessante, mas é nota de 24/09 não promovida e com atribuição aberta. Apresentar
   como tal. Ele também mostra que o kernel RPA **não** é Stieltjes no contínuo estrito de QED.
4. **Observação do redator, não verificada (para discussão, não para imprimir):** se D(s) = 1/(s[1−Π(s)]), então
   Im D = Im Π/(s|1−Π|²) no corte; positividade da densidade espectral completa do fóton e Im Π ≥ 0 da 1PI parecem a mesma
   condição (fora de zeros de 1−Π). Isso sugere que as frentes 2 e 3 da nota H3 podem ser a mesma pergunta. Conferir
   convenções antes de usar.
5. **Observação do redator:** se QED contínua for trivial, (W) pode não ter realização não trivial para QED; P‑E2 é sobre
   teorias que satisfazem (W). Não está registrado no projeto.
6. `check_numbers.py` precisa ser executado (dados da figura da p. 3; recomputa r_×, Γ, B_K(3), tabela Z₃, polo único).
   Se algum valor divergir de CONTENT.md, o CONTENT deve ser corrigido, não o script ajustado.
7. A analogia com relaxometria T2 na p. 3 é do redator, não do projeto; está marcada como analogia.
8. Notação: o artigo usa Γ para a inclinação e Γ_E para a função gama; manter na diagramação.
9. `test_cpt_reality_removes_the_null_dual` impõe a realidade CPT como entrada: α′=0 **não** é verificado por computador
   independentemente do lema de CPT não lido.
10. P‑E2 ≠ H3: a conclusão do roadmap não tem gap e admite polinômio de contato; o gap H2 do artigo não decorre da QFT.
11. Densidade: a p. 2 excede leitura de 30–60 s. Cortar primeiro para o backup as linhas O(g⁶) e CBF da tabela; na p. 4,
    cortar primeiro a frase sobre termos locais.
