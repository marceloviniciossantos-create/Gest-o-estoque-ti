import sqlite3

#primeiro criar um estoque onde as peças ficaram armazenadas
conexao = sqlite3.connect('estoque_ti.db')
cursor = conexao.cursor()

#quero mostrar a quantidade aqui enqaunto não encontro outra opção melhor e mais simples (cod IA simplificado)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS estoque (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT NOT NULL,
        quantidade INTEGER NOT NULL
    )
''')

#encontrei um jeito que vai mostrar sempre o estoque sem precisar printar toda vez (usando o DEF: define - ele me ajuda com a repetição da vitrine )
def mostrar_estoque():
    print("\n VITRINE DO ESTOQUE ")
    cursor.execute('SELECT * FROM estoque')
    itens = cursor.fetchall()
    if not itens:
        print("Estoque vazio!")
    for linha in itens:
        # Se a quantidade for 0, mostra mensagem especial
        status = f"{linha[2]} unidades" if linha[2] > 0 else " PEÇA ESGOTADA "
        print(f"ID: {linha[0]} | Peça: {linha[1]} | Qtd: {status}")


# A interface do úsuario
while True:
    mostrar_estoque()
    print("\n1. Cadastrar/Adicionar Peça | 2. Retirar Peça | 3. Sair")
    opcao = input("Escolha uma opção: ")
#inclui a opção de upper e strip para não causar problemas quando for verificar as peças e quantidades
    if opcao == '1':
        nome = input("Nome da peça (ex: Mouse): ").strip().upper()
        qtd = int(input("Quantidade a adicionar: "))

        # Verifica se a peça já existe
        cursor.execute('SELECT id, quantidade FROM estoque WHERE item = ?', (nome,))
        item_existente = cursor.fetchone()

        if item_existente:
            nova_qtd = item_existente[1] + qtd
            cursor.execute('UPDATE estoque SET quantidade = ? WHERE id = ?', (nova_qtd, item_existente[0]))
        else:
            cursor.execute('INSERT INTO estoque (item, quantidade) VALUES (?, ?)', (nome, qtd))

        conexao.commit()

    elif opcao == '2':
        id_peca = input("Digite o ID da peça que está saindo: ")
        qtd_saida = int(input("Quantidade a retirar: "))

        cursor.execute('SELECT quantidade FROM estoque WHERE id = ?', (id_peca,))
        resultado = cursor.fetchone()

        if resultado and resultado[0] >= qtd_saida:
            nova_qtd = resultado[0] - qtd_saida
            cursor.execute('UPDATE estoque SET quantidade = ? WHERE id = ?', (nova_qtd, id_peca))
            conexao.commit()
        else:
            print("\n[ERRO] Quantidade insuficiente ou ID inválido!")

    elif opcao == '3':
        break
    else:
           print("\n[ERRO!] Por favor, escolha 1, 2 ou 3.")
conexao.close()