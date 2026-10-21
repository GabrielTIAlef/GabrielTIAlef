"""SVGs de perfil usando dados públicos, sem token pessoal ou serviços de badges."""
from datetime import date, datetime, timezone
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import os
import re
import tempfile
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
USER = 'GabrielTIAlef'
BG, BORDER, TEXT, MUTED, BLUE, CYAN = '#0d1526', '#23334e', '#eef4ff', '#a4b4cd', '#6495ff', '#56d6db'


class SourceError(ValueError):
    pass


class Calendar(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells, self.tips, self.current = {}, {}, None

    def handle_starttag(self, tag, attributes):
        a = dict(attributes)
        if tag == 'td' and 'data-date' in a:
            self.cells[a['id']] = {'date': a['data-date'], 'level': int(a['data-level'])}
        if tag == 'tool-tip' and 'for' in a:
            self.current = a['for']
            self.tips[self.current] = ''

    def handle_data(self, data):
        if self.current:
            self.tips[self.current] += data

    def handle_endtag(self, tag):
        if tag == 'tool-tip':
            self.current = None


def parse_calendar(content, as_of):
    parser = Calendar()
    parser.feed(content)
    result = []
    for identifier, cell in parser.cells.items():
        day = date.fromisoformat(cell['date'])
        if not date(as_of.year, 1, 1) <= day <= as_of:
            continue
        match = re.fullmatch(r'(No|[\d,]+) contributions? on .+\.', parser.tips.get(identifier, '').strip())
        if not match or not 0 <= cell['level'] <= 4:
            raise SourceError('Formato do calendário público mudou; imagem anterior preservada.')
        count = 0 if match[1] == 'No' else int(match[1].replace(',', ''))
        if (count == 0) != (cell['level'] == 0):
            raise SourceError('Contagem e intensidade do calendário não coincidem.')
        result.append(dict(cell, count=count))
    result.sort(key=lambda x: x['date'])
    expected = (as_of - date(as_of.year, 1, 1)).days + 1
    if len(result) != expected or len({x['date'] for x in result}) != expected:
        raise SourceError('Cobertura incompleta do calendário público.')
    return result


def streaks(days):
    longest, run = 0, 0
    for day in days:
        run = run + 1 if day['count'] > 0 else 0
        longest = max(longest, run)
    # O dia atual ainda pode estar em andamento; admite terminar em ontem.
    position = len(days) - 1
    if position >= 0 and days[position]['count'] == 0:
        position -= 1
    current = 0
    while position >= 0 and days[position]['count'] > 0:
        current += 1
        position -= 1
    return current, longest


def languages(repositories):
    totals = {}
    for repository in repositories:
        for name, size in repository.items():
            if not isinstance(size, int) or size < 0:
                raise SourceError('Estatística de linguagem inválida.')
            totals[name] = totals.get(name, 0) + size
    if not totals or sum(totals.values()) == 0:
        raise SourceError('Não há estatística de linguagens disponível.')
    return dict(sorted(totals.items(), key=lambda pair: (-pair[1], pair[0])))


def svg(width, height, title, body, description=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">'
            f'<title>{escape(title)}</title><desc>{escape(description or title)}</desc>'
            f'<rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="18" fill="{BG}" stroke="{BORDER}"/>'
            '<g font-family="Segoe UI,Arial,sans-serif">' + body + '</g></svg>\n')


def text(x, y, value, size=14, color=TEXT, weight=400):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}">{escape(str(value))}</text>'


def cards(snapshot):
    days, langs, today = snapshot['days'], snapshot['languages'], date.fromisoformat(snapshot['as_of'])
    current, longest = streaks(days)
    total = sum(day['count'] for day in days)
    dated = f'Dados públicos · {today:%d/%m/%Y} UTC'
    stats = text(24, 32, 'GITHUB STATS', 12, CYAN, 700)
    for x, number, label in [(24, snapshot['public_repositories'], 'repositórios públicos'),
                              (220, total, 'contribuições no ano')]:
        stats += text(x, 94, number, 42, TEXT, 700) + text(x, 122, label, 13, MUTED)
    stats += text(24, 161, dated, 11, MUTED)
    language_card = text(24, 32, 'TOP LANGUAGES', 12, CYAN, 700)
    palette = [BLUE, CYAN, '#ba9bfa', '#efb86c', '#d781a5']
    top = list(langs.items())[:4]
    other = sum(langs.values()) - sum(size for _, size in top)
    if other:
        top.append(('Outras', other))
    total_bytes, offset = sum(langs.values()), 24.
    for index, (name, size) in enumerate(top):
        width = 388 * size / total_bytes
        language_card += f'<rect x="{offset:.2f}" y="53" width="{width:.2f}" height="12" fill="{palette[index]}"/>'
        offset += width
        x, y = 24 + (index % 2) * 205, 94 + (index // 2) * 23
        language_card += text(x, y, f'{name} · {100*size/total_bytes:.1f}%', 12, palette[index])
    language_card += text(24, 169, 'Por bytes de código; não mede domínio técnico.', 10, MUTED)
    streak = text(24, 32, f'STREAK · CALENDÁRIO {today.year}', 12, CYAN, 700)
    for x, number, label in [(24, current, 'sequência atual'), (220, longest, 'maior sequência no ano')]:
        streak += text(x, 94, number, 42, TEXT, 700) + text(x, 122, label, 12, MUTED)
    streak += text(24, 161, 'Em dias · considera hoje ou ontem para a sequência atual.', 10, MUTED)
    # Marcos são entregas registradas, nunca certificações ou prêmios oficiais.
    milestones = text(24, 32, 'MARCOS DO PORTFÓLIO', 12, CYAN, 700)
    for x, number, label in [(24, '05', 'projetos com demonstração'), (220, '05', 'projetos com testes e CI')]:
        milestones += f'<path d="M{x+2} 54h22v12q0 13-11 13T{x+2} 66Z M{x+13} 79v9 M{x+5} 89h16" fill="none" stroke="{CYAN}" stroke-width="2"/>'
        milestones += text(x+40, 83, number, 30, TEXT, 700) + text(x, 122, label, 12, MUTED)
    milestones += text(24, 161, 'Entregas verificadas em 20/10/2026 · não são prêmios GitHub.', 10, MUTED)
    activity = text(24, 32, 'ACTIVITY GRAPH · ÚLTIMOS 90 DIAS', 12, CYAN, 700)
    recent = days[-90:]
    maximum = max(1, max(d['count'] for d in recent))
    activity += text(24, 55, 'Contribuições públicas por dia; sem escala de produtividade.', 12, MUTED)
    for i, day in enumerate(recent):
        x = 26 + i * 9.15
        height = day['count'] / maximum * 120
        activity += f'<rect x="{x:.2f}" y="{196-height:.2f}" width="6" height="{max(height, 1):.2f}" rx="2" fill="{CYAN if height else BORDER}"><title>{day["date"]}: {day["count"]}</title></rect>'
    activity += text(24, 225, recent[0]['date'], 11, MUTED) + text(720, 225, recent[-1]['date'], 11, MUTED)
    return {'stats.svg': svg(440, 184, 'GitHub Stats de Gabriel Álef', stats),
            'languages.svg': svg(440, 184, 'Linguagens nos repositórios públicos próprios, por bytes', language_card),
            'streak.svg': svg(440, 184, 'Sequências de contribuições do ano público', streak),
            'milestones.svg': svg(440, 184, 'Marcos técnicos do portfólio; não são certificações', milestones),
            'activity.svg': svg(896, 250, 'Gráfico de contribuições públicas recentes', activity),
            'snake.svg': snake(days, today), 'snake-static.svg': snake(days, today, animated=False)}


def snake(days, today, animated=True):
    body = text(24, 32, f'SNAKE CONTRIBUTION · {today.year}', 12, CYAN, 700)
    palette = ['#17263b', '#174969', '#247a9d', '#45b5c5', '#68e0d4']
    points = []
    first = date.fromisoformat(days[0]['date'])
    # Percurso serpentino no calendário real, sem alterar as quantidades.
    coordinates = []
    week_count = ((date.fromisoformat(days[-1]['date']) - first).days + first.weekday()) // 7 + 1
    spacing = min(18, 830 / week_count)
    for day in days:
        d = date.fromisoformat(day['date'])
        week = ((d - first).days + first.weekday()) // 7
        x, y = 30 + week * spacing, 64 + d.weekday() * 18
        coordinates.append((week, d.weekday(), x+6, y+6))
        body += f'<rect x="{x}" y="{y}" width="12" height="12" rx="3" fill="{palette[day["level"]]}"><title>{day["date"]}: {day["count"]} contribuições</title></rect>'
    for week in sorted({c[0] for c in coordinates}):
        group = sorted([c for c in coordinates if c[0] == week], key=lambda c: c[1], reverse=bool(week % 2))
        points.extend((c[2], c[3]) for c in group)
    path = 'M' + ' L'.join(f'{x},{y}' for x, y in points)
    for index in range(4, -1, -1) if animated else []:
        body += (f'<circle cx="0" cy="0" r="{5 if index else 6}" fill="{BLUE if index else CYAN}" opacity="{1-index*.12}">'
                 f'<animateMotion dur="32s" begin="-{index*.11}s" repeatCount="indefinite" path="{path}"/></circle>')
    body += text(24, 226, f'Calendário público até {today:%d/%m/%Y}; a animação percorre os dias, sem mudar os dados.', 11, MUTED)
    return svg(896, 250, 'Cobra animada sobre as contribuições públicas', body)


def fetch(url):
    headers = {'User-Agent': 'GabrielTIAlef-profile', 'Accept': '*/*'}
    # Token efêmero opcional do próprio Actions, somente na API pública GitHub.
    # Nunca enviar autorização para o HTML do calendário ou serviços de terceiros.
    if url.startswith('https://api.github.com/') and os.getenv('GITHUB_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GITHUB_TOKEN']
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=25) as response:
        return response.read().decode('utf-8')


def collect(as_of):
    # /users/USERNAME/repos lista repositórios públicos; não usar /user/repos.
    repos = json.loads(fetch(f'https://api.github.com/users/{USER}/repos?per_page=100&type=owner'))
    if not isinstance(repos, list) or len(repos) >= 100:
        raise SourceError('Lista de repositórios inesperada; revisar paginação antes de atualizar.')
    own = [r for r in repos if not r['fork'] and r['owner']['login'].casefold() == USER.casefold()]
    data = []
    for repo in own:
        if not re.fullmatch(r'[A-Za-z0-9_.-]+', repo['name']):
            raise SourceError('Nome de repositório não suportado.')
        data.append(json.loads(fetch(f'https://api.github.com/repos/{USER}/{repo["name"]}/languages')))
    html = fetch(f'https://github.com/users/{USER}/contributions?from={as_of.year}-01-01&to={as_of.year}-12-31')
    return {'as_of': as_of.isoformat(), 'username': USER, 'public_repositories': len(own),
            'languages': languages(data), 'days': parse_calendar(html, as_of),
            'scope': 'Somente repositórios públicos próprios e calendário público do ano atual.'}


def write(snapshot):
    output = ROOT / 'assets/metrics'
    output.mkdir(parents=True, exist_ok=True)
    rendered = cards(snapshot)
    # Só preparar imagens após todas as fontes terem sido coletadas e validadas.
    with tempfile.TemporaryDirectory(prefix='profile-metrics-') as directory:
        stage = Path(directory)
        for name, content in rendered.items():
            (stage / name).write_text(content, encoding='utf-8')
        for name in rendered:
            (output / name).write_bytes((stage / name).read_bytes())
    (output / 'snapshot.json').write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    write(collect(datetime.now(timezone.utc).date()))
    print('Indicadores públicos atualizados; nenhum token pessoal necessário.')
