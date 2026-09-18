import ast
import math
from typing import Any, Dict


class SafeSandbox:
    ALLOWED_BUILTINS = {
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
        "sum": sum,
        "len": len,
        "range": range,
        "float": float,
        "int": int,
        "math": math,
    }

    @classmethod
    def execute(cls, code_str: str) -> Dict[str, Any]:
        try:
            tree = ast.parse(code_str, mode="exec")
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    return {"success": False, "error": "Imports are disabled in sandbox"}
                if isinstance(node, ast.Name) and node.id in ("open", "eval", "exec", "__import__"):
                    return {"success": False, "error": f"Forbidden symbol '{node.id}'"}

            safe_globals = {"__builtins__": cls.ALLOWED_BUILTINS, "math": math}
            local_vars: Dict[str, Any] = {}
            exec(compile(tree, filename="<sandbox>", mode="exec"), safe_globals, local_vars)
            return {"success": True, "result": local_vars}
        except Exception as e:
            return {"success": False, "error": str(e)}
