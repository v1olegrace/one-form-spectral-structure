# Auditoria severa de E2c — 2 de outubro de 2026

## Escopo e estado anterior ao patch

Esta auditoria foi escrita antes de qualquer alteração científica desta rodada.
HEAD no início: `0becf85e2e36407b2ec0b37cdc800f43b820823e`. O worktree já tinha
alterações alheias a E2c em `reproducibility/canonical_pdf_qa.py` e
`tests/test_pdf_qa_record.py`, além de arquivos não rastreados; foram
preservados. Não consultei fontes primárias nesta etapa. A ponte de continuação,
a classificação de E2b e a literatura do vácuo estocástico continuam sujeitas
à verificação bibliográfica independente.

## Defeitos confirmados

### E2c-1 — fator 2 extra na fórmula de contorno

**Gravidade:** alta para a derivação publicada; o código numérico usa o fator
correto. **Arquivo/linhas:** `notes/E2c_transport_linear_probe.md:101-113`;
docstring de `boundary_cumulant` em `reproducibility/transport_linear_probe.py`;
teste de Stokes em `tests/test_e2c_transport.py`.

Para cada par de lados horizontais, as duas auto-interações e as duas
interações cruzadas dão, antes do fator global (1/2),
\(2\int_{-T}^{T}(T-|u|)[a(u,0)-a(u,r)]du\). Portanto, depois de multiplicar
por (1/2), o coeficiente da integral bilateral é **1**. O mesmo vale para os
lados verticais. Usando paridade, a forma equivalente é
\(2\int_0^T(T-u)[a(u,0)-a(u,r)]du\), mais o termo vertical análogo.

Reprodução independente anterior ao patch, com \(a(\rho)=e^{-\rho^2}\),
\(T=2\), \(r=0.7\): a implementação retorna `1.431780191197684`; a expressão
literal impressa na nota, com `2` multiplicando cada integral bilateral,
retorna `2.863560382395367`. A razão é exatamente `2`. O teste existente
confirma a integral de superfície contra a função de contorno implementada,
mas não compara o resultado com a fórmula bilateral impressa; por isso não
detecta o erro.

**Impacto:** a Lemma 2, lida literalmente, não é igual à identidade de Stokes
nem ao código/teste. **Correção mínima:** remover o `2` externo das integrais
bilaterais (ou manter a forma unilateral `2 integral_0^...`) e adicionar um
teste independente que compare a integral bilateral publicada com essa forma
de quatro lados. **Confiança:** alta; contagem orientada dos quatro lados e
reprodução numérica concordam.

### E2c-2 — a taxa mistura limite regulado e não regulado e omite \(q_W^2\)

**Gravidade:** alta para a afirmação da taxa; a fórmula do limite principal
continua separada. **Arquivo/linhas:** `notes/E2c_transport_linear_probe.md:115-149`
e `:251-266`; `tests/test_e2c_transport.py`, teste
`test_static_limit_and_its_measured_rate`.

A prova e o teste trabalham com \(a_\varepsilon\) a \(\varepsilon>0\) fixo; o
teste usa \(q_W=1\). O enunciado escreve \(C(r)\), sem índice do regulador e
sem o fator \(q_W^2\), embora \(V_T\) seja definido para carga arbitrária e
\(V_T-V_\infty\) seja proporcional a essa carga. O coeficiente sustentado
pelas contas é
\[
 V_{T,\varepsilon}(r)-V_{\infty,\varepsilon}(r)
 =\frac{q_W^2 C_\varepsilon(r)}{T}+o_\varepsilon(T^{-1}),
\]
onde ambas as integrais que definem \(C_\varepsilon\) usam \(a_\varepsilon\).

Também não há limite finito uniforme de \(C_\varepsilon\) quando o regulador
é removido. Para uma massa unitária \(\mu=\delta_{s=0}\), o regulador usado
no código dá
\(a_\varepsilon(\rho)=(1-e^{-\rho^2/(4\varepsilon)})/(4\pi^2\rho^2)\).
Então o termo curto \(2\int_0^r(r-v)a_\varepsilon(v)dv\) cresce como
\(r/(2\pi^2\sqrt{\varepsilon})\); o outro termo da taxa permanece finito.
Uma reprodução numérica em \(r=1\) dá \(C_{.01}=0.20599\),
\(C_{.001}=1.06014\), \(C_{.0001}=4.01340\). Isso não contradiz a ordem de
limites \(T\to\infty\) antes de \(\varepsilon\to0\); mostra que a taxa não
pode ser transportada ao limite UV sem prova uniforme.

**Impacto:** a frase de taxa sem subscritos promete uma expansão mais forte
que a verificada e o fator de carga está ausente. **Correção mínima:** declarar
taxa apenas a \(\varepsilon>0\) fixo, incluir \(q_W^2\) e \(C_\varepsilon\),
e retirar qualquer leitura de uniformidade na remoção do regulador. **Confiança:**
alta; decorre da própria prova e da fórmula do kernel regulado.

### E2c-3 — lei de área do contato local não é uma tensão física finita

**Gravidade:** alta para a interpretação física. **Arquivo/linhas:**
`notes/E2c_transport_linear_probe.md:191-199`,
`reproducibility/transport_linear_probe.py` (rotinas do termo local),
`tests/test_e2c_transport.py` (teste de inclinação),
`paper/appendix.tex:176-182`, `paper/professor_brief.tex:98-106`.

O teste mede, a regulador fixo, a contribuição do contato local \(cG\):
\(\sigma_\varepsilon=q_W^2c/(8\pi\varepsilon)\), além da correção finita em
\(T\). A inclinação diverge como \(1/\varepsilon\) quando o regulador é
removido. Isso confirma uma contribuição de área **regulada**, não uma tensão
de corda finita. A estrutura local \(G\delta^{(4)}(x)\) também não pode ser
identificada automaticamente com a função não local \(D(x^2)G\) da
decomposição do vácuo estocástico.

**Impacto:** a coincidência de estrutura tensorial não prova identidade entre
um contato UV e a função de correlação de alcance finito que dá tensão no
modelo estocástico. **Correção mínima:** chamar o primeiro de contato local
regulador-dependente, registrar sua divergência e separar a discussão de
\(D(x^2)\); não reivindicar tensão física finita. **Confiança:** alta para a
divergência; a identificação bibliográfica da função \(D\) requer fonte primária.

## Lacunas documentais e de escopo confirmadas

### E2c-4 — a continuação Wightman–Euclides ainda está embutida como se fosse consequência

**Gravidade:** bloqueia a alegação geral “Wightman W1–W3 basta”; não demonstra
que o resultado condicional Euclidiano seja falso. **Arquivo/linhas:**
`notes/E2c_transport_linear_probe.md:18-62, 173-187`;
`paper/appendix.tex:118-158`; `README.md:25-28, 154-164`.

A nota reconhece que os lemas de E2b e a continuação não foram conferidos, mas
passa de W1–W3 para uma função de dois pontos Euclidiana com representação
espectral. Sem localizar e checar a hipótese exata que permite essa passagem
para o campo considerado, a derivação não sustenta a alegação em W1–W3 apenas.
Não afirmo aqui que localidade seja necessariamente requerida; o ponto é que a
continuação sem localidade não foi estabelecida neste checkout.

**Impacto:** o texto público parece concluir a ponte a partir de axiomas que
não foram demonstrados suficientes. **Correção mínima:** enunciar como premissa
explícita a representação Euclidiana positiva de \(\langle FF\rangle\) com
\(\mu\ge0\), e deixar Wightman \(\to\) Euclides como caminho condicional em
aberto até checagem da fonte. **Confiança:** alta quanto à lacuna documental;
nenhuma conclusão de impossibilidade.

### E2c-5 — “positividade + Bianchi” omite entradas e promove a H3 completa

**Gravidade:** alta para resumo público. **Arquivo/linhas:** `README.md:25-28,
154-164`; `paper/paper.tex:256-273`; `paper/professor_brief.tex:64-69,
117-125`; o ledger C10 em `scripts/build_audit_tables.py` e
`data/claims_matrix.csv`.

A própria nota exige representação Euclidiana/classificação espectral positiva,
integrabilidade \((I)\), Bianchi no produto ordenado incluindo coincidências,
regime linear \((L)\), e uma massa de Coulomb \((C)\) para normalizar o perfil.
O H3 canônico do paper também exige resíduo de Coulomb estritamente positivo e
um gap \(s_*>0\). A medida transportada pode ter contínuo acumulando em zero,
sem átomo de Coulomb ou com termo de contato; essas propriedades não saem da
representação genérica.

**Impacto:** os resumos “segue de positividade e Bianchi” e “deriva H3”
escondem premissas e confundem representação positiva com a H3 completa.
**Correção mínima:** reportar primeiro a representação espectral estática;
identificar a H3 canônica somente sob a hipótese separada de átomo de Coulomb,
gap e integrabilidade. **Confiança:** alta; as hipóteses estão escritas no
próprio paper.

### E2c-6 — “o termo seguinte é \(O(q_W^4)\)” pressupõe cumulantes ímpares nulos

**Gravidade:** média, por escopo. **Arquivo/linhas:**
`notes/E2c_transport_linear_probe.md:58-62, 185-203, 278-280`;
`paper/appendix.tex:183-186`; `paper/professor_brief.tex:64-69`.

A expansão de \(\log\langle e^{iq_W X}\rangle\) é em cumulantes conectados.
Depois do termo quadrático, pode haver um cumulante conectado cúbico, a menos
que simetria de conjugação de carga ou outra condição de paridade do estado
elimine cumulantes ímpares. O termo de quatro campos é conectado e de ordem
\(q_W^4\); chamá-lo automaticamente de “espalhamento luz-luz” também precisa
de hipótese sobre a dinâmica do campo.

**Impacto:** “fora da ordem linear” não implica “o próximo termo é luz-luz de
ordem quatro”. **Correção mínima:** formular o resultado do laço como
truncamento no cumulante quadrático e dizer que o cumulante conectado de quatro
campos contribui em \(q_W^4\); explicitar que a eliminação de termos ímpares
exige simetria apropriada. **Confiança:** alta, pela expansão cumulante geral.

## Limites das verificações atuais

Os testes e o módulo exercitam medidas atômicas finitas escolhidas à mão,
integrais reguladas, identidades tensoriais simbólicas e alguns valores de
parâmetros. Eles não certificam: a desintegração covariante de medidas
temperadas gerais; continuação Wightman–Euclides; restrições de distribuições
às superfícies/linhas infinitas; produtos ordenados e termos de contato em uma
teoria geral; o limite para medida com massa total infinita ou suporte
acumulando em zero; ou todos os passos da prova. A frase “Every algebraic and
numerical step is machine-checked” em `notes/E2c_transport_linear_probe.md:12`
é mais ampla que a cobertura real.

A linha infinita formal envolve \(\delta(p_0)/p_1\); para convertê-la em
\(p_1/(p_1-i0)=1\), o produto deve ser definido como distribuição contra uma
classe especificada de funções. As identidades simbólicas atuais não provam
essa definição nem independência de superfície para distribuições gerais.
Manter a conta da linha como condicional ao regularizador e à identidade de
Bianchi no produto Euclidiano, sem chamá-la de prova geral independente.

O caso de medida geral segue sem prova além da hipótese \((I)\); a derivação
numérica para somas de massas não é contraexemplo nem prova para o caso geral.
Também não se inferiu qualquer resultado sobre existência de QED em quatro
dimensões, resposta não linear, QCD não abeliana, H3 sem gap, nem a novidade da
transportação espectral.

## Resultado da tentativa de refutação

O fator 2 é um erro algébrico demonstrado. A omissão de \(\varepsilon\) e
\(q_W^2\) invalida a formulação não qualificada da taxa, embora a taxa a
regulador fixo seja compatível com a conta e com o teste para \(q_W=1\). A
transportação até o kernel estático continua defensável como resultado
condicional à representação Euclidiana positiva, a \((I)\), a Bianchi no
produto com contatos e à resposta quadrática/linear correspondente. A ponte
desde axiomas Wightman sem localidade, a H3 canônica com Coulomb e gap, e a
generalização além dos exemplos não foram fechadas por esta auditoria.
