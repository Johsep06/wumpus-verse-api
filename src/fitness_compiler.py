import ast
import operator

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg
}

VARIABLES = {
    'PV',   # PASSO VALIDO
    'PI',   # PASSO INVALIDO
    'TV',   # TIRO VALIDO
    'TI',   # TIRO INVALIDO
    'SW',   # SALA COM WUMPUS
    'SP',   # SALA COM POCO
    'SO',   # SALA COM OURO
    'V',    # VITORIA
    'T',    # TOTAL DE AÇÕES
}


class FitnessCompiler(ast.NodeVisitor):
    def visit(self, node):
        return super().visit(node)

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        operator = OPERATORS[type(node.op)]
        return lambda vars: operator(left(vars), right(vars))

    def visit_UnaryOp(self, node):
        value = self.visit(node.operand)
        operator = OPERATORS[type(node.op)]
        return lambda vars: operator(value(vars))

    def visit_Constant(self, node):
        if not isinstance(node.value, (int, float)):
            raise ValueError("Constante inválida")
        return lambda vars: node.value

    def visit_Name(self, node):
        if node.id not in VARIABLES:
            raise ValueError(f"Variável não permitida: {node.id}")
        return lambda vars: vars[node.id]

    def generic_visit(self, node):
        raise ValueError(f"Operação não permitida: {type(node).__name__}")


def compile(expressao: str):
    tree = ast.parse(expressao, mode="eval")
    compiler = FitnessCompiler()
    func = compiler.visit(tree.body)
    return func
