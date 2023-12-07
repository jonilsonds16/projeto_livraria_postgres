from model.livro import Livro
from database.conexao_factory import ConexaoFactory
from dao.categoria_dao import CategoriaDAO
from dao.editora_dao import EditoraDAO
from dao.autor_dao import AutorDAO


class LivroDAO:

    def __init__(self, categoria_dao: CategoriaDAO, editora_dao: EditoraDAO, autor_dao: AutorDAO):
        self.__livros: list[Livro] = list()
        self.__conexao_factory: ConexaoFactory = ConexaoFactory()
        self.__categoria_dao: CategoriaDAO = categoria_dao
        self.__editora_dao: EditoraDAO = editora_dao
        self.__autor_dao: AutorDAO = autor_dao

    def listar(self) -> list[Livro]:
        livros = list()

        conexao = self.__conexao_factory.get_conexao()
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT id, titulo, resumo, ano, paginas, isbn, categoria_id, editora_id, autor_id FROM livros")
        resultados = cursor.fetchall()
        for resultado in resultados:
            categoria = self.__categoria_dao.buscar_por_id(resultado[6])
            editora = self.__editora_dao.buscar_por_id(resultado[7])
            autor = self.__autor_dao.buscar_por_id(resultado[8])

            liv = Livro(resultado[1], resultado[2],
                        int(resultado[3]), int(resultado[4]), resultado[5], categoria, editora, autor)
            liv.id = resultado[0]
            livros.append(liv)
        cursor.close()
        conexao.close()

        return livros

    def adicionar(self, livro: Livro) -> None:
        self.__livros.append(livro)

    def remover(self, livro_id: int) -> bool:
        encontrado = False
        for l in self.__livros:
            if (l.id == livro_id):
                index = self.__livros.index(l)
                self.__livros.pop(index)
                encontrado = True
                break
        return encontrado

    def buscar_por_id(self, livro_id) -> Livro:
        liv = None
        for l in self.__livros:
            if (l.id == livro_id):
                liv = l
                break
        return liv

    def ultimo_id(self) -> int:
        index = len(self.__livros) - 1
        if (index == -1):
            id = 0
        else:
            id = self.__livros[index].id
        return id
