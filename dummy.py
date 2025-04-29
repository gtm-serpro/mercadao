# Imports
import pandas as pd
import random
from faker import Faker
import numpy as np
import os

# Inicializar gerador de dados fake
fake = Faker('pt_BR')

# Configurações básicas
lojas = ['Loja Centro', 'Loja Norte', 'Loja Sul', 'Loja Leste', 'Loja Oeste']
categorias = ['Óculos de Grau', 'Óculos de Sol', 'Lentes de Contato']
formas_pagamento = ['Dinheiro', 'Cartão de Crédito', 'Cartão de Débito', 'Pix']
status_atendimento = ['Em andamento', 'Finalizado', 'Perdido']
campanhas = ['Outono com Estilo', 'Promoção de Lançamento', 'Semana do Consumidor']
meses_referencia = ['Fevereiro/2025', 'Março/2025', 'Abril/2025']

# Funções para gerar dados
def gerar_vendas(loja):
    vendas = []
    for _ in range(20):
        categoria = random.choice(categorias)
        valor_produto = round(random.uniform(150, 800), 2)
        desconto = random.choice([0, 0, 0, 10, 15])  # Descontos ocasionais
        valor_venda = valor_produto * (1 - desconto/100)
        vendas.append([
            fake.date_between(start_date='-30d', end_date='today').strftime("%d/%m/%Y"),
            fake.uuid4(),
            fake.name(),
            fake.word().capitalize(),
            categoria,
            valor_produto,
            round(valor_venda, 2),
            random.choice(formas_pagamento),
            fake.first_name(),
            loja
        ])
    return vendas

def gerar_produtos():
    produtos = []
    for _ in range(15):
        produtos.append([
            fake.uuid4(),
            fake.word().capitalize(),
            random.choice(categorias),
            fake.company(),
            round(random.uniform(80, 300), 2),
            round(random.uniform(300, 800), 2),
            fake.date_between(start_date='-60d', end_date='today').strftime("%d/%m/%Y"),
            random.randint(1, 50),
        ])
    return produtos

def gerar_estoque():
    estoque = []
    for _ in range(15):
        estoque.append([
            fake.uuid4(),
            fake.word().capitalize(),
            random.randint(0, 50),
            5
        ])
    return estoque

def gerar_atendimentos(loja):
    atendimentos = []
    for _ in range(20):
        atendimentos.append([
            fake.date_between(start_date='-30d', end_date='today').strftime("%d/%m/%Y"),
            fake.name(),
            fake.phone_number(),
            fake.word().capitalize(),
            random.choice(status_atendimento),
            fake.first_name(),
            loja
        ])
    return atendimentos

def gerar_financeiro():
    financeiro = []
    for _ in range(20):
        financeiro.append([
            fake.date_between(start_date='-30d', end_date='today').strftime("%d/%m/%Y"),
            fake.uuid4(),
            round(random.uniform(150, 800), 2),
            random.choice(formas_pagamento)
        ])
    return financeiro

def gerar_performance(loja):
    performance = []
    for vendedor in [fake.first_name() for _ in range(5)]:
        vendas_realizadas = random.randint(5, 20)
        valor_total = vendas_realizadas * random.uniform(200, 500)
        ticket_medio = valor_total / vendas_realizadas
        taxa_conversao = random.uniform(20, 80)
        performance.append([
            vendedor,
            loja,
            vendas_realizadas,
            round(valor_total, 2),
            round(ticket_medio, 2),
            round(taxa_conversao, 2)
        ])
    return performance

def gerar_campanhas(loja):
    campanha = []
    for nome_campanha in campanhas:
        campanha.append([
            nome_campanha,
            random.choice(['Óculos de Grau', 'Óculos de Sol']),
            '01/04/2025',
            '30/04/2025',
            random.choice([10, 15, 20]),
            loja,
            random.randint(5, 25)
        ])
    return campanha

# Função para gerar nome seguro de arquivo
def nome_arquivo(loja, mes):
    loja_nome = loja.replace(" ", "_")
    mes_nome = mes.replace("/", "")
    return f"{loja_nome}_{mes_nome}.xlsx"

# Criar diretório
caminho_base = './data/Planilhas_Lojas'
os.makedirs(caminho_base, exist_ok=True)

# Gerar planilhas para cada loja e para cada mês
for loja in lojas:
    for mes in meses_referencia:
        with pd.ExcelWriter(f"{caminho_base}/{nome_arquivo(loja, mes)}") as writer:
            pd.DataFrame(gerar_vendas(loja), columns=[
                "Data da Venda", "Código da Venda", "Cliente", "Produto Vendido", "Categoria",
                "Valor Produto (R$)", "Valor da Venda (R$)", "Forma de Pagamento",
                "Vendedor Responsável", "Loja"
            ]).to_excel(writer, sheet_name='Vendas', index=False)
            
            pd.DataFrame(gerar_produtos(), columns=[
                "Código do Produto", "Nome do Produto", "Categoria", "Marca",
                "Preço de Custo (R$)", "Preço de Venda (R$)", "Data de Entrada no Estoque",
                "Quantidade Atual"
            ]).to_excel(writer, sheet_name='Produtos', index=False)
            
            pd.DataFrame(gerar_estoque(), columns=[
                "Código do Produto", "Nome do Produto", "Quantidade Atual", "Quantidade Mínima"
            ]).to_excel(writer, sheet_name='Estoque', index=False)
            
            pd.DataFrame(gerar_atendimentos(loja), columns=[
                "Data", "Nome do Cliente", "Telefone/WhatsApp", "Produto Interessado",
                "Status do Atendimento", "Vendedor Responsável", "Loja"
            ]).to_excel(writer, sheet_name='Atendimentos', index=False)
            
            pd.DataFrame(gerar_financeiro(), columns=[
                "Data de Recebimento", "Código da Venda", "Valor Recebido (R$)", "Forma de Pagamento"
            ]).to_excel(writer, sheet_name='Financeiro', index=False)
            
            pd.DataFrame(gerar_performance(loja), columns=[
                "Nome do Vendedor", "Loja", "Vendas Realizadas (Qtd)",
                "Valor Total de Vendas (R$)", "Ticket Médio (R$)", "Taxa de Conversão (%)"
            ]).to_excel(writer, sheet_name='Performance', index=False)
            
            pd.DataFrame(gerar_campanhas(loja), columns=[
                "Nome da Campanha", "Produto(s)", "Data de Início", "Data de Fim",
                "% de Desconto", "Loja", "Resultado da Campanha (Vendas)"
            ]).to_excel(writer, sheet_name='Campanhas', index=False)

# Exibir arquivos criados
print(os.listdir(caminho_base))
