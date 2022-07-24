'''
[ (global)
    x = 1
    y = 2

    [(add)
        result = 0
    ]
]
'''

class IndexedIdentifier:
    def __init__(self, index):
        self.index = index

class Identifier:
    def __init__(self, name):
        self.name = name
        # Maybe I should move heap_pointer to the scope class?
        self.heap_pointer = None

class Scope:
    def __init__(self, parent, id):
        self.parent = parent
        self.children = set()
        self.identifiers = []
        self.id = id

    def __getitem__(self, key):
        search = lambda i: i.name == key
        ident = next(filter(search, self.identifiers), None)
    
        if ident == None and self.parent != None:
            return self.parent[key]
        else:
            return ident

    def add(self, ident):
        if self[ident.name] != None:
            raise NameError()

        self.identifiers.append(ident)

    def is_defined(self, ident):
        if type(ident) is Identifier:
            return self[ident.name] != None
        elif type(ident) is str:
            return self[ident] != None
