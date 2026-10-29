# Revisão da entrega R0–R3 e próximos passos

23 de outubro de 2026. Revisão de leitura e execução focada; nenhum arquivo
científico foi alterado. Este relatório é posterior ao candidato de 531 arquivos.

## Resultado da conferência

A entrega está substancialmente apoiada pelos arquivos e pelos registros.
As correções de reescala, positividade da sonda, regularidade C1 e prova do
caso crítico estão presentes. A Proposição 3b contém o argumento de limite
de medidas positivas que faltava. Não encontrei uma refutação do coeficiente
E4 nesta revisão; ele deve continuar CHECKED, com a ordem perturbativa explícita.

Execução nova:

```powershell
python -B -m pytest tests/test_three_photon_window.py tests/test_e3_nonlinear_probe.py tests/test_rpa_general_support.py tests/test_reproducibility_driver.py -q -rs
```

Resultado: **65 passed**, em 51,18 s. Esta execução não substitui uma repetição
de toda a suíte nem certifica as hipóteses físicas.

O log da cópia isolada registra 491 testes em 98,47 s; o HEAD dessa cópia é
7035c0a. A lista atual contém 531 arquivos. Comparação byte a byte com a cópia:
somente R3.md está ausente dela; as diferenças são os oito PNG/SVG e
extended_verification.json já documentados. Não houve divergência adicional
nos arquivos científicos comparados. O workflow usa ubuntu-24.04 e a sintaxe
bash de RUNNER_TEMP é adequada. Não executei Ubuntu nem CI remoto nesta revisão.

## Achados que orientam a continuação

### Dois critérios diferentes de janela

O código distingue corretamente r_Gamma=20,70248/m de r_cross=22,60069/m.
O texto de paper/paper.tex, perto das linhas 457–459, usa “controls the profile”
para o primeiro raio, o que torna essa distinção ambígua. Em cálculo novo,
no próprio modelo de termos líderes, r=21/m dá:

- Phi_3gamma/Phi_pair = 0,0760682076434;
- Gamma/m = 1,95812387439.

Portanto o par ainda domina a amplitude, embora a desigualdade Gamma>=2m
já tenha falhado. Nomear os dois critérios e seus dois raios no texto canônico.

Também explicitar a faixa de validade: a extrapolação do termo s^4 até todo s
é uma aproximação assintótica em grandes distâncias. “Para todo r menor que
22,6/m” não é uma conclusão física. Como diagnóstico da extrapolação, o próprio
modelo dá Phi_3gamma/Phi_pair=2,039 em r=0,1/m; esse valor está fora do regime
de baixa energia e não é uma previsão confiável de QED.

### O erro da janela é o principal problema aberto

No termo líder, o peso normalizado em x é proporcional a x^9 exp(-rx).
Logo <s>/m^2=110/(mr)^2. Em mr=20,70248, isso vale 0,25665387.
Nesse peso extrapolado, 0,330365% vem de x>m. Esses números são diagnósticos
do modelo líder; não limitam a densidade verdadeira desconhecida.

A escolha |b|<=2 para a correção rho=K s^4[1+b s/(4m^2)] é uma análise de
sensibilidade, não uma determinação nem uma cota para b. O deslocamento
pequeno dos raios sob essa escolha não é uma barra de erro física.

### A janela pontual não se transfere diretamente a sondas extensas

Para uma sonda radial positiva compacta, F(x)=1+x^2<u^2>/6+O(x^4).
No termo líder de três fótons, a primeira correção relativa de tamanho é
110<u^2>/(6r^2). Uma bola uniforme de raio a=10/m tem <u^2>=3a^2/5;
em r=20,70248/m essa correção vale 2,56654. Não é pequena.

Isso não calcula o novo cruzamento nem invalida o lema exterior. Mostra que
é necessário integrar o fator F completo, para r>a, e controlar a aproximação
espectral; uma expansão truncada em a/r não basta nessa configuração.

### Uma qualificação residual na interpretação RPA

A prova da Proposição 3b é geral, mas a interpretação nas linhas 270–272
fala em um átomo superior como se ele sempre existisse. Qualificar essa
imagem pelo suporte limitado e pelo regime em que tal átomo existe.
Para eta(ds)=exp(-s)ds em [1,infinito), há massa total e momento inverso
finitos e nenhum intervalo acima do suporte inteiro. O limite crítico ainda
tem a constante positiva 1/mu, sem exigir um átomo superior isolado.
O argumento de compactificação de medidas permanece válido.

## Ordem recomendada de execução

1. **Consolidar as afirmações.** Corrigir a ambiguidade dos dois raios e a
   faixa assintótica; qualificar a interpretação do átomo. Explicitar que a
   identificação da densidade 1PI com a medida usada na resposta é feita à
   ordem perturbativa adotada. Preservar CHECKED e a distinção entre corrente
   clássica e operador quântico. Aceitação: cada afirmação aponta para sua
   hipótese e para o cálculo correspondente.

2. **Prioridade de física: controlar a janela E4.** Calcular o termo s^5 da
   amplitude com uma perna fora da camada de massa, incluindo os operadores
   derivativos relevantes, ou obter uma avaliação independente da amplitude
   completa de uma volta gamma* -> 3gamma. Separar a integral em baixa energia
   e complemento, com escala de separação explícita; variar essa escala e
   registrar o erro ou a parte não controlada. Acrescentar as correções do
   canal de pares de forma consistente, sem duplicar contribuições Coulombianas.

   O alvo quantitativo é D(r)=M1(r)-2m M0(r), cujo sinal determina
   Gamma-2m quando M0>0. Um limite |delta rho(s)|<=B(s) implica
   |delta D|<=integral |sqrt(s)-2m| exp(-r sqrt(s)) B(s) ds.
   Para declarar uma janela robusta, produzir extremos com sinais de D que
   sobrevivam ao erro total. Se só houver sensibilidades, manter CHECKED e
   informar exatamente quais termos continuam sem limite.

3. **Conectar E3 e E4.** Recalcular os dois critérios para as sondas compactas
   com F completo. Depois variar a carga da sonda para comparar o termo
   linear de três fótons com a resposta não linear EH. Não usar os raios
   pontuais para afirmar a janela experimental das sondas de raio 10/m.
   Aceitação: resultados discriminados por raio, perfil, carga e erro de EFT.

4. **Revisar o coeficiente e a novidade em paralelo lógico.** A rota A é
   reconstrução exata em uma base polinomial simétrica: tornar explícita a
   completude dessa base e o posto da interpolação, além das identidades de
   Ward e do fator de partículas idênticas. A rota B deve conservar o mapa
   de corrente, pernas e normalização. Fazer busca dirigida por densidade
   espectral QED de quatro voltas, corte de três fótons e expansão de baixa
   energia; ausência em buscas não demonstra novidade. Esta frente não deve
   bloquear o estudo do erro da janela.

5. **Fechar a reprodução do candidato final.** Após estabilizar as correções,
   gerar nova lista e hashes; incluir este relatório somente por decisão de
   escopo. Testar em Ubuntu quando disponível, preservando a comparação
   científica exata. Deriva exige diagnóstico antes de escolher tolerâncias.
   CI remoto continua pendente até existir autorização para publicar o commit.
   Não iniciar o launcher antigo nem outro escritor concorrente.

Brown–Weisberger e revisão humana permanecem tarefas documentais/humanas
separadas. A leitura daquele trabalho pode esclarecer a interpretação da
linha estática, mas não resolve o erro de truncamento de E4 nem substitui a
construção quântica ainda aberta.

## Fontes primárias conferidas nesta revisão

- Groote–Pivovarov, equações (6), (7), (13)–(15):
  https://arxiv.org/pdf/hep-ph/0103313 . A substituição no funcional e a
  diferenciação em relação à fonte dão suporte à distinção de contagem de
  pernas usada na nota; a nova execução reproduziu os testes das duas rotas.
- Beneke–Ruiz-Femenia, nota de rodapé 1 e equações (5)–(8):
  https://arxiv.org/pdf/1606.02434 . Confirma o início do corte em s=0 na ordem
  alpha^4 e o escopo da aproximação de limiar. Não fornece uma cota para o
  resto usado na janela de E4.

Nenhuma nova alegação de originalidade ou certificação do coeficiente foi feita.
