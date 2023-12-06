import psycopg2


class ConexaoFactory:

    def get_conexao(self):
        return psycopg2.connect(
            host='berry.db.elephantsql.com',
            database='ezofkegd',
            user='ezofkegd',
            password='yyH80Iz2rDit3Yn8f9TnLKdA2U593o-J'
        )
