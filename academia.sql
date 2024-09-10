-- Criação do Banco de Dados
CREATE DATABASE academia_cic;
USE academia_cic;

-- Tabela Usuários (com foto de perfil)
CREATE TABLE usuarios (
    cpf VARCHAR(14) PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    foto_perfil BLOB,
    data_nascimento DATE,
    CONSTRAINT email_unique UNIQUE (email)
);

-- Tabela Professores (com foto de perfil, e relacionados com Treinos)
CREATE TABLE professores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    foto_perfil BLOB,
    CONSTRAINT email_professor_unique UNIQUE (email)
);

-- Tabela Treinos (com relacionamento com Professor)
CREATE TABLE treinos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT NOT NULL,
    grupo_muscular ENUM('Superiores', 'Inferiores', 'Core'),
    professor_id INT,
    FOREIGN KEY (professor_id) REFERENCES professores(id)
);

-- Tabela Exercícios (relacionados com Treinos)
CREATE TABLE exercicios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT NOT NULL,
    repeticoes INT NOT NULL,
    series INT NOT NULL,
    descanso_minutos INT NOT NULL,
    treino_id INT,
    FOREIGN KEY (treino_id) REFERENCES treinos(id)
);

-- Tabela Avaliação Física (relacionada com Usuários)
CREATE TABLE avaliacoes_fisicas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_cpf VARCHAR(14),
    imc FLOAT,
    altura DECIMAL(5, 2),
    peso DECIMAL(5, 2),
    data_avaliacao DATE NOT NULL,
    FOREIGN KEY (usuario_cpf) REFERENCES usuarios(cpf) ON DELETE CASCADE
);

-- Tabela Treinos Personalizados (relacionada com Usuários e Treinos)
CREATE TABLE treinos_personalizados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_cpf VARCHAR(14),
    treino_id INT,
    data_criacao DATE NOT NULL,
    FOREIGN KEY (usuario_cpf) REFERENCES usuarios(cpf),
    FOREIGN KEY (treino_id) REFERENCES treinos(id)
);

-- Tabela Categorias de Exercício
CREATE TABLE categorias_exercicio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT
);

-- Tabela Equipamentos
CREATE TABLE equipamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT
);

-- Tabela Treino_Equipamento (Associação entre Treinos e Equipamentos)
CREATE TABLE treino_equipamento (
    treino_id INT,
    equipamento_id INT,
    PRIMARY KEY (treino_id, equipamento_id),
    FOREIGN KEY (treino_id) REFERENCES treinos(id),
    FOREIGN KEY (equipamento_id) REFERENCES equipamentos(id)
);

-- Tabela Favoritos (Relacionados com Usuários e Treinos/Exercícios)
CREATE TABLE favoritos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_cpf VARCHAR(14),
    treino_id INT,
    exercicio_id INT,
    tipo ENUM('treino', 'exercicio'),
    FOREIGN KEY (usuario_cpf) REFERENCES usuarios(cpf),
    FOREIGN KEY (treino_id) REFERENCES treinos(id),
    FOREIGN KEY (exercicio_id) REFERENCES exercicios(id)
);

SELECT * FROM usuarios;
SELECT * FROM professores;


INSERT INTO professores (nome, email, senha, foto_perfil)
VALUES ('Ronaldinho', 'ronaldinho@gaucho.com', 'barcelona', NULL);