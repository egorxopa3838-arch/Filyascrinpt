import re
import ast
import operator

# Safe operations for eval
SAFE_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.Mod: operator.mod,
}

def safe_eval(expr):
    """Safe expression calculator."""
    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.BinOp):
            return SAFE_OPS[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp):
            return SAFE_OPS[type(node.op)](_eval(node.operand))
        raise ValueError(f"Invalid expression: {ast.dump(node)}")
    return _eval(ast.parse(expr, mode='eval'))

def run(code):
    variables = {}
    lines = code.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        i += 1

        if not line or line.startswith('#'):
            continue

        parts = line.split(' ', 1)
        cmd = parts[0]
        arg = parts[1].strip() if len(parts) > 1 else ''

        try:
            # meow "text" — output
            if cmd == 'meow':
                text = arg.strip('"')
                print(f'🐈‍⬛ {text}')

            # sniff x — keyboard input
            elif cmd == 'sniff':
                var = arg
                value = input('🐾 Enter a value: ')
                try:
                    variables[var] = float(value) if '.' in value else int(value)
                except ValueError:
                    variables[var] = value
                print(f'✅ {var} = {variables[var]}')

            # purr x = 5 — variable
            elif cmd == 'purr':
                var, value = map(str.strip, arg.split('=', 1))
                if value.startswith('"') and value.endswith('"'):
                    variables[var] = value[1:-1]
                else:
                    variables[var] = safe_eval(value)
                print(f'✅ {var} = {variables[var]}')

            # grab x — show
            elif cmd == 'grab':
                var = arg
                if var in variables:
                    print(f'📦 {var} = {variables[var]}')
                else:
                    print(f'❌ No variable {var}')

            # tail expr  OR  tail z = expr — computation
            elif cmd == 'tail':
                if '=' in arg:
                    var, expr = map(str.strip, arg.split('=', 1))
                    result = safe_eval(expr, variables)
                    variables[var] = result
                    print(f'🧮 {var} = {result}')
                else:
                    result = safe_eval(arg, variables)
                    print(f'🧮 {arg} = {result}')

            # sleep — end
            elif cmd == 'sleep':
                print('😴 Program finished')
                break

            else:
                print(f'❓ Unknown command: {cmd}')

        except Exception as e:
            print(f'🐾 Error on line {i}: {e}')