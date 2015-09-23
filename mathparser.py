def parse_nested(text, left=r'[(]', right=r'[)]', operators=r'[-+*/^]'):
    # print("parse_nested({})".format(text))
    """ Based on http://stackoverflow.com/a/17141899/190597 (falsetru) """
    pat = r'({}|{}|{})'.format(left, right, operators)
    tokens = re.split(pat, text)
    stack = [[]]
    for x in tokens:
        # if not x or re.match(sep, x): continue
        if not x:
            continue
        if re.match(left, x):
            stack[-1].append([])
            stack.append(stack[-1][-1])
        elif re.match(right, x):
            stack.pop()
            if not stack:
                raise ValueError('error: opening bracket is missing')
        else:
            stack[-1].append(x)
    if len(stack) > 1:
        # print(stack)
        raise ValueError('error: closing bracket is missing')
    return stack.pop()
