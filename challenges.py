"""
=============================================================================
AULA: PROMPT ENGINEERING - DESAFIOS PRÁTICOS
=============================================================================

Cada desafio = 1 mini-experimento controlado
Você mostra o prompt, executa, analisa a saída e conecta com a teoria.

"Prompt Engineering aplicado como arquitetura de software"

BEST PRACTICE: Todos os exemplos usam System Prompt para definir comportamento!
=============================================================================
"""

# =============================================================================
# CONFIGURAÇÃO INICIAL (Base Técnica)
# =============================================================================

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Inicializa o cliente da OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def run_prompt(
    prompt: str,
    system_prompt: str = None,
    temperature: float = 0.2
) -> str:
    """
    Função base para executar prompts.

    Args:
        prompt: O texto do prompt do usuário (user message)
        system_prompt: Instruções de sistema que definem o comportamento do modelo.
                      BEST PRACTICE: sempre usar para definir papel e restrições!
        temperature: Controla criatividade (0.2 = conservador, 0.9 = criativo)

    Returns:
        Resposta do modelo como string

    Nota sobre System Prompt (Best Practice):
        - System prompt define QUEM o modelo é e COMO ele deve se comportar
        - User prompt contém a TAREFA específica e os DADOS
        - Separar os dois melhora consistência e reusabilidade
    """
    messages = []

    # System prompt define o comportamento persistente do modelo
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    # User prompt contém a tarefa/pergunta específica
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content


# =============================================================================
# DESAFIO 1: O ARQUITETO DE PERSONAS
# =============================================================================
# Objetivo: Demonstrar Contrato de Execução completo com System Prompt
# System prompt define QUEM, User prompt define O QUÊ
# -----------------------------------------------------------------------------

def desafio_01_arquiteto_personas():
    """
    DESAFIO 1: O Arquiteto de Personas

    Demonstra a separação correta:
    - SYSTEM: Define persona, tom, restrições (comportamento)
    - USER: Define contexto, tarefa, dados (requisição específica)
    """
    print("\n" + "=" * 60)
    print("DESAFIO 1: O ARQUITETO DE PERSONAS")
    print("=" * 60)
    print("Objetivo: Contrato de Execução com System Prompt")
    print("-" * 60)

    # System prompt define QUEM o modelo é e COMO deve se comportar
    system_prompt = """Você é um advogado sênior especializado em contratos empresariais.

Características:
- Comunicação clara para não especialistas
- Foco em identificar riscos financeiros
- Linguagem simples, sem juridiquês

Formato de resposta:
- Use tópicos claros e objetivos
- Máximo de 200 palavras
- Destaque apenas os riscos mais relevantes"""

    # User prompt define O QUÊ fazer com quais DADOS
    user_prompt = """Contexto:
Este resumo será entregue a clientes leigos que precisam entender
os riscos de um contrato antes de assinar.

Tarefa:
Analise o contrato abaixo e destaque os principais riscos financeiros.

Contrato:
O contrato estabelece multas por rescisão antecipada, cláusulas de exclusividade
e reajustes automáticos anuais vinculados a índices econômicos."""

    print(f"\n[System Prompt]:\n{system_prompt}\n")
    print(f"[User Prompt]:\n{user_prompt}")
    print("-" * 40)
    print("Resposta:")
    print(run_prompt(user_prompt, system_prompt=system_prompt))

    print("\n" + "-" * 40)
    print("Best Practice:")
    print("'System define QUEM e COMO. User define O QUÊ e COM QUAIS DADOS.'")


# =============================================================================
# DESAFIO 2: FEW-SHOT PROMPTING (CLASSIFICAÇÃO)
# =============================================================================
# Objetivo: Ensinar o modelo por PADRÃO, não por regra abstrata
# System prompt define o papel, User prompt fornece exemplos
# -----------------------------------------------------------------------------

def desafio_02_few_shot_classificacao():
    """
    DESAFIO 2: Few-Shot Prompting

    Técnica: System prompt define o classificador, User prompt dá exemplos.
    O modelo infere o padrão a partir dos exemplos.
    """
    print("\n" + "=" * 60)
    print("DESAFIO 2: FEW-SHOT PROMPTING")
    print("=" * 60)
    print("Objetivo: Ensinar por padrão com System + Few-shot")
    print("-" * 60)

    # System prompt define o papel do classificador
    system_prompt = """Você é um classificador de sentimentos especializado em feedback de apps de meditação.

Regras:
- Classifique como: Positivo, Negativo ou Neutro
- Responda APENAS com a classificação, sem explicações
- Seja consistente com os exemplos fornecidos pelo usuário
- Em caso de ambiguidade, considere o tom geral"""

    # User prompt contém os exemplos (few-shot) e a tarefa
    user_prompt = """Exemplos de classificação:

Texto: "Amei a nova meditação!"
Sentimento: Positivo

Texto: "O app travou no meio."
Sentimento: Negativo

Texto: "Poderia ter mais opções."
Sentimento: Neutro

---
Agora classifique:
Texto: "Não sei se gostei da voz."
Sentimento:"""

    print(f"\n[System Prompt]:\n{system_prompt}\n")
    print(f"[User Prompt com Few-Shot]:\n{user_prompt}")
    print("-" * 40)
    print("Resposta:")
    print(run_prompt(user_prompt, system_prompt=system_prompt))

    print("\n" + "-" * 40)
    print("Best Practice:")
    print("'System define o classificador, User fornece exemplos e tarefa.'")


# =============================================================================
# DESAFIO 3: LABORATÓRIO DE PARÂMETROS (TEMPERATURE)
# =============================================================================
# Objetivo: Mostrar que parâmetros não compensam prompt ruim,
# mas REFORÇAM intenção quando combinados com bom System prompt
# -----------------------------------------------------------------------------

def desafio_03_laboratorio_temperature():
    """
    DESAFIO 3: Laboratório de Parâmetros

    Demonstra: System prompt + Temperature = controle fino sobre a saída
    - Temperature baixa (0.2): Conservador, previsível
    - Temperature alta (0.9): Criativo, mais diversidade
    """
    print("\n" + "=" * 60)
    print("DESAFIO 3: LABORATÓRIO DE PARÂMETROS (TEMPERATURE)")
    print("=" * 60)
    print("Objetivo: System prompt + Temperature = controle fino")
    print("-" * 60)

    # System prompt define o papel criativo
    system_prompt = """Você é um copywriter especializado em marcas sustentáveis.

Estilo:
- Slogans memoráveis e impactantes
- Conexão emocional com sustentabilidade
- Máximo de 10 palavras por slogan
- Responda apenas com o slogan, sem explicações"""

    user_prompt = "Crie um slogan para uma marca de roupas sustentáveis."

    print(f"\n[System Prompt]:\n{system_prompt}\n")
    print(f"[User Prompt]: {user_prompt}")

    # ----- Temperature Baixa (0.2) -----
    print("\n" + "-" * 40)
    print("TEMPERATURE 0.2 (Conservador)")
    print("-" * 40)
    print(run_prompt(user_prompt, system_prompt=system_prompt, temperature=0.2))

    # ----- Temperature Alta (0.9) -----
    print("\n" + "-" * 40)
    print("TEMPERATURE 0.9 (Criativo)")
    print("-" * 40)
    print(run_prompt(user_prompt, system_prompt=system_prompt, temperature=0.9))

    print("\n" + "-" * 40)
    print("Best Practice:")
    print("'System prompt garante consistência, temperature controla variação.'")


# =============================================================================
# DESAFIO 4: DECOMPOSIÇÃO DE PROBLEMAS (PIPELINE)
# =============================================================================
# Objetivo: Mostrar que cada etapa deve ter seu próprio System prompt
# especializado para a tarefa específica
# -----------------------------------------------------------------------------

def desafio_04_prompt_frankenstein():
    """
    DESAFIO 4A: Prompt Frankenstein (Anti-padrão)

    Problema: Mesmo com system prompt, pedir tudo de uma vez é problemático.
    """
    print("\n" + "=" * 60)
    print("DESAFIO 4A: PROMPT FRANKENSTEIN (ANTI-PADRÃO)")
    print("=" * 60)
    print("Problema: Múltiplas tarefas em um único prompt")
    print("-" * 60)

    # System prompt genérico (problema!)
    system_prompt = "Você é um assistente de marketing digital."

    user_prompt = """Crie um plano de marketing completo para um novo SaaS de CRM,
incluindo análise de concorrência, 5 posts para LinkedIn
e uma estratégia de SEO."""

    print(f"\n[System Prompt]: {system_prompt}")
    print(f"[User Prompt]:\n{user_prompt}")
    print("-" * 40)
    print("Resposta:")
    print(run_prompt(user_prompt, system_prompt=system_prompt))

    print("\n" + "-" * 40)
    print("Problema identificado:")
    print("'System prompt genérico + múltiplas tarefas = resultado inconsistente'")


def desafio_04_pipeline_correto():
    """
    DESAFIO 4B: Pipeline Correto (3 Etapas)

    Best Practice: Cada etapa tem seu próprio System prompt especializado.
    """
    print("\n" + "=" * 60)
    print("DESAFIO 4B: PIPELINE CORRETO (3 ETAPAS)")
    print("=" * 60)
    print("Best Practice: System prompt especializado por etapa")
    print("-" * 60)

    # ----- PASSO 1: Pesquisa de Mercado -----
    print("\n" + "-" * 40)
    print("PASSO 1: Pesquisa de Mercado")
    print("-" * 40)

    # System prompt especializado para análise de mercado
    system_prompt_analista = """Você é um analista de mercado especializado em SaaS B2B.

Expertise:
- Análise competitiva de CRMs
- Identificação de diferenciais de mercado
- Tendências de tecnologia empresarial

Formato de resposta:
- Lista objetiva e concisa
- Máximo 5 diferenciais principais
- Foco em oportunidades de posicionamento"""

    user_passo_1 = "Analise o mercado de CRMs e identifique os principais diferenciais competitivos para um novo SaaS."

    print(f"[System]: Analista de mercado SaaS B2B")
    print(f"[User]: {user_passo_1}")
    analise_mercado = run_prompt(user_passo_1, system_prompt=system_prompt_analista)
    print(f"\nResultado:\n{analise_mercado}")

    # ----- PASSO 2: Conteúdo (LinkedIn) -----
    print("\n" + "-" * 40)
    print("PASSO 2: Conteúdo para LinkedIn")
    print("-" * 40)

    # System prompt especializado para social media
    system_prompt_social = """Você é um especialista em conteúdo para LinkedIn B2B.

Estilo:
- Tom profissional e educativo
- Posts que geram engajamento
- Foco em valor para o leitor
- Cada post com hook forte na primeira linha

Formato:
- 5 posts distintos
- Cada post com 3-4 parágrafos curtos
- Inclua CTA sutil no final"""

    user_passo_2 = f"""Com base nos diferenciais abaixo, crie 5 posts para LinkedIn:

Diferenciais:
{analise_mercado}"""

    print(f"[System]: Especialista em LinkedIn B2B")
    posts_linkedin = run_prompt(user_passo_2, system_prompt=system_prompt_social)
    print(f"\nResultado:\n{posts_linkedin}")

    # ----- PASSO 3: SEO -----
    print("\n" + "-" * 40)
    print("PASSO 3: Estratégia de SEO")
    print("-" * 40)

    # System prompt especializado para SEO
    system_prompt_seo = """Você é um especialista em SEO para empresas de tecnologia.

Expertise:
- Keyword research para SaaS
- Estratégia de conteúdo para ranqueamento
- SEO técnico e on-page

Formato de resposta:
- Lista de palavras-chave principais (5-7)
- Lista de palavras-chave de cauda longa (5-7)
- 3 temas de conteúdo prioritários"""

    user_passo_3 = f"""Com base nos diferenciais do CRM abaixo, sugira uma estratégia de SEO:

Diferenciais:
{analise_mercado}"""

    print(f"[System]: Especialista em SEO para SaaS")
    seo_strategy = run_prompt(user_passo_3, system_prompt=system_prompt_seo)
    print(f"\nResultado:\n{seo_strategy}")

    print("\n" + "-" * 40)
    print("Best Practice:")
    print("'Cada etapa = System prompt especializado = resultado de qualidade'")


# =============================================================================
# MENU PRINCIPAL - EXECUÇÃO DOS DESAFIOS
# =============================================================================

def menu_desafios():
    """
    Menu interativo para executar os desafios individualmente.
    """
    desafios = {
        "1": ("Arquiteto de Personas (System + User)", desafio_01_arquiteto_personas),
        "2": ("Few-Shot Prompting (System + Exemplos)", desafio_02_few_shot_classificacao),
        "3": ("Laboratório de Temperature", desafio_03_laboratorio_temperature),
        "4a": ("Prompt Frankenstein (Anti-padrão)", desafio_04_prompt_frankenstein),
        "4b": ("Pipeline Correto (System por etapa)", desafio_04_pipeline_correto),
        "0": ("Executar TODOS os desafios", None),
    }

    while True:
        print("\n" + "=" * 60)
        print("   PROMPT ENGINEERING - DESAFIOS PRÁTICOS")
        print("   (Todos usam System Prompt como best practice)")
        print("=" * 60)
        print("\nEscolha um desafio:\n")

        for key, (name, _) in desafios.items():
            print(f"  [{key:>2}] {name}")

        print("\n  [q] Sair")
        print("=" * 60)

        escolha = input("\nDigite sua escolha: ").strip().lower()

        if escolha == "q":
            print("\n" + "=" * 60)
            print("Fechamento Didático:")
            print("-" * 60)
            print("Você demonstrou com código:")
            print("  - System prompt define QUEM e COMO")
            print("  - User prompt define O QUÊ e COM QUAIS DADOS")
            print("  - Few-shot: System define papel, User dá exemplos")
            print("  - Temperature: System garante consistência, temp controla variação")
            print("  - Pipeline: Cada etapa = System especializado")
            print("\nBest Practice: SEMPRE separe System e User prompts!")
            print("=" * 60)
            break

        if escolha == "0":
            # Executa todos os desafios em sequência
            for key, (_, func) in desafios.items():
                if func is not None:
                    func()
                    input("\n[Pressione ENTER para continuar...]")
        elif escolha in desafios:
            _, func = desafios[escolha]
            if func:
                func()
        else:
            print("\nOpção inválida! Tente novamente.")


# =============================================================================
# EXECUÇÃO DIRETA (para rodar desafios sem menu)
# =============================================================================
# Descomente a função que deseja executar:

if __name__ == "__main__":

    # OPÇÃO 1: Menu interativo (recomendado para aula)
    menu_desafios()

    # OPÇÃO 2: Executar desafios específicos diretamente
    # desafio_01_arquiteto_personas()
    # desafio_02_few_shot_classificacao()
    # desafio_03_laboratorio_temperature()
    # desafio_04_prompt_frankenstein()
    # desafio_04_pipeline_correto()
