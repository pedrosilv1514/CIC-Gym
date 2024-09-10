-- Iniciando o banco de dados
CREATE DATABASE IF NOT exists academia;
USE academia;

-- Tabela Pessoa
CREATE TABLE Pessoa (
    idPessoa INT AUTO_INCREMENT PRIMARY KEY,
    cpf VARCHAR(14) NOT NULL,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    dataNascimento DATE NOT NULL,
    senha VARCHAR(255) NOT NULL
);

-- Tabela Aluno
CREATE TABLE Aluno (
    idAluno INT AUTO_INCREMENT PRIMARY KEY,
    objetivo VARCHAR(255),
    dataMatricula DATE NOT NULL,
    idPessoa INT,
    FOREIGN KEY (idPessoa) REFERENCES Pessoa(idPessoa)
);

-- Tabela Professor
CREATE TABLE Professor (
    idProfessor INT AUTO_INCREMENT PRIMARY KEY,
    especialidade VARCHAR(255) NOT NULL,
    registroCREF VARCHAR(20) NOT NULL,
    idPessoa INT,
    FOREIGN KEY (idPessoa) REFERENCES Pessoa(idPessoa)
);

-- Tabela Gerente
CREATE TABLE Gerente (
    idGerente INT AUTO_INCREMENT PRIMARY KEY,
    cargo VARCHAR(255) NOT NULL,
    idPessoa INT,
    FOREIGN KEY (idPessoa) REFERENCES Pessoa(idPessoa)
);

-- Tabela Avaliação Física
CREATE TABLE AvaliacaoFisica (
    idAvaliacao INT AUTO_INCREMENT PRIMARY KEY,
    peso DECIMAL(5,2) NOT NULL,
    altura DECIMAL(4,2) NOT NULL,
    imc DECIMAL(4,2) GENERATED ALWAYS AS (peso / (altura * altura)) STORED,
    dataAvaliacao DATE NOT NULL,
    idAluno INT,
    FOREIGN KEY (idAluno) REFERENCES Aluno(idAluno)
);

-- Tabela Modalidade
CREATE TABLE Modalidade (
    idModalidade INT AUTO_INCREMENT PRIMARY KEY,
    nomeModalidade VARCHAR(255) NOT NULL,
    descricao TEXT,
    tipo VARCHAR(255)
);

-- Tabela Treino
CREATE TABLE Treino (
    idTreino INT AUTO_INCREMENT PRIMARY KEY,
    nomeTreino VARCHAR(255) NOT NULL,
    tipoTreino VARCHAR(255),
    duracao TIME NOT NULL,
    dataCriacao DATE NOT NULL,
    idAluno INT,
    FOREIGN KEY (idAluno) REFERENCES Aluno(idAluno),
    idProfessor INT,
    FOREIGN KEY (idProfessor) REFERENCES Professor(idProfessor)
);

-- Tabela Frequência
CREATE TABLE Frequencia (
    idFrequencia INT AUTO_INCREMENT PRIMARY KEY,
    data DATE NOT NULL,
    hora TIME NOT NULL,
    presenca BOOLEAN NOT NULL,
    idAluno INT,
    FOREIGN KEY (idAluno) REFERENCES Aluno(idAluno)
);

-- Tabela Exercício
CREATE TABLE Exercicio (
    idExercicio INT AUTO_INCREMENT PRIMARY KEY,
    nomeExercicio VARCHAR(255) NOT NULL,
    descricao TEXT,
    grupoMuscular VARCHAR(255)
);

-- Tabela Local
CREATE TABLE Local (
    idLocal INT AUTO_INCREMENT PRIMARY KEY,
    nomeLocal VARCHAR(255) NOT NULL,
    enderecoLocal VARCHAR(255) NOT NULL
);

-- Relacionamento entre Modalidade e Treino
CREATE TABLE Modalidade_Treino (
    idModalidade INT,
    idTreino INT,
    PRIMARY KEY (idModalidade, idTreino),
    FOREIGN KEY (idModalidade) REFERENCES Modalidade(idModalidade),
    FOREIGN KEY (idTreino) REFERENCES Treino(idTreino)
);

-- Relacionamento entre Treino e Exercício
CREATE TABLE Treino_Exercicio (
    idTreino INT,
    idExercicio INT,
    PRIMARY KEY (idTreino, idExercicio),
    FOREIGN KEY (idTreino) REFERENCES Treino(idTreino),
    FOREIGN KEY (idExercicio) REFERENCES Exercicio(idExercicio)
);

CREATE TABLE LogAtividades (
    idLog INT AUTO_INCREMENT PRIMARY KEY,
    idPessoa INT,
    acao VARCHAR(255),
    dataHora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (idPessoa) REFERENCES Pessoa(idPessoa)
);

CREATE TABLE HistoricoTreino (
    idHistorico INT AUTO_INCREMENT PRIMARY KEY,
    idAluno INT,
    idTreino INT,
    dataCompleto DATE NOT NULL,
    FOREIGN KEY (idAluno) REFERENCES Aluno(idAluno),
    FOREIGN KEY (idTreino) REFERENCES Treino(idTreino)
);
