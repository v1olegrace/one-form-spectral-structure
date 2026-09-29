# Pacote para conversa com professor — conteúdo (rascunho para diagramação)

Redigido em 28/09/2026 por Claude a partir das fontes locais. Não é PDF final (Codex diagrama).
Referências completas de arquivo/linha e cobertura: `SOURCE_AUDIT.md`.

**Etiquetas usadas em todas as caixas (imprimir):**
[TEOREMA] demonstrado no artigo canônico v0.3 · [CONDICIONAL H1–H5] teorema válido sob as hipóteses ·
[HIPÓTESE] · [CONJECTURA P‑E2] · [NOTA DE TRABALHO] resultado em nota não promovida ao artigo ·
[NUMÉRICO‑registrado] valor registrado em 22–23/09, **não reexecutado em 28/09** · [CONTRAEXEMPLO] · [ABERTO].

**Dois níveis de fonte, separados em cada página:**
(i) artigo canônico `paper/paper.tex` + `paper/appendix.tex`, draft v0.3 (hashes conferem com o PDF canônico em 28/09);
(ii) notas de trabalho: `notes/E2b_tensor_classification.tex` (22/09, não compilada, 3 lemas "to read") e
`notes/H3_attack_2026-09-24.md` (24/09, não promovida, atribuição em aberto).

**Correções ao pedido original (o usuário pediu que fossem explicitadas):**
1. A fórmula correta não é `f(r)=∫e^{-μr}dρ(μ)` aplicada a δ(r). É o **perfil reduzido** Φ(r)=δ(r)/r² = ∫e^{-rx}dν(x),
   com ν um *pushforward ponderado* da medida σ do kernel estático, e x=√s a **massa invariante do estado intermediário**.
   Para um férmion de Dirac a um laço a borda é **2m (limiar de par)**, não m.
2. A borda do suporte é o **menor limiar efetivamente acoplado** a esse observável, não "a menor massa da teoria" nem
   automaticamente o limiar carregado. Em QED completa, cortes multi‑fóton começam em s=0: a hipótese de gap H2 falha e o
   limite inferior útil degrada para 0.
3. A relação `r_x ~ log(1/ε)/Δm` só é exata para a família de duas exponenciais puras. No modelo numérico do artigo o
   crossover é 22,76, não 27,63 (decomposição na p. 3).
4. E2.3b: Bianchi elimina a estrutura dual **só para p²>0**. No cone de luz ela sobrevive a Bianchi; positividade só a
   limita; quem a remove é a **localidade via CPT**. A versão antiga (roadmap E2.1 passo 1: "(B) elimina a dual para p²≠0")
   está superada.
5. "Sem supor F=dA" vale para a **classificação** de ⟨FF⟩. O passo que leva ⟨FF⟩ ao observável (laço de Wilson) não
   está escrito. A p. 4 não é progresso demonstrado sobre H3.

Decisão editorial: manter 5 páginas. Versão alternativa de 4 páginas: fundir p. 5 (Hankel/GEVP) como meia página na p. 1 e
meia na p. 3; perde‑se o contraexemplo do localizador, que é o exemplo mais verificável à mão. Não recomendo.

---

## PÁGINA 1 — Visão geral

**Título:** Estrutura espectral da quebra aproximada de uma simetria de 1‑forma: o que o perfil radial determina sobre o limiar

**Pergunta central (caixa):** Numa teoria de gauge abeliana, uma linha de Wilson é blindada pela matéria carregada, e a
"carga de 1‑forma" medida por uma esfera de raio r passa a depender de r. **O formato desse perfil radial determina — e
sob quais hipóteses — o início do suporte espectral acoplado a ele?**

**Objetos (artigo v0.3, Def. 1 e eqs. qdef/delta):**
- q(r): carga efetiva de 1‑forma de uma linha de Wilson, medida pelo operador de superfície U_α(S²_r) (Córdova–Ohmori–Rudelius; Basile–Golmohammadi).
- δ(r) = −(r/q_∞) dq/dr ≥ 0 (blindagem) — o "perfil de quebra".
- Φ(r) = δ(r)/r² — **perfil reduzido; é esta a função observável da representação.**

**Três equações fundamentais:**

(1) [HIPÓTESE H3] kernel de resposta estática com representação de Stieltjes positiva

  𝒢(Q²) = g_R²/Q² + ∫_{s*}^∞ dσ(s)/(Q²+s),  dσ ≥ 0

(2) [TEOREMA, CONDICIONAL H1–H5] (Teorema A)

  Φ(r) = ∫_{M*}^∞ e^{−rx} dν(x),  M* = √s*,  ∫f dν ≡ g_R^{−2} ∫ s f(√s) dσ(s)

  (x = √s: massa invariante do estado intermediário; ν: peso espectral transportado de σ; átomos de σ viram átomos de ν
  com peso s_a w/g_R² — nenhuma hipótese de continuidade absoluta.)

(3) [TEOREMA] (Teoremas C e E) inclinação logarítmica e hierarquia de Hankel

  Γ(r) = −∂_r log Φ = ⟨x⟩_r ≥ M*,  Γ'(r) = −Var_r(x) ≤ 0;  B_K(r) = λ_min(H₁,H₀) ↓ M*

**Diagrama lógico (setas):**

```
 QFT: Wightman para F_{μν} (W) + Bianchi (B)
      │  E2.3b [NOTA DE TRABALHO; 3 lemas "to read"]
      ▼
 ⟨FF⟩ = medida de Källén–Lehmann positiva μ
      │  laço de Wilson O(q_W²), contato, T→∞, p²=0, fase de Coulomb   ◄── [ABERTO: obrigação O2 + O1]
      ▼
 H3: 𝒢 é Stieltjes com σ ≥ 0            (ordem líder: [TEOREMA], via positividade de Lehmann da corrente de matéria)
      │  + H2 (gap; FALHA em QED completa), H4, H5 → Teorema A (Yukawa + Gauss + identidade do núcleo)
      ▼
 Φ(r) = transformada de Laplace de ν ≥ 0
      ├─► Γ(r), B_K(r): cotas SUPERIORES em M* que descem até M*      [TEOREMA]
      ├─► Teorema H / tiny atom: nenhuma cota INFERIOR uniforme       [TEOREMA + CONTRAEXEMPLO]
      └─► Z‑invariância: forma não fixa g|q|M_Pl/m (sem WGC só com positividade)  [TEOREMA]
```

**Estabelecido (caixa verde):**
- Teorema A sob H1–H5, com prova elementar (transformada de Yukawa, lei de Gauss e d/dr[(1+r√s)e^{−r√s}] = −s r e^{−r√s}).
- Em ordem líder, dσ = g_R⁴ ρ_J(s) ds/s ≥ 0 (positividade de Lehmann da corrente de matéria não gaugeada, uma subtração); reproduz Basile–Golmohammadi eq. (13) e o coeficiente de Uehling 2α/3π.
- Cotas C/E, lei de borda, Teorema H, obstrução à inferência WGC.

**Limitação física principal (caixa amarela, não nota de rodapé):** em QED completa, estados multi‑fóton sem massa
contribuem com corte a partir de s=0. A hipótese de gap H2 **não** decorre da massa do elétron; Γ(r) devolve o ínfimo do
suporte **efetivamente acoplado**, que pode ser 0. Identificar a borda com um limiar carregado exige informação de canal
adicional [ABERTO].

**Principal questão aberta (caixa vermelha):** H3 para o kernel estático interagente além da ordem líder — em particular,
se a positividade de ⟨FF⟩ se transporta ao kernel do laço de Wilson.

**Honestidade de novidade (linha pequena no rodapé):** a matemática é clássica (Bernstein–Widder, massa efetiva/GEVP de
rede, Padé/Masjuan–Peris; caráter Stieltjes da polarização do vácuo revisado em Raman 2026). O que o projeto propõe é a
montagem para um observável de simetria generalizada e os modos de falha explícitos.

### O QUE EU FALO AO MOSTRAR ESTA PÁGINA (não imprimir)
"O ponto de partida é um observável de simetrias generalizadas: a linha de Wilson é blindada pela matéria, e a carga
medida por uma esfera depende do raio. Eu não calculo esse perfil — isso já foi feito a um laço por Basile e Golmohammadi.
A minha pergunta é: o *formato* dele diz o quê sobre o espectro? A resposta é condicional. Se o kernel de resposta estática
for uma função de Stieltjes com medida positiva — essa é a hipótese H3 —, então o perfil dividido por r² é exatamente uma
transformada de Laplace de uma medida positiva, e a borda dessa medida é o menor limiar que acopla ao observável. Daí saem
cotas superiores que descem até esse limiar. Mas há dois limites que eu quero deixar claros desde já: primeiro, H3 não
está provada além da ordem líder; segundo, em QED completa há cortes de fótons sem massa, então o limiar pode ser zero.
A página 2 é sobre a H3, a 3 sobre o limite de identificabilidade, a 4 sobre o correlator de F, a 5 sobre a máquina."

---

## PÁGINA 2 — Positividade: a hipótese H3

**O problema em uma linha (caixa):**
"Se existe representação de Stieltjes com medida positiva, então o Teorema A e as cotas seguem" — isso está demonstrado.
"A própria QFT garante essa medida positiva para este observável" — isso **não** está demonstrado.

**H3 (artigo v0.3, formulação atual) [HIPÓTESE]:**
𝒢(Q²) = g_R²/Q² + ∫_{s*}^∞ dσ(s)/(Q²+s), dσ ≥ 0, Q²=|p|²>0, com ∫dσ/(μ₀²+s) < ∞ (forma não subtraída).
Dependem dela: Teorema A e, portanto, toda leitura física das cotas C, E, H e da lei de borda. (Os Teoremas C, E, H são
matemática sobre medidas positivas e valem para qualquer Φ que seja Laplace de ν≥0.)

**Estado, do mais firme ao mais aberto:**

| Afirmação | Estado |
|---|---|
| Ordem líder: dσ_LO = g_R⁴ρ_J ds/s ≥ 0 | [TEOREMA] (Apêndice A), dada a relação de dispersão com uma subtração e ρ_J ≥ 0 da corrente de matéria **não gaugeada** |
| O coeficiente O(g_R⁶) isolado **não** tem a forma H3 (vale 0 em Q²=0, tem máximo interior) | [NOTA DE TRABALHO] (revisão 23/09). Moral: H3 é propriedade do kernel **ressomado**, não de cada ordem |
| Polo único ρ_J = Zδ(s−s₀), c = g_R²Z/s₀ < 1: 𝒢 = g_R²/Q² + [g_R²c/(1−c)]/(Q²+s₀/(1−c)) | [NOTA DE TRABALHO]; conferido à mão em 28/09. H3 vale em todas as ordens da cadeia; o polo **se desloca** para s₀/(1−c) |
| Critério Z₃ (cadeia de Dyson com ρ ≥ 0, uma subtração): **Z₃ ≡ 1 − g_R²∫ρ(s)ds/s > 0 é suficiente** para a H3 canônica. A equivalência com Z₃ ≥ 0 vale para a classe **geral** de Stieltjes, que admite uma constante que a H3 do artigo exclui | [NOTA DE TRABALHO 24/09], não promovida; teoremas de dualidade conferidos em Schilling–Song–Vondraček (Teor. 7.3/6.2); correção de fronteira em `H3_BOUNDARY_CORRECTION_2026-09-28.md`; atribuição **em aberto** |
| Reformulação: H3 ⟺ g²_eff(Q²) = Q²𝒢(Q²) é função de Bernstein completa ⇒ g²_eff não decrescente é **necessária** | [NOTA DE TRABALHO]; antiblindagem estritamente decrescente é incompatível com H3 |
| (W)+(B)+(L)+(C) ⇒ 𝒢 = Z/Q² + ∫_{(0,∞)}dσ/(Q²+s) + P(Q²), σ ≥ 0 (Proposição P‑E2) | [CONJECTURA P‑E2] — "conjectura com esboço; NÃO VERIFICADA" (roadmap). **Não é H3 inteira:** positividade tipo H3, **sem gap** (suporte pode começar em 0), módulo polinômio de contato/subtrações. O gap H2 não sai da QFT |

**Identidade‑chave do critério Z₃ (uma linha, verificável):** por frações parciais Q²/(s(s+Q²)) = 1/s − 1/(s+Q²), logo

  1 − g_R²Π̄(Q²) = [1 − g_R²Π̄(∞)] + g_R²∫ρ(s)ds/(s+Q²) = Z₃ + (Stieltjes positiva)

**O que o critério diz sobre QED (cadeia de bolhas a um laço, α=1/137) [NOTA DE TRABALHO, NUMÉRICO‑registrado]:**
Z₃ = 0,9335 para Λ/m_e = 10¹⁹; 0,6446 para 10¹⁰⁰; Z₃ = 0 perto de log(Λ²/4m²) ≈ 3π/α ≈ 1291 (polo de Landau).
**Admitir com clareza:** sem cutoff, ∫ρ_J/s diverge, então o kernel RPA **não** é Stieltjes no contínuo estrito (fantasma
de Landau). O critério torna isso preciso; não o conserta.

**Condições de QFT usadas na rota P‑E2 (onde entra cada uma):**
- positividade (Hilbert positivo, W3) → medida matricial ⪰ 0 para ⟨FF⟩;
- covariância de Lorentz (W1) → estruturas tensoriais por órbita;
- Bianchi (B), ∂_[λF_μν] = 0 → elimina estruturas magnética/dual para p²>0;
- CPT (via localidade W4) → só no cone de luz, remove a peça quiral;
- representação espectral → medida de Källén–Lehmann μ ≥ 0 em [0,∞);
- **F = dA não é suposto** na classificação;
- **fase de Coulomb (C), μ({0}) > 0, precisa ser suposta**: Proca livre satisfaz (W),(B),(L) e não tem polo de Coulomb (q_∞=0).

**Ponto aberto exato (caixa vermelha, obrigação O2):** transportar μ ≥ 0 de ⟨FF⟩ para o coeficiente O(q_W²) do laço de
Wilson: Stokes (exige caso abeliano), renormalização de perímetro, limite T→∞, termos de contato, componente p²=0.
Fato já verificado simbolicamente: no limite estático ⟨E_iE_j⟩ = D(Q²) p_i p_j (puramente **longitudinal**); o escalar
visto pelo potencial é Q²D(Q²) = g²_eff.

**Pergunta para o professor (imprimir em destaque):**
> Os axiomas de Wightman para F_{μν} mais a identidade de Bianchi dão uma medida de Källén–Lehmann positiva μ para ⟨FF⟩.
> O kernel estático do laço de Wilson, em ordem q_W², herda essa positividade na forma
> 𝒢(Q²) = μ({0})/Q² + ∫_{(0,∞)}dμ(s)/(Q²+s) + polinômio — ou termos de contato, renormalização de perímetro, T→∞ ou o setor p²=0
> escondem uma parte não positiva? A fase de Coulomb μ({0})>0 é a única hipótese adicional?

### O QUE EU FALO AO MOSTRAR ESTA PÁGINA (não imprimir)
"Tudo depende de uma hipótese: o kernel estático ser Stieltjes com medida positiva. Em ordem líder isso sai da positividade
de Lehmann da corrente de matéria — é o cálculo tipo Uehling. Além disso, duas observações. Primeiro, a ordem seguinte
sozinha *não* tem a forma certa; a positividade só aparece no kernel ressomado — no modelo de um polo, o polo simplesmente
se desloca. Segundo, numa nota de trabalho eu mostro que, para a cadeia de Dyson com densidade positiva, a propriedade de
Stieltjes exige Z₃ > 0 (a equivalência com Z₃ ≥ 0 é contra a classe geral, que admite uma constante que a H3 do artigo não
tem). Em QED isso vale com folga para qualquer cutoff físico e só falha no polo de Landau — ou seja,
no contínuo estrito falha, e eu não escondo isso. A rota realmente de QFT é outra: com Wightman e Bianchi, sem supor F=dA,
o correlator de F tem medida positiva. O que falta é o passo do correlator para o laço de Wilson. A minha pergunta é
exatamente essa: esse passo esconde alguma hipótese além da fase de Coulomb?"

---

## PÁGINA 3 — Tiny atom: um estado mais leve, quase invisível

**Construção (artigo v0.3, §Numerical validation, "Vanishing weight at the true edge") [CONTRAEXEMPLO + NUMÉRICO‑registrado]:**

  dν = 10⁻¹² δ₂ + (x−3)^{1/2} e^{−(x−3)} 1_{x≥3} dx

  Φ(r) = 10⁻¹² e^{−2r} + Γ_E(3/2)(1+r)^{−3/2} e^{−3r}

Borda verdadeira M* = 2 (átomo de peso 10⁻¹²); contínuo começa em 3.

**Crossover (igualdade das duas contribuições):** 10⁻¹² e^{r} = Γ_E(3/2)(1+r)^{−3/2} ⇒ **r_× = 22,76**.
Tomando log (conferido à mão em 28/09):

  r_× = ln(10¹²) + ln Γ_E(3/2) − (3/2) ln(1+r_×) ≈ 27,63 − 0,12 − 4,75 ≈ 22,76

**Γ(r) observado [NUMÉRICO‑registrado; os quatro valores conferidos à mão em 28/09 como médias ponderadas das inclinações]:**

| r | 10 | 20 | 22,76 | 30 |
|---|---|---|---|---|
| Γ(r) | 3,136 | 3,018 | 2,532 | 2,0005 |

Em r = 3 a hierarquia inteira B₀…B₄ desce só de 3,375 para 3,108 [NUMÉRICO‑registrado] — **nem o GEVP vê o átomo**.
Nenhuma cota é violada (Γ ≥ 2 sempre); o que se degrada é a **informatividade**.

**Teorema H (artigo) [TEOREMA]:** para M > μ ≥ 0, janela [0,T] e 0<ε<1,
f₀ = e^{−Mt} e f_ε = (1−ε)e^{−Mt} + εe^{−μt} são Laplace de medidas positivas com bordas M e μ, e sup|f_ε − f₀| ≤ ε.
⇒ **Nenhuma cota inferior estritamente positiva em M* vale uniformemente** a partir de dados de precisão finita numa
janela finita. Cotas superiores sobrevivem; localização bilateral exige peso mínimo, modelo espectral ou informação externa.

**Onde r_x ~ log(1/ε)/Δm é exato:** só na família de duas exponenciais: t_× = ln[(1−ε)/ε]/(M−μ). Para ε = 10⁻¹², Δm=1:
27,63. No modelo acima o prefator em lei de potência do contínuo desloca para 22,76. Leitura correta:
r_× = [ln(1/ε) + ln(razão dos prefatores em r_×)]/Δm.

**Figura (dados gerados por `check_numbers.py`, que Codex deve executar; ainda não existem):** painel log‑y, r ∈ [0,40]:
curva 10⁻¹²e^{−2r} (átomo) e Γ_E(3/2)(1+r)^{−3/2}e^{−3r} (contínuo), linha vertical em r_×=22,76; painel menor com Γ(r)
caindo de ≈3 para 2 (mesmo conteúdo de `paper/figures/hidden_threshold.dat`, Fig. 1 esquerda do artigo).

**Consequência conceitual (caixa):** "o decaimento que observo agora determina a menor massa" é falso sem hipótese extra.
O decaimento observado mede o limiar **dominante na janela**; o limiar verdadeiro pode estar abaixo, com peso ε, e só
aparece para r ≳ ln(1/ε)/Δm. Com uma cota externa de peso mínimo perto da borda (P(M ≤ x ≤ M+Δ) ≥ w₀), volta uma
localização bilateral — isso está no rascunho não canônico *Finite-data certificates*, Prop. 3 [NOTA DE TRABALHO].

### O QUE EU FALO AO MOSTRAR ESTA PÁGINA (não imprimir)
"Esta é a página de que eu mais gosto porque é simples e não depende de H3. Coloco um estado em massa 2 com peso 10⁻¹² e
um contínuo a partir de 3. Até r ≈ 23 o perfil é indistinguível de um espectro que começa em 3; a inclinação só cai para 2
depois disso. E não é falha do método: todas as cotas continuam corretas, só deixam de ser informativas. O teorema diz que
isso é inevitável: com dados de precisão finita numa janela finita, não existe cota inferior uniforme para o limiar.
Para física médica isso é familiar: é o mesmo problema mal‑posto da inversão de Laplace multi‑exponencial em relaxometria
T2 de RM — uma componente com fração minúscula e tempo longo simplesmente não aparece na janela. [analogia, não resultado
do projeto] A fórmula log(1/ε)/Δm só é exata para duas exponenciais puras; aqui dá 22,76 em vez de 27,6."

---

## PÁGINA 4 — Classificação do correlator ⟨F_{μν}F_{ρσ}⟩ (E2.3b, versão atual)

**Status (caixa no topo) [NOTA DE TRABALHO]:** nota de 22/09 (conteúdo atual em `72d6dcc`), não compilada. Álgebra linear
verificada em sympy partindo da matriz hermitiana 6×6 geral (36 incógnitas reais), **sem supor F=dA**
(`tests/test_e2_tensor_classification.py`, 13 testes; não reexecutados em 28/09). Três lemas clássicos marcados
"to read": Bochner–Schwartz (medida), CPT/Jost, desintegração covariante. **Não diz nada sobre H3 por si só.**

**Hipóteses:** (W1) covariância de Poincaré como 2‑forma, (W2) condição espectral, (W3) Hilbert positivo, (W4) localidade,
(W5) vácuo único; (B) Bianchi como identidade de operadores. **Não supostos:** F=dA, equações de Maxwell, fase de Coulomb, paridade.

**Ingrediente central:** W̃_AB(p) é medida com valores em matrizes 6×6 hermitianas ⪰ 0 com suporte em V̄₊.
Bianchi ⇒ cada linha/coluna é da forma p∧v ⇒ M(p) = φ_p K(p) φ_p†, K em ℂ⁴/⟨p⟩ (3 dimensões), e M ⪰ 0 ⟺ K ⪰ 0.

**Tabela por setor (imprimir):**

| Setor | Só covariância | + Bianchi | Positividade | CPT (localidade) | Sobrevive |
|---|---|---|---|---|---|
| p = 0 | G e ε (invariantes) | — | autovalores ±√(x²+y²), mult. 3: indefinido | — | **nada** na medida espectral (G, ε podem voltar só como termos locais) |
| p² = s > 0 (little group SO(3)) | 4: EE, BB, EB, iEB | **1**: −T(p) (bloco EE no repouso) | a(s) ≥ 0 | já não atua | −T(p)·a(s)/s |
| p² = 0 (little group ISO(2)) | maior (teste) | **2**: −T(p) e i T^⋆(p) | autovalores 2(α±α′), 0⁴ ⇒ só **α ≥ |α′|** | **α′ = 0** | −T(p)·α |

Com T_{μνρσ}(p) = p_μp_ρg_{νσ} − p_νp_ρg_{μσ} − p_μp_σg_{νρ} + p_νp_σg_{μρ}.
No cone: K_⊥ = α δ_ij + iα′ ε_ij, e α ± α′ são os **pesos espectrais das duas helicidades**.

**Resultado montado [NOTA DE TRABALHO, condicional aos 3 lemas]:**

  W̃_{μνρσ}(p) = 2π θ(p⁰) ∫_{[0,∞)} dμ(s) δ(p² − s) (−T_{μνρσ}(p)),  μ ≥ 0 única

"Sem supor F=dA, (W)+(B) forçam a forma que teria se F=dA com medida de Källén–Lehmann positiva." Provavelmente clássico
(Streater–Wightman, Bogoliubov–Logunov–Todorov, Weinberg vol. I); se estiver lá, é atribuição, não resultado (E2.3e).

**Por que o cone não é continuação trivial do setor massivo (caixa):**
- em p²=0, Bianchi coincide com Maxwell sem fonte: ⋆(p∧e₁) = ±p∧e₂, então o dual de uma linha compatível com Bianchi
  continua compatível — **Bianchi não elimina a dual**;
- o little group tem translações nulas (não compactas) que matam componentes longitudinais;
- positividade só **limita** (α ≥ |α′|); sem localidade, positividade permitiria peso espectral quiral sem massa;
- a remoção vem de **localidade via CPT**, que só entra aqui.

**O que não fecha (caixa vermelha):** μ({0}) ≥ 0 é o peso sem massa e (W)+(B) **não** o forçam a ser > 0 (Proca livre:
μ = Zδ_{m²}). Termos locais: se Bianchi for imposto ao produto T‑ordenado, P(p) = q(p²)T(p) com q polinômio; caso
contrário G, ε e múltiplos sobrevivem. Como chegam ao kernel estático: não resolvido (O2/O3).

### O QUE EU FALO AO MOSTRAR ESTA PÁGINA (não imprimir)
"Aqui é QFT axiomática pura. Parto da matriz 6×6 mais geral para o correlator de F — seis componentes, E e B —, sem supor
potencial vetor. Positividade do espaço de Hilbert torna isso uma medida de matrizes positivas. Em momento zero, os
invariantes de Lorentz são indefinidos, então não entram na medida. No setor massivo, covariância deixa quatro estruturas e
Bianchi mata três: sobra uma, com coeficiente positivo. No cone de luz é diferente: Bianchi vira Maxwell livre e deixa a
estrutura dual viva; positividade só diz que os pesos das duas helicidades são não negativos; quem iguala os dois é a
localidade, via CPT. A álgebra está verificada por computador; três lemas clássicos eu ainda preciso ler na fonte, e
suspeito que o resultado seja clássico. Isto não prova H3: falta levar a medida até o laço de Wilson."

---

## PÁGINA 5 — A máquina: momentos, Hankel, GEVP

**Frase de topo:** positividade espectral ⇒ problema de momentos ⇒ cotas por autovalor generalizado.

**(1) Momentos locais** [TEOREMA, definição]: a_n(r) = (−1)ⁿ Φ⁽ⁿ⁾(r) = ∫ xⁿ e^{−rx} dν(x)

**(2) Hankel e localizador** [TEOREMA]: (H₀)_ij = a_{i+j}, (H₁)_ij = a_{i+j+1}, 0 ≤ i,j ≤ K. Para p_v(x)=Σv_i xⁱ:

  vᵀ(H₁ − M* H₀)v = ∫ (x − M*) p_v(x)² e^{−rx} dν ≥ 0

 ν ≥ 0 ⇒ H₀ ⪰ 0; suporte em [0,∞) ⇒ H₁ ⪰ 0; suporte em [M*,∞) ⇒ H₁ − M*H₀ ⪰ 0.

**(3) GEVP** [TEOREMA E]: com H₀ ≻ 0,

  B_K(r) = λ_min(H₁,H₀) = inf_{deg p ≤ K} ∫x p² e^{−rx}dν / ∫p² e^{−rx}dν ≥ M*,  B₀ = Γ(r),  B_{K+1} ≤ B_K,  B_K ↓ M*

 (convergência: suporte infinito e M* = inf supp ν; densidade de polinômios em L² de medida com momento exponencial.)

**Condições de validade (caixa):** H₀ ≻ 0 exige ≥ K+1 pontos no suporte; L átomos ⇒ exato em K = L−1 e singular acima
(redução de posto, não "nova cota"); crescimento H4; condicionamento: átomos em 2 e 200 exigem ≈86 dígitos
[NUMÉRICO‑registrado] — não reportar Hankel de alta ordem em double. Aprovação finita = `CHECKED_COMPATIBLE`, **nunca**
prova de H3: δ₁+δ₂+δ₃−10⁻⁶δ₄ passa até ordem 5 e falha na 7 [NUMÉRICO‑registrado].

**Duplo uso — estimador e falsificador (caixa):** na rede, positividade é teorema e o GEVP só estima. Aqui positividade é a
hipótese sob teste, então os mesmos determinantes são **teste necessário** de H3.

**Exemplo verificável a lápis [CONTRAEXEMPLO; conferido à mão em 28/09]:** dν = δ₁ + e·δ₂ − e⁹δ₁₀/1000, r = 1.
Momentos reescalados ã_n = eʳa_n = 1 + 2ⁿ − 10ⁿ/1000 = (1,999; 2,99; 4,9; 8) — todos positivos.
det H̃₀ = 1,999·4,9 − 2,99² = 0,855 > 0, mas det H̃₁ = 2,99·8 − 4,9² = −0,09 < 0.
Sem o localizador, o GEVP devolveria B₁ ≈ −0,0645 — uma "massa" negativa. A rotina atual recusa.
Mais simples: δ₁ − ½δ₂ tem Φ > 0 e −Φ′ > 0 (parece blindagem) mas a₃(1) = −0,1735 < 0.

**Exemplo físico (edge law) [TEOREMA + NUMÉRICO‑registrado]:** para densidade ∝ t^{p−1} perto da borda,
Γ(r) = M* + p/r + βp/r² + …; Dirac: Γ = 2m + 3/(2r) − 5/(16mr²) + …; numericamente r(Γ−2m) → 1,4981 (previsto 3/2) e
escalar complexo → 2,4904 (previsto 5/2). O coeficiente de 1/r discrimina o canal (onda S de férmion vs onda P de escalar).

**Rodapé de precedência:** massa efetiva (Lüscher–Wolff 1990), GEVP (Blossier et al. 2009), Padé/momentos (Masjuan–Peris
2009), Lanczos (Wagman 2025), dualidade convexa (Lawrence 2024), gap por LP em separação espacial (Mutzel–Tilloy 2025).
Certificados Arb do benchmark de um laço (288 certificados de peso, registrados 23/09) certificam limites de peso espectral
em modelos sintéticos de um laço; **não** certificam H3 nem a truncagem perturbativa.

### O QUE EU FALO AO MOSTRAR ESTA PÁGINA (não imprimir)
"A máquina é a mesma da massa efetiva em QCD na rede. Se o perfil é Laplace de uma medida positiva, as derivadas formam
momentos, as matrizes de Hankel têm de ser positivas, e o menor autovalor generalizado do par (H₁,H₀) é uma cota superior
para o limiar que desce até ele. A diferença é o uso: na rede a positividade é garantida; aqui é hipótese, então os mesmos
determinantes servem para rejeitar H3. Este exemplo o senhor confere a lápis: quatro momentos positivos, H₀ positiva, e
mesmo assim a medida é assinada — o localizador pega, e sem ele sairia massa negativa. E um teste finito aprovado não prova
nada: há medida assinada que passa até ordem 5."

---

## BACKUP TÉCNICO (opcional)

1. **Prova do Teorema A (artigo):** φ(r) = (q_W/4πr)[g_R² + ∫e^{−r√s}dσ]; q(r)/q_W = 1 + g_R^{−2}∫(1+r√s)e^{−r√s}dσ;
   d/dr[(1+r√s)e^{−r√s}] = −s r e^{−r√s} (os termos O(√s) cancelam, removendo o 1/s da dispersão subtraída); H2 dá q_∞ = q_W.
2. **Sinal (Apêndice A):** 𝒢 = g²/(Q²[1+g²Π_E]); com Π̄(Q²) = Q²∫ρ_J ds/(s(s+Q²)) ≥ 0 e Π_E(0)=0:
   𝒢 = g_R²/(Q²[1−g_R²Π̄]) = g_R²/Q² + g_R⁴∫ρ_J ds/(s(s+Q²)) + O(g_R⁶). Convenção invertida ⇒ medida negativa e antiblindagem (teste discriminante).
3. **Critério Z₃ completo [NOTA DE TRABALHO]:** SSV Teor. 7.3: f≢0 Stieltjes ⟺ 1/f CBF ⟺ z f(z) CBF. W/g_R² = (1−g_R²Π̄)/g_R² Stieltjes (se Z₃ ≥ 0) ⇒ Q²W/g_R² = 1/𝒢 CBF ⇒ 𝒢 Stieltjes **na classe geral**. Recíproca: 𝒢 Stieltjes ⇒ 1−g_R²Π̄ ≥ 0 em (0,∞) ⇒ g_R²Π̄(∞) ≤ 1.
   **Fronteira (correção de 28/09):** a classe geral admite constante; a H3 do artigo não. Z₃ > 0 dá 0 < 𝒢 ≤ g_R²/(zZ₃) → 0 e portanto exclui a constante — é suficiente. Em Z₃ = 0 o caso solúvel ρ = Zδ(s−s₀) dá 𝒢 = g_R²/z + g_R²/s₀, cujo limite é g_R²/s₀ > 0: viola a H3 literal. No caso crítico geral 𝒢 → 1/ρ((0,∞)), logo Z₃ = 0 falha se e somente se a massa total de ρ é finita. Na reformulação CBF a mesma ressalva: o termo **linear** de z𝒢 é exatamente a constante que precisa ser excluída.
   A demonstração usa só (i) Π̄ uma vez subtraída com ρ ≥ 0 e (ii) Dyson — **nenhuma ordem de laço**. A pergunta real vira: a auto‑energia 1PI completa admite representação subtraída com ρ ≥ 0? (não herdada da corrente não gaugeada; métrica indefinida em gauge covariante).
   Com a densidade de um laço completa, Z₃ = 0 ocorre ≈0,3 unidade de L acima de 3π/α (conta à mão; irrelevante na prática).
4. **Local terms (E2b, Prop. local):** lema pontual: X com linhas/colunas anuladas por p∧ e invariante pelo estabilizador de p timelike ⇒ X = c·T(p); com Bianchi no produto T, P(p) = q(p²)T(p), q polinomial (argumento de domínio de integridade).
5. **Corrente (hipótese M, só algébrico):** ∂^μF_μν = j_ν ⇒ ρ_J(s) = s dμ/ds em (0,∞); o átomo sem massa não acopla a j.
6. **Obstrução WGC [TEOREMA condicional]:** cotas invariantes sob ν ↦ Zν ⇒ forma não fixa g|q|M_Pl/m. Com N espécies de Dirac, N Λ² ≤ κM_Pl², δ_obs(1/Λ) ≥ η > τ+ε: max g_R|q_i|M_Pl/m_i ≥ √(6π²(η−τ−ε)/κ). Não é derivação da WGC.
7. **Edge law geral (Apêndice B):** Γ = M* + p/r + βp/r² + [2γp(p+1) − β²p²]/r³ + O(r⁻⁴); átomo separado por d: O(e^{−dr}); átomo e contínuo na mesma borda: Γ − M* ∼ CΓ_E(p+1)r^{−p−1}/Z.
8. **Complete monotonicity ≠ H3:** Φ = e^{−2r} satisfaz com M*=1 (borda efetiva 2); dν = x³1_{x≥1}dx é CM com gap mas a reconstrução de Stieltjes diverge; Φ = e^{−r} − ½e^{−2r} engana diagnóstico só de blindagem.

---

## AS 5 PERGUNTAS QUE O PROFESSOR PROVAVELMENTE FARÁ

**1. "Isso não é só a transformada de Laplace de Uehling, conhecida desde 1935?"**
Em ordem líder, sim — o artigo diz isso e reproduz o coeficiente 2α/3π. O que muda é o status lógico: sob H3, a
representação é exata para o kernel inteiro, com a medida completa σ, e os teoremas de cota valem para qualquer medida
positiva. A novidade possível está na montagem para o observável de 1‑forma e nos modos de falha, não na matemática.

**2. "Por que o limiar não é simplesmente a massa do elétron?"**
Porque x = √s é massa invariante do estado intermediário: a um laço a borda é 2m (par). E em QED completa há cortes
multi‑fóton a partir de s = 0, então o gap H2 falha e Γ(r) devolve o ínfimo do suporte efetivamente acoplado, que pode ser
0. Separar canais carregados de cortes sem massa com positividade preservada está em aberto.

**3. "A positividade não é automática por unitariedade?"**
Não para este objeto. Unitariedade dá positividade de Lehmann para correlatores de operadores num espaço de Hilbert
positivo; o artigo diz explicitamente que H1 (unitariedade) não estabelece H3. O kernel estático vem do laço de Wilson, e o
propagador de gauge em gauge covariante vive em métrica indefinida. Por isso a rota passa por ⟨FF⟩ (gauge‑invariante,
positividade limpa) — e o transporte até o laço de Wilson não está feito. Ademais, a relação entre H3 e positividade de
reflexão é desconhecida nas duas direções (Bachas 1986 tira V′ ≥ 0, V″ ≤ 0 só de positividade de reflexão).

**4. "E o polo de Landau / trivialidade?"**
O critério Z₃ da nota de 24/09, com a correção de fronteira de 28/09, mostra que para a cadeia de Dyson com densidade
positiva **Z₃ > 0 é suficiente** para H3 (a equivalência com Z₃ ≥ 0 é contra a classe geral de Stieltjes). Em QED a um laço
isso vale para todo cutoff abaixo do polo de Landau e falha no contínuo estrito. Então H3 para o kernel RPA exige um
cutoff físico; não há como afirmar H3 para QED contínua. [Observação do redator, não registrada no projeto: se QED contínua
for trivial, os axiomas (W) podem nem ser realizáveis de forma não trivial — a rota P‑E2 é sobre teorias que satisfazem (W).]

**5. "O tiny atom não é só o problema mal‑posto de Laplace, já conhecido?"**
É, e o projeto diz isso: o conceito é conhecido (e.g. Cover 2008; relaxometria multi‑exponencial). O que o projeto oferece
é o enunciado preciso para este observável (Teorema H: nenhuma cota inferior uniforme; superiores sobrevivem), o exemplo
quantitativo com r_× = 22,76 e a observação de que nem a hierarquia GEVP em r=3 se aproxima de 2. Não reivindico novidade
conceitual.

## 3 PERGUNTAS INTELIGENTES PARA EU FAZER A ELE
1. A pergunta da p. 2: a positividade de ⟨FF⟩ passa ao kernel O(q_W²) do laço de Wilson sem hipótese além da fase de
   Coulomb, ou contato/perímetro/T→∞/p²=0 escondem uma parte não positiva?
2. Em problemas de inversão de Laplace que o senhor conhece (relaxometria, cinética de traçadores), que tipo de informação a
   priori — peso mínimo, suavidade, modelo paramétrico — é considerada fisicamente legítima para recuperar uma cota
   inferior? (Liga ao Teorema H e à Prop. 3 do rascunho de certificados.)
3. A classificação de ⟨FF⟩ usa CPT só no cone de luz. O senhor conhece um enunciado de livro (Streater–Wightman, BLT,
   Weinberg) que já dê a forma de Källén–Lehmann para um campo tensorial antissimétrico sem supor F=dA? Se sim, o
   resultado é atribuição e eu cito.

## PONTOS EM QUE EU DEVO ADMITIR "ISSO AINDA NÃO ESTÁ FECHADO"
- H3 além da ordem líder para o kernel interagente — **não provada**.
- Transporte ⟨FF⟩ → laço de Wilson → kernel estático (O2), termos de contato/subtrações (O3), setor p²=0.
- Fase de Coulomb: precisa ser hipótese explícita (Proca).
- Três lemas de E2.3b não lidos na fonte; nota não compilada; possível atribuição clássica.
- Critério Z₃: nota não promovida; atribuição aberta (Brown–Weisberger 1979 não lido; Källén 1952 clássico).
- Isolamento de canais carregados vs cortes sem massa.
- Erro de truncamento perturbativo e inferência em dados reais.
- Sinal de δ(r): o artigo define δ com sinal explícito diferente da fórmula escrita por Basile–Golmohammadi; o valor
  numérico coincide com o resultado explícito deles, mas a comparação linha a linha da cadeia potencial→carga está
  pendente (`paper/paper.tex:200-209`).
- α′ = 0 no cone depende do lema de CPT não lido; o teste computacional **impõe** a realidade CPT como entrada, então não
  dizer "CPT verificado por computador".
- Nenhum CI remoto executado; nenhuma revisão humana do PDF; nada submetido nem arbitrado.

## PONTOS QUE POSSO DEFENDER COM SEGURANÇA
- Teorema A é correto **como implicação** H1–H5 ⇒ Φ = Laplace(ν ≥ 0), com prova elementar e pushforward que trata átomos.
- Ordem líder de H3 (Apêndice A) e o sinal, com teste que falha se a convenção for invertida; coeficiente de Uehling.
- Teoremas C, E, H e a lei de borda são matemática correta sobre medidas positivas (clássica na essência; provas no apêndice).
- Os contraexemplos: medida assinada que passa diagnóstico de blindagem; δ₁+eδ₂−e⁹δ₁₀/1000 (verificável a lápis);
  δ₁+δ₂+δ₃−10⁻⁶δ₄ (aprovação finita não é prova); tiny atom.
- Obstrução de escala à inferência WGC só com positividade.
- A álgebra de E2.3b (reduções 4→1 e 4→2, autovalores 2(α±α′)) está verificada por computador a partir da matriz geral.
- Estado numérico: **171 testes pytest aprovados**, reexecutados em 28/09 (os 169 anteriores mais os dois de
  `test_h3_boundary.py`); certificados Arb do benchmark.
