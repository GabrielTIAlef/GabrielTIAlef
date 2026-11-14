# Perfil: conteúdo, critérios e manutenção

Proposta visual inicial de 21/10/2026. Revisão dos cards, tecnologias e resultados preparada localmente em 13/11/2026; esta nova revisão aguarda autorização para publicação.

## Direção visual e posicionamento

Azul escuro, azul claro e ciano, com cards desenhados para estes projetos. Banner, typing animation, cards, rodapé e indicadores são SVGs locais, sem JavaScript, fontes remotas ou HTML dentro de SVG. Versões compactas atendem celular; a animação de texto tem alternativa para movimento reduzido.

O texto prioriza trabalho em Dados/BI: integrações, SQL, Python, modelagem, indicadores e confiabilidade. Analytics Engineering é apresentado como interesse profissional, não como cargo já ocupado. Não foram acrescentados cloud, dbt, Airflow, anos de experiência, empregador atual ou certificações que não estejam comprovados.

Nome, e-mail, LinkedIn e portfólio foram recuperados do README atual. Formação e contexto profissional também constam dos materiais fornecidos. A redução de cinco dias para menos de cinco minutos é atribuída ao relato de experiência no Gestão Geral, sem transformá-la em benchmark público.

## Contexto de mercado consultado

As vagas públicas abaixo pedem combinações de SQL, Python, Power BI e modelagem. Foram usadas como referência de apresentação, não como comprovação de senioridade ou garantia de contratação:

- [Vibra — Analista de Dados Pl](https://vibraenergia.gupy.io/jobs/12300304?jobBoardSource=gupy_public_page)
- [GOL — Analista de Dados II](https://golcarreiras.gupy.io/jobs/12323205?jobBoardSource=gupy_public_page)

As vagas podem mudar ou encerrar. O perfil mostra as competências por meio de projetos e evidências, sem inserir palavras-chave como experiência que Gabriel não declarou.

## Projetos e formato dos cards

Os sete projetos aparecem juntos, sem tabela duplicada ou separação entre casos
profissionais e estudos. Cada imagem é um link para seu repositório. A distinção
de contexto aparece no próprio card.

Os cards usam 896 × 300 no desktop e 440 × 410 no celular. Todos têm título,
área, problema, conhecimento demonstrado, tecnologias e contexto. As variações
mobile conservam a mesma informação, com quebras adequadas à largura.

`scripts/project_cards.py` concentra textos e desenho. `scripts/build_assets.py`
reconstrói os SVGs locais usando esse módulo. Não há contagens de testes nos
novos cards: os registros de validação continuam nos projetos de origem.

A ordem é Gestão Geral, Agente de Inteligência Operacional, DatAtlas, Gestão
Financeira, Automação Financeira, Análises de Marketing e Bolsa de Valores.
DatAtlas foi incluído em terceiro por solicitação do titular em 13/11/2026.
O conteúdo deriva dos READMEs e decisões já apresentados no portfólio. As
integrações corporativas e os painéis no Power BI Desktop não são homologados
pelas demonstrações sintéticas.

## Resultados e tecnologias

Os resultados profissionais foram conferidos nos materiais de carreira
fornecidos pelo autor: consolidação de aproximadamente cinco dias para cinco
minutos; 15 dashboards, seis gerenciais; contribuição para redução aproximada
de 70% da inadimplência; contribuição para desistências próximas de zero no
fluxo reestruturado; integração de quatro sistemas; indicadores de gestão;
modelagem e migração de transformações; e entregas de dados/web nos estágios.

São relatos profissionais, sem logs empresariais publicados. Resultados de
cobrança e onboarding são apresentados como contribuição junto às equipes.
Os números não são atribuídos aos testes ou aos dados sintéticos do GitHub.

As tecnologias são agrupadas em dados/bancos, BI, análise/visualização,
integração/automação, IA/API/interface e ambiente/testes. Os projetos atuais
sustentam as bibliotecas e ferramentas de demonstração. MySQL, Power Platform
e Google Sheets aparecem separadamente como experiência/formação documentada.
O uso da VM Oracle descreve a implantação da demo, sem alegação de especialização
cloud. Não foram acrescentados AWS, Azure, GCP, Spark, dbt ou Airflow.

Os badges são arquivos locais, com URLs registradas em
`assets/badges/sources.json`. Rótulos sem marca disponível permanecem textuais;
não se inventam logos ou certificações. Currículos e documentos pessoais não
foram copiados para o repositório.

## Adaptação do prompt visual

- Banner personalizado e rodapé: próprios, com variação de tamanho para celular.
- Typing animation: SVG local com frases compatíveis com os projetos, sem depender de endpoint externo.
- Tecnologias com ícones: SVGs do Shields.io preparados como arquivos locais. Origem e URLs registradas em assets/badges/sources.json. Alguns rótulos podem aparecer sem logo quando o catálogo do serviço não contém a marca; não foram atribuídos logos de outras tecnologias.
- Projetos: sete cards próprios e clicáveis, do mesmo tamanho por viewport, com problema, conhecimento, stack e contexto.
- GitHub Stats: contagem de repositórios públicos próprios sem forks e contribuições do calendário público do ano.
- Top Languages: soma de bytes retornados pelo GitHub em repositórios públicos próprios sem forks. Inclui o portfólio, não só os projetos de dados. Percentual não mede proficiência, tempo de trabalho ou relevância de SQL/DAX/Power BI.
- Streak: dias consecutivos com contribuição pública no ano mostrado; maior sequência também restrita a esse ano, não recorde de toda a conta. A sequência atual pode terminar ontem se hoje ainda estiver zerado. Dia sem contribuição não mede desempenho profissional.
- Activity Graph: últimas 90 datas disponíveis do ano público, ou menos no início do ano. Sem extrapolar datas, preencher falhas de fonte ou interpretar intensidade como produtividade.
- GitHub Trophies: adaptado para marcos reais do portfólio. Os dois emblemas não são prêmios oficiais, certificações ou ranking de desenvolvedor. Serviços convencionais de trophy/activity retornaram HTTP 402 na conferência; não foram embutidos como imagens quebradas.
- Snake Contribution: animação própria que percorre os dias do calendário público do ano. Não altera os números, fabrica contribuições ou simula atividade profissional.
- Redes: LinkedIn, e-mail e portfólio já existentes; nenhum contato novo foi inventado.

## Fontes e atualização dos indicadores

`scripts/update_metrics.py` consulta apenas:

- API pública `GET /users/GabrielTIAlef/repos`, sem o endpoint privado `/user/repos`;
- bytes de linguagens dos repositórios públicos próprios;
- página pública de contribuições do ano civil, de janeiro até a data UTC da atualização.

Não utiliza PAT, credenciais corporativas ou dados privados. A coleta local inicial foi sem autenticação. No Actions, o GITHUB_TOKEN efêmero é enviado somente para api.github.com, para reduzir limites de requisições; não vai para o HTML do calendário, Shields ou terceiros. O snapshot versionado contém somente dados públicos e a data da consulta.

A extração exige cobertura diária completa do período e tooltips com contagens exatas; níveis de cor não são tratados como número de contribuições. Se a estrutura da página mudar, a atualização falha antes de substituir imagens. As imagens locais anteriores continuam legíveis. Não há garantia de atualização se GitHub estiver indisponível, se limites forem excedidos ou se o workflow estiver desativado.

O workflow foi preparado para atualização diária às 06:23 UTC (03:23 em São Paulo na data da preparação), além de acionamento manual e mudanças relevantes na main. A validação em PR é somente leitura; o job que faz commit só roda na main, em contexto confiável, com contents:write. Ele publica apenas assets/metrics, assina como github-actions[bot] e não força push. Uma alteração concorrente pode rejeitar o push; o workflow não sobrescreve a main à força.

Publicar este workflow significa autorizar futuros commits automáticos desses indicadores. Se não quiser atualização, remova schedule ou desative o workflow; o README continua usando a última imagem disponível. O token padrão e as regras do repositório precisam permitir o job de escrita. Não é necessário cadastrar segredo pessoal.

## Reprodução local

Python 3.12, somente biblioteca padrão:

```bash
python scripts/build_assets.py
python -m unittest discover -s tests -v
python scripts/update_metrics.py
```

O último comando precisa de internet. Não execute coleta apenas para rodar os testes: eles usam fixtures e o snapshot público já versionado. Nenhum script publica ou faz push localmente. A publicação diária é uma etapa explícita do workflow no GitHub.

## Referências técnicas

- [GitHub: README do perfil](https://docs.github.com/en/account-and-profile/concepts/personal-profile)
- [GitHub Readme Stats: limites do endpoint público e geração por Actions](https://github.com/anuraghazra/github-readme-stats#github-actions)
- [Readme Typing SVG: referência do recurso visual](https://github.com/DenverCoder1/readme-typing-svg)
- [GitHub Profile Trophy: referência do recurso adaptado](https://github.com/ryo-ma/github-profile-trophy)
- [Snake: referência do tipo de visualização](https://github.com/Platane/snk)

Os SVGs e o código desta proposta foram criados para o perfil; não copiam os geradores dos projetos de referência.

## DatAtlas

O card apresenta análise exploratória, qualidade, recortes e IA com cálculo local.
As tecnologias acrescentadas são Recharts, Ruff, ESLint e Playwright, declaradas
no código/manifestos do DatAtlas. Não foram acrescentados resultados empresariais
a partir da demonstração. Os seis cards anteriores mantêm o conteúdo e o tamanho;
a numeração foi atualizada para refletir a nova ordem.

## Formação atualizada em 14/11/2026

Por informação direta do titular: Tecnólogo em Ciência de Dados na Gran Faculdade,
iniciado em novembro de 2026, com conclusão estimada em novembro de 2028.
A estimativa decorre da duração informada, sem confirmação do calendário oficial.
A formação concluída em Análise e Desenvolvimento de Sistemas permanece.
A apresentação atual não inclui o MBA anterior como formação em andamento.
