#!/usr/bin/env python3
"""JSON stdin/stdout OpenGAP wrapper for prepare_blind."""
from pathlib import Path
import json, sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
from review_mcp import FUNCTIONS, BY_NAME
from jsonschema import validate
def main():
    args = json.load(sys.stdin)
    validate(args, BY_NAME['prepare_blind']['inputSchema'])
    print(json.dumps(FUNCTIONS['prepare_blind'](args), ensure_ascii=False))
if __name__ == '__main__':
    main()
