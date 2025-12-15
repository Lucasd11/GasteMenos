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

# GasteMenos – Sistema de Controle de Despesas Pessoais

Projeto desenvolvido em **Python**, com foco em **Programação Orientada a Objetos**, para controle de receitas e despesas pessoais.

O sistema foi projetado seguindo princípios de **organização em camadas**, **encapsulamento**, **responsabilidade única** e **facilidade de manutenção**, atendendo aos requisitos das semanas 1 a 5 do tema proposto.

---

## Objetivo do Sistema

Permitir que o usuário registre suas **receitas** e **despesas**, organize-as por **categorias**, acompanhe o **orçamento mensal**, visualize **relatórios financeiros** e receba **alertas automáticos** quando regras de negócio forem violadas (ex.: gastos excessivos).

---

## Funcionalidades

### 1️⃣ Cadastro de Categorias

* Criação, edição e exclusão de categorias
* Tipos: **RECEITA** ou **DESPESA**
* Limite mensal aplicável apenas a despesas
* Descrição opcional
* Validação para impedir categorias duplicadas (mesmo nome e tipo)

### 2️⃣ Lançamento de Receitas e Despesas

* Registro com: valor, categoria, data, descrição e forma de pagamento
* Formas de pagamento suportadas:

  * DINHEIRO
  * DEBITO
  * CREDITO
  * PIX
* Validação de valor (não permite valores ≤ 0)
* Atualização automática do saldo mensal

### 3️⃣ Orçamento Mensal

* Cálculo do total de receitas
* Cálculo do total de despesas
* Cálculo do saldo disponível
* Detecção de saldo negativo

### 4️⃣ Relatórios e Estatísticas

* Total de despesas por categoria
* Total de despesas por forma de pagamento
* Percentual de cada categoria em relação ao total de despesas
* Comparativo entre receitas e despesas
* Identificação do mês mais econômico

### 5️⃣ Alertas Automáticos

* Alerta para despesa de alto valor
* Alerta para extrapolação de limite de categoria
* Alerta para saldo mensal negativo

### 6️⃣ Configurações do Sistema

As regras de alerta e parâmetros gerais são configuráveis via arquivo `settings.json`.

---

## Decisões de Design

### Arquitetura em Camadas

O projeto foi dividido em camadas para melhorar organização e manutenção:

* **dominio/** → regras de negócio e entidades principais
* **infra/** → persistência de dados (arquivos JSON)
* **main.py** → interface de interação com o usuário (menu)

Essa separação evita acoplamento excessivo e facilita testes.

### Programação Orientada a Objetos

* Uso de **encapsulamento** (atributos privados e getters/setters)
* Classes com responsabilidades bem definidas
* Validações centralizadas nas entidades

### Persistência Simples

* Armazenamento em arquivos JSON
* Evita dependência de banco de dados
* Adequado para fins acadêmicos

### Facade (Classe Financas)

A classe `Financas` atua como **fachada**, centralizando as operações do sistema e escondendo a complexidade interna das outras classes.

---

## Explicação das Principais Classes

### 🔹 Categoria

Representa uma categoria financeira.

Atributos:

* nome
* tipo (RECEITA ou DESPESA)
* limite_mensal
* descrição

Responsabilidade:

* Definir e validar categorias

---

### 🔹 Lancamento (classe base)

Classe abstrata que representa um lançamento financeiro.

Atributos:

* valor
* categoria
* data
* descrição
* forma de pagamento

Responsabilidade:

* Garantir validações comuns a receitas e despesas

---

### 🔹 Receita

Especialização de `Lancamento`.

Responsabilidade:

* Representar entradas de dinheiro

---

### 🔹 Despesa

Especialização de `Lancamento`.

Responsabilidade:

* Representar saídas de dinheiro
* Disparar regras de alerta

---

### 🔹 OrcamentoMensal

Responsável por agrupar lançamentos de um mês específico.

Responsabilidades:

* Calcular totais
* Calcular saldo
* Gerar relatórios
* Verificar limites por categoria

---

### 🔹 Alerta

Representa notificações automáticas do sistema.

Tipos:

* ALTO_VALOR
* LIMITE_EXCEDIDO
* SALDO_NEGATIVO

---

### 🔹 Configuracoes

Responsável por ler e gravar o arquivo `settings.json`.

Permite:

* Alterar valor mínimo para alerta de alto gasto
* Definir meta de economia
* Configurar período de comparativos

---

## Estrutura do Projeto

```
GasteMenos/
│
├── main.py
├── settings.json
│
├── dominio/
│   ├── categoria.py
│   ├── lancamento.py
│   ├── receita.py
│   ├── despesa.py
│   ├── alerta.py
│   ├── financas.py
│   ├── orcamento_mensal.py
│   └── settings.py
│
├── infra/
│   └── repositorio.py
│
├── data/
│   ├── categorias.json
│   └── lancamentos.json
│
└── tests/
    ├── test_categoria.py
    ├── test_lancamento.py
    ├── test_alerta.py
    └── test_relatorio.py
```

---

## ▶️ Como Executar

```bash
python main.py
```

---

## Autor

Lucas Sousa

---

## Observações Finais

Este projeto foi desenvolvido com fins **acadêmicos**, priorizando clareza, organização do código e aderência aos conceitos de orientação a objetos.



