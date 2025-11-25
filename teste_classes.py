import pytest
from datetime import date
from dominio.categoria import Categoria
from dominio.receita import Receita
from dominio.despesa import Despesa

categoria1 = Categoria(1, "Aluguel", "despesa", 700.00, "Aluguel da casa no endereço: [...]")
categoria2 = Categoria(2, "Salario", "receita", 789, "Sou engenheiro de software e tenho renda fixa de R$ 3.000")
lancamento1 = Despesa(101, 500.00, categoria1, date.today(), "Primeiro mês de aluguel pago.", "dinheiro")
lancamento2 = Receita(201, 3000, categoria2, date.today(), "Salário referente ao mês de Dezembro.", "Pix")

print(lancamento2)