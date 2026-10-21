"""Identidade visual própria em SVG, sem imagens geradas ou fontes externas."""
from html import escape
from pathlib import Path
from update_metrics import svg, text, BG, BORDER, TEXT, MUTED, BLUE, CYAN

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = [
    ('gestao_geral', 'Gestão Geral', 'Integração de dados operacionais',
     ['APIs, ETL e PostgreSQL em um fluxo só.', 'Validação de cargas e demonstração reproduzível.'], 'PYTHON / SQL / POSTGRESQL / APIs', 72),
    ('gestao_financeira', 'Gestão Financeira', 'ETL e modelagem dimensional',
     ['Carga transacional, chaves de negócio', 'e reconciliação de dados financeiros.'], 'PANDAS / SQL / POSTGRESQL', 55),
    ('automacao_financeira', 'Automação Financeira', 'Integrações e confiabilidade',
     ['Conta Azul, Notion e controle de falhas.', 'Dados fictícios e efeitos externos simulados.'], 'PYTHON / APIs / AUTOMAÇÃO', 65),
    ('analises_marketing', 'Análises de Marketing', 'Segmentação exploratória de clientes',
     ['KMeans com comparação e estabilidade.', 'Notebook, perfis e métricas documentadas.'], 'PANDAS / SCIKIT-LEARN / KMEANS', 43),
    ('bolsa_valores', 'Bolsa de Valores', 'Análise temporal e SQL',
     ['Indicadores com fórmulas verificadas.', 'SQLite e Python com valores reconciliados.'], 'PYTHON / SQLITE / SÉRIES TEMPORAIS', 61)
]


def build():
    assets = ROOT / 'assets'
    (assets / 'cards').mkdir(parents=True, exist_ok=True)
    banner = '''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="350" viewBox="0 0 1280 350" role="img">
<title>Gabriel Álef — Analista de Dados, BI e Automação</title>
<desc>Python, SQL e Power BI. Integração de fontes, bases analíticas e indicadores.</desc>
<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#0a1120"/><stop offset="1" stop-color="#13233c"/></linearGradient>
<pattern id="grid" width="38" height="38" patternUnits="userSpaceOnUse"><path d="M38 0H0V38" fill="none" stroke="#7ca6de" stroke-opacity=".06"/></pattern></defs>
<rect width="1280" height="350" rx="24" fill="url(#bg)"/><rect width="1280" height="350" rx="24" fill="url(#grid)"/>
<rect x="48" y="48" width="4" height="34" rx="2" fill="#56d6db"/>
<g font-family="Segoe UI,Arial,sans-serif"><text x="72" y="71" fill="#56d6db" font-size="15" font-weight="600" letter-spacing="3">DADOS / BI / AUTOMAÇÃO</text>
<text x="48" y="164" fill="#eef4ff" font-size="69" font-weight="700" letter-spacing="-2">Gabriel Álef</text>
<text x="50" y="207" fill="#bdcce2" font-size="23">Python, SQL e Power BI para rotinas que funcionam.</text>
<text x="50" y="289" fill="#8ba3c5" font-size="13" letter-spacing="2">01 / INTEGRAR</text><text x="245" y="289" fill="#8ba3c5" font-size="13" letter-spacing="2">02 / ORGANIZAR</text><text x="465" y="289" fill="#8ba3c5" font-size="13" letter-spacing="2">03 / ANALISAR</text>
<path d="M906 102H986V158H1080V239H1180" fill="none" stroke="#56d6db" stroke-width="2" stroke-opacity=".6"/>
<path d="M862 239H946V214H1037V100H1180" fill="none" stroke="#6495ff" stroke-width="2" stroke-opacity=".5"/>
<rect x="854" y="74" width="100" height="64" rx="12" fill="#172941" stroke="#355173"/><text x="879" y="113" fill="#56d6db" font-size="19" font-weight="600">API</text>
<rect x="991" y="130" width="100" height="64" rx="12" fill="#172941" stroke="#355173"/><text x="1015" y="169" fill="#9dbbff" font-size="19" font-weight="600">SQL</text>
<rect x="1109" y="211" width="100" height="64" rx="12" fill="#172941" stroke="#355173"/><text x="1145" y="250" fill="#eef4ff" font-size="19" font-weight="600">BI</text>
<circle cx="946" cy="214" r="5" fill="#6495ff"/><circle cx="1080" cy="100" r="5" fill="#56d6db"/>
</g></svg>'''
    (assets / 'banner.svg').write_text(banner, encoding='utf-8')
    mobile = (text(28, 43, 'DADOS / BI / AUTOMAÇÃO', 13, CYAN, 700)
              + text(26, 125, 'Gabriel Álef', 58, TEXT, 700)
              + text(28, 173, 'Python, SQL e Power BI', 23, MUTED)
              + text(28, 207, 'para rotinas que funcionam.', 23, MUTED)
              + text(28, 275, 'INTEGRAR  /  ORGANIZAR  /  ANALISAR', 12, BLUE, 600))
    (assets / 'banner-mobile.svg').write_text(svg(640, 310, 'Gabriel Álef — Dados, BI e Automação', mobile), encoding='utf-8')
    phrases = ['Integrações, ETL e automação com Python.', 'SQL e modelagem para bases analíticas.', 'Power BI e indicadores ligados à operação.']
    (assets / 'typing-static.svg').write_text(svg(896, 56, phrases[0], text(24, 35, phrases[0], 20, CYAN)), encoding='utf-8')
    (assets / 'typing-static-mobile.svg').write_text(svg(440, 56, phrases[0], text(24, 35, phrases[0], 16, CYAN)), encoding='utf-8')
    typing = '<style>.static{display:none}@media(prefers-reduced-motion:reduce){.animated{display:none}.static{display:inline}}</style>'
    typing += '<g class="static">' + text(24, 35, phrases[0], 20, CYAN) + '</g>'
    opacity = ['1;1;0;0;0;0;1', '0;0;1;1;0;0;0', '0;0;0;0;1;1;0']
    for i, phrase in enumerate(phrases):
        typing += (f'<defs><clipPath id="clip{i}"><rect x="24" y="0" width="820" height="55">'
                   f'<animate attributeName="width" values="0;820;820;0;0" keyTimes="0;.2;.25;.3;1" begin="{i*5}s" dur="15s" repeatCount="indefinite"/></rect></clipPath></defs>'
                   f'<g class="animated" opacity="{1 if i == 0 else 0}"><animate attributeName="opacity" values="{opacity[i]}" keyTimes="0;.30;.33;.63;.66;.96;1" dur="15s" repeatCount="indefinite"/>'
                   f'<g clip-path="url(#clip{i})">' + text(24, 35, phrase + '  ▍', 20, CYAN) + '</g></g>')
    (assets / 'typing.svg').write_text(svg(896, 56, 'Integrações, modelagem e BI — texto animado', typing), encoding='utf-8')
    (assets / 'typing-mobile.svg').write_text(svg(440, 56, 'Integrações, modelagem e BI — texto animado',
        typing.replace('font-size="20"', 'font-size="16"').replace('820', '392')), encoding='utf-8')
    for index, (slug, name, category, lines, stack, count) in enumerate(PROJECTS):
        hero = index == 0
        width = 896 if hero else 440
        body = text(24, 31, f'0{index+1} / {category.upper()}', 10, CYAN, 700)
        body += text(24, 78, name, 34 if hero else 24, TEXT, 700)
        for y, line in zip([111, 132], lines):
            body += text(24, y, line, 14, MUTED)
        body += f'<path d="M24 155H{width-24}" stroke="{BORDER}"/>'
        body += text(24, 180, stack, 10, BLUE, 600)
        body += text(24, 203, f'{count} testes · validação em 20/10/2026', 12, MUTED)
        body += text(width-43, 78, '↗', 23, CYAN)
        if hero:
            body += text(626, 100, 'ETL', 48, BLUE, 700) + text(628, 132, 'da fonte à base analítica', 14, MUTED)
        (assets / 'cards' / (slug + '.svg')).write_text(svg(width, 220, f'{name}: {category}. {count} testes registrados.', body), encoding='utf-8')
        if hero:
            mobile_card = (text(24, 31, '01 / INTEGRAÇÃO DE DADOS', 10, CYAN, 700)
                           + text(24, 78, name, 28, TEXT, 700)
                           + text(24, 111, 'APIs, ETL e PostgreSQL em um fluxo só.', 14, MUTED)
                           + text(24, 132, 'Cargas validadas e demo reproduzível.', 14, MUTED)
                           + text(24, 180, stack, 10, BLUE, 600)
                           + text(24, 203, f'{count} testes · validação em 20/10/2026', 12, MUTED))
            (assets / 'cards/gestao_geral-mobile.svg').write_text(svg(440, 220, name, mobile_card), encoding='utf-8')
    footer = text(24, 32, 'GABRIEL ÁLEF', 12, CYAN, 700) + text(24, 59, 'Dados, BI e automação. Vamos conversar sobre o próximo projeto?', 15, MUTED)
    footer += '<path d="M650 48h45l13-13 22 23 14-10h126" fill="none" stroke="#6495ff" stroke-width="2"/>'
    (assets / 'footer.svg').write_text(svg(896, 85, 'Gabriel Álef — contato e projetos de dados', footer), encoding='utf-8')
    (assets / 'footer-mobile.svg').write_text(svg(440, 100, 'Gabriel Álef — vamos conversar',
        text(24, 28, 'GABRIEL ÁLEF', 12, CYAN, 700) + text(24, 56, 'Dados, BI e automação.', 17, MUTED)
        + text(24, 81, 'Vamos conversar sobre o próximo projeto?', 15, MUTED)), encoding='utf-8')
    print('Banner, animação, cinco cards e rodapé gerados.')


if __name__ == '__main__':
    build()
