#!/usr/bin/env python3
"""Validate portable definitions and cross-file contracts without network or inference."""
from pathlib import Path
import json
import re
import sys
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return yaml.safe_load(path.read_text())

def validate(root=ROOT):
    counts = {k: 0 for k in ('agents', 'tools', 'skills', 'workflows', 'knowledge')}
    errors = []

    def require(ok, message):
        if not ok:
            errors.append(message)

    def schema(kind, value, path):
        spec = json.loads((root / 'schemas/opengap' / (kind + '.schema.json')).read_text())
        for error in Draft202012Validator(spec).iter_errors(value):
            errors.append(f'{path.relative_to(root)}: {list(error.path)}: {error.message}')

    manifests = [root / 'agent.yaml', *sorted((root / 'agents').glob('*/agent.yaml'))]
    roster = {}
    for path in manifests:
        data = load(path)
        roster[data['name']] = data
        base = path.parent
        schema('agent-yaml', data, path)
        counts['agents'] += 1
        require(data['name'] == base.name, f'{path}: name/directory mismatch')
        for name in ('SOUL.md', 'RULES.md', 'PROMPT.md'):
            require((base / name).is_file() and bool((base / name).read_text().strip()), f'{path}: missing {name}')
        require((base / 'PROMPT.md').read_text().strip() in (base / 'SOUL.md').read_text(), f'{path}: output contract omitted from exportable SOUL.md')
        for skill in data.get('skills', []):
            require((base / 'skills' / skill / 'SKILL.md').is_file(), f'{path}: missing skill {skill}')
        for tool in data.get('tools', []):
            require((base / 'tools' / (tool + '.yaml')).is_file(), f'{path}: missing tool {tool}')
        for tool in sorted((base / 'tools').glob('*.yaml')):
            tool_data = load(tool)
            schema('tool', tool_data, tool)
            require(tool_data['name'] == tool.stem, f'{tool}: name mismatch')
            implementation = tool_data.get('implementation', {})
            if implementation.get('type') == 'script':
                require((tool.parent / implementation['path']).is_file(), f'{tool}: missing implementation')
            counts['tools'] += 1
        for skill in sorted((base / 'skills').glob('*/SKILL.md')):
            front = yaml.safe_load(skill.read_text().split('---', 2)[1])
            schema('skill', front, skill)
            require(front['name'] == skill.parent.name, f'{skill}: name mismatch')
            counts['skills'] += 1
        if data['name'].endswith('-judge'):
            require(not data.get('tools') and not data.get('skills') and not data.get('agents') and not data.get('mcp_servers'), f'{path}: judge gained capability')
            embedded = re.findall(r'```json\n(.*?)\n```', (base / 'PROMPT.md').read_text(), re.S)
            require(len(embedded) == 1 and json.loads(embedded[0]) == json.loads((root / 'schemas/judgment.schema.json').read_text()), f'{path}: inline judgment schema drift')
        if base != root:
            require('compliance' not in data, f'{path}: duplicated root policy')

    parent = load(root / 'agent.yaml')
    dirs = {p.name for p in (root / 'agents').iterdir() if p.is_dir()}
    require(set(parent['agents']) == dirs, 'declared agent roster differs from child directories')
    sod = parent['compliance']['segregation_of_duties']
    roles = {r['id'] for r in sod['roles']}
    require(set(sod['assignments']) == set(roster), 'SOD assignments do not cover exactly the roster')
    for agent, assigned in sod['assignments'].items():
        require(set(assigned) <= roles, f'{agent}: unknown SOD role')
        for a, b in sod['conflicts']:
            require(a in roles and b in roles, 'unknown conflict role')
            require(not {a, b} <= set(assigned), f'{agent}: conflicting SOD assignments')
    assigned_roles = {r for values in sod['assignments'].values() for r in values}
    for handoff in sod['handoffs']:
        require(set(handoff['required_roles']) <= assigned_roles, 'handoff requires unassigned role')
    for path in sorted((root / 'workflows').glob('*.yaml')):
        flow = load(path)
        schema('workflow', flow, path)
        steps = {s['id']: s for s in flow['steps']}
        require(len(steps) == len(flow['steps']), f'{path}: duplicate step IDs')
        declared_inputs = {i['name'] for i in flow.get('inputs', [])}
        visiting, visited = set(), set()

        def visit(step_id):
            require(step_id in steps, f'{path}: missing dependency {step_id}')
            if step_id not in steps or step_id in visited:
                return
            if step_id in visiting:
                errors.append(f'{path}: dependency cycle at {step_id}')
                return
            visiting.add(step_id)
            for dependency in steps[step_id].get('depends_on', []):
                visit(dependency)
            visiting.remove(step_id)
            visited.add(step_id)

        def ancestors(step_id):
            found, pending = set(), list(steps[step_id].get('depends_on', []))
            while pending:
                item = pending.pop()
                if item not in found and item in steps:
                    found.add(item)
                    pending.extend(steps[item].get('depends_on', []))
            return found

        for sid, step in steps.items():
            visit(sid)
            kinds = [k for k in ('agent', 'tool', 'skill') if k in step]
            require(len(kinds) == 1, f'{sid}: exactly one execution binding required')
            if 'agent' in step:
                require(step['agent'] in parent['agents'], f'{sid}: missing agent')
            if 'tool' in step:
                require(step['tool'] in parent['tools'], f'{sid}: missing tool')
            if 'skill' in step:
                require(step['skill'] in parent['skills'], f'{sid}: missing skill')
            for expression in re.findall(r'\$\{\{\s*(.*?)\s*\}\}', json.dumps(step)):
                if expression.startswith('inputs.'):
                    require(expression[7:] in declared_inputs, f'{sid}: unknown input {expression}')
                    continue
                match = re.fullmatch(r'steps\.([a-z0-9-]+)\.outputs\.([a-z0-9_]+)', expression)
                require(bool(match), f'{sid}: unsupported reference {expression}')
                if match:
                    dependency, output = match.groups()
                    require(dependency in ancestors(sid), f'{sid}: reference without dependency: {expression}')
                    require(output in steps.get(dependency, {}).get('outputs', []), f'{sid}: undeclared output {expression}')
        counts['workflows'] += 1

    index = root / 'knowledge/index.yaml'
    schema('knowledge', load(index), index)
    for document in load(index)['documents']:
        require((index.parent / document['path']).is_file(), f'{index}: missing knowledge file')
        counts['knowledge'] += 1
    for path in (root / 'schemas').glob('*.schema.json'):
        Draft202012Validator.check_schema(json.loads(path.read_text()))
    require(not (root / '.gitagent').exists(), 'runtime state must not be authored')
    require('.gitagent/' in (root / '.gitignore').read_text(), 'runtime state must be ignored')
    require(not (root / 'plugin.json').exists(), 'legacy manifest is active at root')
    if errors:
        raise ValueError('\n'.join(errors))
    return counts

if __name__ == '__main__':
    try:
        print(json.dumps({'valid': True, 'checked': validate()}, indent=2))
    except (ValueError, KeyError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
