# Cadastro de Alunos — Python

Aplicativo desktop feito com Python, Tkinter e SQLite. A interface tem organização própria e não copia os elementos visuais da referência.

## Requisitos
- Python 3.10 ou superior
- Tkinter (normalmente incluído na instalação do Python para Windows)
- SQLite já é incluído na biblioteca padrão do Python

## Como executar no Windows
1. Extraia a pasta do projeto.
2. Abra a pasta.
3. Na barra de endereço do Explorador de Arquivos, digite `cmd` e pressione Enter.
4. Execute:

```bash
python cadastro_alunos.py
```

O banco `alunos.db` será criado automaticamente na mesma pasta quando o programa for aberto.

## Recursos
- Cadastrar aluno com nome e e-mail obrigatórios
- Telefone, sexo, nascimento, CPF e curso/turma
- Selecionar o caminho de uma foto
- Listar e pesquisar alunos
- Selecionar um registro para preencher o formulário
- Atualizar, visualizar e excluir cadastros
- Persistência local usando SQLite

## Observações
- A foto é registrada pelo caminho do arquivo; ela não é incorporada ao banco nem exibida como miniatura.
- Use dados fictícios durante testes. O banco guarda dados localmente sem criptografia.
