# Banco de Imagens

Sistema de armazenamento de imagens desenvolvido em Python 3.8 com Flask, Flask-SQLAlchemy, Flask Migrate, Flask Script, PyJWT, Pillow, Docker e Docker-compose.

# Sobre o sistema

Este é um sistema de armazenamento de imagens, em que será possível realizar uploads, downloads, modificar e deletar imagens, além do gerenciamento dos usuários da plataforma.

## Tecnologias utilizadas

 - Python 3.8
 - Flask
 - Flask SQLAlchemy
 - Flask Migrate
 - Flask Script
 - PyJWT
 - Pillow
 - MySQL

## Diagrama do banco de dados

<a href="https://ibb.co/zPFySVW"><img src="https://i.ibb.co/XFDhzxf/Banco-De-Dados.png" alt="Banco-De-Dados" border="0"></a>

## Execução

Para executar o projeto é necessário o [Docker](https://docs.docker.com/engine/install/ubuntu/). 

Para executá-lo:	

    docker-compose up --build

## Arquitetura

A tecnologia de banco de dados utilizada é a MySQL: Todos os dados são salvos nele, com excessão dos dados binários das imagens. Com a finalidade de não pesar o banco de dados, cada imagem é separada pela sua extensão e salva no diretório imagem. Ao solicitar alguma imagem, o software buscará nesta pasta a imagem correspondente ao label apresentado pelo usuário - que deverá ser único - e usará a biblioteca Pillow para fazer os devidos redimensionamentos e sua conversão em base64, que será enviado como resposta ao usuário.

O padrão de projeto utilizado na confecção do sistema é basicamente a MVC com a inclusão das camadas Repository e Service - camadas muito utilizadas em outras frameworks, como SpringBoot - para uma melhor organização do código.
