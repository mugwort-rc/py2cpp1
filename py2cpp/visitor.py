# -*- coding: utf-8 -*-

import ast


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

    def code(self, code):
        return self.indent_base*self.indent_level + code

    # Statements

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
                temp.append(self.visit(child))
        temp.append(self.code('}'))
        return '\n'.join(temp)

    def visit_Pass(self, node):
        return ''  # no indent

    def visit_Print(self, node):
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

    def visit_Name(self, node):
        return node.id

    def visit_Str(self, node):
        return '"{}"'.format(node.s)

    def visit_Num(self, node):
        return '{}'.format(node.n)
