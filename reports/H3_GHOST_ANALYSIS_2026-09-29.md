# O polo spacelike como obstrução a H3 na cadeia de Dyson

*(Obstrução necessária, não equivalente: ver a fronteira $Z_3=0$, §9.)*

29 de setembro de 2026. Análise dentro da estrutura RPA/Dyson.
**Não é prova de H3 para a resposta estática não perturbativa e invariante de
gauge.** O teto do que aqui se estabelece está enunciado na seção 9.

Código, testes e figuras: `reports/h3_ghost_2026-09-29/`.

---

## 1. Reformulação matemática precisa

O artigo escreve H3 como: existe medida σ ≥ 0 tal que

$$\mathcal{G}(Q^2)=\frac{Z}{Q^2}+\int_0^\infty\frac{d\sigma(s)}{Q^2+s},
\qquad \int\frac{d\sigma(s)}{\mu_0^2+s}<\infty,$$

**sem termo constante**. Nas convenções do apêndice,

$$\mathcal{G}(Q^2)=\frac{g_R^2}{Q^2\bigl[1-g_R^2\overline{\Pi}(Q^2)\bigr]},
\qquad
\overline{\Pi}(Q^2)=Q^2\!\int_{4m^2}^{\Lambda^2}\!\frac{\rho_J(s)\,ds}{s(s+Q^2)} .$$

Definindo $W(Q^2):=1-g_R^2\overline{\Pi}(Q^2)$, o problema é:

> **Para quais $(\rho_J,g_R^2,\Lambda)$ a função $\mathcal{G}=g_R^2/(Q^2W)$
> pertence à classe de Stieltjes?**

Duas classes, e a distinção é o eixo de todo o trabalho: a classe **geral**
de Stieltjes admite uma constante aditiva; a **H3 do artigo** não. Elas
coincidem em $Z_3>0$ e divergem exatamente na fronteira $Z_3=0$. O quadro
dos três regimes está na §9 e é o enunciado que vale.

Reformulação equivalente pela dualidade de Schilling–Song–Vondraček (numeração
não conferida no livro; o conteúdo é:
$f\not\equiv0$ é Stieltjes $\iff$ $1/f$ é Bernstein completa $\iff$ $zf(z)$ é
Bernstein completa): basta decidir se $W$ é Stieltjes.

## 2. Suposições, numeradas

1. $\rho_J\ge0$ — positividade de Lehmann da corrente de matéria **não
   gaugeada**. Métrica positiva, sem o problema de gauge covariante.
2. Uma subtração basta para $\Pi$ (log-divergência de QED). É o que o apêndice
   já assume.
3. Estrutura de Dyson $\mathcal{G}=g_R^2/(Q^2W)$ com $\overline\Pi$ dado pela
   bolha de matéria — isto é RPA, **não** a auto-energia 1PI completa.
4. Regulador: corte rígido em $s=\Lambda^2$. Necessário porque
   $\int^\infty\rho_J/s\,ds$ diverge logaritmicamente.
5. Unidades $m=q=1$, $\hbar=c=1$. Densidade de um laço
   $\rho_J=\frac{1}{12\pi^2}(1+2/s)\sqrt{1-4/s}$, $s\ge4$.
6. **Varro o acoplamento a corte fixo**, não o corte a acoplamento fixo. O
   critério depende só do produto $g_R^2\overline\Pi(\infty)$, e isso mantém a
   quadratura bem condicionada. O polo de Landau físico de QED exige
   $\Lambda\sim e^{646}m_e$; varrer $g^2$ é o mesmo problema, numericamente sadio.

**Análise dimensional.** $[\mathcal{G}]=[Q^2]^{-1}$, $[\rho_J]$ adimensional,
$[\overline\Pi]$ adimensional, $[g_R^2]$ adimensional em 4D. Logo $Z_3$ e o
critério são **adimensionais** — como têm de ser, já que separam classes de
funções. Duas linhas; não há mais o que extrair daqui.

## 3. Cinco abordagens, e por que quatro foram descartadas

| # | Abordagem | Veredito |
|---|---|---|
| A | **Classe de funções** (Stieltjes/CBF): decidir a classe de $W$ por representação integral explícita | **ESCOLHIDA** — é a única que separa os três regimes de $Z_3$ e identifica a constante aditiva; as demais dão no máximo condição necessária |
| B | Positividade da densidade espectral: computar $\operatorname{Im}\mathcal{G}$ na linha de corte e exigir $\ge0$ | Descartada como critério: a densidade é **automaticamente** $\ge0$ (§6), logo não discrimina nada |
| C | Momentos/Hankel: testar $(-1)^n\Phi^{(n)}\ge0$ numericamente | Descartada como critério: é **cega** ao modo real de falha (§6, T5) — mas mantida como teste de controle, e o resultado virou achado |
| D | Grupo de renormalização: integrar o fluxo de $g^2_{\rm eff}$ e achar onde diverge | Descartada: localiza o polo de Landau mas não decide pertinência a classe de funções |
| E | Analogia com resposta linear em matéria condensada (relações de Kramers–Kronig, regra de soma f) | Descartada: dá as mesmas relações de dispersão já usadas, sem conteúdo novo sobre a constante aditiva |

**Critério de escolha:** só A produz um enunciado *se e somente se*. B e C
produzem condições necessárias que, como se vê abaixo, são satisfeitas mesmo
quando H3 falha — o que as torna perigosas se usadas como certificado.

## 4. Derivação, sem pular álgebra

**Passo 1 — frações parciais.** Para $s,Q^2>0$,
$$\frac{Q^2}{s(s+Q^2)}=\frac{(s+Q^2)-s}{s(s+Q^2)}=\frac1s-\frac1{s+Q^2}.$$

**Passo 2 — separar a parte constante.**
$$\overline\Pi(Q^2)=\int\rho_J\Bigl[\frac1s-\frac1{s+Q^2}\Bigr]ds
=\overline\Pi(\infty)-\int\frac{\rho_J(s)\,ds}{s+Q^2},
\qquad \overline\Pi(\infty)=\int\frac{\rho_J(s)}{s}ds .$$

**Passo 3 — a identidade central.**
$$\boxed{\;W(Q^2)=\underbrace{\bigl[1-g_R^2\overline\Pi(\infty)\bigr]}_{=:Z_3}
+\;g_R^2\!\int\frac{\rho_J(s)\,ds}{s+Q^2}\;}$$

Consequências imediatas e exatas:
$$W(0)=Z_3+g_R^2\overline\Pi(\infty)=1,\qquad W(\infty)=Z_3,$$
e $W$ é **estritamente decrescente** (a integral é decrescente em $Q^2$).

**Passo 4 — a classe.** O membro direito tem a forma $b+\int d\sigma/(Q^2+s)$
com $b=Z_3$ e $d\sigma=g_R^2\rho_J\,ds\ge0$. Isso é Stieltjes **se e somente
se** $b\ge0$, isto é $Z_3\ge0$.

**Passo 5 — de $W$ para $\mathcal{G}$.** Pela dualidade SSV, $W/g_R^2$ Stieltjes
$\Rightarrow$ $Q^2W/g_R^2=1/\mathcal{G}$ é CBF $\Rightarrow$ $\mathcal{G}$ é
Stieltjes.

**Passo 6 — a fronteira, onde a redação ingênua erra.** A classe **geral** de
Stieltjes admite constante aditiva; a H3 do artigo **não**. Então:

- $Z_3>0$: $0<\mathcal{G}\le g_R^2/(Q^2Z_3)\to0$. **Suficiente** para a H3 literal.
- $Z_3=0$: $\mathcal{G}\to1/\rho_J((0,\infty))$ por convergência monótona.
  Falha **se e somente se** $\rho_J$ tem massa total finita. Exemplo de falha:
  $\rho_J=Z\delta(s-s_0)$ dá $\mathcal{G}=g_R^2/Q^2+g_R^2/s_0$.
- $Z_3<0$: falha — e o modo de falha é o assunto da §5.

## 5. A obstrução: um polo fantasma no eixo spacelike

*Escopo desta seção: ela caracteriza o **polo**, que é uma obstrução
**necessária** a H3, não um critério suficiente. A fronteira $Z_3=0$ não tem
polo e ainda assim pode falhar — ver §9.*

Esta é a contribuição real desta rodada. Como $W(0)=1>0$ e $W(\infty)=Z_3$,
com $W$ estritamente decrescente:

$$Z_3<0\iff W \text{ tem um zero em algum } Q^2_{\rm g}>0
\iff \mathcal{G}\ \text{tem um POLO em } Q^2_{\rm g}>0 .$$

Uma função de Stieltjes é analítica fora do eixo real **negativo**: a medida
vive em $s\ge0$ e produz polos só em $Q^2=-s\le0$. **Um polo em $Q^2>0$ é
precisamente um estado com $s=-Q^2_{\rm g}<0$** — taquiônico, de resíduo
negativo. É o fantasma de Landau.

Verificado numericamente (`ghost_analysis.py`, T2), com $\Lambda^2=10^6$:

| $g^2/g^2_c$ | $Z_3$ | $Q^2_{\rm fantasma}$ |
|---|---|---|
| 1,02 | $-0{,}020$ | $3{,}72\times10^{6}$ |
| 1,10 | $-0{,}100$ | $4{,}96\times10^{5}$ |
| 1,50 | $-0{,}500$ | $1{,}77\times10^{4}$ |
| 3,00 | $-2{,}000$ | $2{,}98\times10^{2}$ |

O fantasma **corre para o infinito** quando $Z_3\to0^-$ e entra no domínio
físico conforme o acoplamento cresce. Em $Z_3\ge0$ ele não existe.

## 6. Verificação cruzada: três ângulos independentes

**Ângulo 1 — densidade espectral (analítico).** Continuando
$Q^2\to-s-i0$: $\operatorname{Im}\overline\Pi=-\pi\rho_J(s)$, e
$$\frac{d\sigma}{ds}=\frac1\pi\operatorname{Im}\mathcal{G}(-s-i0)
=\frac{g_R^4\,\rho_J(s)}{s\,\bigl|1-g_R^2\overline\Pi(-s-i0)\bigr|^2}\;\ge\;0 .$$

**Resultado inesperado, e é o ponto central: a densidade do contínuo é não
negativa para QUALQUER acoplamento, inclusive $Z_3<0$.** Ela é $\rho_J$
dividida por um módulo ao quadrado. A quebra de H3 **não** é perda de
positividade do contínuo.

*(Nota de honestidade: minha primeira passagem simbólica deu esta expressão com
sinal trocado, por erro na conjugação. Refiz à mão e o código T3 compara a
fórmula fechada com $\operatorname{Im}\mathcal{G}$ calculada numericamente —
concordam a $10^{-9}$ relativo.)*

**Ângulo 2 — numérico direto.** T3 verifica $d\sigma/ds\ge0$ em grade de $s$
para $g^2/g^2_c\in\{0{,}5;1;1{,}5;3\}$, e confirma a fórmula fechada.
T4 verifica que $\mathcal{G}>0$ em todo $(0,\infty)$ sse $Z_3\ge0$, e que
$\mathcal{G}$ **troca de sinal** ao cruzar o fantasma.

**Ângulo 3 — o filtro do próprio projeto.** Apliquei `moment_conditions.moment_gate`
aos momentos do contínuo. Resultado (T5):

| Caso | Veredito do filtro |
|---|---|
| $Z_3>0$ | `CHECKED_COMPATIBLE` |
| $Z_3<0$ (H3 **falsa**) | `CHECKED_COMPATIBLE` |

> **ACHADO: o filtro de momentos do projeto é cego ao fantasma.**
> Ele examina o contínuo, e o contínuo continua positivo. A violação está no
> polo discreto spacelike, que nenhum momento do contínuo enxerga.

Os três ângulos **convergem**: a densidade é positiva sempre (1 e 2), o filtro
passa sempre (3), e mesmo assim H3 é falsa para $Z_3<0$ — porque o objeto que
falha é o polo, não a medida.

**Checagem de limite (T6).** $g_R^2\to0$ reproduz
$d\sigma_{\rm LO}=g_R^4\rho_J(s)/s$ do Apêndice A, a $5\times10^{-3}$ relativo.

**Checagem independente da quadratura.** $\overline\Pi(\infty)$ por quadratura
versus a forma assintótica $\frac{1}{12\pi^2}\log(\Lambda^2/4m^2)$:
a diferença é $-0{,}002367$ em $\Lambda^2=10^{20}$ **e exatamente a mesma** em
$\Lambda^2=10^{30}$ — é a constante de limiar, independente do corte, como deve ser.

## 7. Análise de erro

- **Quadratura:** substituição $s=4e^t$ doma o intervalo logarítmico. Erros
  absolutos reportados por `quad`: $10^{-15}$ a $10^{-13}$ (tabela de
  sensibilidade). Sem ela, a integração direta em $[4,10^{200}]$ **falha
  silenciosamente** — eu cometi esse erro numa rodada anterior e obtive
  $g^2\overline\Pi=0{,}079$ onde o valor correto é $0{,}355$.
- **Valor principal:** `quad(weight='cauchy')`, que trata o polo analiticamente
  em vez de por cancelamento numérico.
- **Raiz do fantasma:** `brentq` com `rtol=1e-13` sobre uma função monótona com
  bracket garantido por $W(0)=1>0>Z_3=W(\infty)$ — convergência incondicional.
- **Truncamento:** o corte $\Lambda$ é físico aqui (supos. 4), não erro numérico.
- **Propagação:** $Z_3=1-g^2P$ é linear em $P$; $\delta Z_3=P\,\delta g^2+g^2\delta P$,
  com $\delta P\sim10^{-13}$ desprezível frente a qualquer incerteza em $g^2$.

## 7-bis. Tabela única de reprodutibilidade

Unidades: $m=q=1$, $\hbar=c=1$; $s$ e $\Lambda^2$ em $m^2$. Todas as linhas de
uma execução: `python reports/h3_ghost_2026-09-29/ghost_analysis.py`.
A última coluna verifica a identidade $Z_3=1-g_R^2/g_c^2$.

| $\Lambda^2$ | acoplamento | $g_R^2$ | $\bar\Pi(\infty)$ | err. quad. | $g_c^2$ | $g_R^2/g_c^2$ | $Z_3$ | $Q^2_{
m polo}$ | $|Z_3-(1-g_R^2/g_c^2)|$ |
|---|---|---|---|---|---|---|---|---|---|
| $10^{4}$ | QED $4\pi/137$ | 0,0917 | 0,063694 | 1,2e-14 | 15,6999 | 5,842e-03 | 0,994158 | — | 0,0 |
| $10^{6}$ | QED $4\pi/137$ | 0,0917 | 0,102578 | 6,5e-14 | 9,7487 | **9,409e-03** | 0,990591 | — | 0,0 |
| $10^{10}$ | QED $4\pi/137$ | 0,0917 | 0,180345 | 6,5e-15 | 5,5449 | 1,654e-02 | 0,983458 | — | 0,0 |
| $10^{20}$ | QED $4\pi/137$ | 0,0917 | 0,374762 | 1,9e-13 | 2,6684 | 3,437e-02 | **0,965625** | — | 0,0 |
| $10^{30}$ | QED $4\pi/137$ | 0,0917 | 0,569179 | 4,9e-14 | 1,7569 | 5,221e-02 | 0,947792 | — | 0,0 |
| $10^{6}$ | modelo $k=0{,}5$ | 4,8743 | 0,102578 | 6,5e-14 | 9,7487 | 0,5 | $+0{,}500000$ | — | 0,0 |
| $10^{6}$ | modelo $k=1{,}0$ | 9,7487 | 0,102578 | 6,5e-14 | 9,7487 | 1,0 | $0{,}000000$ | — | 0,0 |
| $10^{6}$ | modelo $k=1{,}02$ | 9,9437 | 0,102578 | 6,5e-14 | 9,7487 | 1,02 | $-0{,}020000$ | 3,718e+06 | 0,0 |
| $10^{6}$ | modelo $k=1{,}5$ | 14,6230 | 0,102578 | 6,5e-14 | 9,7487 | 1,5 | $-0{,}500000$ | 1,773e+04 | 0,0 |
| $10^{6}$ | modelo $k=3{,}0$ | 29,2461 | 0,102578 | 6,5e-14 | 9,7487 | 3,0 | $-2{,}000000$ | 2,979e+02 | 0,0 |

**Sobre os dois números que circulavam soltos.** A razão $9{,}4	imes10^{-3}$ é
de $\Lambda^2=10^{6}$; o valor $Z_3=0{,}9656$ é de $\Lambda^2=10^{20}$.
São **cortes diferentes**, e a discrepância aparente entre eles é apenas a
dependência esperada de $\bar\Pi(\infty)$ com $\Lambda$ — não uma contradição.
Ambos aparecem agora na mesma tabela, com o corte explícito.

**Status da evidência.** Os erros da coluna "err. quad." são estimativas
retornadas por `scipy.integrate.quad`. São **evidência numérica**, não
certificação rigorosa: não são enclosures de intervalo. A distinção
`CHECKED` × `CERTIFIED` do projeto se aplica, e isto é `CHECKED`.

## 8. Discussão física

**Enunciado de trabalho (é este, e não uma equivalência).**

> Dentro das hipóteses RPA/Dyson especificadas (supos. 1–6), $Z_3<0$ produz um
> polo spacelike que **impede** H3. Para $Z_3>0$, a representação obtida
> satisfaz a versão **sem constante aditiva**. Na fronteira $Z_3=0$, a ausência
> de polo spacelike **não basta**: é necessário examinar o limite do kernel no
> infinito.

**O que isso reposiciona, e o que não reposiciona.** A positividade do
contínuo é automática (§6), então dentro deste modelo H3 não é uma hipótese
sobre positividade da densidade. O obstáculo em $Z_3<0$ é a singularidade
spacelike. Mas **"ausência de fantasma" e "H3" não são o mesmo enunciado**: a
fronteira $Z_3=0$ é exatamente o caso em que não há polo e H3 ainda assim pode
falhar, pelo termo constante. A ausência de polo é **necessária, não
suficiente**. Uma redação anterior desta seção afirmava a equivalência; estava
mais forte do que a própria análise de fronteira permite.

**Surpresa.** Eu esperava que a violação aparecesse como densidade negativa em
alguma região de $s$. Não aparece: $d\sigma/ds=g^4\rho_J/(s|W|^2)$ é
manifestamente positiva. Consequência prática desagradável: **testes de
positividade baseados em momentos do contínuo não detectam a falha.** O filtro
do projeto, que foi construído justamente para recusar medidas assinadas,
aprova este caso. Não é defeito de implementação — é limite de escopo do que
momentos do contínuo podem ver.

**Ordem de grandeza, com os cortes declarados.** Os dois números citados usam
cortes **diferentes**, e isso não é contradição — é a dependência esperada de
$\overline\Pi(\infty)$ com $\Lambda$. A tabela da §7-bis registra os dois na
mesma linha de raciocínio. Em resumo: a $\Lambda^2=10^6$, $g^2_c=9{,}75$ contra
$g^2_{\rm QED}=4\pi/137=0{,}0917$, razão $9{,}4\times10^{-3}$; a
$\Lambda^2=10^{20}$, $Z_3(\text{QED})=0{,}9656$. Nos dois cortes o modelo RPA
está **muito longe** do fantasma.

**Onde o modelo quebra.** Conforme $Z_3\to0^-$ — isto é, aproximando a
fronteira **por baixo**, que é o único lado em que o polo existe — a posição do
polo $Q^2_{\rm g}$ diverge (§5, tabela e fig. 2). Em $Z_3=0$ não há polo, e o
que decide H3 passa a ser o limite do kernel no infinito. Para $Z_3<0$ o polo
está em $Q^2$ finito.

**Uma afirmação que eu tinha errado aqui.** A redação anterior dizia que
$Z_3<0$ significa "acoplamento renormalizado negativo". **Não significa.**
No modelo, $g_R^2>0$ é um parâmetro de entrada e permanece positivo; $Z_3<0$ é
uma afirmação sobre $1-g_R^2\overline\Pi(\infty)$, não sobre o sinal de $g_R^2$.
O que $Z_3<0$ produz é o polo spacelike com resíduo negativo
($\operatorname{Res}=g_R^2/[x_*W'(x_*)]<0$, pois $W'<0$), não um acoplamento
negativo. A relação com o limite de Källén $0\le Z_3\le1$ é de **analogia de
conteúdo**, e não foi demonstrada aqui para esta construção.

## 8-bis. CORREÇÃO de 29/09 — a medida sai do suporte da densidade de entrada

Uma revisão externa encontrou um erro na Prop. 3 da nota, e ele atinge este
relatório. A **ressoma cria um átomo discreto fora do suporte de $\rho_J$**.

Contraexemplo conferido simbolicamente: $\rho_J\equiv1$ em $[4,10]$,
$g_R^2=1/(2\log(5/2))$, $Z_3=1/2$ dá $W(-14)=0$ com resíduo $10/21>0$ — átomo
em $s=14$, acima do corte $10$.

Para a densidade **Dirac** usada aqui o mesmo ocorre: com $\Lambda^2=10^6$ e
$Z_3=0{,}5$ há **exatamente um** átomo em $s_a=1{,}00000529\times10^6$ com peso
$w=6{,}2698\times10^{-4}>0$. Em $Z_3<0$ não há átomo algum.

**Consequência direta para este relatório.** A concordância de $\sim10^{-8}$
que eu havia atribuído a erro de quadratura **era o átomo omitido**: incluí-lo
leva o resíduo a $\sim10^{-12}$, quatro ordens de grandeza melhor. A
representação completa é
$$\mathcal{G}=\frac{g_R^2}{Q^2}+\int\frac{d\sigma_{\rm cont}}{Q^2+s}
+\frac{w}{Q^2+s_a},\qquad s_a>\Lambda^2,\ w>0 .$$

**O que NÃO muda.** O átomo tem peso positivo em $s_a>0$: a positividade de
Stieltjes continua valendo, e os três regimes de $Z_3$ (§9) ficam de pé. O erro
era sobre o **suporte** da medida, não sobre a positividade.

**O átomo é artefato do corte rígido**, por argumento analítico em dois casos
(Prop. 4 da nota): com suporte até o infinito não sobra região real onde $W$
possa zerar. A checagem numérica com regulador suave não foi confiável e não é
apresentada como evidência.

## 9. Teto do que foi estabelecido, e o que continua aberto

**Estabelecido (dentro das suposições 1–6), nos três regimes separadamente:**

| Regime | Polo spacelike | H3 (sem constante aditiva) |
|---|---|---|
| $Z_3>0$ | não existe | **vale** — $0<\mathcal{G}\le g_R^2/(Q^2Z_3)\to0$ |
| $Z_3=0$ | não existe | **indecidido pelo polo**; decide-se pelo limite $\mathcal{G}(Q^2\to\infty)=1/\rho_J((0,\infty))$. Sob a supos. 4 (corte rígido) a massa é finita e H3 **falha** |
| $Z_3<0$ | existe, em $Q^2_{\rm g}$ finito, resíduo negativo | **falha** |

A ausência de polo spacelike é portanto **necessária e não suficiente** para
H3. A classe **geral** de Stieltjes (que admite constante aditiva) é
caracterizada por $Z_3\ge0$; a H3 do artigo, que não admite a constante, exige
a análise separada da fronteira.

**NÃO estabelecido:**
- H3 para a resposta estática **não perturbativa e invariante de gauge**.
  O transporte $\langle FF\rangle\to$ laço de Wilson $\to$ kernel continua
  intocado (termos de contato, perímetro, $T\to\infty$, setor $p^2=0$).
- Nada além de RPA: trocar $\rho_J$ pela auto-energia 1PI completa **não**
  herda a positividade de Lehmann de graça — em gauge covariante a métrica é
  indefinida.
- Atribuição. O limite $0\le Z_3\le1$ é clássico (Källén 1952); a propriedade
  de Stieltjes da polarização é conhecida (Raman 2026, já auditado no repo).
  A identificação **H3 $\iff$ ausência de fantasma** não foi encontrada nas
  fontes pesquisadas, o que não é o mesmo que ser nova. Brown–Weisberger 1979
  segue não lido.

## 10. Extensões que valem a pena

1. **Fechar a cegueira do filtro.** Acrescentar ao gate um teste de sinal de
   $\mathcal{G}$ em grade spacelike, ou de $W(\infty)\ge0$. É barato e pega
   exatamente o caso que os momentos perdem. **Recomendo fazer.**
2. **Massa total de $\rho_J$ na fronteira — cuidado, o sinal é o oposto do
   intuitivo.** Em $Z_3=0$ vale
   $\mathcal{G}=1/\!\int\![Q^2/(s+Q^2)]\rho_J\,ds\to1/\rho_J((0,\infty))$.
   Sob a **suposição 4** (corte rígido) a massa é **finita**:
   numericamente $\int_4^{\Lambda^2}\rho_J\,ds\simeq\Lambda^2/(12\pi^2)$
   **como aproximação assintótica** (a razão massa$/\Lambda^2$ vale
   $8{,}4434\times10^{-3}$ e coincide com $1/12\pi^2$ em seis casas de
   $\Lambda^2=10^6$ a $10^{20}$; não é identidade exata). Logo **na teoria com corte o caso de
   fronteira $Z_3=0$ FALHA** — $\mathcal{G}$ tende à constante
   $\approx 118{,}4/\Lambda^2>0$, que a H3 literal não admite.
   A massa só diverge no continuum estrito, e lá $Z_3<0$ de qualquer modo.
   *(Numa redação anterior eu afirmei o contrário aqui. Estava errado sob a
   minha própria suposição 4; verificado e corrigido.)*
3. **Além do RPA:** a pergunta bem posta é se a auto-energia 1PI completa admite
   representação subtraída com densidade não negativa. Distinta do transporte
   via Wilson, e talvez mais tratável.
4. **Outras densidades espectrais.** A derivação usa apenas $\rho\ge0$ e
   integrabilidade; nada nela é específico do $\rho_J$ de um laço. Vale
   instanciá-la para outras $\rho$ e ver como os três regimes se movem.
   *Não* afirmo aqui nada sobre teorias assintoticamente livres nem sobre QED
   completa: seriam conclusões sem demonstração própria neste trabalho.

## 11. Autocrítica

- **Errei o sinal** na primeira passagem simbólica da densidade espectral
  (conjugação). Só peguei ao conferir à mão contra a expectativa física.
  Corrigido, e o código agora compara duas rotas independentes.
- **Errei a quadratura** antes, integrando direto num intervalo de 200 décadas
  e obtendo um $\overline\Pi$ 4,5× menor. Corrigido com substituição logarítmica
  e verificado contra a assintótica.
- **Minha redação de 24/09 identificou classe geral com H3 canônica** — erro
  achado por outro agente, confirmado por mim, corrigido aqui na §4 passo 6.
- **A varredura em $g^2$ a corte fixo é um artifício** (supos. 6). Ela é
  legítima porque o critério depende só do produto, mas não é "QED com
  acoplamento grande" — é um modelo. Não deve ser lido como previsão física.
- **T5 é um resultado sobre o filtro, não sobre a natureza.** Que o gate passe
  não diz nada sobre H3; diz que aquele teste não é sensível a este modo. Se eu
  tivesse rodado só o gate, teria concluído errado — e é exatamente o tipo de
  falso conforto que este projeto existe para evitar.
- **Errei a §10.2 na primeira redação**, afirmando que a massa total de $\rho_J$
  é infinita e que portanto a fronteira $Z_3=0$ não falharia. Sob a suposição 4
  a massa é finita e a fronteira **falha**. Verificado numericamente antes de
  publicar esta versão. É o terceiro erro meu nesta sessão pego por verificação
  e não por intuição — o que é o argumento a favor de verificar tudo.

---

## 12. Reprodução

```
python reports/h3_ghost_2026-09-29/ghost_analysis.py
```

Roda T1–T6 com asserts, imprime a tabela de sensibilidade e escreve as quatro
figuras em `reports/h3_ghost_2026-09-29/figures/`. Requer NumPy, SciPy,
Matplotlib e mpmath; importa `moment_conditions` do próprio projeto.
Última execução: 29/09/2026, todos os asserts passaram.
