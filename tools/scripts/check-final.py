#!/usr/bin/env python3
"""JSON stdin/stdout OpenGAP wrapper for check_final."""
from pathlib import Path
import json, sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
from review_mcp import FUNCTIONS, BY_NAME
from jsonschema import validate
def main():
    args = json.load(sys.stdin)
    validate(args, BY_NAME['check_final']['inputSchema'])
    print(json.dumps(FUNCTIONS['check_final'](args), ensure_ascii=False))
if __name__ == '__main__':
    main()
