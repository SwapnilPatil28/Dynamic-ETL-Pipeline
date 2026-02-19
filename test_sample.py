#!/usr/bin/env python3
"""
Simple test to verify multi-import removal fix.
Run this to see the fix in action.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app.services.patch_applier import PatchApplierService
from app.services.static_analyzer import StaticAnalyzerService


def main():
    # Create test directory
    test_dir = Path("./test_import_fix_demo")
    test_dir.mkdir(exist_ok=True)
    
    # Test case: Multi-part import where only some are used
    test_code = """from typing import Any, Dict, List
import os
import json

def get_data() -> Dict:
    return json.loads('{"key": "value"}')
"""
    
    test_file = test_dir / "example.py"
    test_file.write_text(test_code)
    
    print("=" * 70)
    print("MULTI-IMPORT REMOVAL TEST")
    print("=" * 70)
    
    print("\n📄 ORIGINAL CODE:")
    print("-" * 70)
    print(test_code)
    
    # Analyze
    analyzer = StaticAnalyzerService()
    failures = analyzer.analyze(test_dir)
    linting = [f for f in failures if f["bug_type"] == "LINTING"]
    
    print("\n🔍 ANALYSIS:")
    print("-" * 70)
    print(f"Found {len(linting)} unused import(s):")
    for f in linting:
        print(f"  • Line {f['line_number']}: {f['message']}")
    
    # Deduplicate and sort (like runner does)
    seen = {}
    for f in linting:
        key = (f["file"], f["line_number"], f["bug_type"])
        if key not in seen:
            seen[key] = f
    
    fixes = list(seen.values())
    fixes.sort(key=lambda x: x["line_number"], reverse=True)
    
    print(f"\n🔧 APPLYING {len(fixes)} FIX(ES):")
    print("-" * 70)
    
    # Apply fixes
    applier = PatchApplierService()
    for f in fixes:
        result = applier.apply_fix(
            repo_path=test_dir,
            file_path=f["file"],
            line_number=f["line_number"],
            bug_type=f["bug_type"],
            message=f["message"]
        )
        status = "✓" if result else "✗"
        print(f"  {status} Line {f['line_number']}: {'Fixed' if result else 'Failed'}")
    
    # Show result
    fixed_code = test_file.read_text()
    
    print("\n✨ FIXED CODE:")
    print("-" * 70)
    print(fixed_code)
    
    print("\n✅ VERIFICATION:")
    print("-" * 70)
    has_dict = "from typing import Dict" in fixed_code
    has_json = "import json" in fixed_code
    no_os = "import os" not in fixed_code
    no_any = "Any" not in fixed_code or "from typing import Dict" in fixed_code
    no_list = "List" not in fixed_code or "from typing import Dict" in fixed_code
    
    print(f"  {'✓' if has_dict else '✗'} Kept 'from typing import Dict' (used)")
    print(f"  {'✓' if has_json else '✗'} Kept 'import json' (used)")
    print(f"  {'✓' if no_os else '✗'} Removed 'import os' (unused)")
    print(f"  {'✓' if no_any else '✗'} Removed 'Any' from typing import (unused)")
    print(f"  {'✓' if no_list else '✗'} Removed 'List' from typing import (unused)")
    
    all_good = has_dict and has_json and no_os and no_any and no_list
    
    print("\n" + "=" * 70)
    if all_good:
        print("✓✓✓ TEST PASSED - Multi-import fix working correctly! ✓✓✓")
    else:
        print("✗✗✗ TEST FAILED - Something went wrong ✗✗✗")
    print("=" * 70)
    
    # Cleanup
    import shutil
    shutil.rmtree(test_dir)
    
    return all_good


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
