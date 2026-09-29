# Correções e validação — 23 de setembro de 2026

Escopo: manuscrito canônico em `paper/`, implementação numérica e evidências
reproduzíveis. Os diretórios preexistentes `base_cientifica/`, `laplace/` e
`reports/memoria_viole_2026-09-14/` foram preservados. Não houve commit, push
ou publicação. Relatórios antigos são registros históricos, não o status atual.

## Problemas corrigidos

1. **Localizador ausente.** A medida δ1 + e δ2 − e⁹ δ10/1000 dava momentos
   reescalados (1.999, 2.99, 4.9, 8), det H0 = .855 e det H1 = −.09.
   A versão anterior aceitava os dados e retornava B1 ≈ −.0644645.
   Agora G3 rejeita H1 indefinida, inclusive em chamada direta a
   `falsification_suite.hankel_bound`. **Correção posterior (v0.3a):** havia uma
   segunda função homônima, `laplace_geometry.hankel_bound`, sem filtro nenhum,
   e ela é a do caminho canônico de certificação. O filtro foi extraído para
   `reproducibility/moment_conditions.py` e agora as duas o aplicam. Ver
   `reports/REVIEW_CLAUDE_2026-09-23.md`, achado A1.
2. **Escopo do filtro.** A aprovação se chama `CHECKED_COMPATIBLE`: condições
   necessárias finitas. O exemplo δ1 + δ2 + δ3 − 10⁻⁶ δ4 passa em ordem 5 e
   falha em ordem 7. Positividade global e H3 não são certificadas pelo filtro.
3. **Posto e precisão.** Medida positiva com poucos átomos pode gerar H0 singular.
   A recusa é `UNRESOLVED_RANK_OR_PRECISION`. Não se fabrica um limite nem se
   afirma refutação física; ordem menor, precisão maior ou redução de posto
   são necessários. Redução automática de posto não foi implementada.
4. **Enunciados.** Inclusão de suporte foi separada de borda efetiva; limiar
   acoplado de limiar carregado; perda do gap H2 de perda de positividade.
   Medida não nula, caso atômico finito, lei de borda e inferência com precisão
   finita receberam as hipóteses explícitas correspondentes.
5. **Gravidade.** A implicação condicional tem agora sua cadeia de desigualdades
   e as hipóteses sobre espécies leves, cauda e erro; o teto de uma espécie
   foi demonstrado no apêndice canônico. Isso não constitui prova da WGC.
6. **Proveniência numérica.** A contagem fixa de 40 integrais "únicas" foi
   substituída por 40 avaliações / 28 entradas distintas. Reintegrações são
   deduplicadas pelos parâmetros completos e todas as ocorrências são
   comparadas; metadados conflitantes são recusados. O verificador liga raios
   e parâmetros à configuração e recusa execução com assertions desativadas.
   **Correções posteriores (v0.3a):** os contadores foram renomeados para o que
   de fato contam (`source_enclosure_evaluations` = 40 chamadas a
   `certify_sample`; `distinct_source_enclosures` = 28), e as 12 integrais de
   benchmark e as 40 checagens independentes em mpmath passaram a ser contadas
   separadamente — antes "40 avaliações" podia ser lido como o total de
   quadraturas. O verificador ganhou as checagens de completude que faltavam:
   cardinalidades, produto cartesiano datasets × graus × cortes e bijeção dos
   índices de certificado. Achados A2 e A4 do parecer de revisão.
7. **Reprodutibilidade editorial.** Datas/IDs variáveis dos SVG foram removidos;
   terminologia de certificação numérica corrigida; inventários apontam para
   as provas corretas. O rascunho não inventa URL de publicação ou DOI.

## Evidências verificadas

A coluna "v0.3" é a evidência original desta remediação, executada por Codex.
A coluna "v0.3a" foi executada por Claude depois de unificar as guardas e
completar o verificador; os números que mudaram estão em **negrito**.

| Verificação | v0.3 (Codex) | v0.3a (Claude) |
|---|---|---|
| pytest com Tectonic no PATH | 121 aprovados, zero omitidos | **169 aprovados**, zero omitidos |
| Pipeline numérico | exit 0 | exit 0 (duas execuções) |
| Análise estendida | 52 verificações aprovadas | **70 verificações aprovadas** |
| Falsificação | 21 verificações aprovadas, FATAL=0, FAIL=0 | 21 aprovadas, FATAL=0, FAIL=0 |
| Geometria de Laplace | todas aprovadas | todas aprovadas, **incluindo o filtro em cada (r,K)** |
| Backend Arb | 12 conjuntos, 144 comparações, 288 certificados verificados | idem, `configuration_sha256` inalterado |
| Reintegração | 28/28 amostras distintas; quatro pares modelo/raio | idem **+ 12/12 benchmarks, cardinalidades, produto cartesiano e bijeção de índices** |
| Contadores de proveniência | 40 avaliações / 28 distintas | idem, **renomeados e todos recomputados pelo verificador** |
| SVG | quatro arquivos idênticos byte a byte em regeneração | idem, reconfirmado em duas execuções consecutivas |
| PDF canônico v0.3 | 12 páginas; sem avisos LaTeX/BibTeX ou caixas excedentes | **não recompilado**: os 6 hashes de fonte e o hash do PDF continuam iguais |
| Fontes PDF | Type0 e Type1; nenhuma Type3 | inalterado (mesmo PDF) |
| Inspeção visual | todas as 12 páginas inspecionadas; sem cortes ou sobreposições observados | não repetida; o PDF é bit a bit o mesmo |

O teste de compilação usa uma cópia temporária do diretório `paper/`.
A inspeção visual por Codex é distinta de revisão humana ou parecer de
especialista; nenhuma dessas revisões humanas foi declarada concluída.
`output/data/canonical_pdf_qa.json` registra o hash do PDF, das fontes e do log.
O script de QA não declara aprovação visual por conta própria.

Ambiente: Windows 11, Python 3.13.7, mpmath 1.3.0, NumPy 2.3.5, SciPy 1.15.3,
SymPy 1.13.1, python-flint 0.9.0, Tectonic 0.17.0 portátil.
O binário foi obtido da distribuição oficial do Tectonic e seu SHA-256 foi
comparado ao digest publicado na API de releases:
`f61ce51f0b0ade1015b7de7ef368541c5424e9756ecbd0d7af97d6d48030845f` (ZIP MSVC).

## Reexecutar no PowerShell deste ambiente

```powershell
$env:PYTHONIOENCODING='utf-8'
$env:PATH=(Resolve-Path 'tmp/tools/tectonic-0.17.0').Path+';'+$env:PATH
$env:FONTCONFIG_FILE=(Resolve-Path 'tmp/tools/tectonic-0.17.0/fonts.conf').Path
python make.py all
python make.py certified
python reproducibility/verify_one_loop_output.py --reintegrate --no-write
python make.py pdf
python reproducibility/canonical_pdf_qa.py --render-dir tmp/pdfs/review
```

Use `python -m pytest tests -q`, não `python -m pytest` na raiz: a cópia de
trabalho não rastreada em `laplace/` tem nomes de teste colidentes e quebra a
coleta. As duas últimas linhas só são necessárias se as fontes em `paper/`
mudarem; para confirmar que não mudaram, compare os hashes gravados em
`output/data/canonical_pdf_qa.json` com os arquivos atuais.

O compilador portátil fica em `tmp/`, não é versionado. Em outra máquina,
instale Tectonic no PATH ou use pdflatex/bibtex. A QA de PDF requer PyMuPDF.
O PDF entregue está em `output/pdf/spectral_structure_v03.pdf`; `make.py pdf`
gera `paper/paper.pdf`. Os dois caminhos têm papéis distintos e explícitos.

## Obrigações científicas que permanecem abertas

- Derivar H3 além da ordem líder para o kernel físico, ou restringir o domínio
  de aplicação com uma hipótese controlada. A nota E2b não conclui essa ponte.
- Justificar Wilson loop, limite estático, termos de contato e subtrações ao
  transportar a medida de ⟨FF⟩ para o kernel de resposta.
- Demonstrar quando se pode isolar canais carregados preservando positividade.
- Quantificar erro perturbativo e controlar inferência em dados físicos
  desconhecidos. Envelopes sintéticos não são cobertura estatística empírica.
- Concluir leituras primárias pendentes antes de elevar atribuições, novidade
  ou lemas de E2b ao status de verificação bibliográfica concluída.
- CI remoto e revisão humana continuam sem execução verificada nesta sessão.
- Redução automática de posto continua não implementada: a recusa
  `UNRESOLVED_RANK_OR_PRECISION` é o comportamento correto, não a solução.

Essas obrigações não foram apresentadas como resolvidas por correções de código.
A revisão v0.3a mexeu em guardas, contadores e testes; nenhum enunciado
científico, teorema ou hipótese foi alterado por ela. A rota concreta sugerida
para a primeira obrigação está no fim de `reports/REVIEW_CLAUDE_2026-09-23.md`,
registrada como proposta, não como resultado.
