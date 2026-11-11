"""Offline fixtures exercise packet boundaries; they do not represent a real code audit."""
from copy import deepcopy
from pathlib import Path
import json
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from review_packets import make_blind, make_cross, final_gate, ContractError, IDENTITY
from review_mcp import Server

def fixture():
    source = {'task_id': 'fixture', 'document_revision': 'd1', 'repository_revision': 'fixture-revision',
              'draft': 'The fixture parser returns JSON.', 'register': {
                  'field': 'Fixture only', 'tenor': 'Peer', 'mode': 'Markdown', 'genre': 'adapted-test',
                  'dial': 'Compressed', 'template': 'Fixture template', 'task_type': 'audit', 'output_contract': {}}}
    blind = make_blind(source)
    identity = {k: blind[k] for k in IDENTITY}
    judgments = [{**identity, 'phase': 'blind', 'judge': judge, 'evidence_sha256': None,
                  'status': 'COMPLETE', 'verdict': 'PROVISIONAL', 'findings': [],
                  'summary': {'method': 'Fixture; no linguistic scoring performed'}, 'blockers': []}
                 for judge in ('ideational', 'interpersonal', 'textual')]
    evidence = {**identity, 'phase': 'evidence', 'status': 'COMPLETE', 'project': 'fixture', 'tier': 'Verify',
                'graph': {'generation': 'fixture-generation', 'freshness': 'current', 'repository_revision': identity['repository_revision']},
                'scope': ['fixture/parser.py'],
                'queries': [{'tool': 'fixture__check_index_coverage', 'arguments': {'paths': ['fixture/parser.py']}, 'pages_complete': True, 'pagination': {}}],
                'coverage': {'checked': True, 'paths': ['fixture/parser.py'], 'state': 'clean', 'fallback': [], 'unresolved_ranges': []},
                'evidence': [{'id': 'e1', 'kind': 'source', 'location': 'fixture/parser.py:1', 'excerpt': 'return {}', 'claim_ids': ['c1']}],
                'claims': [{'claim_id': 'c1', 'classification': 'supported', 'treatment': 'asserted', 'evidence_refs': ['e1'], 'claim_type': 'positive'}],
                'assumptions': ['Synthetic fixture, not actual repository evidence'], 'blockers': []}
    cross = make_cross(blind, judgments, evidence)
    reviewed = [{**j, 'phase': 'cross_examination', 'evidence_sha256': cross['evidence_sha256'], 'verdict': 'PASS'} for j in judgments]
    gates = {**identity, 'evidence_sha256': cross['evidence_sha256'], 'gates': {
        name: {'status': 'PASS', 'reason': 'Synthetic fixture check'}
        for name in ('process_coverage', 'modality', 'cohesion', 'connectives', 'negative_capability')}}
    return source, blind, judgments, evidence, cross, reviewed, gates

class PacketTests(unittest.TestCase):
    def test_current_complete_cycle_accepts(self):
        _, _, _, _, cross, reviewed, gates = fixture()
        self.assertTrue(final_gate(cross, reviewed, gates)['accepted'])

    def test_blind_allowlist_strips_extra_context(self):
        source, *_ = fixture()
        source.update(evidence_packet={'secret': True}, peer_findings=['leak'], editorial_decisions=['leak'])
        blind = make_blind(source)
        self.assertNotIn('evidence_packet', blind)
        self.assertNotIn('peer_findings', blind)
        self.assertNotIn('editorial_decisions', blind)

    def test_blind_cannot_approve(self):
        _, blind, judgments, evidence, *_ = fixture()
        judgments[0]['verdict'] = 'PASS'
        with self.assertRaises(ContractError):
            make_cross(blind, judgments, evidence)

    def test_duplicate_judge_rejected(self):
        _, blind, judgments, evidence, *_ = fixture()
        judgments[1] = deepcopy(judgments[0])
        with self.assertRaises(ContractError):
            make_cross(blind, judgments, evidence)

    def test_changed_draft_invalidates_hash(self):
        _, blind, judgments, evidence, *_ = fixture()
        blind['draft'] += ' Changed.'
        with self.assertRaises(ContractError):
            make_cross(blind, judgments, evidence)

    def test_stale_judgment_blocks(self):
        _, _, _, _, cross, reviewed, gates = fixture()
        reviewed[0]['document_revision'] = 'd0'
        with self.assertRaises(ContractError):
            final_gate(cross, reviewed, gates)

    def test_changed_evidence_invalidates_digest(self):
        _, _, _, _, cross, reviewed, gates = fixture()
        cross['evidence_packet']['evidence'][0]['excerpt'] = 'Changed evidence'
        with self.assertRaises(ContractError):
            final_gate(cross, reviewed, gates)

    def test_unsupported_assertion_cannot_accept(self):
        _, blind, judgments, evidence, _, reviewed, gates = fixture()
        evidence['claims'][0]['classification'] = 'unsupported'
        cross = make_cross(blind, judgments, evidence)
        for j in reviewed:
            j['evidence_sha256'] = cross['evidence_sha256']
        gates['evidence_sha256'] = cross['evidence_sha256']
        self.assertFalse(final_gate(cross, reviewed, gates)['accepted'])

    def test_negative_claim_requires_auditor(self):
        _, blind, judgments, evidence, _, reviewed, gates = fixture()
        evidence['claims'][0]['claim_type'] = 'negative'
        cross = make_cross(blind, judgments, evidence)
        for j in reviewed:
            j['evidence_sha256'] = cross['evidence_sha256']
        gates['evidence_sha256'] = cross['evidence_sha256']
        self.assertFalse(final_gate(cross, reviewed, gates)['accepted'])

    def test_missing_coverage_rejected(self):
        _, blind, judgments, evidence, *_ = fixture()
        evidence['queries'][0]['tool'] = 'fixture__search_graph'
        with self.assertRaises(ContractError):
            make_cross(blind, judgments, evidence)

    def test_unresolved_gate_cannot_accept(self):
        _, _, _, _, cross, reviewed, gates = fixture()
        gates['gates']['modality']['status'] = 'REVISE'
        self.assertFalse(final_gate(cross, reviewed, gates)['accepted'])

    def test_script_wrapper_works_outside_repository_cwd(self):
        source, blind, *_ = fixture()
        result = subprocess.run([sys.executable, str(ROOT / 'tools/scripts/prepare-blind.py')],
                                input=json.dumps({'source': source}), text=True, capture_output=True, cwd=ROOT.parent, check=True)
        self.assertEqual(json.loads(result.stdout), blind)

    def test_mcp_requires_initialization(self):
        server = Server()
        response = server.handle({'jsonrpc': '2.0', 'id': 1, 'method': 'tools/list'})
        self.assertIn('error', response)

    def test_stdio_mcp_transport_and_validation_error(self):
        source, blind, *_ = fixture()
        messages = [
            {'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {'protocolVersion': '2025-03-26', 'capabilities': {}, 'clientInfo': {'name': 'fixture', 'version': '1.0'}}},
            {'jsonrpc': '2.0', 'method': 'notifications/initialized'},
            {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/list'},
            {'jsonrpc': '2.0', 'id': 3, 'method': 'tools/call', 'params': {'name': 'prepare_blind', 'arguments': {'source': source}}},
            {'jsonrpc': '2.0', 'id': 4, 'method': 'tools/call', 'params': {'name': 'prepare_blind', 'arguments': {}}}]
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/review_mcp.py')],
                                input='\n'.join(map(json.dumps, messages))+'\n', text=True, capture_output=True, cwd=ROOT.parent, check=True)
        replies = {r['id']: r for r in map(json.loads, result.stdout.splitlines())}
        self.assertEqual(len(replies[2]['result']['tools']), 3)
        self.assertEqual(json.loads(replies[3]['result']['content'][0]['text']), blind)
        self.assertTrue(replies[4]['result']['isError'])

if __name__ == '__main__':
    unittest.main()
