from datetime import date
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import update_metrics as metrics


def html(counts):
    parts = []
    for i, count in enumerate(counts, start=1):
        parts.append(f'<td id="d{i}" data-date="2026-01-{i:02d}" data-level="{1 if count else 0}"></td>')
        label = 'No contributions' if not count else f'{count} contribution' + ('s' if count > 1 else '')
        parts.append(f'<tool-tip for="d{i}">{label} on January {i}th.</tool-tip>')
    return ''.join(parts)


class MetricsTests(unittest.TestCase):
    def test_counts_come_from_tooltips_not_color_level(self):
        days = metrics.parse_calendar(html([0, 24, 1]), date(2026, 1, 3))
        self.assertEqual([d['count'] for d in days], [0, 24, 1])

    def test_missing_day_rejected_not_filled_with_zero(self):
        with self.assertRaises(metrics.SourceError):
            metrics.parse_calendar(html([1, 2]), date(2026, 1, 3))

    def test_missing_tooltip_rejected(self):
        with self.assertRaises(metrics.SourceError):
            metrics.parse_calendar('<td id="d" data-date="2026-01-01" data-level="1"></td>', date(2026, 1, 1))

    def test_future_days_do_not_affect_current_counts(self):
        days = metrics.parse_calendar(html([2, 4, 10]), date(2026, 1, 2))
        self.assertEqual(sum(d['count'] for d in days), 6)

    def test_streak_counts_days_not_contributions(self):
        self.assertEqual(metrics.streaks([{'count': n} for n in [0, 5, 25, 1]]), (3, 3))

    def test_current_day_grace_without_resetting_yesterday(self):
        self.assertEqual(metrics.streaks([{'count': n} for n in [1, 1, 0]]), (2, 2))

    def test_two_empty_days_end_streak(self):
        self.assertEqual(metrics.streaks([{'count': n} for n in [1, 1, 0, 0]]), (0, 2))

    def test_languages_sum_bytes(self):
        self.assertEqual(metrics.languages([{'Python': 100}, {'Python': 50, 'HTML': 60}]), {'Python': 150, 'HTML': 60})

    def test_invalid_language_bytes_rejected(self):
        with self.assertRaises(metrics.SourceError): metrics.languages([{'Python': -1}])

    def test_no_languages_is_not_a_fake_percent(self):
        with self.assertRaises(metrics.SourceError): metrics.languages([{}])

    def test_snapshot_renders_valid_safe_svg(self):
        snapshot = json.loads((ROOT / 'assets/metrics/snapshot.json').read_text(encoding='utf-8'))
        rendered = metrics.cards(snapshot)
        self.assertEqual(len(rendered), 7)
        for name, content in rendered.items():
            with self.subTest(name=name):
                document = ET.fromstring(content)
                self.assertTrue(document.tag.endswith('svg'))
                self.assertNotIn('<script', content)
                self.assertNotIn('<foreignObject', content)

    def test_optional_token_is_only_sent_to_github_api(self):
        class Response:
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def read(self): return b'{}'
        with patch.dict('os.environ', {'GITHUB_TOKEN': 'invented-test-token'}):
            with patch.object(metrics.urllib.request, 'urlopen', return_value=Response()) as request:
                metrics.fetch('https://github.com/users/GabrielTIAlef/contributions')
                self.assertIsNone(request.call_args.args[0].get_header('Authorization'))
                metrics.fetch('https://api.github.com/users/GabrielTIAlef/repos')
                self.assertEqual(request.call_args.args[0].get_header('Authorization'), 'Bearer invented-test-token')


if __name__ == '__main__':
    unittest.main()
