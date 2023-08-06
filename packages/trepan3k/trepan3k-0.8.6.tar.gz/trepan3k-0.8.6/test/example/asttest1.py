import ast
tree = ast.parse('''
import pdb; pdb.set_trace()
def five():
    return 5
eval_str = '1+2'
x = eval(eval_str)
x = eval('five()')
exec_str = 'x = 30'
exec(exec_str)
print(x)
''')
print(tree)
exec(compile(tree, filename="<ast>", mode="exec"))
