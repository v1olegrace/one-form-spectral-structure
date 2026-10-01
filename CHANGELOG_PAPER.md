# Changelog do manuscrito (`paper/paper.tex`)

## v0.5 — 2026-10-01 — Do ⟨FF⟩ ao kernel estático, em ordem linear na sonda

O artigo mudou; o PDF canônico e o registro em
`output/data/canonical_pdf_qa.json` foram refeitos para a v0.5.

- **Apêndice A, Proposição 7 (nova).** Em ordem linear na carga da sonda, o
  potencial estático do laço de Wilson e o campo de uma linha estática dependem
  de ⟨FF⟩ só através de $a^{(3)}(r)=\int d\mu(s)\,e^{-\sqrt s r}/(4\pi r)$, com
  $\mu\ge0$ a medida de Källén–Lehmann de ⟨FF⟩. Em $r>0$ isso dá as Hipóteses 3
  e 5, com $g_R^2=\mu(\{0\})$, a menos de um polinômio de contato. As hipóteses
  usadas são de $F$, não de um propagador de gauge: Wightman sem localidade,
  Bianchi incluindo pontos coincidentes e $\int d\mu/(1+s)<\infty$. A prova
  completa e 24 testes estão em `notes/E2c_transport_linear_probe.md` e
  `tests/test_e2c_transport.py`; o apêndice traz o esboço.
- **As Hipóteses 3 e 5 continuam hipóteses.** A classificação de ⟨FF⟩ usa
  Bochner–Schwartz e uma desintegração covariante que ainda não foram conferidas
  nas fontes primárias. O texto diz isso onde a proposição é anunciada.
- **O que Bianchi nos pontos coincidentes exclui** é a estrutura local
  $\delta\delta-\delta\delta$, que dá lei de área. É a função $D$ do modelo do
  vácuo estocástico, creditada a Di Giacomo, Dosch, Shevchenko e Simonov
  (Phys. Rept. 372, 2002), lida nas seções 2.1, 3.1, 3.2 e 4.2. A entrada veio
  do INSPIRE, com o ano de publicação (2002) do Crossref, porque o INSPIRE dava
  o ano do preprint.
- **Cadeia de bolhas em $Z_3=0$.** A constante $1/\mu$ é um termo de contato,
  suportado em $r=0$: a conclusão do Teorema A em $r>0$ sobrevive, e só a H3
  literal falha. A falha genuína é $Z_3<0$, que nenhuma medida positiva em
  $[0,\infty)$ produz.
- **Texto principal.** A lista "What is and is not claimed" ganha o item sobre
  o vácuo estocástico; o parágrafo depois das hipóteses anuncia a Proposição 7
  com suas ressalvas; a discussão troca "estabelecer H3 além da ordem líder"
  por conferir os lemas e ir além da ordem linear na sonda, onde entra o
  espalhamento luz-luz.

Não mudou: teoremas A, C, E e H, a frase sobre positividade de reflexão
(decisão D6) e o fato de que nada se afirma em $O(q_W^4)$.

## v0.4 — 2026-09-29 — A cadeia de bolhas ressomada entra no apêndice

O artigo mudou nesta versão, ao contrário da v0.3a. O PDF canônico precisa ser
recompilado e o registro de hashes em `output/data/canonical_pdf_qa.json`
deixa de valer para as fontes atuais.

- **Apêndice A, parágrafo novo.** A v0.3 terminava a ordem líder dizendo que o
  resto $O(g_R^6)$ não era afirmado positivo. Isso continua certo em ordem fixa,
  e agora o texto mostra por quê: o termo de ordem $g_R^6$ se anula em $Q^2=0$,
  cresce e decai como $1/Q^2$, e nenhuma $\int d\sigma/(Q^2+s)$ com
  $d\sigma\ge0$ tem esse formato. A positividade é propriedade da soma. Para a
  cadeia ressomada, frações parciais dão $W=Z_3+g_R^2\int\rho_J/(s+Q^2)$ e a
  hipótese H3 se reduz ao sinal de $Z_3$: vale para $Z_3>0$; falha para
  $Z_3<0$ por um polo spacelike de resíduo negativo; e falha em $Z_3=0$ por uma
  constante aditiva quando a massa total é finita. A ausência de polo é
  necessária e não basta.
- **Duas consequências, também no apêndice.** A densidade do contínuo é
  $g_R^4\rho_J/(s|W|^2)$, não negativa para qualquer acoplamento, de modo que um
  teste feito com momentos do contínuo não vê a falha em $Z_3<0$. E, com corte
  rígido e densidade que não se anula na borda, a medida ressomada ganha um
  átomo de peso positivo acima do corte.
- **Atribuição do átomo.** O mecanismo é o de Giacosa e Wolkanowski (2012,
  arXiv:1209.2332), agora citado: ressoma produzindo polo na folha física fora
  do espectro de entrada, com resíduo positivo e regra de soma. O artigo não o
  apresenta como resultado próprio. A entrada bibliográfica veio do INSPIRE e do
  Crossref pelo pipeline de proveniência, e não à mão.
- **Dualidade Stieltjes / Bernstein completa.** Citada em
  Schilling–Song–Vondraček (2ª ed., 2012), acrescentada à tabela de monografias
  com a ressalva de que o número do teorema está `PENDING_VERIFICATION`: fontes
  secundárias divergem entre Teor. 7.3 e Cor. 7.4, e o livro não foi aberto.
- **Texto principal.** A seção de escopo agora diz explicitamente que passar nos
  testes de momentos finitos não exclui uma falha de H3 fora do contínuo. O
  parágrafo que discute H3 aponta para a redução por $Z_3$ no apêndice. Uma
  frase iniciada por "Moreover" foi reescrita.
- **QED a um laço.** $Z_3=0{,}966$ em $\Lambda^2=10^{20}\,m^2$; $Z_3$ só se anula
  perto de $\log(\Lambda^2/4m^2)=3\pi/\alpha$, o polo de Landau do acoplamento a
  um laço, o que coincide com a escala usual $\sim m\,e^{3\pi/2\alpha}$.

Não mudou: teoremas A, C, E e H, as hipóteses H1–H5 e a conclusão de que H3
permanece uma hipótese para o kernel físico não perturbativo.

## v0.3a — 2026-09-23 — Revisão independente por Claude (código e evidência)

As fontes do artigo **não** mudaram nesta rodada: os seis hashes de
`paper/` registrados em `output/data/canonical_pdf_qa.json` e o hash do PDF
continuam idênticos, logo o PDF canônico v0.3 segue válido e não foi
recompilado. Mudaram o código de suporte, o verificador e as evidências.

- **Filtro unificado.** As condições necessárias finitas saíram de
  `falsification_suite.py` para `reproducibility/moment_conditions.py` e agora
  são importadas por todas as rotinas que emitem limite: `falsification_suite`,
  `laplace_geometry` (feixe de Laplace), `extended_analysis` (feixe de Hausdorff
  amostrado) e `analysis` (feixe de Stieltjes). Antes o filtro era um auxiliar
  local de um único script, enquanto três módulos irmãos publicavam limites sem
  verificação alguma. O chamador declara qual matriz é o **denominador** do
  feixe (`strict_shift`), porque só essa recebe a recusa estrita por
  quase-singularidade; as duas orientações são opostas e proteger a matriz
  errada seria silencioso.
- **Guarda de domínio.** Tudo que toma logaritmo de razão de momentos passa por
  `mass_from_log_ratio`, que recusa razões fora de (0,1] em vez de devolver
  massa negativa. `extended_analysis` calculava `-log(L)/h` sem checar L.
- **Verificador completo.** `verify_one_loop_output.py` recomputa todos os
  contadores, exige que a tabela de comparação seja o produto cartesiano
  datasets × graus × cortes e que os índices de certificado formem uma bijeção.
  Presença deixou de ser confundida com completude: linha removida ou índice
  reutilizado é recusado.
- **Contadores com o nome do que contam.** `raw_integral_evaluations` e
  `unique_raw_integrals` passaram a `source_enclosure_evaluations` (40) e
  `distinct_source_enclosures` (28); as 12 integrais de benchmark e as 40
  checagens independentes em mpmath são contadas à parte, com um campo
  `counter_scope` dizendo que nenhum contador é o total de quadraturas.
- **Precisão medida no feixe de Stieltjes.** `analysis.localizing_bound` passou
  a 120 dígitos e registra por linha os dígitos que o denominador exige (1 a 13
  em K = 0..5) e a diferença da rota float64 anterior (no máximo 5,9e-12). O
  resultado: a precisão dupla *era* suficiente ali — mas agora isso é medição
  com caminho de recusa, não suposição.
- **Testes discriminantes.** `tests/test_bound_guards.py` (32) e novos casos em
  `tests/test_one_loop_verifier.py` (21 no total) falham nas versões
  incompletas. Suíte: 169 aprovados, nenhum omitido.
- Parecer e obrigações remanescentes: `reports/REVIEW_CLAUDE_2026-09-23.md`.

## v0.3 — 2026-09-23 — Correções da auditoria científica

- Filtro finito verifica momentos reais/finitos, H0 e o localizador H1;
  `hankel_bound` verifica seus próprios dados antes de emitir um resultado.
  Posto/precisão não resolvidos produzem recusa, não uma refutação de H3.
  (Em v0.3 isso valia só para `falsification_suite.hankel_bound`; ver v0.3a.)
- Novos contraexemplos cobrem H1 indefinida apesar de momentos positivos,
  medida assinada compatível em baixa ordem e átomos positivos singulares.
- Monotonicidade completa garante inclusão do suporte, não igualdade da borda.
  O texto distingue limiar acoplado, limiar carregado, gap e positividade.
- Condição de medida não nula, término da hierarquia para espectros finitos,
  condições da lei de borda e alcance da falsificação foram explicitados.
- A implicação gravitacional agora contém as hipóteses de espécies leves,
  aditividade, cauda, erro e positividade da margem, além da cadeia algébrica;
  o teto de uma espécie ganhou uma prova no apêndice canônico.
- H3 permanece um problema aberto além da ordem líder. A relação com
  positividade por reflexão não é declarada uma implicação estrita já provada.
- Certificados: 40 avaliações de amostras-fonte correspondem a 28 entradas
  distintas; cada cópia dos dados é verificada, inclusive em conjuntos com
  ruído diferente. O verificador recusa `python -O` e permite execução sem
  escrever arquivos. (Os nomes dos contadores e as checagens de completude
  chegaram em v0.3a.)
- Metadados SVG estáveis; terminologia `CHECKED` corrigida; tabelas de auditoria
  apontam para as provas canônicas e distinguem resultados do rascunho Quarto.
- PDF canônico compilado com Tectonic; teste de build agora aceita esse motor.
  Validação atual e limitações: `reports/AUDIT_REMEDIATION_2026-09-23.md`.

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
