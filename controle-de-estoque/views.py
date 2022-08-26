
from flask_mysqldb import MySQL
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy.exc import IntegrityError
import json
from config import app, mysql, cursor, conn

def queryprodutos():
    query = '''SELECT * FROM produtos ORDER BY nome'''
    cursor.execute(query)
    res = cursor.fetchall()
    produtos = []
    content = {}
    for result in res:
        content = {'ID': result[0], 'nome': result[1], 'valor_compra': result[2], 'valor_venda': result[3], 'quantidade_estoque': result[4], 'quantidade_minima': result[5]}
        produtos.append(content)
        content={}
    return produtos



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/produtos')
def produtos():
    produtos = queryprodutos()
    return render_template('produtos.html', produtos=produtos)


@app.route('/produtos_faltando')
def produtos_faltando():

    listaprodutos=queryprodutos()
    produtos = cursor.execute('SELECT * FROM produtos ORDER BY nome')
    #produtos = Estoque.query.order_by(Estoque.nome).all()
    produtos_em_falta = []

    for produto in listaprodutos:
        if int(produto['quantidade_estoque']) < int(produto['quantidade_minima']):
            produtos_em_falta.append(produto)
        #if int(produto.quantidade_estoque) < int(produto.quantidade_minima):
        #    produtos_em_falta.append(produto)

    return render_template('produtos_faltando.html', produtos=produtos_em_falta)


@app.route('/novo_produto/<erro_nome>', methods=['GET'])
def novo_produto(erro_nome):
    if erro_nome == 'sim':
        #TODO ALERT
        print('sim')
    return render_template('novo_produto.html')


@app.route('/criar_produto', methods=['POST'])
def criar_produto():

    nome = request.form['nome']
    valor_compra = request.form['valor_compra']
    valor_venda = request.form['valor_venda']
    quantidade_estoque = request.form['quantidade_estoque']
    quantidade_minima = request.form['quantidade_minima']

    try:
        cursor.execute(f'''INSERT INTO produtos (nome, valor_compra, valor_venda, quantidade_estoque, quantidade_minima)
    VALUES ("{nome}",{valor_compra},{valor_venda},{quantidade_estoque},{quantidade_minima}) ''')
        conn.commit()
    except IntegrityError:
        return redirect(url_for('novo_produto', erro_nome='sim'))
    produtos = queryprodutos()
    return render_template('produtos.html', produtos=produtos)


@app.route('/alterar_produto/<id>')
def alterar_produto(id):
    query = f'''SELECT * FROM produtos WHERE id = {id}'''
    cursor.execute(query)
    res = cursor.fetchall()
    produto_para_modificar = []
    content = {}
    for result in res:
        content = {'ID': result[0], 'nome': result[1], 'valor_compra': result[2], 'valor_venda': result[3], 'quantidade_estoque': result[4], 'quantidade_minima': result[5]}
        produto_para_modificar.append(content)
        content={}
    return render_template('alterar_produto.html', produto=produto_para_modificar)
    #produto_para_modificar = cursor.execute(f'''SELECT * FROM produtos WHERE id = {id}''')
    #return render_template('alterar_produto.html', produto=produto_para_modificar)

@app.route('/modificar', methods=['POST'])
def modificar():
    id = request.form['id']
    produto_para_modificar = cursor.execute(f'SELECT * FROM produtos WHERE id = {id}')
    produto_para_modificar.nome = request.form['nome']
    produto_para_modificar.valor_compra = request.form['valor_compra']
    produto_para_modificar.valor_venda = request.form['valor_venda']
    produto_para_modificar.quantidade_estoque = request.form['quantidade_estoque']
    produto_para_modificar.quantidade_minima = request.form['quantidade_minima']

    cursor.execute(produto_para_modificar)
    conn.commit()
    return redirect(url_for('produtos'))



@app.route('/excluir_produto/<id>')
def excluir_produto(id):
    cursor.execute(f'DELETE FROM produtos WHERE id = {id}')
    conn.commit()
    return redirect(url_for('produtos'))

@app.route('/venda')
def venda():
    produtos = queryprodutos()
    return render_template('venda.html', produtos=produtos)


@app.route('/reestoque')
def reestoque():
    produtos = queryprodutos()
    return render_template('reestoque.html', produtos=produtos)


if __name__ == '__main__':
    app.run(host='localhost',debug=True, port=8080)