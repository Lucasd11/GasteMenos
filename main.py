# main.py
import os
from datetime import date
from infra.repositorio import RepositorioFinancas
from dominio.categoria import Categoria
from dominio.receita import Receita
from dominio.despesa import Despesa
from dominio.orcamentoMensal import OrcamentoMensal

def limpar_arquivos_teste():
    """Remove arquivos JSON para garantir que o teste seja sempre do zero."""
    for file in [RepositorioFinancas.CATEGORIAS_FILE, RepositorioFinancas.LANCAMENTOS_FILE]:
        if os.path.exists(file):
            os.remove(file)
            print(f"Arquivo {file} limpo.")

def inicializar_e_executar():
    """Cria dados, persiste e gera os relatórios da Semana 3."""

    # Limpar arquivos antigos para um teste limpo
    limpar_arquivos_teste()

    # --- 1. CONFIGURAÇÃO E INSTANCIAÇÃO ---
    print("--- 1. INICIALIZAÇÃO E CRIAÇÃO DE DADOS ---")
    repo = RepositorioFinancas()
    
    # Simula o mês de teste (o mês atual)
    MES_TESTE = date.today().month

    # --- 2. CRIAÇÃO DE CATEGORIAS ---
    
    # Categorias de RECEITA
    c_salario = Categoria(ID_categoria=1, nome="Salário", tipo="RECEITA", limite_mensal=0, descricao="Renda principal")
    c_extra = Categoria(ID_categoria=2, nome="Renda Extra", tipo="RECEITA", limite_mensal=0, descricao="Trabalhos extras")

    # Categorias de DESPESA
    c_aluguel = Categoria(ID_categoria=3, nome="Moradia", tipo="DESPESA", limite_mensal=1200.0, descricao="Aluguel e taxas")
    c_alimentacao = Categoria(ID_categoria=4, nome="Alimentação", tipo="DESPESA", limite_mensal=800.0, descricao="Mercado e restaurantes")
    c_transporte = Categoria(ID_categoria=5, nome="Transporte", tipo="DESPESA", limite_mensal=300.0, descricao="Gasolina e Uber")

    # Salva as categorias no disco
    repo.salvar_categoria(c_salario)
    repo.salvar_categoria(c_extra)
    repo.salvar_categoria(c_aluguel)
    repo.salvar_categoria(c_alimentacao)
    repo.salvar_categoria(c_transporte)
    print("Categorias salvas com sucesso.")


    # --- 3. CRIAÇÃO DE LANÇAMENTOS (RECEITAS e DESPESAS) ---
    
    # Receitas
    r1 = Receita(ID_lancamento=101, valor=3500.00, categoria=c_salario, data=date(2025, MES_TESTE, 5), descricao="Salário Mensal", forma_pagmto = "dinheiro")
    r2 = Receita(ID_lancamento=102, valor=500.00, categoria=c_extra, data=date(2025, MES_TESTE, 15), descricao="Freelance projeto X", forma_pagmto = "pix")

    # Despesas
    d1 = Despesa(ID_lancamento=201, valor=1100.00, categoria=c_aluguel, data=date(2025, MES_TESTE, 1), descricao="Pagamento Aluguel", forma_pagmto="PIX")
    d2 = Despesa(ID_lancamento=202, valor=450.50, categoria=c_alimentacao, data=date(2025, MES_TESTE, 10), descricao="Compras do Mercado Semanal", forma_pagmto="DÉBITO")
    d3 = Despesa(ID_lancamento=203, valor=150.00, categoria=c_transporte, data=date(2025, MES_TESTE, 12), descricao="Combustível", forma_pagmto="CRÉDITO")
    d4 = Despesa(ID_lancamento=204, valor=350.00, categoria=c_alimentacao, data=date(2025, MES_TESTE, 20), descricao="Jantar Fora", forma_pagmto="CRÉDITO")

    # Salva os lançamentos no disco
    repo.salvar_lancamento(r1)
    repo.salvar_lancamento(r2)
    repo.salvar_lancamento(d1)
    repo.salvar_lancamento(d2)
    repo.salvar_lancamento(d3)
    repo.salvar_lancamento(d4)
    print("Lançamentos salvos com sucesso.")


    # --- 4. CARREGAMENTO, AGRUPAMENTO E ORDENAÇÃO ---
    print("\n--- 2. CARREGAMENTO E ORDENAÇÃO ---")
    
    # Carrega todos os lançamentos
    lancamentos_carregados = repo.carregar_lancamentos()
    
    # Demonstração do método mágico __lt__ (ordenação)
    lancamentos_ordenados = sorted(lancamentos_carregados)
    
    print("Lançamentos carregados e ordenados por data:")
    for l in lancamentos_ordenados:
        # Demonstra o método mágico __str__ de Lancamento/Despesa/Receita
        print(f"  [{l.data.strftime('%d/%m')}] R$ {l.valor:,.2f} - {l.categoria.nome}")

    
    # Cria a instância de OrcamentoMensal para o mês de teste
    orcamento = OrcamentoMensal(
        mes=MES_TESTE, 
        prev_receita=4000.00, 
        lancamentos=lancamentos_ordenados, 
        meta_economia=500.00
    )


    # --- 5. GERAÇÃO DOS RELATÓRIOS DA SEMANA 3 ---
    print("\n--- 3. RELATÓRIOS FINAIS (Entrega Semana 3) ---")
    
    # Relatório 1: Saldo Mensal
    total_receitas = orcamento.calcular_total_receitas()
    total_despesas = orcamento.calcular_total_despesas()
    saldo_final = orcamento.calcular_saldo_mensal()

    print(f"\nRELATÓRIO DE SALDO MENSAL (Mês {MES_TESTE}):")
    print("-" * 35)
    print(f"Total Receitas: R$ {total_receitas:,.2f}")
    print(f"Total Despesas: R$ {total_despesas:,.2f}")
    print("-" * 35)
    print(f"SALDO FINAL:    R$ {saldo_final:,.2f}")
    
    # Relatório 2: Despesas por Categoria
    relatorio = orcamento.relatorio_despesas_por_categoria()
    
    print("\nRELATÓRIO DE DESPESAS POR CATEGORIA:")
    print("-" * 35)
    for nome_cat, total_gasto in relatorio.items():
        print(f"  {nome_cat.ljust(15)}: R$ {total_gasto:,.2f}")
    print("-" * 35)
    
    # Demonstração do método mágico __add__
    print("\nDEMONSTRAÇÃO __ADD__:")
    soma_despesas = d1 + d2 + d3 + d4
    print(f"Soma de todas as despesas (d1+d2+d3+d4) usando o método __add__: R$ {soma_despesas:,.2f}")

if __name__ == "__main__":
    inicializar_e_executar()