# Fechamento local do trabalho do Claude — v0.5.7

Registro R7, 23 de outubro de 2026. Repositório principal mantido no HEAD
`78b637cb6a2cf4d92691a3eb7e31312baf23ef32`. Nenhum commit, push ou publicação
foi feito na branch do usuário. Os commits mencionados abaixo pertencem somente
a repositórios descartáveis de verificação.

## O que foi concluído

- R4–R6 foram lidos antes de qualquer alteração. Seus cálculos longos não foram
  refeitos indiscriminadamente. A revisão independente de E4 e CI foi feita
  em paralelo, com um único escritor na árvore principal.
- O comparador do CI agora rejeita resultados científicos infinitos/NaN e
  aplica oito passos reais de representação binary64. Antes, finito contra
  infinito passava, e o limite relativo podia aceitar mais de oito ULP.
- `profile_moments` recusa parâmetros fora do modelo declarado antes de integrar:
  r>a>=0, acoplamento positivo finito, momentos e número de termos válidos,
  uma ou duas voltas no canal de pares e corte 0<smax<=4.
- Artigo v0.5.7, nota E4, catálogo, projeção e tabelas foram conciliados com
  a evidência. Os raios 20,649/m e 22,567/m permanecem CHECKED para o modelo de
  seis termos até s^9, cortado em 4m². O resto espectral não foi limitado
  uniformemente. A estimativa 0,002/m depende de uma envoltória não demonstrada.
- O cálculo novo da amplitude usa ponto flutuante. Quadratura com grau de
  exatidão polinomial não é aritmética racional exata. A fração 335/714 é uma
  reconstrução numérica; seis razões de coeficientes não provam um raio de
  convergência. O cálculo racional independente do coeficiente EH líder foi
  preservado.
- Caderno v0.3: 12 folhas e índice dos 60 itens, 20 páginas quadriculadas,
  com as pranchas GPT já existentes. v0.1 e v0.2 continuam íntegras. O gerador
  confere a versão do artigo em CITATION.cff e oferece uma checagem de fontes
  explícita para cópias sem PDFs. `.gitattributes` preserva os bytes dos arquivos
  congelados, evitando invalidar hashes por normalização de finais de linha.

Uma previsão de R5 não se confirmou: o aumento da densidade completa em s=3
foi 8,59 vezes o termo líder, acima do fator 3 antecipado. Isso reforça a
necessidade de separar verificação de amplitude, previsão numérica e cota
uniforme; não invalida por si os coeficientes baixos verificados.

## Verificação desta rodada

- Windows: **519 testes passaram**, nenhum pulado, 279,36 s.
- Regressões focadas de comparador, domínio, caderno e driver: 39 passaram.
- Após a última correção de metadados: 9 testes de catálogo/caderno passaram.
- `make.py bib`: 31 registros verificados offline; bibliografia regenerada.
- `make.py audit`: tabelas regeneradas.
- `build_claim_graph.py --check`: 60 itens, 32 unidades, nenhuma descoberta.
  Esse inventário não é uma revisão de cada prova.
- `make.py numerics`: exit 0.
- `make.py certified`: exit 0; reintegração independente Arb: PASS, 12 conjuntos,
  144 linhas, 288 certificados, 28 amostras e 12 benchmarks.
- Artigo Windows: build e QA estrutural PASS, v0.5.7, 16 páginas. Todas as páginas
  foram inspecionadas em imagens; páginas alteradas 1, 6 e 7 conferidas.
- Resumo para professor: build concluído, 6 páginas.
- Caderno: todas as 20 páginas inspecionadas em imagens, sem texto fora da página;
  checagens de integridade das três edições passaram. A checagem só de fontes
  informa expressamente que não verifica o PDF.

O ambiente Windows desta execução não é o ambiente novo de R6: Python 3.13.7,
numpy 2.3.5, scipy 1.15.3, sympy 1.13.1, matplotlib 3.10.3, pytest 8.4.1,
mpmath 1.3.0, python-flint 0.9.0 e PyMuPDF 1.28.0. Versões e logs:
`tmp/codex_finish_claude_2026-10-23/`.

### Ubuntu nativo

O artigo e o resumo compilaram com **Tectonic Linux 0.17.0**, e o QA do artigo
passou com 16 páginas. Isso valida um compilador nativo Linux, mas não substitui
o CI remoto com TeX Live. O resumo emite dois avisos de compatibilidade de engine
(inputenc ignorado e shell escape desativado); a compilação não é descrita como
livre de avisos. As etapas restantes estão EM EXECUÇÃO e serão registradas aqui.

## Candidato e limites da reprodução

O snapshot de fontes contém 701 arquivos e está em
`tmp/codex_finish_claude_2026-10-23/candidate/`, commit descartável
`37f21f4195b772381b984c67142b5745b53e28e6`.
`candidate_sha256.json` identifica seus bytes Windows; `candidate.tar` contém
os blobs do Git para a verificação Linux. As fontes congeladas do caderno
mantêm os bytes exatos, independentemente de CRLF/LF.

Uma pequena correção posterior envolveu só três arquivos: nota E4, catálogo
e projeção de claims (histórico das cinco buscas e redação de aritmética
numérica). Está identificada em `metadata_delta_sha256.json` e recebeu a
checagem focada. Os registros finais e o QA do caderno são documentação posterior
ao snapshot; não se deve apresentá-los como tendo sido executados antes dele.

## O que continua aberto

- **Pesquisa:** envoltória uniforme para o resto espectral, contribuições acima
  do corte e ordens perturbativas omitidas; verificação independente da
  divergência com Dicus–Kao–Repko em omega^8; originalidade do coeficiente.
- **Fonte primária:** Brown–Weisberger continua ABSTRACT_READ. APS e ADS não
  forneceram o integral. Identificadores recuperados: DOI
  10.1103/PhysRevD.20.3239, preprint RLO-1388-793, INSPIRE 141197 e OSTI 5542094.
  A próxima rota é acesso autorizado por biblioteca. Evidência das tentativas:
  `tmp/brown_primary_final_2026-10-23/READ_RESULT.md`.
- **Externos:** CI remoto sobre a futura versão commitada e revisão humana.
  Não foram simulados como concluídos. H3 física e a construção quântica geral
  da linha permanecem abertas nos termos do artigo.

O resultado desta rodada é fechamento local de código, escopo e reprodução.
Não é certificação da QED completa nem READY_FOR_EXPERT_REVIEW.
