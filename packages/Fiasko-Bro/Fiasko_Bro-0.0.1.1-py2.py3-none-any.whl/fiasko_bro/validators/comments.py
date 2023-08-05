import ast

from .. import ast_helpers


def has_no_extra_dockstrings(solution_repo, whitelists, functions_with_docstrings_percent_limit, *args, **kwargs):
    whitelist = whitelists.get('has_no_extra_dockstrings_whitelist', [])
    for file_name, tree in solution_repo.get_ast_trees(with_filenames=True):
        for whitelisted_part in whitelist:  # TODO: refactor black/whitelist filtering for paths
            if whitelisted_part in file_name:
                break
        else:
            defs = ast_helpers.get_nodes_of_type(tree, ast.FunctionDef)
            if not defs:
                continue

            docstrings = [ast.get_docstring(d) for d in defs if ast.get_docstring(d) is not None]
            if len(docstrings) / len(defs) * 100 > functions_with_docstrings_percent_limit:
                return 'extra_comments', ''
