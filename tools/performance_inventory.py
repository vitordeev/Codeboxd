"""Offline source inventory; never imports the app or reads configuration."""
import ast
import argparse
import hashlib
import json
from pathlib import Path


def expression(node):
    return ast.unparse(node) if node is not None else ''


def inventory(root):
    root = Path(root)
    files = []
    routes = []
    functions = []
    bindings = []
    for path in sorted((root / 'Codeboxd_main').rglob('*.py')):
        source = path.read_text(encoding='utf-8-sig')
        tree = ast.parse(source)
        relative = path.relative_to(root).as_posix()
        files.append({'path': relative, 'sha256': hashlib.sha256(source.encode()).hexdigest()})

        class Visitor(ast.NodeVisitor):
            def __init__(self):
                self.scope = []

            def visit_ClassDef(self, node):
                self.scope.append(node.name)
                self.generic_visit(node)
                self.scope.pop()

            def visit_FunctionDef(self, node):
                self.record_function(node)

            def visit_AsyncFunctionDef(self, node):
                self.record_function(node)

            def record_function(self, node):
                self.scope.append(node.name)
                # Nested functions are separate entries, avoiding attribution to parents.
                calls = []
                class Calls(ast.NodeVisitor):
                    def visit_FunctionDef(self, child):
                        pass
                    visit_AsyncFunctionDef = visit_FunctionDef
                    def visit_Call(self, child):
                        calls.append({'line': child.lineno, 'target': expression(child.func),
                                      'arguments': [expression(arg) for arg in child.args],
                                      'keywords': {kw.arg or '**': expression(kw.value) for kw in child.keywords}})
                        self.generic_visit(child)
                collector = Calls()
                for statement in node.body:
                    collector.visit(statement)
                functions.append({'file': relative, 'name': '.'.join(self.scope),
                                  'line': node.lineno,
                                  'decorators': [expression(d) for d in node.decorator_list],
                                  'calls': sorted(calls, key=lambda c: c['line'])})
                self.generic_visit(node)
                self.scope.pop()

            def visit_Call(self, node):
                if expression(node.func) == 'app.add_page':
                    keywords = {kw.arg: kw.value for kw in node.keywords}
                    routes.append({'file': relative, 'line': node.lineno,
                                   'route': ast.literal_eval(keywords['route']),
                                   'component': expression(node.args[0]),
                                   'on_load': expression(keywords.get('on_load'))})
                for keyword in node.keywords:
                    if keyword.arg and keyword.arg.startswith('on_'):
                        bindings.append({'file': relative, 'line': node.lineno,
                                         'function': '.'.join(self.scope),
                                         'trigger': keyword.arg,
                                         'handler': expression(keyword.value)})
                self.generic_visit(node)

        Visitor().visit(tree)
    return {'schema_version': 1, 'layer': 'static-source-analysis',
            'limitations': ['Calls are syntactic possibilities, not runtime counts.',
                            'Dynamic dispatch, inheritance, generated setters and callback arguments require manual interpretation.',
                            'No server, browser, network or credentials are used.'],
            'files': files, 'routes': routes, 'bindings': bindings, 'functions': functions}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = inventory(Path(__file__).resolve().parents[1])
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: len(result[key]) for key in ('files', 'routes', 'bindings', 'functions')}))
