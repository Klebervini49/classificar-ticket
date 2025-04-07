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
        "Tela raramente usada não está funcionando após atualização estética",
        # Exemplos específicos para resolver o problema de componentes críticos com problemas estéticos
        "A tela de login é feia",
        "A tela de login tem aparência antiquada",
        "O botão de login está com cor fora do padrão",
        "O formulário de pagamento tem design ultrapassado",
        "A tela de checkout possui visual desagradável",
        "O sistema de autenticação tem aparência pouco profissional",
        "A interface de login precisa ser modernizada",
        "A tela de pagamento tem cores que não combinam",
        "A página de entrada do sistema é esteticamente pobre",
        "O módulo financeiro tem interface desatualizada",
        "Os ícones da tela de login precisam ser redesenhados",
        "A tela de cadastro de usuários tem layout confuso",
        "A página de pagamento precisa de melhorias visuais",
        "O visual do sistema de login está fora do padrão da marca",
        "A tela de login quebra em alguns tamanhos de tela",
        "O sistema de pagamento tem elementos visuais mal alinhados",
        "A área de autenticação tem problemas de posicionamento de botões",
        "A interface do painel principal está desatualizada",
        "O formulário de cadastro tem espaçamento inadequado",
        "A tela de processamento de pedidos tem design confuso",
        "O sistema de login tem fontes inconsistentes",
        "A página inicial possui contraste de cores inadequado",
        "A tela de login tem proporções erradas em dispositivos móveis",
        "O sistema de autenticação tem animações desnecessárias",
        "A tela de login tem problemas de alinhamento visual",
        "O formulário de login é antiquado e precisa ser atualizado",
        "A interface de pagamento tem elementos visuais inconsistentes",
        "O dashboard principal tem elementos visuais mal posicionados",
        "A tela de relatórios tem aparência desorganizada",
        "O sistema de login não segue as diretrizes visuais da empresa"
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

# Palavras relacionadas a problemas estéticos/visuais
palavras_estéticas = [
    "feio", "feia", "desagradável", "antiquado", "antiquada", "datado", "datada",
    "ultrapassado", "ultrapassada", "desalinhado", "desalinhada", "mal posicionado",
    "aparência ruim", "visual pobre", "estética inadequada", "mal formatado",
    "cores erradas", "design ruim", "layout confuso", "visualmente desagradável",
    "esteticamente pobre", "mal projetado", "desorganizado", "desorganizada",
    "não intuitivo", "não intuitiva", "confuso", "confusa", "poluído", "poluída",
    "aparência amadora", "desproporcional", "inconsistente", "desatualizado",
    "desatualizada", "mal estruturado", "mal estruturada"
]

# Componentes críticos do sistema
componentes_críticos = [
    "login", "autenticação", "pagamento", "checkout", "senha", "cadastro", 
    "faturamento", "bancário", "financeiro", "emissão de nota", "dashboard principal",
    "relatório gerencial", "pedido", "compra", "venda", "transação", "saldo"
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
def gerar_tickets(quantidade=30000):
    """
    Gera tickets sintéticos para treinamento do modelo
    """
    # Definir exemplos para cada nível de prioridade
    exemplos = {
        "alto": [
            "Sistema não está respondendo",
            "Erro crítico na aplicação",
            "Não consigo acessar o sistema",
            "Aplicação está fora do ar",
            "Erro 500 ao acessar o sistema",
            "Serviço indisponível",
            "Falha crítica no servidor",
            "Erro de banco de dados crítico",
            "Dados de clientes expostos",
            "Vazamento de informações sensíveis",
            "Sistema de pagamento não processa transações",
            "API principal retornando erro",
            "Não consigo fazer login no sistema",
            "Erro de autenticação em todos os acessos",
            "Sistema financeiro fora do ar",
            "Gateway de pagamento não responde",
            "Clientes não conseguem finalizar compras",
            "O botão de login não funciona",
            "A tela de login não permite acesso",
            "O sistema de autenticação não valida senhas",
            "O pagamento não é processado",
            "O checkout falha ao finalizar",
            "O botão de compra não responde aos cliques",
            "O sistema de autenticação falha ao validar credenciais",
            "A tela de login trava ao tentar acessar",
            "O módulo financeiro não calcula valores corretamente",
            "O gateway de pagamento retorna erro em todas as transações",
            "O sistema de login está fora do ar",
            "Clientes não conseguem fazer login",
            "O sistema está rejeitando todas as transações",
            "A autenticação de usuários está completamente inoperante",
            "Checkout não funciona de jeito nenhum",
            "Login quebrado completamente",
            "Sistema inoperante na parte de pagamentos",
        ],
        "medio": [
            "Lentidão no sistema",
            "Sistema está instável",
            "Performance degradada",
            "Páginas carregando com atraso",
            "Timeout em algumas requisições",
            "Alguns usuários relatando erros",
            "Falha intermitente no login",
            "Sistema apresenta erro ocasionalmente",
            "Algumas funcionalidades estão lentas",
            "Atraso no processamento de dados",
            "Relatórios apresentando informações incompletas",
            "Notificações com atraso",
            "Alguns botões não funcionam corretamente",
            "Parte dos usuários não consegue acessar",
            "Erros em algumas transações",
            "Pesquisa retornando resultados incompletos",
            "Emails de confirmação não chegando",
            "Algumas imagens não carregam",
            "Cálculos incorretos em alguns cenários",
            "Validação de formulários com falhas",
            "Algumas transações estão sendo rejeitadas",
            "Login funciona, mas está lento",
            "Sistema de pagamento processa com atraso",
            "Alguns usuários relatam problemas no checkout",
            "O login falha ocasionalmente",
            "Apenas alguns clientes não conseguem efetuar pagamento",
            "A autenticação funciona, mas com lentidão",
            "O sistema de pagamento está instável, mas funciona",
            "O formulário de login está lento",
            "Sistema lento para fazer login, mas funciona",
            "Checkout por vezes apresenta travamentos",
        ],
        "baixo": [
            "Erro de ortografia na interface",
            "Cor do botão incorreta",
            "Fonte muito pequena",
            "Layout desalinhado",
            "Logotipo com baixa resolução",
            "Texto truncado em alguns componentes",
            "Mensagem de erro com texto confuso",
            "Espaçamento incorreto entre elementos",
            "Menu com item duplicado",
            "Ícones não padronizados",
            "Tradução incompleta em página secundária",
            "Texto em idioma errado em página pouco acessada",
            "Pequena falha no design responsivo",
            "Formato de data inconsistente",
            "Paginação com contador incorreto",
            "Rodapé com informações desatualizadas",
            "Badge de notificação mostrando número errado",
            "Erro de digitação em mensagem de ajuda",
            "Imagem de background com qualidade baixa",
            "A interface está feia",
            "O sistema tem aparência amadora",
            "O design está ultrapassado",
            "A paleta de cores não é atraente",
            "A tela de login é feia",
            "O botão de login tem cor inadequada",
            "A interface de login tem aparência antiquada",
            "A tela de pagamento tem design ultrapassado",
            "O formulário de login tem layout desalinhado",
            "Os botões de pagamento estão com cores que não combinam",
            "A tela de login precisa ser modernizada",
            "O módulo financeiro tem aparência desagradável",
            "A página de checkout tem cores desarmoniosas",
            "O formulário de autenticação tem design pouco profissional",
            "A página de login tem aparência amadora",
            "O sistema de autenticação tem design ultrapassado",
            "O botão de pagamento está com cor errada",
            "A interface do gateway de pagamento não é atraente",
            "Os campos do formulário de login têm tamanho desproporcional",
            "A estética da tela de login está ruim",
            "A aparência da página de checkout não é moderna",
            "O visual do sistema de autenticação é antiquado",
            "A página de login tem layout confuso mas funcional",
            "A estética do sistema de pagamento precisa ser melhorada",
            "O design do módulo de autenticação é pouco atraente",
            "Login feio demais",
            "Login feio mas funcional",
            "Login extremamente feio",
            "UI do login é terrível, mas funciona",
            "UI feia no login mas funcional",
            "Interface terrível mas funcional no login",
            "Aparência de login horrível mas operante",
            "Tela de pagamento visualmente terrível mas que funciona",
            "Design péssimo no login",
            "Login com aparência horrível mas que funciona",
            "Interface do login extremamente feia",
            "Login terrivelmente feio mas operacional"
        ]
    }
    
    # Gerar dados sintéticos
    dados = {"texto": [], "prioridade": []}
    
    # Quantidade de exemplos por prioridade
    quantidade_por_prioridade = quantidade // 3
    
    # Gerar dados para cada prioridade
    for prioridade, exemplos_lista in exemplos.items():
        for _ in range(quantidade_por_prioridade):
            # 1/3 dos exemplos são exemplos diretos da lista
            if random.random() < 0.3:
                texto = random.choice(exemplos_lista)
            # 2/3 são variações
            else:
                base = random.choice(exemplos_lista)
                # Adicionar variações e ruído
                prefixos = ["", "Olá, ", "Estou com um problema: ", "Preciso de ajuda com: ", 
                           "Bom dia, ", "Urgente: ", "Verificar: ", "Problema: "]
                sufixos = ["", " por favor me ajudem", " o que devo fazer?", " isso está me impedindo de trabalhar",
                          " preciso de uma solução", " desde ontem", " aconteceu agora", " após a atualização"]
                
                texto = random.choice(prefixos) + base + random.choice(sufixos)
            
            dados["texto"].append(texto)
            dados["prioridade"].append(prioridade)
    
    # Adicionar casos específicos que falharam anteriormente (com mais peso)
    casos_especificos = {
        "baixo": [
            "Login feio demais",
            "Login feio mas funcional",
            "Login extremamente feio",
            "UI do login é terrível, mas funciona",
            "UI feia no login mas funcional",
            "Interface terrível mas funcional no login",
            "Aparência de login horrível mas operante",
            "Tela de pagamento visualmente terrível mas que funciona",
            "Design péssimo no login",
            "Login com aparência horrível mas que funciona",
            "Interface do login extremamente feia",
            "Login terrivelmente feio mas operacional"
        ],
        "medio": [
            "O formulário de login está lento",
            "O formulário de login está um pouco lento",
            "Formulário de login com lentidão moderada",
            "Login com performance reduzida",
            "Velocidade do login abaixo do esperado"
        ]
    }
    
    # Adicionar casos específicos (com repetição para dar mais peso)
    for prioridade, casos in casos_especificos.items():
        for caso in casos:
            # Adicionar cada caso várias vezes para aumentar seu peso
            for _ in range(30):  # Repetir 30 vezes
                dados["texto"].append(caso)
                dados["prioridade"].append(prioridade)
    
    # Criar dataframe
    df = pd.DataFrame(dados)
    
    # Embaralhar os dados
    df = df.sample(frac=1).reset_index(drop=True)
    
    return df

def main():
    # Gerar o dataset
    df = gerar_tickets()

    # Criar diretório de dados se não existir
    Path("data").mkdir(exist_ok=True)
    
    # Salvar dataset
    caminho_dataset = os.path.join("data", "dataset_tickets_prioridade.csv")
    df.to_csv(caminho_dataset, index=False)
    print(f"Dataset salvo em: {os.path.abspath(caminho_dataset)}")

if __name__ == "__main__":
    main()
