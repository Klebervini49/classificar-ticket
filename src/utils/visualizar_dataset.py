import pandas as pd

# Carregar o dataset
df = pd.read_csv('dataset_tickets_prioridade.csv', encoding='utf-8')

# Mostrar as primeiras 10 linhas
print("Primeiros registros do dataset:")
print(df.head(10))

# Mostrar estatísticas do dataset
print("\nEstatísticas do dataset:")
print(f"Total de registros: {len(df)}")
print(f"Distribuição de prioridades:\n{df['prioridade'].value_counts()}") 