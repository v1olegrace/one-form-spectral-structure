# Changelog do manuscrito (`paper/paper.tex`)

## v0.5.8 — 2026-10-24 — O termo O(α⁵) do coeficiente de três fótons

Registro em `.agent/reports/R8.md`; nota E4, §11. As previsões foram
registradas antes de calcular.

- **O termo O(α⁵).** Abaixo de 4m², o corte de três fótons em O(α⁵) é a
  interferência dos vértices de um e de dois loops. Na ordem dominante em s,
  ele é fixado pelos coeficientes de Euler–Heisenberg de dois loops de
  Ritus: 40/9 e 1315/252, em unidades de α/π. Eles foram lidos em Dunne
  (hep-th/0406216, eq. (4.11)) e em Ravndal. A forma fechada autodual
  (Dunne eqs. (6.2) e (6.6)) os confirma, pois dá 25/4 para 4c₁ − c₂.
- **Fator do coeficiente dominante:** 1 + (1555/153)α/π, isto é, +2,36%. A
  densidade pondera os invariantes como 5(a−b)² + 3(a+b)².
- **Para γγ→γγ, o fator é 1 + (25555/2502)α/π.** O fator 186685/17514 de
  Dicus–Kao–Repko (nota [10]) é a mesma expressão com um sinal trocado. Ele
  era a base da estimativa anterior de 0,015/m.
- **Raios.** O parágrafo "The first threshold need not be charged" passa a
  dar r_Γ ≈ 20,64/m e r_× ≈ 22,55/m, com o fator incluído; os dois raios
  entram 0,013/m. As demais ordens em α são estimadas em cerca de 0,003/m,
  somando linearmente as linhas da nota E4, §11.5, sem cota.
- **Bibliografia.** Nova referência `dunne_2004`, com metadados obtidos por
  API e registrados no harvester. O gerador deixa de escapar `_` no campo
  `doi`, porque o estilo compõe o DOI como URL e o `\_` aparecia literalmente.
- **Envoltória do truncamento** (R9; nota E4, §12).
  - *A cota.* É analítica e avaliada em float64; cada constante foi
    conferida no código.
  - *Os dados.* Os produtos até a ordem 22 reproduzem a série a 2×10⁻¹⁵.
  - *O resultado.* A cota limita o truncamento espectral para s ≤ 1,5m².
    Acima disso, uma hipótese de fator 2 cobre 0,04% de Φ₃γ. Juntas, as duas
    partes mudam os raios em menos de 3×10⁻⁴/m. O texto do artigo substitui
    "the spectral remainder is not uniformly bounded".
- **Confirmação independente** (Abdul Hameed–Chaubey–Shao, arXiv:2604.00099,
  nova referência `abdulhameed_chaubey_shao_2026`). O nosso box coincide com a
  expansão de baixa energia publicada deles de ω⁴ a ω¹⁴, a 4×10⁻¹⁶. As
  amplitudes de dois loops deles dão exatamente 25/4 e 1955/396, os
  coeficientes de Ritus nas combinações que usamos. O artigo ganha uma frase
  com essa citação. Com isso, o fator 2 em ω⁸ e o sinal trocado na nota [10]
  são de DKR.
- **Referências só no arXiv.** O estilo (`physofall.bst`) não imprimia o
  identificador arXiv nem o DOI de entradas `@misc`. Seis referências do
  artigo (Pobylitsa, Raman, Lawrence, Mutzel–Tilloy, Hinrichs–Polzer e Abdul
  Hameed et al.) saíam sem como serem encontradas; agora mostram
  `arXiv:NNNN.NNNNN`.
- **DKR em ω⁸.** As lagrangianas efetivas deles, eqs. (13)–(15), dão
  exatamente as nossas amplitudes ω⁴ e ω⁶ e o dobro da ω⁸. A seção de choque
  completa deles apoia o nosso valor. Se o fator é deles, entrou na expansão
  ω⁸ antes da Tabela II e da eq. (15), e a citação de 2025 (Heinzl et al.,
  L₄,₄) o repete (CHECKED, não estabelecido).

## v0.5.7 — 2026-10-23 — Fechamento local e alcance do erro E4

- Os raios E4 são resultados do modelo de seis termos até s^9, com corte em
  4m². Três avaliações da amplitude completa não limitam o resto num intervalo;
  0,002/m é uma estimativa sob uma hipótese adicional, não uma cota verificada.
- A expansão nova usa float64/complex128; a reconstrução racional de c1/c0 e
  seis razões sucessivas não demonstram uma fração exata nem raio de convergência.
- Comparador do CI recusa infinitos/NaN e aplica oito passos binary64 de fato.
- Guardas de domínio para os momentos de sondas e caderno integrado aos 60 itens.

## v0.5.6 — 2026-10-23 — Estudo numérico do erro da janela E4

Resposta à revisão `reports/NEXT_STEPS_E4_REVIEW_2026-10-23.md`. Registros
em `.agent/reports/R4.md` e `R5.md`; as previsões foram registradas antes de
calcular.

- **Amplitude completa de um loop γ*→3γ** (nota E4, §10; novo módulo
  `reproducibility/three_photon_amplitude.py`). Os parâmetros de Feynman somam
  as seis ordenações, e os traços de Dirac são calculados uma única vez.
  Checagens:
  - identidade de Ward em todas as pernas, inclusive a virtual;
  - simetria de Bose;
  - limite EH com normalização absoluta $-2/15$, que não é entrada do
    cálculo;
  - amplitudes on-shell de Dicus–Kao–Repko em $\omega^4$ e $\omega^6$,
    exatas;
  - seção de choque completa contra a Tabela III deles, dentro de 0,5% em
    sete energias.

  A coluna $\omega^8$ deles é o dobro da nossa, e a própria seção de choque
  completa deles apoia o nosso valor (CHECKED).
- **Densidade de três fótons além de $s^4$.** Série em $s/4m^2$ com
  coeficientes 1,877 ($c_1/c_0=335/714$), 2,457, 2,793, 2,960, 3,018. A
  amplitude não expandida em $s=1,2,3$ confirma a série com sua cauda.
- **Par em $O(\alpha^2)$.** Usa a densidade de dois loops de
  Laporta–Jentschura, eq. (55). Não se soma um fator de Sommerfeld separado.
- **Dois raios no artigo.** O parágrafo "The first threshold need not be
  charged" agora separa os dois critérios:
  - $\Gamma\ge2m$ até $r_\Gamma\approx20{,}65/m$;
  - o par domina o perfil até $r_\times\approx22{,}57/m$;
  - entre os dois, o par ainda domina $\Phi$, mas $\Gamma<2m$.

  O texto também declara que $\nu$ é a densidade 1PI na ordem adotada, e que
  a forma $s^4$ é assintótica em $r$ grande. As ordens superiores em $\alpha$
  são estimadas em $0{,}015/m$, sem cota.
- **Sondas.** Com o fator exterior completo, uma bola de raio $10/m$ desloca
  os raios em cerca de $8/m$. Para carga $e$, a cauda EH da própria sonda
  fecha a janela perto de $11{,}6/m$. A cauda de três fótons vem antes só
  abaixo de $q\approx10^{-4}e$.
- **RPA.** A imagem do "átomo que escapa" fica restrita ao corte duro com
  borda positiva. Com suporte ilimitado, como $\eta=e^{-s}ds$, a massa escapa
  por uma ressonância embutida no contínuo (CHECKED).
- **Novas referências:** Laporta–Jentschura (2024).
- **Versão:** v0.5.6.

## v0.5.5 — 2026-10-23 — Correções da revisão independente e a janela QED do limiar

Uma revisão independente da entrega da v0.5.4, feita por outro agente
(`reports/INDEPENDENT_REVIEW_CLAUDE_2026-10-23.md`), encontrou os problemas
corrigidos abaixo. Registros: `.agent/reports/R0.md`, `R1.md` e `R2.md`.

- **Dois números errados na quinta casa.** São CHECKED, não aparecem no
  artigo, estão na nota E3 e nos testes.
  - $\Gamma_{\rm Gauss}(300/m)$: era $2{,}00755$, o correto é $2{,}00752$.
  - $\Gamma_{\rm bola}(50/m)$: era $2{,}03646$, o correto é $2{,}03647$.
  - **Causa:** o `mp.quad` para quando a estimativa de erro fica abaixo de
    um limiar *absoluto*. Integrandos da ordem de $e^{-200}$ eram integrados
    no nível mais grosso, de forma estável e errada.
  - **Correção:** os integrandos são divididos por uma cota a priori, e uma
    guarda recusa erro relativo grande.
  - Os três raios de cruzamento e $\Gamma(50/m)=0{,}932$ da gaussiana não
    mudaram.
- **Sondas finitas.**
  - O artigo agora declara $\rho\ge0$; sem isso $F\ge1$ falha. Uma
    densidade com sinal e carga total 1 tem $F(4)=-1{,}258$.
  - A frase da v0.5.4 "as cotas exigem suporte compacto" superestimava.
    Suporte compacto com $\rho\ge0$ é condição suficiente; não se afirma que
    seja necessária.
  - O molificador da linha é declarado não negativo.
  - O perfil $(1-u^2/a^2)^2$ é $C^1$, não suave.
- **Caso crítico $Z_3=0$.**
  - A afirmação de que $\mathcal G-1/\mu$ é Stieltjes positiva não tinha
    prova. Agora tem: Proposição 3b da nota RPA, por um limite de
    acoplamentos subcríticos. A massa que escapa para o infinito vira a
    constante. É CHECKED em $\eta=1_{[4,10]}$.
  - O apêndice ganha uma frase. O Teorema 2.2 de Schilling–Song–Vondraček,
    lido com prova na prévia da editora, é citado só para comparação.
- **Novo: a janela QED do limiar de pares** (nota E4; parágrafo "The first
  threshold need not be charged").
  - O corte de três fótons acrescenta
    $d\nu=\frac{17}{11\,664\,000}(\alpha/\pi)^4s^4/m^8\,ds$ para $s\ll m^2$.
  - Duas rotas concordam exatamente: o corte de três corpos a partir do
    vértice de Euler–Heisenberg, e o resultado de QCD de Groote–Pivovarov
    com o mapa abeliano. O mapa leva um fator 16, porque a fonte se acopla às
    quatro pernas.
  - Para o coeficiente linear, $\Gamma\ge2m$ só até $r\approx20{,}7/m$
    (CHECKED).
  - Nova referência: Groote–Pivovarov (2001).
- **Versão:** v0.5.5.

## v0.5.4 — 2026-10-23 — Sondas finitas, créditos lidos e a linha por correntes conservadas

Continuação do plano P0–P14 do Codex (`.agent/plan.yaml`), interrompido por
limite de uso; relatórios em `.agent/reports/`.

- **Sondas finitas (novo parágrafo em "Scope and failure modes").**
  - Fora de uma sonda radial de suporte compacto, o perfil é a transformada
    de Laplace de $F\nu$, com $1\le F\le\sinh(xa)/(xa)$. A borda e os
    teoremas C e E valem em $r>a$ (nota E3, §11.1).
  - Para uma nuvem gaussiana de largura $10/m$, a cauda da própria sonda
    domina e $\Gamma(50/m)=0{,}932\,m<2m$ (CHECKED, duas rotas independentes).
    As cotas exigem suporte compacto.
- **Proposição 7.** O campo da linha estática passa a ser definido como
  limite ordenado de correntes conservadas suaves (nota E2c, §12). A prova
  dizia que o regulador tornava $\delta(p_0)/(p_1-i0)$ bem definido; isso
  não se sustenta, porque o núcleo em momento mantém a singularidade de
  Coulomb.
- **Cadeia de bolhas.**
  - $\mathcal G$ Stieltjes para $Z_3>0$ agora tem prova direta, por
    aproximação atômica positiva e truncamento, sem depender do enunciado do
    SSV, que não foi lido no nível de teorema.
  - O átomo acima do corte exige limite positivo na borda, com
    contraexemplo exato.
  - Lacunas internas podem ter átomos.
  - A falha em ordem fixa recebe o crédito de Masjuan–Peris.
- **Créditos lidos no nível de equação.**
  - Benedetti–Casini–Magán (JHEP06(2023)095, §3): a forma de
    Källén–Lehmann de $\langle FF\rangle$ e a exclusão do termo de cone de
    luz.
  - Masjuan–Peris (eqs. 12–14): o determinante de Hankel como falsificador.
- **Discussão.** A extensão Euler–Heisenberg casada para sondas compactas
  e a cota de energia para fontes arbitrárias.

Não mudou: os teoremas A, C, E e H e as hipóteses H1–H5.

PDF: 16 páginas; registro estrutural PASS (`output/data/canonical_pdf_qa.json`),
sem avisos de LaTeX. Suíte: 469 testes no snapshot candidato. São 466
na árvore de trabalho, onde três arquivos novos ainda não são rastreados e o
teste de higiene roda por arquivo rastreado.

## v0.5.3 — 2026-10-05 — Alcance da sonda e Bianchi a tempos iguais

- O produto ordenado precisa de localidade a tempos iguais e prescrição de
  contatos compatível; $F=dA$ sozinho não garante essa premissa.
- A subtração das energias isoladas continua independente de r. Interações
  mistas podem depender da separação e da forma da fonte; a ponte usada
  no artigo é de resposta linear.
- A discussão distingue os sinais dos setores EH calculados do sinal de
  um cumulante geral; bolas/cascas são benchmarks do termo local.
- QA compara o inventário completo de fontes atuais, normalizando só CRLF
  para LF; o teste de hash funciona sem PyMuPDF.

PDF: 15 páginas; registro estrutural PASS. Os 397 testes passaram sem
omissões; numerics, audit, certified, reintegração Arb e duas execuções de
bib passaram. Relatório: `reports/CONCLUSAO_CLAUDE_2026-10-05.md`.

## v0.5.2 — 2026-10-03 — Revisão: o s* da Proposição 7 e a bibliografia conferida

Revisão adversarial da v0.5.1, no mesmo dia. O PDF canônico e o registro em
`output/data/canonical_pdf_qa.json` foram refeitos para a v0.5.2.

- **Proposição 7 e o s\*.** A v0.5.1 dizia que o resultado é a Hipótese 3
  "com $s_*=\inf\operatorname{supp}\sigma$, que pode ser zero". No artigo,
  porém, $s_*$ nasce na Hipótese 2 já positivo. Agora a proposição diz que,
  com peso de Coulomb, o kernel tem a *forma* da Hipótese 3, com a integral
  começando em $\inf\operatorname{supp}\sigma$, e que esse limite ser positivo
  é o gap da Hipótese 2, que não decorre dela. O parágrafo depois das
  hipóteses diz o mesmo.
- **Bibliografia.** `make.py bib` agora confere, sem rede, que cada valor do
  harvest é o que a API citada na procedência devolve, ou uma correção à mão
  cuja nota cita o valor. Refazê-lo achou dois erros: Banks–Seiberg estava
  impresso com o ano do preprint (2010) em vez do ano da revista (2011, Phys.
  Rev. D 83, 084019), e uma entrada não citada tinha página "3" em vez do
  número de artigo 035003. Os títulos de Hackett–Wagman e de Lawrence e o
  formato de autor de Hinrichs–Polzer passam a ser os valores que as APIs
  devolvem; a forma anterior não vinha de nenhuma API.

Não mudou: o conteúdo matemático da Proposição 7, os teoremas A, C, E e H. O
artigo continua com 15 páginas.

## v0.5.1 — 2026-10-03 — A Proposição 7 com o enunciado que ela sustenta

Correções da auditoria de E2c de 2 de outubro
(`reports/AUDITORIA_SEVERA_E2C_2026-10-02.md`). Cada achado foi reproduzido
por conta antes de entrar no texto. O PDF canônico e o registro em
`output/data/canonical_pdf_qa.json` foram refeitos para a v0.5.1.

- **A representação euclidiana virou premissa.** A Proposição 7 já supunha a
  forma $S=T^E[\int d\mu/(p^2+s)+q]$ com $\mu\ge0$; o texto em volta dizia que
  ela saía dos axiomas de Wightman. Agora o apêndice diz que essa passagem usa
  dois lemas e a continuação para a assinatura euclidiana, nenhum conferido, e
  que por isso a forma é suposta.
- **O que sai é um kernel de Stieltjes positivo.** É a Hipótese 3 só com peso
  de Coulomb $\mu(\{0\})>0$; $s_*=\inf\operatorname{supp}\sigma$ pode ser zero,
  e o gap da Hipótese 2 é outra entrada. Isso está no enunciado da proposição,
  no parágrafo depois das hipóteses e no item da introdução.
- **Lei de área.** O contato local que viola Bianchi dá um termo de área com
  coeficiente proporcional a $1/\varepsilon$: contato regulado, não tensão de
  corda finita. A comparação com a função $D$ do vácuo estocástico passou a
  ser declarada como comparação de estrutura tensorial.
- **Cumulantes.** "Ordem linear" é truncamento no cumulante quadrático. O
  cúbico só some com conjugação de carga; o de quatro campos entra em
  $O(q_W^4)$, e chamá-lo de luz-luz é afirmação sobre a dinâmica. Discussão e
  observação final ajustadas.
- **Esboço da prova.** Diz que $T\to\infty$ vem antes de remover o regulador,
  que a correção em $1/T$ tem coeficiente divergente quando o regulador sai, e
  que o produto $\delta(p_0)/(p_1-i0)$ da linha só está justificado com
  regulador.

Fora do artigo, na nota E2c: o fator 2 sobrando na fórmula de contorno do
Lema 2 (o código estava certo) e a expansão exata do coeficiente da taxa para
a medida de Coulomb. Quatro testes novos em E2c, e um caso a mais no teste de higiene de texto para o relatório da auditoria; o total vai a 357.

Não mudou: o resultado da Proposição 7 sob as suas hipóteses, os teoremas A,
C, E e H, e a cadeia de bolhas. O artigo passa de 14 para 15 páginas.

## Revisão local da v0.5 — 2026-10-02 — Auditoria adversarial

Rodada ainda não publicada. O registro de correções e verificações desta
rodada não foi entregue naquela data. A conclusão atual está em
`reports/CONCLUSAO_CLAUDE_2026-10-05.md`; os números e afirmações
da entrada histórica abaixo não substituem esse registro. A auditoria exige
separar o resultado sob uma representação euclidiana assumida da derivação
dessa representação a partir de axiomas de Wightman, e distinguir o contato
de área divergente de uma tensão física finita.

O controle do PDF agora compara o registro de QA com as fontes do diretório
de trabalho, normalizando somente CRLF para LF. Assim, uma alteração local
é detectada antes de commit; comparar apenas com `HEAD` deixava esse caso
passar. Um teste verifica que diferenças de conteúdo e CR isolado continuam
sendo detectadas.

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
