import seedir as sd
a=sd.seedir(
    r'C:\Users\1\Desktop\photosearch', 
    style='emoji', 
    exclude_folders=[
        '__pycache__', 
        'Include', 
        'Lib', 
        'Scripts', 
        'examples', 
        'user data/*', 
        'images', 
        '.git'
        ], 
    exclude_files=[
        'images/*', 
        'user data/*',
        'Dockerfile',
        'pyvenv\.cfg',
            'run\.sh',
        'setup\.ps1',
        '_doc\.py',
        '\.gitkeep',
        '__init__\.py',
        
        ], regex=True, printout=False)
print(a)