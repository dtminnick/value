
import ast
from collections import defaultdict

class TkinterContainerLayoutChecker(ast.NodeVisitor):
    def __init__(self):
        self.widget_parents = {}           # widget_name -> parent_name
        self.parent_layouts = defaultdict(set)  # parent_name -> set of layouts used

    def visit_Assign(self, node):
        # Look for widget creation
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute):
            func_name = node.value.func.attr
            if func_name in {'Button', 'Label', 'Frame', 'Entry', 'Text', 'Checkbutton', 'Radiobutton'}:
                widget_name = node.targets[0].id
                parent = ast.unparse(node.value.args[0])
                self.widget_parents[widget_name] = parent
        self.generic_visit(node)

    def visit_Call(self, node):
        # Look for pack(), grid(), place() usage
        if isinstance(node.func, ast.Attribute):
            method = node.func.attr
            if method in {'pack', 'grid', 'place'}:
                widget = ast.unparse(node.func.value)
                parent = self.widget_parents.get(widget)
                if parent:
                    self.parent_layouts[parent].add(method)
        self.generic_visit(node)

    def report_conflicts(self):
        for parent, layouts in self.parent_layouts.items():
            if len(layouts) > 1:
                print(f"Conflict detected in container '{parent}': uses multiple layouts {layouts}")

def check_file_for_container_conflicts(filepath):
    with open(filepath, "r") as file:
        tree = ast.parse(file.read())
    checker = TkinterContainerLayoutChecker()
    checker.visit(tree)
    checker.report_conflicts()

