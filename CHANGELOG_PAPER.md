# Changelog do manuscrito (`paper/paper.tex`)

## v0.2 — 2026-09-21 — Etapa E0 (consolidação técnica)

Conteúdo científico (teoremas, hipóteses e conclusões) **inalterado**. Mudanças:

- **Autoria:** Mauro de Oliveira Cardoso (research name: Viole). Afiliação:
  pesquisador independente, Botucatu, SP.
- **Seção 7, medida com sinal:** os valores brutos a₃(1) = −0.1735 e
  det H₀(1) = −0.0249 agora aparecem, e a normalização eʳaₙ dos valores
  anteriores (−0.4715 e −0.1839) está declarada.
- **Seção 7, limiar escondido:** o modelo aparece explicitamente
  (contínuo (x−3)^{1/2}e^{−(x−3)}). O crossover r× = 22.76 é identificado como
  propriedade do modelo, distinto do t× do Teorema H (27.6 para o mesmo ε).
- **Seção 2, convenção de sinal:** o argumento de orientação da superfície de
  linking foi removido, por ser inválido. δ é definido, e a comparação com
  Basile–Golmohammadi ficou marcada como pendente.
- **Introdução:** a relação com trabalhos recentes (Raman; Wagman;
  Hackett–Wagman; Lawrence; Mutzel–Tilloy; Hinrichs–Polzer) e com Seiler agora
  é declarada.
- **Seção 6:** o teste de positividade é reconhecido como diagnóstico
  estabelecido (Loveridge–Oliveira–Silva). A diferença está só na
  profundidade do gate.
- **Figura 1:** limiar escondido e lei de borda de Dirac, com dados de
  `reproducibility/figure_data.py`.
- **Bibliografia:**
  - Bachas corrigido ("Concavity", 1986);
  - anos de revista em vez de anos de preprint;
  - 8 entradas novas com metadados de API;
  - proveniência em `annote` (não impressa);
  - estilo `physofall.bst` enviado junto com as fontes.
- **Build:** zero warnings, zero overfull e zero fontes bitmap, garantidos
  por `tests/test_paper_build.py`.
