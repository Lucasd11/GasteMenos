# GasteMenos
Projeto da disciplina de Programação Orientada a Objetos (POO) da Universidade Federal do Cariri (UFCA).
Descrição do Projeto e Objetivo
O Sistema de Controle de Despesas Pessoais é uma aplicação de linha de comando (CLI) desenvolvida para auxiliar no gerenciamento de finanças pessoais, focando no registro rigoroso de receitas e despesas, na definição de orçamentos mensais e na geração de alertas automáticos para controle de gastos.

O principal objetivo é aplicar e consolidar os conceitos de Programação Orientada a Objetos (POO), como encapsulamento, herança, polimorfismo (implícito), métodos especiais e relacionamentos entre classes, para construir um sistema robusto, manutenível e com validações rigorosas.

Estrutura Planejada de Classes (Modelagem OO)
A arquitetura do projeto é baseada em classes bem definidas, com foco na herança e no encapsulamento (@property e @setter). A seguir, estão as classes principais e seus papéis no sistema:

| Classe | Atributos | Métodos Principais |
| :--- | :--- | :--- |
| **Categoria** | ID_categoria, nome, tipo (RECEITA/DESPESA), limite_mensal, descricao | __init__(), @property/@setter, __str__(), __eq__() |
| **Lancamento** (Base) | ID_lancamento, valor, categoria, data, descricao, forma_pagmto | __init__(), @property/@setter, __str__(), __repr__(), __eq__(), __lt__(), __add__() |
| **Receita** | (Herda de Lancamento) | (Implementa validações de tipo) |
| **Despesa** | (Herda de Lancamento) | (Implementa validação: valor > 0) |
| **OrcamentoMensal** | mes, prev_receita, lancamentos (list), meta_economia (percentual) | calcular_saldo(), calcular_total_receitas(), calcular_total_despesas() |
| **Alerta** | tipo, mensagem, data, referencia (Lancamento) | __str__() |
| **SistemaControle** | categorias (list), orcamentos (list), configuracoes (dict) | adicionar_lancamento(), salvar_dados(), carregar_dados(), registrar_alerta() |
| **Relatorio** | (Classe de Serviço) | total_por_categoria(), total_por_forma_pagamento(), comparativo_mensal(), percentual_categorias() |

<img width="765" height="694" alt="image" src="https://github.com/user-attachments/assets/7650aedb-45f1-41fc-89da-52a9348844da" />

