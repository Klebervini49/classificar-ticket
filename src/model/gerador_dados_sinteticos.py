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
        # Novos exemplos para situações de "não está funcionando" com alta prioridade
        "Tela de pagamento não está funcionando para nenhum usuário",
        "Sistema de autenticação não funciona para todos os clientes",
        "Módulo crítico de faturamento parou de funcionar completamente",
        "API principal não está funcionando, impedindo todas as integrações",
        "Sistema de checkout não funciona, impossibilitando vendas",
        "Portal do cliente não está funcionando para nenhum usuário",
        "Tela de emissão de notas fiscais não funciona, paralisando entregas",
        "Módulo financeiro não está funcionando, impedindo fechamento contábil",
        "Banco de dados principal parou de funcionar",
        "O sistema de login parou completamente de funcionar",
        "Nenhum usuário consegue acessar o sistema, não está funcionando",
        "Função vital de processamento de pedidos não está funcionando",
        "Dashboard principal utilizado por toda empresa não funciona",
        "Serviço de autenticação parou de funcionar, bloqueando todos os acessos",
        "Sistema crítico de monitoramento não está funcionando"
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
        # Novos exemplos para situações de "não está funcionando" com média prioridade
        "Tela de relatórios não está funcionando para alguns departamentos",
        "Função de exportação para Excel não está funcionando corretamente",
        "Alguns botões de ação não estão funcionando em determinadas telas",
        "Módulo de busca avançada não funciona como esperado",
        "Filtros da tela de pedidos não estão funcionando para alguns usuários",
        "Integração com sistema secundário não está funcionando corretamente",
        "Tela de cadastro não funciona em navegadores específicos",
        "Notificações por email não estão funcionando para alguns usuários",
        "Dashboard secundário não está funcionando após atualização",
        "Ferramentas de análise não estão funcionando adequadamente",
        "Alguns relatórios não estão funcionando corretamente",
        "Importação de dados não funciona em determinados formatos",
        "Função de agendamento não está funcionando para eventos futuros",
        "Tela X não está funcionando para um grupo específico de usuários",
        "Botão de confirmação não está funcionando em alguns dispositivos móveis"
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
        # Novos exemplos para situações de "não está funcionando" com baixa prioridade
        "Animação do botão de ajuda não está funcionando",
        "Ícone de notificação não está funcionando na versão móvel",
        "Função de ordenar por data não está funcionando na tela de histórico",
        "Link do rodapé para termos de uso não está funcionando",
        "Contador de caracteres não está funcionando em comentários",
        "Botão de tema escuro não está funcionando no perfil do usuário",
        "Preview de imagem não está funcionando no upload de avatar",
        "Tela de créditos não está funcionando no menu Sobre",
        "Modo paisagem não está funcionando em tablets específicos",
        "Formulário de feedback não está funcionando na página de contato",
        "Decoração visual não está funcionando em resoluções ultrawide",
        "Auto-complete de endereço não está funcionando em cadastros secundários",
        "Badge de notificação não está funcionando no ícone do perfil",
        "Opção de compartilhar por email não está funcionando",
        "Tela raramente usada não está funcionando após atualização estética"
    ]
}

# Variações para aumentar a diversidade de descrições
variações_não_funciona = [
    "não está funcionando",
    "não funciona",
    "parou de funcionar",
    "deixou de funcionar",
    "apresenta falha de funcionamento",
    "está fora do ar",
    "não opera corretamente",
    "está inoperante",
    "apresenta erro de funcionamento",
    "não responde como deveria",
    "falha ao executar",
    "não está operacional",
    "quebrou",
    "está com defeito",
    "está com problema"
]

# Qualificadores de contexto para cada prioridade
contexto_alto = [
    "para todos os usuários",
    "completamente",
    "impedindo operações críticas",
    "bloqueando o sistema inteiro",
    "paralisando toda a operação",
    "gerando grande prejuízo",
    "afetando todos os clientes",
    "de forma crítica",
    "em todas as tentativas",
    "impactando toda a empresa"
]

contexto_medio = [
    "para alguns usuários",
    "intermitentemente",
    "em casos específicos",
    "ocasionalmente",
    "após determinadas ações",
    "em alguns navegadores",
    "parcialmente",
    "em certas condições",
    "para um departamento específico",
    "em horários de pico"
]

contexto_baixo = [
    "em casos muito raros",
    "apenas visualmente",
    "sem impactar funcionalidades principais",
    "em uma área pouco utilizada",
    "apenas na versão de testes",
    "para usuários com configurações não padrão",
    "apenas em dispositivos desatualizados",
    "sem afetar a experiência principal",
    "em uma tela secundária",
    "apenas em condições específicas e raras"
]

# Gerador de tickets sintéticos melhorado
def gerar_tickets(categoria, exemplos_base, total=12000):
    tickets = []
    
    # Determinar o contexto baseado na categoria
    if categoria == "alto":
        contextos = contexto_alto
    elif categoria == "medio":
        contextos = contexto_medio
    else:
        contextos = contexto_baixo
    
    # Gerar tickets a partir dos exemplos base
    for _ in range(total // 2):  # Metade dos tickets virá dos exemplos base
        base = random.choice(exemplos_base)
        complemento = random.choice([
            "", " conforme relatado pela equipe", " com impacto parcial",
            " que afeta usuários em produção", " após atualização", 
            " causando atraso em entregas", " durante horário de pico",
            " de forma aleatória", " que precisa ser resolvido urgentemente",
            " que pode afetar outros módulos"
        ])
        tickets.append(f"{base}{complemento}")
    
    # Gerar tickets com padrão "X não está funcionando Y"
    templates = [
        "A tela de {0} {1} {2}",
        "O módulo de {0} {1} {2}",
        "A função de {0} {1} {2}",
        "O sistema de {0} {1} {2}",
        "O recurso de {0} {1} {2}",
        "A página de {0} {1} {2}",
        "O botão de {0} {1} {2}",
        "A integração com {0} {1} {2}",
        "O processo de {0} {1} {2}",
        "A ferramenta de {0} {1} {2}"
    ]
    
    funcionalidades = {
        "alto": [
            "login", "pagamento", "checkout", "faturamento", "emissão de notas fiscais",
            "autenticação", "controle de acesso", "processamento de pedidos", "gestão financeira",
            "banco de dados", "dashboard principal", "monitoramento", "backup", "conciliação bancária",
            "relatórios gerenciais"
        ],
        "medio": [
            "relatórios", "cadastro de clientes", "busca avançada", "exportação de dados",
            "filtros", "notificações", "importação", "agendamento", "análise", "dashboards secundários",
            "gestão de usuários", "configurações", "controle de estoque", "atendimento", "integração de APIs"
        ],
        "baixo": [
            "ajuda", "temas", "perfil", "preferências", "compartilhamento", "feedback",
            "histórico", "preview de imagens", "notificações visuais", "ordenação de listas",
            "personalização", "estatísticas secundárias", "tutoriais", "dicas", "créditos do sistema"
        ]
    }
    
    # Gerar tickets adicionais com o padrão de funcionalidade que não funciona
    for _ in range(total // 2):  # Metade dos tickets com esse padrão
        template = random.choice(templates)
        funcionalidade = random.choice(funcionalidades[categoria])
        variação = random.choice(variações_não_funciona)
        contexto = random.choice(contextos)
        
        ticket = template.format(funcionalidade, variação, contexto)
        tickets.append(ticket)
    
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
