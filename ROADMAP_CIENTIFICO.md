# Roadmap científico — Physics of All

**Autor:** Mauro de Oliveira Cardoso (nome de pesquisador: Viole)
**Versão do plano:** 1.0 — 21/09/2026
**Manuscrito de trabalho:** `paper/paper.tex` → PDF v0.2 (etapa E0 concluída)

## Pergunta central

> Quais informações sobre o espectro de uma teoria quântica podem ser extraídas
> de um observável de quebra aproximada de simetria de 1-forma, e quais
> hipóteses físicas são necessárias para que essa extração seja válida?

A primeira meta é um resultado **delimitado e matematicamente defensável** sobre
o perfil de quebra Φ(r) = δ(r)/r². Não é uma "descoberta fundamental". A
ambição maior só vem depois que esse resultado estiver de pé.

## Regras que valem em todas as etapas

1. **Nenhum número entra no texto sem um script que o recalcule e o verifique
   com `assert`.** Exemplo: `reproducibility/figure_data.py --check`.
2. **Nenhuma referência entra no `.bib` sem metadados de API** (INSPIRE,
   Crossref ou Semantic Scholar), com a proveniência registrada em
   `data/literature_harvest.json`. **Nenhuma referência é citada no texto sem
   ter sido lida por você** no nível daquilo que a frase afirma sobre ela.
   A política do arXiv prevê banimento por referências alucinadas.
3. **Vocabulário de status:** `CHECKED` (alta precisão, sem cota rigorosa) ≠
   `CERTIFIED` (intervalo rigoroso ou desigualdade provada) ≠ `PENDING`.
4. **Cada etapa termina com:**
   - um PDF versionado (`python make.py pdf` → `paper/paper.pdf`);
   - uma entrada em `CHANGELOG_PAPER.md`;
   - um commit e uma tag git `paper-vX.Y`;
   - build limpo, garantido por `tests/test_paper_build.py`: zero warnings,
     zero fontes bitmap e todos os números citados reproduzidos.
5. **Critério para encerrar uma etapa:** ela precisa produzir uma
   demonstração, um contraexemplo decisivo ou um dado reproduzível que reduza
   uma incerteza concreta. Um relatório novo não encerra etapa.

## Visão geral

| Etapa | Prioridade | Pergunta | Entregável | PDF |
|---|---|---|---|---|
| E0 | P0 | O manuscrito atual compila, está correto nos números e cita o que deve? | Build limpo, números verificados, bibliografia saneada | **v0.2 ✔** |
| E1 | P0 | Qual texto será a primeira submissão? | Matriz comparativa formal e decisão provisória | v0.3 |
| E2 | P0 | A positividade (de reflexão / Wightman) implica H3? Em que regime? | Proposição provada, ou contraexemplo, com escopo exato | v0.4 |
| E3 | P0 | O que exatamente é novo depois da literatura de 2024–2026? | Matriz claim → precedente lida no nível de equação | v0.5 |
| E4 | P1 | O método é robusto a ruído e a dados finitos? | Testes L/M/N, certificados corretos e figuras | v0.6 |
| E5 | P1 | O manuscrito está no formato da revista escolhida? | Texto final, template e material suplementar | v0.9 |
| E6 | P1 | A submissão está pronta? | arXiv, DOI do código e submissão | v1.0 |

As dependências são E0 → E1 → E2 → E3 → E4 → E5 → E6. O endosso do arXiv
(tarefa E6.1) começa **já**, em paralelo. E1 é **provisória** até o fim de E2,
porque o resultado de E2 pode exigir a Proposição 1 do rascunho
*Finite-data certificates*.

---

## E0 — Consolidação técnica do manuscrito ✔ (v0.2)

Feito nesta sessão. Cada item foi verificado por cálculo ou por metadados, e
não copiado de relatório.

- [x] **Build autocontido.** `JHEP.bst` não existe no TeX Live. Ele foi
  substituído por `paper/physofall.bst`, derivado de `unsrtnat` e enviado junto
  com as fontes. Esse estilo preserva a caixa dos títulos e imprime os links do
  arXiv.
- [x] **Build limpo.** Zero warnings, zero overfull e zero fontes Type 3 (os
  marcadores TS1 foram trocados por versões em modo matemático). Coberto por
  `tests/test_paper_build.py`.
- [x] **Autoria:** Mauro de Oliveira Cardoso, com nota "Research name: Viole".
  Os metadados ficam em macros (`\authorname`, `\researchname`,
  `\authoremail`).
- [x] **Normalização declarada.** Para ν = δ₁ − ½δ₂, os valores brutos são
  a₃(1) = −0.1735 e det H₀ = −0.0249; os reescalados (eʳaₙ) são −0.4715 e
  −0.1839.
- [x] **Origem do crossover 22.76.** Ele vem do modelo específico, com
  contínuo (x−3)^{1/2}e^{−(x−3)}, e **não** do t× do Teorema H (que daria 27.6).
  O modelo agora está escrito explicitamente no texto.
- [x] **Convenção de sinal.** Foi removida a justificativa por "orientação da
  superfície", que é inválida: q e q∞ trocam de sinal juntos. δ passou a ser
  tratado como definição, e a comparação linha a linha com
  Basile–Golmohammadi ficou marcada como pendente.
- [x] **Bibliografia.**
  - Bachas corrigido para "Concavity…", 1986, conforme Crossref/APS.
  - Anos de preprint trocados pelos anos de revista em 7 entradas.
  - Unicode convertido para LaTeX.
  - A proveniência passou para o campo `annote`, que não é impresso.
  - 8 referências novas com metadados de API: Raman 2026, Wagman 2025,
    Hackett–Wagman 2025, Lawrence 2024, Mutzel–Tilloy 2025,
    Loveridge–Oliveira–Silva 2022, Seiler 1978 e Hinrichs–Polzer 2025.
- [x] **Figura 1**, feita com pgfplots a partir de `paper/figures/*.dat`,
  gerados por `reproducibility/figure_data.py`. Painel esquerdo: limiar
  escondido. Painel direito: lei de borda de Dirac.
- [x] **Declaração de disponibilidade de dados e código** (a URL entra na
  submissão).

**Pendências herdadas, com a etapa que as resolve:**
- Ler Raman, Wagman, Hackett–Wagman, Lawrence, Mutzel–Tilloy e
  Hinrichs–Polzer **na íntegra** para confirmar as frases que os citam (E3).
  Por ora, elas afirmam apenas o que consta nos abstracts.
- `harlow_heidenreich_reece_rudelius_2022`: o campo `pages = 3` parece ser o
  número do fascículo. A entrada não é citada; verificar ou remover (E3).
- A suíte numérica de alta precisão (`mpmath`) não foi reexecutada neste
  ambiente, porque o PyPI estava bloqueado. Rodar `python make.py all`
  localmente (E4).

---

## E1 — Decidir o artigo principal (P0)

**Objetivo:** comparar formalmente `paper/paper.tex` ("Spectral structure…")
com o rascunho *Finite-data certificates for spectral weight in radial
symmetry-breaking profiles* (15/09/2026). **Não fundir os dois
automaticamente.**

**Tarefas**
1. **E1.1** Recuperar o `.tex` do rascunho *Finite-data certificates*. No
   pacote atual só existe o PDF (`base_cientifica/.../paper_draft.pdf`).
   Versioná-lo em `drafts/finite_data/`.
2. **E1.2** Montar `data/manuscript_comparison.csv` com as colunas
   `claim_id, manuscrito, enunciado, tipo (teorema/proposição/observação),
   hipóteses, status de prova, precedente mais próximo, dependências`.
3. **E1.3** Classificar cada claim como **física** (depende do observável) ou
   **matemática** (vale para qualquer transformada de Laplace positiva).
4. **E1.4** Registrar a decisão em `DECISIONS.md`: qual texto é a primeira
   submissão e quais claims vão para o segundo artigo.

**Critério de aceitação:** cada claim dos dois textos aparece exatamente uma
vez na matriz, com o destino decidido (paper 1, paper 2 ou descartado).

**Hipótese de trabalho, a confirmar:** o paper 1 é o físico. Do rascunho, ele
absorve apenas a Proposição 1 (subtrações locais não alteram o perfil
exterior), porque E2 provavelmente precisa dela. O restante (ambiguidade de
amostras finitas, certificados de Bernstein, filtros polinomiais) fica para o
paper 2, mais matemático.

---

## E2 — Positividade ⟹? H3 (P0, núcleo científico)

### E2.0 Enunciado alvo

Seja uma teoria de gauge **abeliana** em 3+1 dimensões, com matéria de carga
**somente elétrica**. Hipóteses:

- **(W)** Axiomas de Wightman para o campo local invariante de gauge F_{μν}:
  positividade, covariância de Lorentz, condição espectral e temperança. No
  lado euclidiano, isso equivale a positividade de reflexão para as funções de
  Schwinger de F (reconstrução de Osterwalder–Schrader).
- **(B)** Identidade de Bianchi como equação de operadores: ∂_{[λ}F_{μν]} = 0,
  isto é, ausência de cargas magnéticas.
- **(L)** Regime de sonda linear: o potencial estático é tomado na ordem
  O(q_W²) na carga da sonda. Isso é exatamente a Hipótese 5 do paper.

> **Proposição P-E2 (conjectura com esboço; NÃO VERIFICADA).** Sob (W), (B) e
> (L), o kernel de resposta estática admite
> 𝒢(Q²) = Z/Q² + ∫_{(0,∞)} dσ(s)/(Q²+s) + P(Q²), com σ ≥ 0 e P um polinômio
> (termos de contato). Portanto, para todo r > 0, Φ(r) é a transformada de
> Laplace de uma medida positiva. O suporte pode começar em s = 0: a
> hipótese de gap (H2) **não** decorre de (W), (B) e (L).

### E2.1 Esboço da prova (a ser escrito com rigor)

1. **Källén–Lehmann para F.** Sob (W), a função de dois pontos de F se
   decompõe em estruturas tensoriais de spin 1 com densidades positivas. O
   que é preciso provar: (B) elimina a estrutura "dual" (ε_{μνρσ}p^ρ…) para
   p² ≠ 0, e sobra ⟨FF⟩(p) = T_{μνρσ}(p) Δ(p²) + contato, com
   Δ(p²) = ∫ ρ(s) ds/(s − p²), ρ ≥ 0 e ρ ⊃ Z δ(s) (o fóton).
2. **Do laço de Wilson para ⟨FF⟩.** Em O(q_W²), log⟨W⟩ é o segundo cumulante
   −(q_W²/2)∮∮⟨AA⟩. Por Stokes, isso é igual a −(q_W²/2)∫_Σ∫_Σ⟨FF⟩, que é
   invariante de gauge para laços fechados e **exige** o caso abeliano. Para
   o laço retangular T×r com T→∞, obtém-se V(r) como transformada de Fourier
   3D de Δ_E(Q²).
3. **Subtrações.** Em QED, ρ(s) → constante no UV (running logarítmico), então
   ∫ρ/(s+μ²) diverge e a relação precisa de subtrações. Os termos
   polinomiais correspondem a derivadas de δ³(r) e **não afetam r > 0**. Esse
   é exatamente o conteúdo da Proposição 1 de *Finite-data certificates*.
4. **Pushforward.** A identidade do núcleo e a Gauss já estão no Teorema 1
   do paper, e dão Φ(r) = ∫e^{−rx}dν com ν ≥ 0.

### E2.2 Onde está a fronteira entre positividade de reflexão e H3

- **Sonda linear, O(q_W²):** se P-E2 valer, a positividade de H3 é um
  **teorema**. O que continua sendo hipótese é o gap H2 e a própria restrição
  à sonda linear.
- **Sonda não linear, O(q_W⁴) em diante** (luz-luz, Wichmann–Kroll): a
  positividade de reflexão do laço completo dá o resultado de Bachas
  (V' ≥ 0, V'' ≤ 0) e a cota de Seiler, mas **não se espera** uma
  representação de Stieltjes. Essa é a pergunta aberta real.
- **Caso não abeliano:** F não é invariante de gauge e o passo 2 falha. O
  resultado não se estende sem trabalho novo.
- **Monopolos (U(1) compacta):** (B) falha e a estrutura dual pode sobreviver.
  Isso é consistente, como **hipótese**, com a violação de positividade
  observada por Loveridge–Oliveira–Silva 2022. Atenção: lá o objeto é o
  propagador em gauge de Landau, não ⟨FF⟩, então a relação ainda precisa ser
  estabelecida.

### E2.3 Tarefas

1. **E2.3a** Escrever `notes/E2_positivity_H3.tex` com a prova completa dos
   passos 1–4. Cada passo deve listar hipóteses, o lema clássico usado (com
   fonte lida) e as condições técnicas: temperança, IR do fóton sem massa,
   domínio de convergência.
2. **E2.3b** Classificar as estruturas tensoriais de ⟨F_{μν}F_{ρσ}⟩ e provar
   que (B) elimina a dual para p² ≠ 0. Cuidado com o ponto p² = 0.
   **Status 22/09/2026:** feito em `notes/E2b_tensor_classification.tex`, com
   verificação em `tests/test_e2_tensor_classification.py`. (B) elimina a dual
   para p² > 0. **Em p² = 0, não elimina:** sobra i·T⋆, que a positividade só
   limita (|α′| ≤ α) e que é removida pela localidade, via CPT. Três lemas
   clássicos ainda estão marcados "to read", e a nota não foi compilada.
3. **E2.3c** **Checagem de consistência a uma ordem:** o ρ de ⟨FF⟩ em O(e²)
   deve reproduzir dσ = g⁴ρ_J ds/s do Apêndice A. Escrever como teste
   simbólico em `tests/test_e2_one_loop.py`.
4. **E2.3d** Modelo de brinquedo: campo de Proca livre, com Δ = 1/(m²−p²).
   Verificar numericamente que Φ(r) passa no gate de Hankel.
5. **E2.3e Busca de anterioridade específica:** a positividade do espectral
   do fóton é clássica (é usada no argumento de Källén para 0 ≤ Z₃ ≤ 1). Ler
   as fontes primárias (Källén, Lehmann; Strocchi sobre campos locais e
   estados carregados) antes de citá-las. **Se P-E2 já estiver na literatura,
   ela vira atribuição, não novidade.**
6. **E2.3f** Tentar um contraexemplo em O(q_W⁴): calcular o sinal da
   contribuição luz-luz ao potencial estático (fontes: literatura sobre
   Wichmann–Kroll, a ler).

**Critérios de aceitação (um dos três):**
- (a) P-E2 provada, com escopo exato. Nesse caso, a Hipótese 3 do paper é
  reescrita como teorema no regime (L), e a H2 fica como hipótese física
  separada.
- (b) Contraexemplo explícito. Nesse caso, o paper declara precisamente
  quais desigualdades a positividade de reflexão fornece.
- (c) Prova parcial, com a lacuna isolada num enunciado técnico único.

**Risco:** alto. **Estimativa:** 3–6 semanas de trabalho focado.

### E2.4 Estado em 23/09/2026 — o que a auditoria fechou e o que não fechou

A auditoria de 23/09 corrigiu enunciados, o filtro numérico e a proveniência
dos certificados. **Nenhuma das obrigações científicas de E2 foi resolvida
por essas correções**, e o relatório não as apresenta como resolvidas.
Registro aqui, no estágio a que pertencem, as seis que continuam abertas:

1. **H3 além da ordem líder.** Derivar H3 para o kernel físico, ou restringir
   o domínio de aplicação com uma hipótese controlada. É E2.3a. A nota E2b
   não conclui essa ponte, e o apêndice agora declara explicitamente que o
   resto O(g_R⁶) não é afirmado positivo.
2. **⟨FF⟩ → laço de Wilson → kernel estático.** Justificar laço de Wilson,
   limite estático, termos de contato e subtrações ao transportar a medida.
   É o passo 2 de E2.1 e o O2 de [D5](DECISIONS.md). **Obrigação prioritária.**
3. **Isolamento de canais carregados.** Demonstrar quando se pode isolar canais
   carregados preservando positividade. O paper já recuou de "limiar carregado"
   para "limiar efetivamente acoplado" em v0.3; o recuo torna a lacuna visível,
   não a fecha.
4. **Erro perturbativo e inferência.** Quantificar o erro de truncamento e
   controlar inferência em dados físicos desconhecidos. Envelopes sintéticos
   determinísticos não são cobertura estatística empírica; `summary.json`
   declara isso no próprio campo `scope`.
5. **Leituras primárias pendentes.** Concluir as leituras antes de elevar
   atribuições, novidade ou os lemas de E2b a verificação bibliográfica
   concluída. Três lemas de E2.3b seguem marcados "to read". É E2.3e.
6. **CI remoto e revisão humana.** Continuam sem execução verificada. O
   workflow existe e nunca rodou; a inspeção visual do PDF foi feita por
   agente, não por revisor humano.

**Fronteira agora explícita (ver [D6](DECISIONS.md)).** A v0.3 deixou de
afirmar que H3 é "estritamente mais forte" que positividade de reflexão. Com
isso, E2.2 deixa de ser clarificação e passa a ser o núcleo: a relação entre
as duas hipóteses é desconhecida **nas duas direções**.

**O que é evidência e o que não é.** O filtro finito de momentos aprova com o
rótulo `CHECKED_COMPATIBLE`, que significa apenas que as condições necessárias
finitas testadas passaram. O contraexemplo δ₁+δ₂+δ₃−10⁻⁶δ₄ passa em ordem 5
e falha em ordem 7: nenhum número de testes finitos aprovados estabelece H3.

### E2.5 Estado em 29/09/2026 — a cadeia de bolhas ficou fechada

Das seis obrigações de E2.4, uma mudou de estado, e só em parte: a obrigação 1
(H3 além da ordem líder) está **resolvida para a cadeia de bolhas ressomada** e
continua aberta para o kernel interagente. As outras cinco seguem como estavam.

**O que ficou demonstrado, dentro do modelo.** Com $\rho_J\ge0$ não nula,
momento inverso finito, $g_R^2>0$ e a forma de Dyson subtraída, frações parciais
dão $W=Z_3+g_R^2\int\rho_J/(s+Q^2)$, e H3 sem constante:

| $Z_3$ | Polo spacelike | Átomo acima do corte | H3 |
|---|---|---|---|
| $>0$ | não | um, peso positivo (se $\rho_J$ não se anula na borda) | vale |
| $=0$ | não | não | falha se a massa total é finita |
| $<0$ | um, resíduo negativo | não | falha |

As demonstrações estão em `notes/H3_RPA_proof_note_2026-09-29.md` (Props. 1–6)
e o enunciado entrou no apêndice A do artigo na v0.4. Não há zeros de $W$ fora
do eixo real (Prop. 6), então a lista de contribuições espectrais é completa, e
duas regras de soma controlam o peso total.

**O que se aprendeu que não era óbvio.** A densidade do contínuo fica positiva
para qualquer acoplamento. Toda a falha em $Z_3<0$ está num polo discreto, e um
teste de positividade feito com momentos do contínuo não a vê. O filtro do
próprio projeto aprova esse caso; é limite de alcance, e o artigo passou a
dizê-lo. Uma segunda lição foi de método: a concordância de $10^{-8}$ que
parecia erro de quadratura era um átomo omitido, e duas rotas numéricas que
concordavam entre si a $5\times10^{-9}$ erravam ambas $2\times10^{-6}$ porque
consumiam a mesma raiz. A forma fechada da integral de borda levou posição e
peso do átomo à precisão de máquina, conferida contra aritmética de 50 dígitos.

**Atribuição.** O átomo não é descoberta do projeto: é o mecanismo de Giacosa e
Wolkanowski (2012), polo na folha física fora do espectro de entrada, resíduo
positivo, regra de soma. O limite $0\le Z_3\le1$ é de Källén. A redução de H3
ao sinal de $Z_3$ para este kernel não apareceu nas fontes pesquisadas, o que
não estabelece novidade; Brown–Weisberger (1979) segue não lido.

**Próximo passo, com critério de aceitação.** A pergunta física continua sendo
o transporte $\langle FF\rangle\to$ laço de Wilson $\to$ kernel estático. Um caso
controlado em que ele possa ser feito explicitamente, antes da versão
interagente:

- *Hipótese a testar:* para um campo livre massivo acoplado linearmente à fonte,
  o coeficiente $O(q_W^2)$ de $\log\langle W\rangle$ reproduz a medida positiva
  de $\langle FF\rangle$ sem termos de contato em $r>0$.
- *Observável:* $V(r)$ obtido do laço retangular $T\times r$, $T\to\infty$,
  comparado com a transformada de Yukawa da medida de $\langle FF\rangle$.
- *Refutação:* um termo em $r>0$ que não venha da medida — um contato que
  sobreviva, ou dependência de $T$ que não cancele com a renormalização de
  perímetro.
- *Aceitação:* igualdade analítica nos dois lados, com cada troca de limite
  justificada, e verificação numérica independente em dois valores de massa.

### E2.6 Estado em 01/10/2026 — o transporte em ordem linear fechou, condicionalmente

O próximo passo de E2.5 foi feito, e em versão mais geral que a planejada: não
só para o campo livre massivo, mas para qualquer ⟨FF⟩ que satisfaça E2b. A
prova está em `notes/E2c_transport_linear_probe.md`, com 24 testes em
`tests/test_e2c_transport.py`.

**O que ficou demonstrado.** Sob W1–W3 para F (sem localidade, sem CPT, sem
F = dA), Bianchi na função de dois pontos euclidiana *incluindo pontos
coincidentes* (B<sub>T</sub>) e sonda linear, o potencial estático do laço de
Wilson e o campo de uma linha estática dependem de ⟨FF⟩ só através de
a⁽³⁾(r) = ∫dμ(s) e^{−√s r}/(4πr), com μ ≥ 0 a medida de Källén–Lehmann de E2b.
Em r > 0 isso é a H3, com g_R² = μ({0}), a menos de um polinômio de contato, e
dá também a relação de resposta linear da H5. Os critérios de aceitação de
E2.5 foram cumpridos: as trocas de limite estão justificadas (Fejér,
Riemann–Lebesgue, Tonelli) e a verificação numérica usa duas massas, mais o
caso de Coulomb puro.

**O que se aprendeu que não era óbvio.**
- O termo helicoidal sem massa, que E2b só remove por CPT, não chega a nenhum
  dos dois observáveis estáticos: a componente do laço plano é zero
  identicamente, e a da linha é proporcional a p₀, que a integral no tempo
  mata. O lema de CPT deixa de ser necessário para este passo.
- O que (B<sub>T</sub>) exclui é a estrutura local G = δδ − δδ, e ela dá lei de
  área: potencial linear. É a função D do modelo do vácuo estocástico
  (Dosch–Simonov), em que D ≠ 0 confina e D₁ só dá perímetro e potencial. Em
  teoria abeliana sem monopolos, Bianchi zera D. Isso está na revisão de
  Di Giacomo, Dosch, Shevchenko e Simonov (2002), lida nas seções 2.1, 3.1,
  3.2 e 4.2; as fontes primárias não foram lidas.
- A taxa de T → ∞ não é log T/T, como eu esperava pela cauda 1/u² de a(u, r).
  É 1/T, com o coeficiente previsto, porque as caudas se cancelam no
  colchete que entra.
- Consequência para a cadeia de bolhas: em Z₃ = 0 a constante 1/μ é um termo
  de contato, δ³ na origem. A H3 literal falha, mas a conclusão do Teorema A
  em r > 0 sobrevive. A única falha física é Z₃ < 0, e o polo tipo espaço é
  um estado taquiônico: violação de W2, coerente com o teorema.

**O que continua aberto.**
1. Os lemas clássicos de E2b, agora só dois mais a continuação
   Wightman → Schwinger: Bochner–Schwartz e a desintegração covariante.
2. As fontes primárias do vácuo estocástico e uma citação de livro para o
   potencial como superposição de Yukawas.
3. O caso temperado geral, sem ∫dμ/(1+s) < ∞.
4. **O(q_W⁴).** A pergunta aberta real agora é aqui: o sinal da contribuição
   luz-luz ao potencial estático (E2.3f). A sonda linear está fechada; a não
   linear não foi tocada.
5. A existência da QED em 4D como teoria de Wightman não é conhecida. O
   resultado é condicional a ela, como qualquer enunciado axiomático.

---

## E3 — Consolidar a contribuição original (P0)

**Objetivo:** uma matriz claim → precedente, lida **no nível de equação**, que
separe a originalidade da *combinação* da originalidade dos *métodos*
(Laplace, Hankel, Padé, GEVP, Lanczos).

**Leituras obrigatórias.** Para cada uma, responder à pergunta indicada.

| Fonte | Pergunta a responder |
|---|---|
| Masjuan–Peris 2010 (0903.0294) | O que extraem exatamente: uma cota ou um ajuste? Com quais hipóteses? |
| Brown–Weisberger 1979 | Há representação espectral do potencial estático? |
| Bachas 1986; Seiler 1978 | Quais derivadas de V são controladas, e sob quais hipóteses? |
| Hinrichs–Polzer 2025 (2511.02867) | A lei de borda Γ = M* + p/r já está lá (Teorema/Corolário nº)? |
| Wagman 2025; Hackett–Wagman 2025 | As cotas bilaterais do Lanczos exigem que hipótese de peso? Isso contradiz ou complementa o Teorema H? |
| Lawrence 2024; Mutzel–Tilloy 2025 | Existe cota inferior certificada de janela finita **sem** hipótese de peso mínimo? Se existir, o Teorema H precisa ser reformulado. |
| Raman 2026 | Quais enunciados do paper são revisão (Eqs. 19–22, 119–120)? |
| Loveridge–Oliveira–Silva 2022 | Como o diagnóstico deles se relaciona com o gate de Hankel? |

**Tarefas**
- **E3.1** Atualizar `data/claims_matrix.csv` com as colunas `equação exata do
  precedente` e `diferença demonstrável`.
- **E3.2** Escrever uma seção curta no paper, "Relation to spectral
  reconstruction methods": uma tabela claim → precedente → diferença.
- **E3.3** Remover toda frase do tipo "no previous work": a busca não está
  saturada, conforme `reports/SEARCH_SATURATION_REPORT.md`.

**Critério de aceitação:** cada claim do paper tem um precedente lido e uma
diferença que pode ser verificada por outra pessoa.

---

## E4 — Robustez numérica e certificação (P1)

**Tarefas**
- **E4.1** Implementar os testes pendentes:
  - **L:** dados sintéticos com ruído controlado;
  - **M:** derivação numérica ruidosa de Φ;
  - **N:** recuperação cega de M* e p a partir das amostras.
- **E4.2** Corrigir `reproducibility/interval_bounds.py`. Perturbações
  aleatórias aprovadas são **teste**, não certificado, e não podem levar o
  rótulo `CERTIFIED`. A verificação deve ser feita em aritmética racional
  exata, como no protótipo de `spectral_weight_certificates.py`.
- **E4.3** Rodar o modelo de faixa dinâmica larga (I) como caso de
  recuperação, e não só como sonda de condicionamento.
- **E4.4** Gerar a segunda figura (convergência da hierarquia B_K com ruído),
  com rótulos em inglês e dados vindos de script.
- **E4.5** Congelar o ambiente: `requirements.in` + `requirements-lock.txt`
  (pip-tools) e rodar o CI pela primeira vez.

**Critério de aceitação:** `python make.py all` passa num clone limpo, e cada
número do texto está coberto por um `assert`.

---

## E5 — Manuscrito final (P1)

- **E5.1** Incorporar E2 (reescrever as Hipóteses 3/5), E3 (seção de trabalhos
  relacionados) e E4 (figuras e robustez).
- **E5.2** Escolher a revista conforme o que foi **efetivamente demonstrado**:
  - E2(a) + observação física → JHEP ou SciPost Physics;
  - E2(c) + nota de montagem → PRD ou SciPost Physics Core;
  - só os certificados → J. Phys. A.
  Verificar as diretrizes vigentes da revista escolhida no dia da escolha.
- **E5.3** Migrar para o template da revista. Hoje o texto usa `article`,
  compatível com a submissão ao arXiv.
- **E5.4** Revisão hostil simulada, lida por alguém que não escreveu o texto.

---

## E6 — Submissão (P1)

- **E6.1 (começar já, em paralelo)** Endosso no arXiv para hep-th/hep-ph.
  Pela política de 21/01/2026, quem não tem autoria prévia na categoria
  precisa de endosso pessoal. Candidatos naturais são pesquisadores com quem
  você já tem contato acadêmico.
- **E6.2** Release do código no Zenodo com DOI, `CITATION.cff` com o autor
  real e a URL pública do repositório.
- **E6.3** Verificação humana de 100% das referências contra a fonte
  primária.
- **E6.4** Declaração de uso de ferramentas de IA, conforme a política da
  revista e do arXiv vigentes na data.
- **E6.5** Checagem de similaridade, cover letter e sugestão de revisores sem
  conflito de interesse.

---

## Registro de versões do PDF

| Versão | Etapa | Data | Conteúdo |
|---|---|---|---|
| v0.2 | E0 | 21/09/2026 | Build limpo, autoria, números e crossover corrigidos, bibliografia saneada, Figura 1 |
| v0.3 | Auditoria | 23/09/2026 | Filtro finito com localizador H₁, contraexemplos novos, enunciados com hipóteses explícitas, teto de uma espécie provado no apêndice, cadeia WGC condicional completa, proveniência 40/28 |
| v0.4 | E2.5 | 29/09/2026 | Cadeia de bolhas ressomada no apêndice A (três regimes de $Z_3$, átomo acima do corte atribuído a Giacosa–Wolkanowski), limitação dos testes de momentos no texto principal, dualidade Stieltjes/Bernstein citada |
| v0.5 | E2.6 | 01/10/2026 | Proposição 7 no apêndice A: transporte ⟨FF⟩ → kernel estático em ordem linear na sonda, condicional aos lemas de E2b; estrutura de lei de área creditada ao vácuo estocástico (Di Giacomo et al. 2002); constante de $Z_3=0$ identificada como termo de contato; 14 páginas; registro de QA gerado de um clone LF e conferido por teste |

O PDF entregue da v0.3 é `output/pdf/spectral_structure_v03.pdf` (12 páginas,
compilado com Tectonic 0.17.0 portátil). Esse diretório é gitignored: o PDF
não está versionado. `make.py pdf` gera `paper/paper.pdf`, que é outro
artefato. Hashes das fontes e do PDF em `output/data/canonical_pdf_qa.json`,
reconferidos de forma independente em 23/09/2026
(`reports/VERIFICATION_CLAUDE_2026-09-23.md`).
