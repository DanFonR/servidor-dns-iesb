# Trabalho DNS

## Instalação

1. No arquivo de hosts do seu sitema (C:\Windows\System32\drivers\etc\hosts ou /etc/hosts), adicione as seguintes linhas:  
    127.0.0.1  db.aredanvisa.local  
    127.0.0.1  api.aredanvisa.local  
    127.0.0.1  www.aredanvisa.local  

2. Instale Docker;
3. Certifique-se que o Docker Engine esteja rodando;
4. Crie um arquivo .env na raíz do projeto (conforme o arquivo `template.env`);
5. Acesse a pasta `docker`;
6. Rode o script em `up.sh` (ou copie o conteúdo e cole no terminal);