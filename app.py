import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename


app = Flask(__name__)

# Chave secreta para gerenciar as sessões
app.secret_key = 'sua_chave_secreta_aqui'

# Configurações do banco de dados
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Pe023194)' 
app.config['MYSQL_DB'] = 'academia'
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

# Rota para exibir e processar o formulário de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'GET':
        return render_template('cadastro.html')
    
    elif request.method == 'POST':
        data = request.form
        nome = data.get('nome')
        cpf = data.get('cpf')
        email = data.get('email')
        data_nascimento = data.get('dataNascimento')
        senha = data.get('senha')
        senha2 = data.get('senha2')

        # Verifica se as senhas coincidem
        if senha != senha2:
            return jsonify({'message': 'As senhas não coincidem'}), 400

        # Criptografa a senha
        hashed_password = bcrypt.generate_password_hash(senha).decode('utf-8')

        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO Pessoa (cpf, nome, email, dataNascimento, senha) 
                VALUES (%s, %s, %s, %s, %s)
            """, (cpf, nome, email, data_nascimento, hashed_password))
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
            cur.execute("SELECT * FROM Pessoa WHERE email = %s", [email])
            user = cur.fetchone()
            cur.close()

            # Verifica se o usuário existe e se a senha está correta
            if user and bcrypt.check_password_hash(user['senha'], senha):
                # Salva o nome de usuário na sessão
                session['user'] = user['nome']
                session['email'] = user['email']
                return redirect(url_for('homepage'))  # Redireciona para a homepage
            else:
                return jsonify({'message': 'Credenciais inválidas'}), 401

        except Exception as e:
            print(e)
            return jsonify({'message': 'Erro no login'}), 500

# Rota para a homepage, acessível apenas se o usuário estiver logado
@app.route('/homepage')
def homepage():
    if 'user' in session:
        return render_template('homepage.html', nome=session['user'])
    else:
        return redirect(url_for('login'))

# Rota para a página de conta (GET para exibir o formulário e POST para processar o upload)
@app.route('/conta', methods=['GET', 'POST'])
def conta():
    if request.method == 'GET':
        return render_template('conta.html')
    
    elif request.method == 'POST':
        # Processar atualização da conta
        email = request.form['email']
        telefone = request.form['telefone']
        perfil_img = request.files['perfil']  # Obtém o arquivo de imagem

        # Verifica se foi enviado um arquivo de imagem
        if perfil_img:
            # Garante que o nome do arquivo seja seguro
            filename = secure_filename(perfil_img.filename)
            # Salva a imagem no diretório de uploads
            perfil_img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Define o caminho da imagem para salvar no banco de dados
            imagem_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        try:
            # Atualiza os dados no banco de dados
            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE Pessoa 
                SET email = %s, telefone = %s, imagem_perfil = %s
                WHERE id = %s
            """, (email, telefone, imagem_path, 1))  # Substitua o '1' pelo id do usuário autenticado
            mysql.connection.commit()
            cur.close()
            return jsonify({'message': 'Conta atualizada com sucesso!'}), 200
        except Exception as e:
            print(e)
            return jsonify({'message': 'Erro ao atualizar a conta.'}), 500
        


# Rota para logout
@app.route('/logout')
def logout():
    session.clear()  # Remove todos os dados da sessão
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
