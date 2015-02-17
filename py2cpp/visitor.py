# -*- coding: utf-8 -*-

import ast


class SourceGenerator(ast.NodeVisitor):

    # Statements

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
        return '{};'.format(' << '.join(temp))

    # Expressions

    def visit_Name(self, node):
        return node.id

    def visit_Str(self, node):
        return '"{}"'.format(node.s)

    def visit_Num(self, node):
        return '{}'.format(node.n)
