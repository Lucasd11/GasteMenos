import pytest
from datetime import date
from dominio.categoria import Categoria
from dominio.lancamento import Lancamento
from dominio.receita import Receita
from dominio.despesa import Despesa

@pytest.fixture
def cat_despesa_valida():
    return Categoria(101, "Alimentação", "DESPESA", 500, "Gastos com mercado e restaurante.")

@pytest.fixture
def cat_receita_valida():
    return Categoria(201, "Salário","RECEITA", 0,"Recebimento mensal fixo.")

@pytest.fixture
def lancamento_base_valido(cat_despesa_valida):
    return Lancamento(1, 150.50, cat_despesa_valida, date(2025, 11, 24), "Jantar com amigos.", "CRÉDITO")

def test_categoria_criacao_e_str(cat_despesa_valida):
    assert cat_despesa_valida.nome == "Alimentação"
    assert cat_despesa_valida.tipo == "DESPESA"

    assert "Limite: R$ 500,00" in str(cat_despesa_valida)

def test_categoria_receita_sem_limite(cat_receita_valida):
    assert cat_receita_valida.tipo == "RECEITA"
    assert "Limite:" not in str(cat_receita_valida)

def test_categoria_eq_duplicidade(cat_despesa_valida):
    cat_duplicada = Categoria(999, "Alimentação", "DESPESA", 600.00, "Descrição diferente.")

    assert cat_despesa_valida == cat_duplicada

def test_categoria_setter_nome_vazio(cat_despesa_valida):
    with pytest.raises(ValueError, match = "O nome da categoria não pode ser vazio."):
        cat_despesa_valida.nome = ""
