# Nota de demonstração — a obstrução do polo spacelike na cadeia RPA

29 de setembro de 2026. Nota curta. As proposições 1 e 2 são demonstradas
aqui; a dualidade Stieltjes/Bernstein usa referências com o estado de
verificação discriminado na seção 9.
**Escopo: modelo RPA/Dyson.** Não trata do kernel físico definido pelo laço de
Wilson; ver §8 e a discussão no relatório do dia.

---

## 1. Definições

Trabalhamos em $Q^2\in(0,\infty)$ (região spacelike), unidades $m=q=1$,
$\hbar=c=1$.

- **Regulador.** Corte rígido $\Lambda^2<\infty$ no suporte espectral. É
  necessário: $\int^\infty\rho_J(s)/s\,ds$ diverge logaritmicamente para o
  $\rho_J$ de um laço.
- **Medida espectral da matéria.** $\rho_J$ mensurável em $[4,\Lambda^2]$,
  com $\rho_J\ge0$ (positividade de Lehmann da corrente **não gaugeada**).
- **Polarização subtraída.**
  $\overline\Pi(Q^2)=Q^2\int_4^{\Lambda^2}\dfrac{\rho_J(s)\,ds}{s(s+Q^2)}$,
  normalizada por $\overline\Pi(0)=0$.
- **Kernel.** $W(Q^2):=1-g_R^2\overline\Pi(Q^2)$ e
  $\mathcal{G}(Q^2):=\dfrac{g_R^2}{Q^2\,W(Q^2)}$ (equação de Dyson).
- **Constante.** $Z_3:=1-g_R^2\overline\Pi(\infty)$, com
  $\overline\Pi(\infty)=\int_4^{\Lambda^2}\rho_J(s)/s\,ds$.

## 2. Hipóteses

**(P) Positividade.** $\rho_J\ge0$ q.t.p.
**(I) Integrabilidade.** $\int_4^{\Lambda^2}\rho_J(s)/s\,ds<\infty$ é uma
hipótese independente: positividade e corte finito não bastam para uma
densidade mensurável arbitrária. Para a densidade de Dirac aqui utilizada,
ela segue da continuidade e limitação no intervalo compacto.
**(N) Peso não nulo.** $\mu:=\int_4^{\Lambda^2}\rho_J(s)\,ds>0$. Sem ela $W\equiv1$
e tudo é trivial; com ela $W$ é *estritamente* monótona (§4).
**(G) Acoplamento.** $g_R^2>0$, **parâmetro de entrada, sempre positivo**.
Nada abaixo altera o sinal de $g_R^2$.
**(D) Estrutura de Dyson.** $\mathcal{G}=g_R^2/(Q^2W)$ com $\overline\Pi$ dada
pela bolha de matéria. Isto é RPA, não a auto-energia 1PI completa.

## 3. Identidade por frações parciais

Para $s,Q^2>0$:
$$\frac{Q^2}{s(s+Q^2)}=\frac{(s+Q^2)-s}{s(s+Q^2)}=\frac1s-\frac1{s+Q^2}.$$
Integrando contra $\rho_J$, lícito por (I):
$$\overline\Pi(Q^2)=\overline\Pi(\infty)-\int_4^{\Lambda^2}\frac{\rho_J(s)\,ds}{s+Q^2},$$
e portanto
$$\boxed{\;W(Q^2)=Z_3+g_R^2\!\int_4^{\Lambda^2}\frac{\rho_J(s)\,ds}{s+Q^2}\;}\tag{3.1}$$

## 4. Monotonicidade e limites de $W$

Derivando sob o sinal (justificado por (I) e dominação em compactos de
$(0,\infty)$):
$$W'(Q^2)=-g_R^2\!\int_4^{\Lambda^2}\frac{\rho_J(s)\,ds}{(s+Q^2)^2}\;<\;0
\quad\text{por (P), (N), (G).}\tag{4.1}$$
Logo $W$ é **estritamente decrescente** e contínua em $(0,\infty)$.
Dos limites em (3.1), por convergência monótona:
$$W(0^+)=Z_3+g_R^2\overline\Pi(\infty)=1,\qquad W(+\infty)=Z_3.\tag{4.2}$$

## 5. Existência e unicidade do zero

**Proposição 1.** *Sob (P), (I), (N), (G): $W$ tem zero em $(0,\infty)$ se e
somente se $Z_3<0$, e nesse caso o zero $x_*$ é único e simples.*

*Demonstração.* ($\Leftarrow$) Se $Z_3<0$, por (4.2) $W(0^+)=1>0>Z_3=W(\infty)$;
$W$ é contínua, logo pelo teorema do valor intermediário existe $x_*>0$ com
$W(x_*)=0$. ($\Rightarrow$) Se $Z_3\ge0$, então por (3.1) $W(Q^2)\ge Z_3\ge0$ com
a integral estritamente positiva por (N), logo $W>0$ em todo $(0,\infty)$: não há
zero. **Unicidade:** $W$ é estritamente decrescente por (4.1), logo injetora.
**Simplicidade:** $W'(x_*)<0\neq0$ por (4.1). $\blacksquare$

## 6. Resíduo do polo

**Proposição 2.** *Se $Z_3<0$, $\mathcal{G}$ tem polo simples em $x_*$ com*
$$\operatorname{Res}_{x=x_*}\mathcal{G}(x)=\frac{g_R^2}{x_*\,W'(x_*)}\;<\;0.\tag{6.1}$$

*Demonstração.* Perto de $x_*$, $W(x)=W'(x_*)(x-x_*)+O((x-x_*)^2)$ com
$W'(x_*)\neq0$ (Prop. 1). Então
$\mathcal{G}(x)=g_R^2/[x\,W(x)]$ tem polo simples e
$\operatorname{Res}=\lim_{x\to x_*}(x-x_*)\mathcal{G}(x)=g_R^2/[x_*W'(x_*)]$.
O sinal: $g_R^2>0$ por (G), $x_*>0$, $W'(x_*)<0$ por (4.1). $\blacksquare$

**Verificação numérica** (`ghost_analysis.py`, $\Lambda^2=10^6$,
$g_R^2/g_c^2=1{,}5$): $x_*=1{,}7732\times10^{4}$,
$W'(x_*)=-6{,}8393\times10^{-6}$, fórmula $=-1{,}205768\times10^{2}$,
limite numérico $(x-x_*)\mathcal{G}\to-1{,}205768\times10^{2}$;
concordância relativa $4{,}6\times10^{-9}$.

## 7. Classificação nos três regimes

A H3 do artigo pede
$\mathcal{G}(Q^2)=Z/Q^2+\int_0^\infty d\sigma(s)/(Q^2+s)$ com $\sigma\ge0$ e
**sem termo constante**, o que implica $\mathcal{G}(Q^2)\to0$ quando
$Q^2\to\infty$.

**(a) $Z_3>0$.** Por (3.1) e (N), $W\ge Z_3>0$, logo
$0<\mathcal{G}(Q^2)\le g_R^2/(Q^2Z_3)\to0$. Além disso $W/g_R^2$ é da forma
$b+\int d\sigma/(Q^2+s)$ com $b=Z_3/g_R^2\ge0$ e $d\sigma=\rho_J\,ds\ge0$: é
Stieltjes. Por **SSV Teor. 7.3** ($f\not\equiv0$ Stieltjes $\iff$ $zf(z)$ é
Bernstein completa $\iff$ $1/f$ é Bernstein completa), $Q^2W/g_R^2=1/\mathcal{G}$
é CBF e portanto $\mathcal{G}$ é Stieltjes.

**Pertencer à classe de Stieltjes ainda não é a H3 do artigo.** A H3 canônica
é a forma específica
$$\mathcal{G}(Q^2)=\frac{Z}{Q^2}+\int_0^\infty\frac{d\sigma(s)}{Q^2+s},
\qquad Z>0,\ \ \sigma\ge0,\ \ \operatorname{supp}\sigma\subset[0,\infty),\ \
\int\frac{d\sigma(s)}{\mu_0^2+s}<\infty,$$
e identificar uma com a outra exige quatro verificações que a classe **não**
fornece. Enuncio-as e registro o status de cada uma.

**Proposição 3.** *Sob (P), (I), (N), (G), (D) e $Z_3>0$, a representação do
modelo coincide com a forma canônica acima, com:*

| Condição | Status |
|---|---|
| **(a1) Polo de Coulomb com resíduo positivo.** $\lim_{Q^2\to0}Q^2\mathcal{G}=g_R^2>0$, pois $W(0)=1$ por (4.2). | **demonstrada** (4.2) + (G); confirmada numericamente a 10 casas |
| **(a2) Suporte em $[0,\infty)$.** $\sigma$ tem suporte em $[4m^2,\Lambda^2]\subset(0,\infty)$, pois $\rho_J\equiv0$ abaixo do limiar. | **demonstrada** por construção de $\rho_J$ |
| **(a3) Ausência de termo constante.** $\mathcal{G}\le g_R^2/(Q^2Z_3)\to0$. | **demonstrada** acima |
| **(a4) Momento inverso finito.** $\int d\sigma/(\mu_0^2+s)<\infty$. | **verificada numericamente**, não demonstrada em geral — ver abaixo |

*Sobre (a4).* Para o $\rho_J$ de um laço a densidade do contínuo é
$d\sigma/ds=g_R^4\rho_J(s)/(s|W(-s-i0)|^2)$ (§6 do relatório do dia). Com
$\rho_J$ limitada e $|W|^2$ limitada inferiormente por uma constante positiva no
intervalo compacto $[4m^2,\Lambda^2]$, o integrando é $O(1/s^2)$ e a integral
converge. **Isto é argumento para a densidade concreta com corte finito, não
para $\rho_J$ mensurável arbitrária**; para o caso geral (a4) permanece
hipótese, e é exatamente a hipótese (I) da §2 transportada para $\sigma$.

**Verificação numérica das quatro** ($\Lambda^2=10^6$, $g_R^2/g_c^2=0{,}5$,
$Z_3=0{,}5$):

- (a1) $Q^2\mathcal{G}\to4{,}8743425248=g_R^2$ (concordância em 10 casas
  decimais em $Q^2=10^{-10}$), positivo.
- (a2) $\rho_J(2)=\rho_J(3{,}9)=0$ exatamente.
- (a3) e a decomposição: $\mathcal{G}-g_R^2/Q^2$ contra
  $\int d\sigma/(Q^2+s)$ dá diferença relativa $1{,}7\times10^{-8}$ em $Q^2=1$,
  $2{,}8\times10^{-8}$ em $Q^2=10$, $9{,}2\times10^{-8}$ em $Q^2=100$
  — limitado pela quadratura, não por discrepância estrutural.
- (a4) $\int d\sigma/(\mu_0^2+s)=3{,}66\times10^{-2}$ para $\mu_0^2=1$ e
  $2{,}98\times10^{-2}$ para $\mu_0^2=4$, ambos finitos.

**Conclusão de (a):** com (a1)–(a3) demonstradas e (a4) demonstrada para a
densidade concreta, **a representação de Stieltjes sem constante do modelo RPA
vale**, e ela tem a forma canônica de H3 com $Z=g_R^2$. Isto é um enunciado
sobre o modelo RPA; **não** é H3 para o kernel físico do laço de Wilson.

**(b) $Z_3=0$.** Não há polo (Prop. 1). Mas (3.1) dá
$$\mathcal{G}(Q^2)=\Bigl[\int_4^{\Lambda^2}\frac{Q^2}{s+Q^2}\rho_J(s)\,ds\Bigr]^{-1}
\;\xrightarrow[Q^2\to\infty]{}\;\frac{1}{\mu},$$
por convergência monótona ($Q^2/(s+Q^2)\uparrow1$). **Sob corte finito $\mu<\infty$
por (N)+(I), então o limite é estritamente positivo e H3 FALHA** — o objeto está
na classe geral de Stieltjes, com constante $1/\mu$, mas não na H3 sem constante.
*A ausência de polo não é suficiente.* (Se $\mu=\infty$, o limite é $0$ e H3 vale;
isso requer abandonar o corte. Para a densidade de Dirac deste modelo a
integral inversa diverge nesse limite a acoplamento fixo, invalidando (I).
Isso não se aplica a toda medida positiva de massa infinita: por exemplo,
$\rho(s)=s^{-1/2}$ em $[1,\infty)$ tem massa infinita e integral inversa finita.)

**(c) $Z_3<0$.** Prop. 1 e 2 dão polo simples em $x_*\in(0,\infty)$ com resíduo
negativo. Uma função de Stieltjes é analítica em $\mathbb{C}\setminus(-\infty,0]$;
um polo em $Q^2=x_*>0$ é incompatível. **H3 falha**, e falha já na classe geral.

| Regime | Polo | Classe geral | H3 (sem constante) |
|---|---|---|---|
| $Z_3>0$ | não | sim | **vale** |
| $Z_3=0$ | não | sim (constante $1/\mu$) | **falha** se $\mu<\infty$ |
| $Z_3<0$ | sim, resíduo $<0$ | não | **falha** |

## 8. Contatos e suporte

A H3 do artigo é **não subtraída** e sem polinômio. A P-E2 do roadmap admite
$P(Q^2)$ — termos de contato, que em posição são derivadas de $\delta^3(\mathbf r)$
e **não afetam $r>0$**. As duas coisas não se confundem:

- A **constante** que aparece em (b) é o termo $P(Q^2)=\text{const}$ de grau zero.
  Em três dimensões espaciais é um contato na origem. É legítimo estudar a
  resposta em $r>0$ após removê-lo — **desde que a escolha seja enunciada**.
  A H3 do artigo já é escrita sem esse termo e não foi modificada.
- A **subtração de $\overline\Pi$** (§1, $\overline\Pi(0)=0$) é outra coisa: é a
  renormalização do acoplamento, não a constante de $\mathcal{G}$. Confundir as
  duas é erro fácil; registrado em `DECISIONS.md`, O3.
- **Suporte.** H3 exige $\sigma$ suportada em $s\ge0$. O polo de (c) corresponde
  formalmente a $s=-x_*<0$: fora do suporte admissível, e com peso negativo.
  São duas violações independentes do mesmo objeto.

## 9. Fontes conferidas e o que permanece pendente

- **SSV Teor. 7.3 e 6.2** (Schilling–Song–Vondraček, *Bernstein Functions*,
  2ª ed.): enunciados conferidos em fonte secundária citando numeração.
  Ressalva $f\not\equiv0$ satisfeita, pois $W(0)=1$.
- **Källén 1952** e o limite $0\le Z_3\le1$: clássico. A relação com a presente
  construção é **analogia de conteúdo, não demonstrada aqui**.
- **Raman 2026** (`arxiv:2603.28454v1`): contém a propriedade de Stieltjes de
  $-\Pi/Q^2$; **não** contém o objeto ressomado, $Z_3$, polo de Landau nem
  potencial estático. Leitura dirigida feita.
- **Brown–Weisberger 1979**: **NÃO LIDO** (paywall). Se enunciam representação
  espectral de $V(r)$ equivalente, a atribuição muda. Item de auditoria aberto.
- **Atribuição desta nota:** pendente. "Não encontrei nas fontes pesquisadas"
  **não é prova de novidade** e não deve ser usado como tal.

## 10. Validação condicional do kernel implementada

Implementação em `reproducibility/rpa_kernel_conditions.py`, separada de
`moment_conditions.py`. O contrato dos quatro consumidores do filtro de
momentos permanece o mesmo. A análise Dirac chama a implementação através
de `ghost_analysis.kernel_diagnostic`; os testes chamam o código de produção.

O `moment_gate` deve manter o significado atual: *compatibilidade dos momentos
fornecidos*, nada mais. A etapa **separada** trata as hipóteses e
singularidades do modelo RPA. Compatibilidade dos momentos é um resultado
independente; não é inferida do sinal de Z3:

| Veredicto | Condição |
|---|---|
| `CONTINUUM_MOMENTS_COMPATIBLE` | momentos do contínuo passam no gate |
| `SPACELIKE_POLE_DETECTED` | existência de polo inferida do sinal negativo de Z3 sob as hipóteses; posição não calculada pelo classificador |
| `NO_SPACELIKE_POLE` | sinal positivo de Z3; ou identidade crítica exata com massa infinita |
| `BOUNDARY_CONSTANT_FAILURE` | $Z_3=0$ e $\mu<\infty$ |
| `UNRESOLVED` | precisão insuficiente ou hipótese não verificada |

**Disciplina obrigatória, na mesma linha do `UNRESOLVED_RANK_OR_PRECISION` já
existente:** se um intervalo numérico para $Z_3$ **contiver zero**, o resultado
é `UNRESOLVED` — não se decide o sinal por ponto flutuante. E uma malha
spacelike finita é conferência auxiliar: **não certifica ausência global de
polos**. A garantia de ausência vem da Prop. 1 (monotonicidade), não da malha.

A exceção à recusa de intervalos contendo zero é uma identidade crítica
independente e exata, indicada por `exact_critical=True`, intervalo `[0,0]`
e `interval_kind="exact"`. Uma estimativa numericamente igual a zero não
autoriza essa exceção. Massa finita, infinita ou desconhecida é declarada
separadamente. Todas as hipóteses são afirmações explícitas do chamador;
o classificador não as demonstra e recusa decidir se alguma estiver ausente.

O diagnóstico Dirac propaga o erro estimado de quadratura sem promovê-lo a
intervalo rigoroso. O resultado é `CHECKED_CONDITIONAL`, nunca `CERTIFIED`.
O teste que antes continha `_verdict_from_interval` foi substituído por
chamadas à implementação real.
