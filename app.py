import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, send_file, abort
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from io import BytesIO

app = Flask(__name__)


# Chave secreta para gerenciar as sessões
app.secret_key = 'sua_chave_secreta_aqui'

# Configurações do banco de dados
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Pe023194)' 
app.config['MYSQL_DB'] = 'academia_cic'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # Para retornar resultados como dicionários

# Configuração do caminho de upload
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Diretório onde as imagens serão salvas
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite de 16MB para o upload de arquivos

mysql = MySQL(app)
bcrypt = Bcrypt(app)

#Teste para adicionar treinos
# Rota para criar treino personalizado
@app.route('/criar-treino', methods=['POST'])
def criar_treino():
    data = request.json
    treinos_selecionados = data.get('treinos')

    # Aqui você pode fazer o processamento e armazenar o treino personalizado no banco de dados

    return jsonify({'status': 'success', 'treinos': treinos_selecionados})

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'GET':
        return render_template('cadastro.html')
    
    elif request.method == 'POST':
        data = request.form
        nome = data.get('nome')
        cpf = data.get('cpf')
        email = data.get('email')
        data_nascimento = data.get('data_nascimento')
        senha = data.get('senha')
        senha2 = data.get('senha2')

        # Verifica se as senhas coincidem
        if senha != senha2:
            return jsonify({'message': 'As senhas não coincidem'}), 400

        # Criptografa a senha
        hashed_password = bcrypt.generate_password_hash(senha).decode('utf-8')

        # Verifica se uma foto de perfil foi enviada
        foto_perfil = request.files.get('foto_perfil')
        foto_perfil_blob = None

        if foto_perfil:
            foto_perfil_blob = foto_perfil.read()

        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO usuarios (cpf, nome, email, senha, foto_perfil, data_nascimento) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (cpf, nome, email, hashed_password, foto_perfil_blob, data_nascimento))
            mysql.connection.commit()
            cur.close()
            return jsonify({'message': 'Cadastro realizado com sucesso'}), 201
        except Exception as e:
            print(e)  # Para fins de depuração
            return jsonify({'message': 'Erro no cadastro'}), 500


# Rota para a página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        data = request.form
        email = data.get('email')
        senha = data.get('senha')

        try:
            cur = mysql.connection.cursor()

            # Verifica se o email pertence a um professor
            cur.execute("SELECT * FROM professores WHERE email = %s", [email])
            professor = cur.fetchone()

            if professor:
                # Se o email pertence a um professor, verifica a senha
                if professor['senha'] == senha:  # Comparação direta de senha
                    # Salva o nome do professor na sessão
                    session['user'] = professor['nome']
                    session['email'] = professor['email']
                    return render_template('professor.html', nome=professor['nome'])  # Redireciona para a página do professor
                else:
                    return jsonify({'message': 'Credenciais inválidas'}), 401

            # Se não for um professor, verifica se é um usuário
            cur.execute("SELECT * FROM usuarios WHERE email = %s", [email])
            user = cur.fetchone()
            cur.close()

            # Verifica se o usuário existe e se a senha está correta
            if user and bcrypt.check_password_hash(user['senha'], senha):
                # Salva o nome de usuário na sessão
                session['user'] = user['nome']
                session['email'] = user['email']
                session['cpf'] = user['cpf']  # Ajuste conforme a coluna do CPF no seu banco
                return redirect(url_for('homepage'))  # Redireciona para a homepage
            else:
                return jsonify({'message': 'Credenciais inválidas'}), 401

        except Exception as e:
            print(e)
            return jsonify({'message': 'Erro no login'}), 500


# Rota para a homepage, acessível apenas se o usuário estiver logado
@app.route('/homepage')
def homepage():
    if 'cpf' not in session:
        return redirect(url_for('login'))  # Redirecionar se não estiver autenticado

    cpf = session['cpf']

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT nome, foto_perfil FROM usuarios
        WHERE cpf = %s
    """, (cpf,))
    usuario = cur.fetchone()
    cur.close()

    if usuario is None:
        return redirect(url_for('login'))  # Redirecionar se não encontrar o usuário

    return render_template('homepage.html', usuario=usuario)

# Rota para carregar a página de treino
@app.route('/treino')
def treino():
    return render_template('teste.html')

# Rota API para Grupo Muscular
@app.route('/api/treinos/<grupo_muscular>', methods=['GET'])
def get_treinos(grupo_muscular):
    cur = mysql.connection.cursor()
    query = """
        SELECT * 
        FROM treinos 
        WHERE grupo_muscular = %s
    """
    cur.execute(query, (grupo_muscular,))
    treinos = cur.fetchall()
    cur.close()
    return jsonify(treinos)

# Rota API para Treino

@app.route('/api/treino/<int:treino_id>/exercicios', methods=['GET'])
def get_exercicios(treino_id):
    cur = mysql.connection.cursor()
    query = "SELECT * FROM exercicios WHERE treino_id = %s"
    cur.execute(query, (treino_id,))
    exercicios = cur.fetchall()
    cur.close()
    return jsonify(exercicios)

# Rota API para Diversos
@app.route('/api/exercicios/diversos', methods=['GET'])
def get_exercicios_diversos():
    cur = mysql.connection.cursor()
    query = "SELECT * FROM exercicios"
    cur.execute(query)
    exercicios = cur.fetchall()
    cur.close()
    return jsonify(exercicios)



#Rota para a página de avaliação
@app.route('/avaliacao')
def avaliacao():
    return render_template('avaliacao.html')

# Para o professor adicionar os treinos

# Rota para o professor adicionar treinos
@app.route('/api/treinos', methods=['POST'])
def create_treino():
    data = request.get_json()
    nome = data['nome']
    descricao = data['descricao']
    grupo_muscular = data['grupo']
    professor_id = session.get('professor_id')  # Extraia o ID do professor da sessão

    if not professor_id:
        return jsonify({'message': 'Usuário não autenticado'}), 401

    cur = mysql.connection.cursor()
    query = """
        INSERT INTO treinos (nome, descricao, grupo_muscular, professor_id) 
        VALUES (%s, %s, %s, %s)
    """
    cur.execute(query, (nome, descricao, grupo_muscular, professor_id))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Treino criado com sucesso!'}), 201

# Rota para o professor adicionar exercícios
@app.route('/api/exercicios', methods=['POST'])
def create_exercicio():
    data = request.get_json()
    nome = data['nome']
    descricao = data['descricao']
    repeticoes = data['repeticoes']
    series = data['series']
    descanso = data['descanso']
    treino_id = data['treinoId']

    cur = mysql.connection.cursor()
    query = """
        INSERT INTO exercicios (nome, descricao, repeticoes, series, descanso_minutos, treino_id) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cur.execute(query, (nome, descricao, repeticoes, series, descanso, treino_id))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Exercício criado com sucesso!'}), 201

# Rota para obter todos os treinos
@app.route('/api/treinos', methods=['GET'])
def fetch_treinos():
    cur = mysql.connection.cursor()
    query = "SELECT * FROM treinos"
    cur.execute(query)
    treinos = cur.fetchall()
    cur.close()
    return jsonify(treinos)

# Rota para obter todos os exercícios
@app.route('/api/exercicios', methods=['GET'])
def fetch_exercicios():
    cur = mysql.connection.cursor()
    query = "SELECT * FROM exercicios"
    cur.execute(query)
    exercicios = cur.fetchall()
    cur.close()
    return jsonify(exercicios)

@app.route('/api/treinos/<int:id>', methods=['DELETE'])
def delete_treino(id):
    cur = mysql.connection.cursor()

    # Primeiro, exclua os exercícios associados ao treino
    cur.execute("DELETE FROM exercicios WHERE treino_id = %s", (id,))

    # Em seguida, exclua o treino
    cur.execute("DELETE FROM treinos WHERE id = %s", (id,))
    
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Treino excluído com sucesso!'}), 200

@app.route('/api/favoritos', methods=['POST'])
def add_favorito():
    try:
        data = request.json
        usuario_cpf = data.get('usuario_cpf')
        treino_id = data.get('treino_id')
        exercicio_id = data.get('exercicio_id')
        tipo = data.get('tipo')  # Pode ser 'treino' ou 'exercicio'

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO favoritos (usuario_cpf, treino_id, exercicio_id, tipo)
            VALUES (%s, %s, %s, %s)
        """, [usuario_cpf, treino_id, exercicio_id, tipo])
        mysql.connection.commit()
        cur.close()

        return jsonify({'message': 'Favorito adicionado com sucesso'})
    except Exception as e:
        print(e)
        return jsonify({'message': 'Erro ao adicionar favorito'}), 500

@app.route('/api/favoritos/<usuario_cpf>', methods=['GET'])
def get_favoritos(usuario_cpf):
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT * FROM favoritos
            WHERE usuario_cpf = %s
        """, [usuario_cpf])
        favoritos = cur.fetchall()
        cur.close()

        return jsonify(favoritos)
    except Exception as e:
        print(e)
        return jsonify({'message': 'Erro ao listar favoritos'}), 500

@app.route('/api/favoritos/<int:favorito_id>', methods=['DELETE'])
def delete_favorito(favorito_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            DELETE FROM favoritos
            WHERE id = %s
        """, [favorito_id])
        mysql.connection.commit()
        cur.close()

        return jsonify({'message': 'Favorito removido com sucesso'})
    except Exception as e:
        print(e)
        return jsonify({'message': 'Erro ao remover favorito'}), 500

@app.route('/conta', methods=['GET'])
def conta():
    if 'cpf' not in session:
        return redirect(url_for('login'))  # Redirecionar se não estiver autenticado

    cpf = session['cpf']
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT * FROM usuarios
        WHERE cpf = %s
    """, (cpf,))
    usuario = cur.fetchone()
    cur.close()

    return render_template('conta.html', usuario=usuario)


@app.route('/conta', methods=['POST'])
def atualizar_conta():
    if 'cpf' not in session:
        return redirect(url_for('login'))

    cpf = session['cpf']
    foto_perfil = request.files.get('perfil')
    novo_email = request.form.get('email')
    senha = request.form.get('senha')

    cur = mysql.connection.cursor()

    if foto_perfil:
        filename = secure_filename(foto_perfil.filename)
        foto_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        foto_perfil.save(foto_path)
        cur.execute("""
            UPDATE usuarios
            SET foto_perfil = %s, email = %s
            WHERE cpf = %s
        """, (filename, novo_email, cpf))
    else:
        cur.execute("""
            UPDATE usuarios
            SET email = %s
            WHERE cpf = %s
        """, (novo_email, cpf))

    if senha:
        hashed_senha = bcrypt.generate_password_hash(senha).decode('utf-8')
        cur.execute("""
            UPDATE usuarios
            SET senha = %s
            WHERE cpf = %s
        """, (hashed_senha, cpf))

    mysql.connection.commit()
    cur.close()

    return redirect(url_for('homepage'))


@app.route('/api/usuario/<cpf>/foto', methods=['GET'])
def get_foto_perfil(cpf):
    # Consulta para buscar a imagem no banco de dados
    cur = mysql.connection.cursor()
    cur.execute('SELECT foto_perfil FROM usuarios WHERE cpf = %s', (cpf,))
    result = cur.fetchone()
    cur.close()

    # Se a imagem for encontrada, enviá-la como um arquivo
    if result and result['foto_perfil']:
        # Retornando a imagem binária armazenada no BLOB
        return send_file(BytesIO(result['foto_perfil']), mimetype='image/jpeg')  # Ajuste o tipo MIME se necessário
    else:
        # Se não houver imagem, retornar uma imagem padrão ou erro
        return jsonify({'message': 'Foto não encontrada'}), 404

@app.route('/foto_perfil/<cpf>')
def foto_perfil(cpf):
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT foto_perfil FROM usuarios
            WHERE cpf = %s
        """, (cpf,))
        foto_binario = cur.fetchone()['foto_perfil']
        cur.close()

        if foto_binario:
            return send_file(BytesIO(foto_binario), mimetype='image/jpeg')
        else:
            return send_file('static/uploads/default_profile.png', mimetype='image/jpeg')  # Imagem padrão
    except Exception as e:
        print(e)
        abort(500, description="Erro ao carregar a imagem")


# Rota para logout
@app.route('/logout')
def logout():
    session.clear()  # Remove todos os dados da sessão
    return redirect(url_for('index.html'))

if __name__ == '__main__':
    app.run(debug=True)
