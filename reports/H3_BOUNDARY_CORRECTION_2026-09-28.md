# Correção do caso limite no critério de Stieltjes

28 de setembro de 2026. Resultado algébrico exato; não é prova de H3 em QFT.

A nota exploratória `notes/H3_attack_2026-09-24.md` identifica a classe geral
de Stieltjes com a H3 sem subtrações de `paper/paper.tex`, equação H3. Essa
identificação omite a constante permitida na classe geral.

No modelo `rho = Z delta(s-s0)`, ponha `z=Q²`, `c=g_R² Z/s0`. Então

    G(z) = g_R² (s0+z) / [z (s0+(1-c)z)].

Para `0 <= c < 1`, a decomposição é

    G(z) = g_R²/z + [g_R² c/(1-c)]/[z+s0/(1-c)].

O resíduo adicional é não negativo e o polo está deslocado. Em `c=1`,

    G(z) = g_R²/z + g_R²/s0.

É uma função de Stieltjes na definição geral, mas não satisfaz a H3 literal.
De fato, fixado `z0>0`, `1/(z+s) <= 1/(z0+s)` para `z>=z0`; a
integrabilidade de H3 e a convergência dominada dão `G(z) -> 0`.
O exemplo tem limite estritamente positivo. Esse argumento não exige
consultar uma atribuição bibliográfica para verificar o contraexemplo.

No caso crítico geral, escrevendo `d rho` para a medida de matéria,
`Z3=0` implica `G(z)=1/[integral z/(z+s) d rho(s)]`.
Pela convergência monótona seu limite é `1/rho((0,infinito))`, com
`1/infinito=0`. Logo nem todos os casos críticos falham, mas o critério
`Z3>=0` sozinho é insuficiente. Para `Z3>0`,
`0<G(z)<=g_R²/(z Z3)` garante a ausência da constante no infinito.
Isso não resolve o transporte entre correlacionador e resposta estática,
nem substitui a exigência de fase de Coulomb e de suporte apropriado.

A reformulação por funções de Bernstein completas deve carregar a mesma
ressalva: `z G(z)` CBF caracteriza a classe geral de Stieltjes de `G`;
o termo linear de `z G` representa a constante de `G`.

Em três dimensões espaciais, a constante é um contato na origem. É possível
estudar a resposta para `r>0` depois de removê-lo, desde que essa escolha
seja enunciada. H3 no artigo já é escrita sem tal termo; não foi modificada.

Verificação: `tests/test_h3_boundary.py` verifica exatamente as identidades
e o limite, inclusive o resíduo positivo abaixo da fronteira. A definição
geral pode ser conferida em Schilling, Song e Vondraček, *Bernstein Functions*,
capítulo 2; os teoremas 6.2 e 7.3 sustentam a dualidade citada pela nota,
não a remoção automática de contatos. Fonte editorial e erratas:
https://www.motapa.de/bernstein_functions/ . O texto integral do livro não
foi recuperado nesta rodada; a correção acima é independente dessa leitura.
