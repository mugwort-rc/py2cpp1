# -*- coding: utf-8 -*-

import ast

class FunctionVisitor(ast.NodeVisitor):
    def visit_Module(self, node):
        result = {}
        for child in node.body:
            ret = self.visit(child)
            if ret is None:
                continue
            result.update(ret)
        return result

    def visit_ClassDef(self, node):
        functions = {}
        for child in node.body:
            ret = self.visit(child)
            if ret is None:
                continue
            functions.update(ret)
        return {
            node.name: functions,
        }

    def visit_FunctionDef(self, node):
        args = {}
        for i,name in enumerate(node.args.args):
            arg = self.visit(name)
            if i == 0 and arg == 'self':
                continue
            args[arg] = ''

        inner = []
        for child in node.body:
            ret = self.visit(child)
            if ret is None:
                continue
            inner.append(ret)

        result = {}
        if args:
            result.update({
                'args': args,
            })
        if inner:
            result.update({
                'inner': inner,
            })

        return {
            node.name: result,
        }

    def visit_Name(self, node):
        return node.id

def function_list(node):
    visitor = FunctionVisitor()
    return visitor.visit(node)
