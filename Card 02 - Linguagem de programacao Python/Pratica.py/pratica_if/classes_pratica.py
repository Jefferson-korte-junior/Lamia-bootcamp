class livro:
    def __init__(self, titulo, autor, ano):
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
    
    def descrição (self):
        return f"' O livro {self.titulo}' foi escrito por {self.autor} no ano de {self.ano}"
    
meu_livro = livro('The walking dead', 'Robert Kirkman', '2003')

print (meu_livro.descrição())