"""Cards editoriais do portfólio, com o mesmo formato por viewport."""
from pathlib import Path
from textwrap import wrap
from update_metrics import svg, text, BORDER, TEXT, MUTED, BLUE, CYAN

PROJECTS = [
    dict(slug='gestao_geral', name='Gestão Geral', area='Integração e BI operacional',
         problem='Como consolidar tarefas e cadastros para acompanhar uma operação?',
         knowledge='Integração de fontes, ETL e indicadores operacionais, com resultado corporativo relatado.',
         stack='PYTHON / SQL / POSTGRESQL / APIs / POWER BI',
         scope='Experiência corporativa + demonstração pública sintética'),
    dict(slug='gestao_financeira', name='Gestão Financeira', area='Modelagem e BI financeiro',
         problem='Como organizar informações financeiras sem perder lançamentos ou duplicar títulos?',
         knowledge='Modelagem dimensional, chaves de negócio e reconciliação para BI.',
         stack='PYTHON / PANDAS / SQL / POSTGRESQL / POWER BI',
         scope='Experiência profissional + demonstração pública sintética'),
    dict(slug='automacao_financeira', name='Automação Financeira', area='Integração e automação financeira',
         problem='Como combinar recebíveis automáticos e acompanhamento manual?',
         knowledge='Integração de APIs, preservação de informações e recuperação de falhas.',
         stack='PYTHON / APIs / CONTA AZUL / NOTION / POSTGRESQL',
         scope='Experiência profissional + demonstração pública sintética'),
    dict(slug='analises_marketing', name='Análises de Marketing', area='Análise exploratória e segmentação',
         problem='Como descrever perfis de clientes e avaliar uma segmentação?',
         knowledge='Análise exploratória, KMeans, sensibilidade e interpretação dos grupos.',
         stack='PYTHON / PANDAS / SCIKIT-LEARN / MATPLOTLIB / JUPYTER',
         scope='Estudo analítico · versão pública com dados fictícios'),
    dict(slug='bolsa_valores', name='Bolsa de Valores', area='Séries temporais e análise de risco',
         problem='Como comparar séries sem confundir preço, retorno e risco?',
         knowledge='Indicadores temporais, SQL e comunicação de resultados descritivos.',
         stack='PYTHON / PANDAS / NUMPY / SQLITE / JUPYTER',
         scope='Estudo analítico · ativos e resultados da demo fictícios'),
    dict(slug='agente_inteligencia_operacional', name='Agente de Inteligência Operacional', area='BI, automação e IA aplicada',
         problem='Como conectar perguntas operacionais, indicadores, monitoramento e IA?',
         knowledge='Análise de negócio, PostgreSQL, BI e uso de ferramentas restritas no assistente.',
         stack='PYTHON / SQL / FASTAPI / REACT / GEMINI / N8N',
         scope='Projeto autoral · cenário e pedidos sintéticos'),
]


def lines(body, value, y, width, size, color=MUTED, weight=400, step=21):
    for line in wrap(value, width=width, break_long_words=False, break_on_hyphens=False):
        body += text(24, y, line, size, color, weight)
        y += step
    return body


def render(project, index, mobile=False):
    width, height = (440, 410) if mobile else (896, 300)
    body = text(24, 29, f'{index:02d} / {project["area"].upper()}', 10, CYAN, 700)
    if mobile:
        title = wrap(project['name'], width=27, break_long_words=False)
        for line, y in zip(title, [68, 98]):
            body += text(24, y if len(title)>1 else 82, line, 27, TEXT, 700)
        body += text(24, 127, 'PROBLEMA', 10, CYAN, 700)
        body = lines(body, project['problem'], 150, 49, 14)
        body += text(24, 225, 'CONHECIMENTO DEMONSTRADO', 10, CYAN, 700)
        body = lines(body, project['knowledge'], 248, 49, 14)
        body += f'<path d="M24 315H416" stroke="{BORDER}"/>'
        body = lines(body, project['stack'], 338, 57, 10, BLUE, 600, 17)
        body = lines(body, project['scope'], 383, 56, 10, MUTED, step=14)
    else:
        body += text(24, 74, project['name'], 32, TEXT, 700)
        body += text(24, 110, 'PROBLEMA', 10, CYAN, 700)
        body = lines(body, project['problem'], 132, 105, 16)
        body += text(24, 179, 'CONHECIMENTO DEMONSTRADO', 10, CYAN, 700)
        body = lines(body, project['knowledge'], 201, 105, 16)
        body += f'<path d="M24 234H872" stroke="{BORDER}"/>'
        body += text(24, 257, project['stack'], 11, BLUE, 600)
        body += text(24, 282, project['scope'], 11, MUTED)
        body += text(842, 74, '↗', 24, CYAN)
    description = ' '.join(project[key] for key in ('name','problem','knowledge','stack','scope'))
    return svg(width, height, project['name'], body, description)


def build_project_cards(assets: Path):
    folder = assets / 'cards'
    folder.mkdir(parents=True, exist_ok=True)
    for index, project in enumerate(PROJECTS, 1):
        for mobile in (False, True):
            suffix = '-mobile' if mobile else ''
            (folder/(project['slug']+suffix+'.svg')).write_text(render(project,index,mobile),encoding='utf-8')
