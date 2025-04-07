import pandas as pd
import random
import os
from pathlib import Path

# Obter o diretório raiz do projeto
PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()
DATA_DIR = PROJECT_ROOT / "data"

# Garantir que o diretório de dados existe
os.makedirs(DATA_DIR, exist_ok=True)

# Categorias
prioridades = ["alto", "medio", "baixo"]

# Exemplos base para cada prioridade
exemplos = {
    "alto": [
        "Sistema está completamente fora do ar",
        "Erro crítico impedindo o acesso de todos os usuários",
        "Falha de segurança detectada com impacto recorrente",
        "Dados sensíveis estão sendo expostos",
        "Usuários não conseguem efetuar login no sistema",
        "Autenticação falha completamente para todos os usuários",
        "Pagamentos estão falhando em todas as tentativas",
        "Integração com sistema bancário parou de funcionar",
        "Aplicativo fecha sozinho ao abrir",
        "Nota fiscal não é emitida após liberação da nova versão",
        "Relatórios de vendas apresentam valores incorretos",
        "Sistema travando completamente ao processar pedidos",
        "Erro crítico impede processamento de dados",
        "Perda de dados importante detectada no servidor",
        "Falha severa no banco de dados",
        "Sistema não está processando transações",
        "Serviço principal completamente inoperante",
        "Falha catastrófica no servidor principal",
        "Serviço de backend não responde a nenhuma requisição",
        "Erro fatal no processamento de pagamentos",
        "Sistema deu erro grave",
        "Erro crítico no sistema",
        "Sistema apresentou falha total",
        "Sistema caiu completamente",
        "Sistema com erro que impede operação",
    ],
    "medio": [
        "Funcionalidade importante com comportamento intermitente",
        "Gráficos não estão atualizando conforme relatório recebido",
        "Demora acima do normal ao carregar alguns módulos",
        "Usuários reportam lentidão esporádica no sistema",
        "Erro aparece após várias tentativas de cadastro",
        "Exportação de planilhas falha em alguns casos",
        "Usuários recebem mensagem de erro ao tentar salvar dados",
        "Funcionalidade de pesquisa retorna resultados incorretos",
        "Mensagens de alerta estão em inglês em vez de português",
        "Sistema não envia notificação para usuários inativos",
        "Sistema deu erro",
        "Sistema apresentou falha",
        "Sistema com erro intermitente",
        "Erro no sistema ao processar alguns dados",
        "Sistema apresenta erro em algumas operações",
        "Sistema com falha parcial",
        "Erro no sistema durante uso específico",
        "Sistema apresenta mensagens de erro esporádicas",
        "Sistema deu erro em algumas funcionalidades",
        "Falha no sistema que afeta parte dos usuários",
    ],
    "baixo": [
        "Erro de digitação no site com impacto recorrente",
        "Botão desalinhado na tela de cadastro",
        "Campo de busca não limpa após enviar formulário",
        "Sugestão de melhoria na interface do painel de controle",
        "Layout quebra em resoluções muito pequenas",
        "Texto de ajuda desatualizado em algumas páginas",
        "Usuário pediu mudança na cor do botão",
        "Requisição de melhoria estética no formulário",
        "Tooltip não aparece corretamente ao passar o mouse",
        "Espaçamento entre campos pode ser otimizado",
        "Botão de login está com cor errada",
        "Cor do cabeçalho não corresponde à identidade visual",
        "Ícones de menu estão desalinhados",
        "Fonte de texto muito pequena em algumas telas",
        "Problema visual no rodapé em navegadores específicos",
        "Elementos visuais desalinhados na página de perfil",
        "Cores de botões inconsistentes entre páginas",
        "Problema cosmético na interface do usuário",
        "Ajuste visual requisitado no menu lateral",
        "Logo aparece levemente distorcida em alguns dispositivos",
        "O sistema é feio",
        "Interface não agrada visualmente aos usuários",
        "Usuários acham o design desagradável",
        "Layout pouco atrativo para os usuários",
        "Design da interface precisa ser modernizado",
        "Aparência do sistema está datada",
        "Sistema visualmente pouco atraente",
        "Usuários reclamam da aparência do sistema",
        "Estética da interface não agrada aos usuários",
        "Solicitação para deixar o sistema mais bonito",
        "O sistema é ruim",
        "Os usuários não gostam do sistema",
        "O sistema tem uma experiência de usuário ruim",
        "A plataforma é difícil de usar",
        "O sistema não é intuitivo",
        "Reclamação sobre a experiência geral do sistema",
        "Os usuários acham o sistema péssimo",
        "Feedback negativo sobre a experiência do usuário",
        "Sistema considerado inadequado pelos usuários",
        "Sistema avaliado como de baixa qualidade",
        "Usuários reportam insatisfação com o sistema",
        "Interface confusa para os usuários",
        "Sistema considerado obsoleto pelos usuários",
        "Experiência de usuário considerada frustrante",
    ]
}

# Gerador de tickets sintéticos
def gerar_tickets(categoria, exemplos_base, total=10000):
    tickets = []
    for _ in range(total):
        base = random.choice(exemplos_base)
        complemento = random.choice([
            "", " conforme relatado pela equipe", " com impacto parcial",
            " que afeta usuários em produção", " após atualização", 
            " causando atraso em entregas", " durante horário de pico",
            " de forma aleatória", " que precisa ser resolvido urgentemente",
            " que pode afetar outros módulos"
        ])
        tickets.append(f"{base}{complemento}")
    return tickets

def main():
    # Gerar o dataset
    data = []
    for prioridade in prioridades:
        tickets = gerar_tickets(prioridade, exemplos[prioridade])
        for texto in tickets:
            data.append({"texto": texto, "prioridade": prioridade})

    # Criar DataFrame
    df = pd.DataFrame(data)

    # Salvar como CSV
    csv_path = DATA_DIR / "dataset_tickets_prioridade.csv"
    df.to_csv(csv_path, index=False, encoding='utf-8')
    print(f"Dataset salvo em: {csv_path}")
    return csv_path

if __name__ == "__main__":
    main()
