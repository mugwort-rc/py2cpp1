# -*- coding: utf-8 -*-

import ast

import six


OPERATORS = {
    ast.Add: '+',
    ast.Sub: '-',
    ast.Mult: '*',
    ast.Div: '/',
    ast.Mod: '%',
    ast.Pow: '**',
    ast.LShift: '<<',
    ast.RShift: '>>',
    ast.BitOr: '|',
    ast.BitXor: '^',
    ast.BitAnd: '&',
    ast.FloorDiv: '//',
}


if six.PY3:
    class Print(object):
        def __init__(self, values, nl=True):
            self.dest = None
            self.values = values
            self.nl = nl


class CodeBlock(object):
    def __init__(self, generator, node):
        self.generator = generator
        self.config = self.generator.config
        self.node = node

    def __enter__(self):
        self.generator.current_block.append(self.node.name)
        if self.node.name in self.config:
            self.generator.config = self.config[self.node.name]
        self.generator.indent_level += 1

    def __exit__(self, type, value, traceback):
        self.generator.current_block.pop()
        self.generator.config = self.config
        self.generator.indent_level -= 1


class SourceGenerator(ast.NodeVisitor):
    def __init__(self, config={}):
        self.config = config
        self.current_block = []
        self.indent_base = ' '*4
        self.indent_level = 0

        self.system_headers = []

    def code(self, code):
        return self.indent_base*self.indent_level + code

    def add_system_header(self, header):
        if header not in self.system_headers:
            self.system_headers.append(header)

    def headers(self):
        headers = []
        sys_header = '#include <{}>'
        headers += [sys_header.format(x) for x in sorted(self.system_headers)]
        return '\n'.join(headers)

    # Statements

    def visit_Assign(self, node):
        targets = [self.visit(x) for x in node.targets]
        value = self.visit(node.value)
        return self.code('{} = {};'.format(' = '.join(targets), value))

    def visit_AugAssign(self, node):
        target = self.visit(node.target)
        op = OPERATORS[node.op.__class__]
        value = self.visit(node.value)
        code = ''
        if op in ['**', '//']:
            self.add_system_header('cmath')
            if op == '**':
                code = '{0} = std::pow({0}, {1});'.format(target, value)
            elif op == '//':
                code = '{0} = std::floor(double({0}) / {1});'.format(target, value)
        else:
            code = '{} {}= {};'.format(target, op, value)
        return self.code(code)

    def visit_Expr(self, node):
        # print special case
        if isinstance(node.value, ast.Call) and node.value.func.id == 'print':
            kw = {x.arg: x.value for x in node.value.keywords}
            dummy = Print(node.value.args, 'end' not in kw)
            if 'end' in kw:
                dummy.values.append(kw['end'])
            return self.visit(dummy)
        value = self.visit(node.value)
        return self.code('{};'.format(value))

    def visit_FunctionDef(self, node):
        temp = []
        config = self.config.get(node.name, {})
        # function type
        rettype = config.get('rettype', 'void')
        # args
        argtypes = config.get('args', {})
        args = []
        for arg in node.args.args:
            id = self.visit(arg)
            argtype = argtypes.get(id, '')
            args.append(' '.join([argtype, id]))
        args = ', '.join(args)
        temp.append(self.code('{} {}({}) {{'.format(rettype, node.name, args)))
        with CodeBlock(self, node):
            for child in node.body:
                line = self.visit(child)
                if line is not None:
                    temp.append(line)
        temp.append(self.code('}'))
        return '\n'.join(temp)

    def visit_Pass(self, node):
        return ''  # no indent

    def visit_Print(self, node):
        self.add_system_header('iostream')
        temp = []
        dest = 'std::cout'
        if node.dest:
            dest = self.visit(node.dest)
        temp.append(dest)
        for value in node.values:
            temp.append(self.visit(value))
        if node.nl:
            temp.append('std::endl')
        return self.code('{};'.format(' << '.join(temp)))

    # Expressions

    def visit_Call(self, node):
        name = self.visit(node.func)
        args = []
        for arg in node.args:
            args.append(self.visit(arg))
        return '{}({})'.format(name, ', '.join(args))

    def visit_Name(self, node):
        return node.id

    def visit_Str(self, node):
        return '"{}"'.format(node.s)

    def visit_Num(self, node):
        return '{}'.format(node.n)
