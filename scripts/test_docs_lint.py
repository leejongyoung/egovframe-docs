import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name('docs_lint.py')


class DocsLintInlineCodeTest(unittest.TestCase):
    def lint(self, content, files=(), source=False, test_source=False):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / 'docs'
            docs.mkdir()
            (docs / 'README.md').write_text(content, encoding='utf-8')
            for name in files:
                (docs / name).write_text('# Target\n', encoding='utf-8')
            command = [sys.executable, str(SCRIPT), str(docs), '--json']
            if source:
                java = root / 'src/main/java/example/Existing.java'
                java.parent.mkdir(parents=True)
                java.write_text('package example; class Existing {}', encoding='utf-8')
                command.extend(['--src', str(root / 'src')])
            if test_source:
                if not source:
                    java = root / 'src/main/java/org/egovframe/Existing.java'
                    java.parent.mkdir(parents=True)
                    java.write_text('package org.egovframe; class Existing {}', encoding='utf-8')
                    command.extend(['--src', str(root / 'src')])
                sample = root / 'src/test/java/org/egovframe/vo/OnlyInTest.java'
                sample.parent.mkdir(parents=True)
                sample.write_text('package org.egovframe.vo; class OnlyInTest {}', encoding='utf-8')
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            return json.loads(result.stdout)['findings']

    def broken_links(self, content, files=()):
        return [item['msg'] for item in self.lint(content, files) if item['rule'] == 'L2']

    def test_real_links_are_still_checked(self):
        findings = self.broken_links('[정상](target.md) [누락](missing.md)', ['target.md'])
        self.assertEqual(['상대링크 대상 부재: missing.md'], findings)

    def test_inline_link_and_image_examples_are_ignored(self):
        content = '`[이름](missing.md)`와 `![이미지](missing.png)` [실제](real.md)'
        self.assertEqual(['상대링크 대상 부재: real.md'], self.broken_links(content))

    def test_matching_backtick_runs_and_unmatched_delimiters(self):
        content = '``예시 ` [이름](example.md) ``와 `닫히지 않은 [실제](real.md)'
        self.assertEqual(['상대링크 대상 부재: real.md'], self.broken_links(content))

    def test_code_in_link_label_does_not_hide_the_link(self):
        self.assertEqual(['상대링크 대상 부재: missing.md'],
                         self.broken_links('[`코드`](missing.md)'))

    def test_escaped_backticks_and_fenced_code(self):
        content = '\\`[실제](real.md)\\`\n\n```markdown\n[예시](example.md)\n```\n'
        self.assertEqual(['상대링크 대상 부재: real.md'], self.broken_links(content))

    def test_class_references_in_inline_code_are_still_checked(self):
        findings = self.lint('`egovframework.example.EgovMissing`', source=True)
        self.assertIn('L5', [item['rule'] for item in findings])

    def rules(self, findings, rule):
        return [item['msg'] for item in findings if item['rule'] == rule]

    def test_class_only_in_test_sources_is_informational_not_l5(self):
        findings = self.lint('`org.egovframe.vo.OnlyInTest`', test_source=True)
        self.assertEqual([], self.rules(findings, 'L5'))
        self.assertEqual(['테스트 소스에만 있는 참조: org.egovframe.vo.OnlyInTest'],
                         self.rules(findings, 'L5-test'))

    def test_class_missing_everywhere_is_still_l5(self):
        findings = self.lint('`org.egovframe.vo.Nowhere`', test_source=True)
        self.assertEqual(['실소스 부재 참조: org.egovframe.vo.Nowhere'], self.rules(findings, 'L5'))
        self.assertEqual([], self.rules(findings, 'L5-test'))

    def test_class_in_main_sources_has_no_finding(self):
        findings = self.lint('`org.egovframe.Existing`', test_source=True)
        self.assertEqual([], self.rules(findings, 'L5') + self.rules(findings, 'L5-test'))


if __name__ == '__main__':
    unittest.main()
