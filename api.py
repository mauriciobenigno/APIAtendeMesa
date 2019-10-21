from flask import Flask, jsonify, request
import MySQLdb
import json

#API MESAS
dbMesa = MySQLdb.connect(host="mauriciojbas.mysql.pythonanywhere-services.com",
                     user="mauriciojbas",
                     passwd="atendemesa",
                     db="mauriciojbas$dbmesa")

app = Flask(__name__)

mesas = [
    {
        'id': 1,
        'Nome': 'Mesa 1',
        'Status': 'Livre',
        'Lugares': '5',
        'Garcom':'',
        'CodigoComanda':''
    },
    {
        'id': 2,
        'Nome': 'Mesa 2',
        'Status': 'Livre',
        'Lugares': '2',
        'Garcom':'',
        'CodigoComanda':''
    }
]

def CarregaMesas():
    cur = dbMesa.cursor()
    cur.execute(""" SELECT * FROM Mesa; """)
    mesas.clear()
    for linha in cur.fetchall():
        mesa = {
            'id':linha[0],
            'Nome':linha[1],
            'Status':linha[2],
            'Lugares':linha[3],
            'Garcom':linha[4],
            'CodigoComanda':linha[5]
        }
        mesas.append(mesa)

def AlteraMesa(mesa):
    cur = dbMesa.cursor()
    query = "UPDATE Mesa SET Nome=%s, Status=%s, Lugares=%s, Garcom=%s, CodigoComanda=%s WHERE idMesa=%s"
    cur.execute(query, (mesa['Nome'], mesa['Status'], int(mesa['Lugares']), mesa['Garcom'], int(mesa['CodigoComanda']), int(mesa['id']) ))
    dbMesa.commit()
    CarregaMesas()

def RemoveMesa(id):
    cur = dbMesa.cursor()
    query = "DELETE FROM Mesa WHERE idMesa = %s"
    cur.execute(query, (int(id),))
    dbMesa.commit()
    CarregaMesas()

@app.route('/mesa', methods=['GET'])
def home():
    CarregaMesas()
    return jsonify(mesas), 200


@app.route('/mesa/<string:status>', methods=['GET'])
def mesas_por_status(status):
    mesas_por_status = [mesa for mesa in mesas if mesa['Status'] == status]
    return jsonify(mesas_por_status), 200


@app.route('/mesa/<int:id>', methods=['POST'])
def mudarStatus(id):
    for mesa in mesas:
        if mesa['id'] == id:
            mesa['Nome'] = request.get_json().get('Nome')
            mesa['Status'] = request.get_json().get('Status')
            mesa['Lugares'] = request.get_json().get('Lugares')
            mesa['Garcom'] = request.get_json().get('Garcom')
            mesa['CodigoComanda'] = request.get_json().get('CodigoComanda')
            AlteraMesa(mesa)
            return jsonify(mesa), 200
    return jsonify({'Erro': 'Mesa nao encontrada'}), 404


@app.route('/mesa/<int:id>', methods=['GET'])
def mesa_por_id(id):
    for mesa in mesas:
        if mesa['id'] == id:
            return jsonify(mesa), 200
    return jsonify({'Erro': 'Mesa nao encontrada'}), 404


@app.route('/mesa', methods=['POST'])
def adicionar_mesa():
    data = request.get_json()
    cur = dbMesa.cursor()
    query = "INSERT INTO Mesa (Nome, Status, Lugares, Garcom, CodigoComanda)" \
        "VALUES (%s,%s,%s,%s,%s)"
    cur.execute(query, (data['Nome'], data['Status'], int(data['Lugares']), data['Garcom'], int(data['CodigoComanda']) ))
    dbMesa.commit()
    CarregaMesas()
    return jsonify(data), 201


@app.route('/mesa/<int:id>', methods=['DELETE'])
def remove_mesa(id):
    print("id a ser deletado: ",id)
    index = id - 1
    del mesas[index]
    RemoveMesa(id)
    return jsonify({'Sucesso': 'Mesa removida'}), 200
	
# API COMANDA
comandas = [
    {
        "codComanda": 0,
        "Comida": ["Arroz", "Feijao", "Carne"],
        "Bebida": ["CocaCola", "Suco"],
        "Observacao" : "Sem acucar"
    },
    {
        "codComanda": 1,
        "Comida": ["Arroz", "Feijao", "Carne"],
        "Bebida": ["CocaCola", "Suco"],
        "Observacao" : "Sem acucar"
    },
    {
        "codComanda": 2,
        "Comida": ["Arroz", "Feijao", "Carne"],
        "Bebida": ["CocaCola", "Suco"],
        "Observacao" : "Sem acucar"
    }
]

def CarregaComandas():
    global comandas
    comandas.clear()
    with open('comandas.json', 'r') as f:
        comandas = json.load(f)

def GravarComandas():
    with open('comandas.json', 'w') as json_file:
        json.dump(comandas, json_file)

@app.route('/comanda', methods=['GET'])
def homeComandas():
    CarregaComandas()
    return jsonify(comandas), 200

@app.route('/comanda', methods=['POST'])   
def adicionar_comanda():
    data = request.get_json()
    comandas.append(data)
    GravarComandas()
    return jsonify(comandas), 201

@app.route('/comanda/<int:id>', methods=['POST'])
def editarComanda(id):
    for comanda in comandas:
        if comanda['codComanda'] == id:
            comanda['Comida'] = request.get_json().get('Comida')
            comanda['Bebida'] = request.get_json().get('Bebida')
            comanda['Observacao'] = request.get_json().get('Observacao')
            return jsonify(comanda[id]), 200
    return jsonify({'Erro': 'Comanda nao encontrada'}), 404

@app.route('/comanda/<int:id>', methods=['GET'])
def comanda_por_id(id):
    for comanda in comandas:
        if comanda['codComanda'] == id:
            return jsonify(comanda), 200
    return jsonify({'Erro': 'Comanda nao encontrada'}), 404

#@app.route('/comanda', methods=['POST'])
#def adicionar_comanda():


if __name__ == '__main__':
    CarregaMesas()
    app.run(host='0.0.0.0', port=500)
    #app.run(debug=True)