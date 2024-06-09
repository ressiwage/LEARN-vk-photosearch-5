def pick(options, title, *args, **kwargs):
    print(title)
    print(*[f'{ind}:{i}' for ind, i in enumerate(options)], sep='\n')
    option=-1
    while option not in list(range(len(options))):
        option = int(input('enter number: ').strip())
    return options[option], option