"""
=============================================================================
AULA: PROMPT ENGINEERING - DEMONSTRAÇÕES PRÁTICAS
=============================================================================

Objetivos didáticos:
1. Prompt é especificação
2. Estrutura importa mais que eloquência
3. Encadeamento (pipeline) melhora qualidade
4. Parâmetros e contexto alteram comportamento do modelo

"Estamos programando a comunicação com o LLM"
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


def call_llm(
    prompt: str,
    system_prompt: str = None,
    temperature: float = 0
) -> str:
    """
    Função base para chamar o LLM.

    Args:
        prompt: O texto do prompt do usuário (user message)
        system_prompt: Instruções de sistema que definem o comportamento do modelo
                      (role, restrições, formato). BEST PRACTICE: sempre usar!
        temperature: Controla a criatividade (0 = determinístico, 1 = criativo)

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
# MÓDULO 2: PROMPT VAGO VS PROMPT ESTRUTURADO
# =============================================================================
# Demonstra a diferença entre um prompt sem especificação e um prompt
# que funciona como "contrato de execução"
# -----------------------------------------------------------------------------

def demo_01_prompt_vago():
    """
    DEMONSTRAÇÃO 1: Prompt Vago

    Problema: Não definimos quem a IA é, para quem escreve, nem o formato.
    Estamos deixando tudo aberto para interpretação.
    """
    print("\n" + "=" * 60)
    print("DEMO 1: PROMPT VAGO (SEM SYSTEM PROMPT)")
    print("=" * 60)

    # Sem system prompt - modelo não sabe qual papel assumir
    prompt_vago = "Resuma este artigo sobre redes neurais em diagnósticos médicos."

    print("\n[System Prompt]: Nenhum")
    print(f"[User Prompt]: {prompt_vago}\n")
    print("-" * 40)
    print("Resposta:")
    print(call_llm(prompt_vago))


def demo_02_prompt_estruturado():
    """
    DEMONSTRAÇÃO 2: Prompt Estruturado com System Prompt (Best Practice)

    Componentes separados:
    - SYSTEM: Persona, Tom, Restrições (comportamento persistente)
    - USER: Contexto, Tarefa, Formato (específico da requisição)
    """
    print("\n" + "=" * 60)
    print("DEMO 2: PROMPT ESTRUTURADO (COM SYSTEM PROMPT)")
    print("=" * 60)

    # System prompt define O QUE o modelo É
    system_prompt = """Você é um revisor acadêmico experiente especializado em tecnologia médica.

Suas características:
- Comunicação clara e acessível para estudantes de graduação
- Evita jargões técnicos excessivos
- Foco em precisão e clareza

Formato de resposta:
- Sempre responda de forma estruturada
- Use no máximo 100 palavras"""

    # User prompt define O QUE FAZER agora
    user_prompt = """Contexto:
O artigo aborda o uso de redes neurais em diagnósticos médicos.

Tarefa:
Crie um resumo executivo destacando os pontos principais."""

    print(f"\n[System Prompt]:\n{system_prompt}\n")
    print(f"[User Prompt]:\n{user_prompt}")
    print("-" * 40)
    print("Resposta:")
    print(call_llm(user_prompt, system_prompt=system_prompt))

    print("\n" + "-" * 40)
    print("Best Practice:")
    print("'System prompt define QUEM. User prompt define O QUÊ.'")


# =============================================================================
# MÓDULO 3: PIPELINE / ENCADEAMENTO DE PROMPTS
# =============================================================================
# Demonstra por que dividir tarefas complexas em etapas é melhor
# do que pedir tudo de uma vez
# -----------------------------------------------------------------------------

def demo_03_prompt_frankenstein():
    """
    DEMONSTRAÇÃO 3: Prompt Frankenstein (Anti-padrão)

    Problema: Pedir tudo de uma vez. O modelo tenta fazer tudo...
    e não faz nada excepcionalmente bem.
    """
    print("\n" + "=" * 60)
    print("DEMO 3: PROMPT FRANKENSTEIN (ANTI-PADRÃO)")
    print("=" * 60)

    # Mesmo com system prompt, pedir muitas tarefas juntas é problemático
    system_prompt = "Você é um assistente de escrita profissional."

    prompt_frankenstein = """Revise o texto abaixo, corrija erros gramaticais,
resuma em 3 tópicos, sugira melhorias de estilo e gere um título criativo.

Texto: A inteligência artificial tem mudado o mundo de forma rapida."""

    print(f"\n[System Prompt]: {system_prompt}")
    print(f"[User Prompt]:\n{prompt_frankenstein}")
    print("-" * 40)
    print("Resposta:")
    print(call_llm(prompt_frankenstein, system_prompt=system_prompt))

    print("\n" + "-" * 40)
    print("Problema: 'Múltiplas tarefas = resultados inconsistentes'")


def demo_04_pipeline_correto():
    """
    DEMONSTRAÇÃO 4: Pipeline Correto (Prompts Encadeados)

    Técnica: Cada prompt faz uma coisa só - e faz bem.
    System prompt especializado para cada etapa.
    """
    print("\n" + "=" * 60)
    print("DEMO 4: PIPELINE CORRETO (ENCADEAMENTO)")
    print("=" * 60)

    texto_original = "A inteligência artificial tem mudado o mundo de forma rapida."

    print(f"\nTexto original: {texto_original}")

    # ----- PASSO 1: Revisão gramatical -----
    print("\n" + "-" * 40)
    print("PASSO 1: Revisão Gramatical")
    print("-" * 40)

    # System prompt especializado para revisão
    system_revisor = """Você é um revisor gramatical especializado em português brasileiro.

Regras:
- Corrija APENAS erros gramaticais e ortográficos
- Não altere o estilo ou tom do texto
- Retorne apenas o texto corrigido, sem explicações"""

    user_revisao = f"Revise o texto: {texto_original}"

    print(f"[System]: Revisor gramatical especializado")
    texto_revisado = call_llm(user_revisao, system_prompt=system_revisor)
    print(f"Resultado: {texto_revisado}")

    # ----- PASSO 2: Resumo estruturado -----
    print("\n" + "-" * 40)
    print("PASSO 2: Resumo Estruturado")
    print("-" * 40)

    # System prompt especializado para resumo
    system_resumidor = """Você é um especialista em síntese de conteúdo.

Regras:
- Extraia os pontos principais em formato de lista
- Seja conciso e objetivo
- Use no máximo 3 tópicos"""

    user_resumo = f"Resuma em tópicos: {texto_revisado}"

    print(f"[System]: Especialista em síntese")
    resumo = call_llm(user_resumo, system_prompt=system_resumidor)
    print(f"Resultado:\n{resumo}")

    print("\n" + "-" * 40)
    print("Best Practice: 'System prompt especializado por etapa'")


# =============================================================================
# MÓDULO 3: FEW-SHOT LEARNING (Aprendizado por Padrão)
# =============================================================================
# Demonstra como exemplos melhoram a consistência da saída
# "Não expliquei a regra. Mostrei exemplos. O modelo aprende pelo padrão."
# -----------------------------------------------------------------------------

def demo_05_few_shot():
    """
    DEMONSTRAÇÃO 5: Classificação de Sentimento com Few-Shot

    Técnica: System prompt define o papel + User prompt com exemplos
    """
    print("\n" + "=" * 60)
    print("DEMO 5: FEW-SHOT LEARNING")
    print("=" * 60)

    # System prompt define o classificador
    system_prompt = """Você é um classificador de sentimentos especializado em feedback de usuários.

Regras:
- Classifique como: Positivo, Negativo ou Neutro
- Responda APENAS com a classificação, nada mais
- Seja consistente com os exemplos fornecidos"""

    # User prompt contém os exemplos (few-shot) e a tarefa
    user_prompt = """Exemplos:
Texto: "O produto é excelente e superou minhas expectativas."
Sentimento: Positivo

Texto: "O atendimento foi péssimo e demorou muito."
Sentimento: Negativo

Texto: "Poderia ter mais opções."
Sentimento: Neutro

Agora classifique:
Texto: "O serviço foi aceitável, nada extraordinário."
Sentimento:"""

    print(f"\n[System Prompt]:\n{system_prompt}\n")
    print(f"[User Prompt com Few-Shot]:\n{user_prompt}")
    print("-" * 40)
    print("Resposta:")
    print(call_llm(user_prompt, system_prompt=system_prompt))

    print("\n" + "-" * 40)
    print("Best Practice: 'System define o papel, User fornece exemplos'")


# =============================================================================
# MÓDULO 3: CHAIN-OF-THOUGHT (Raciocínio Explícito)
# =============================================================================
# Demonstra como forçar o modelo a "pensar passo a passo"
# "Não tornei a IA mais inteligente. Tornei o raciocínio explícito."
# -----------------------------------------------------------------------------

def demo_06_sem_chain_of_thought():
    """
    DEMONSTRAÇÃO 6: Sem Chain-of-Thought

    Problema: Resposta direta pode conter erros em problemas complexos.
    """
    print("\n" + "=" * 60)
    print("DEMO 6: SEM CHAIN-OF-THOUGHT")
    print("=" * 60)

    system_prompt = "Você é uma calculadora matemática. Responda de forma direta."

    user_prompt = "Quanto é 17 * 24 + 38?"

    print(f"\n[System Prompt]: {system_prompt}")
    print(f"[User Prompt]: {user_prompt}\n")
    print("-" * 40)
    print("Resposta:")
    print(call_llm(user_prompt, system_prompt=system_prompt))


def demo_07_com_chain_of_thought():
    """
    DEMONSTRAÇÃO 7: Com Chain-of-Thought

    Técnica: System prompt instrui a pensar passo a passo
    """
    print("\n" + "=" * 60)
    print("DEMO 7: COM CHAIN-OF-THOUGHT")
    print("=" * 60)

    # System prompt instrui o raciocínio passo a passo
    system_prompt = """Você é um tutor de matemática paciente e didático.

Método de resolução:
1. Identifique as operações necessárias
2. Resolva uma operação por vez, mostrando cada cálculo
3. Apresente o resultado final claramente

Sempre mostre seu raciocínio antes da resposta."""

    user_prompt = "Quanto é 17 * 24 + 38?"

    print(f"\n[System Prompt]:\n{system_prompt}\n")
    print(f"[User Prompt]: {user_prompt}")
    print("-" * 40)
    print("Resposta:")
    print(call_llm(user_prompt, system_prompt=system_prompt))

    print("\n" + "-" * 40)
    print("Best Practice: 'System prompt pode instruir o MÉTODO de raciocínio'")


# =============================================================================
# MÓDULO 4: TEMPERATURE (Criatividade vs Precisão)
# =============================================================================
# Demonstra como o parâmetro temperature afeta a criatividade/determinismo
# "Mesma pergunta, mesmo modelo. Só mudei o grau de aleatoriedade."
# -----------------------------------------------------------------------------

def demo_08_temperature_baixa():
    """
    DEMONSTRAÇÃO 8: Temperature Baixa (Código / Fato)

    temperature=0: Determinístico, previsível, consistente
    Use para: código, análises, dados estruturados, fatos
    """
    print("\n" + "=" * 60)
    print("DEMO 8: TEMPERATURE BAIXA (0) - PRECISÃO")
    print("=" * 60)

    system_prompt = """Você é um instrutor de programação Python experiente.

Estilo de resposta:
- Explicações claras e técnicas
- Exemplos práticos quando apropriado
- Linguagem profissional"""

    user_prompt = "Explique o que é uma função em Python."

    print(f"\n[System Prompt]: Instrutor de Python")
    print(f"[User Prompt]: {user_prompt}")
    print(f"[Temperature]: 0\n")
    print("-" * 40)
    print("Resposta:")
    print(call_llm(user_prompt, system_prompt=system_prompt, temperature=0))


def demo_09_temperature_alta():
    """
    DEMONSTRAÇÃO 9: Temperature Alta (Criatividade)

    temperature=0.9: Criativo, variado, menos previsível
    Use para: brainstorm, criatividade, marketing, nomes
    """
    print("\n" + "=" * 60)
    print("DEMO 9: TEMPERATURE ALTA (0.9) - CRIATIVIDADE")
    print("=" * 60)

    system_prompt = """Você é um diretor criativo de uma agência de branding inovadora.

Estilo:
- Pense fora da caixa
- Seja ousado e memorável
- Considere impacto emocional"""

    user_prompt = "Crie um nome criativo para uma startup de IA educacional."

    print(f"\n[System Prompt]: Diretor criativo de branding")
    print(f"[User Prompt]: {user_prompt}")
    print(f"[Temperature]: 0.9\n")
    print("-" * 40)
    print("Resposta:")
    print(call_llm(user_prompt, system_prompt=system_prompt, temperature=0.9))

    print("\n" + "-" * 40)
    print("Best Practice: 'System prompt + temperature = controle fino'")


# =============================================================================
# MÓDULO 5: MULTI-AGENTES (LLM avaliando LLM)
# =============================================================================
# Demonstra como usar um segundo LLM para validar/auditar respostas
# "Aqui a IA não é autora. Ela é parte do sistema de controle."
# -----------------------------------------------------------------------------

def demo_10_multi_agentes():
    """
    DEMONSTRAÇÃO 10: Auditor de Respostas (Multi-Agentes)

    Técnica: Agentes com system prompts diferentes
    - Agente 1: Gerador (system prompt de redator)
    - Agente 2: Auditor (system prompt de QA)
    """
    print("\n" + "=" * 60)
    print("DEMO 10: MULTI-AGENTES (LLM AUDITANDO LLM)")
    print("=" * 60)

    # ----- AGENTE 1: Gerador -----
    print("\n" + "-" * 40)
    print("AGENTE 1: Gerador de Conteúdo")
    print("-" * 40)

    system_gerador = """Você é um redator corporativo especializado em comunicação B2B.

Estilo:
- Tom formal e profissional
- Foco em benefícios para o cliente
- Estrutura clara com saudação, corpo e CTA"""

    user_gerador = "Escreva um e-mail de vendas oferecendo um software de CRM corporativo."

    print(f"[System]: Redator corporativo B2B")
    resposta_ia = call_llm(user_gerador, system_prompt=system_gerador)
    print(f"E-mail gerado:\n{resposta_ia}")

    # ----- AGENTE 2: Auditor -----
    print("\n" + "-" * 40)
    print("AGENTE 2: Auditor de Qualidade")
    print("-" * 40)

    system_auditor = """Você é um auditor de qualidade de comunicação corporativa.

Critérios de avaliação:
- Tom formal mantido (sem gírias ou informalidades)
- Linguagem apropriada para ambiente empresarial
- Estrutura profissional (saudação, corpo, fechamento)
- Clareza na proposta de valor

Formato de resposta:
- Liste cada critério com APROVADO ou REPROVADO
- Justifique brevemente cada avaliação
- Dê uma nota final de 1 a 10"""

    user_auditor = f"Avalie o seguinte e-mail corporativo:\n\n{resposta_ia}"

    print(f"[System]: Auditor de qualidade corporativa")
    print("Avaliação do auditor:")
    print(call_llm(user_auditor, system_prompt=system_auditor))

    print("\n" + "-" * 40)
    print("Best Practice: 'Cada agente tem seu próprio system prompt'")


# =============================================================================
# DEMO BÔNUS: COMPARAÇÃO SYSTEM PROMPT
# =============================================================================

def demo_bonus_comparacao_system():
    """
    DEMONSTRAÇÃO BÔNUS: Mesmo prompt, system prompts diferentes

    Mostra como o system prompt muda completamente o comportamento.
    """
    print("\n" + "=" * 60)
    print("DEMO BÔNUS: COMPARAÇÃO DE SYSTEM PROMPTS")
    print("=" * 60)

    user_prompt = "O que você acha de investir em criptomoedas?"

    # Versão 1: Consultor conservador
    print("\n" + "-" * 40)
    print("VERSÃO 1: Consultor Conservador")
    print("-" * 40)

    system_conservador = """Você é um consultor financeiro conservador com 30 anos de experiência.

Princípios:
- Priorize sempre a segurança do capital
- Seja cético com investimentos voláteis
- Recomende diversificação e renda fixa
- Responda de forma breve e direta"""

    print(f"[System]: Consultor conservador")
    print(call_llm(user_prompt, system_prompt=system_conservador))

    # Versão 2: Entusiasta de cripto
    print("\n" + "-" * 40)
    print("VERSÃO 2: Entusiasta de Tecnologia")
    print("-" * 40)

    system_entusiasta = """Você é um analista de tecnologias emergentes e finanças descentralizadas.

Princípios:
- Foque no potencial de inovação
- Considere o longo prazo e adoção tecnológica
- Mencione riscos, mas destaque oportunidades
- Responda de forma breve e direta"""

    print(f"[System]: Entusiasta de tecnologia")
    print(call_llm(user_prompt, system_prompt=system_entusiasta))

    print("\n" + "-" * 40)
    print("Conclusão: 'Mesmo prompt, comportamentos completamente diferentes'")


# =============================================================================
# MENU PRINCIPAL - EXECUÇÃO DAS DEMOS
# =============================================================================

def menu_principal():
    """
    Menu interativo para executar as demonstrações individualmente.
    """
    demos = {
        "1": ("Prompt Vago (sem system)", demo_01_prompt_vago),
        "2": ("Prompt Estruturado (com system)", demo_02_prompt_estruturado),
        "3": ("Prompt Frankenstein (Anti-padrão)", demo_03_prompt_frankenstein),
        "4": ("Pipeline Correto (Encadeamento)", demo_04_pipeline_correto),
        "5": ("Few-Shot Learning", demo_05_few_shot),
        "6": ("Sem Chain-of-Thought", demo_06_sem_chain_of_thought),
        "7": ("Com Chain-of-Thought", demo_07_com_chain_of_thought),
        "8": ("Temperature Baixa (Precisão)", demo_08_temperature_baixa),
        "9": ("Temperature Alta (Criatividade)", demo_09_temperature_alta),
        "10": ("Multi-Agentes (Auditor)", demo_10_multi_agentes),
        "11": ("BÔNUS: Comparação System Prompts", demo_bonus_comparacao_system),
        "0": ("Executar TODAS as demos", None),
    }

    while True:
        print("\n" + "=" * 60)
        print("   PROMPT ENGINEERING - DEMONSTRAÇÕES PRÁTICAS")
        print("   (Todas as demos usam System Prompt como best practice)")
        print("=" * 60)
        print("\nEscolha uma demonstração:\n")

        for key, (name, _) in demos.items():
            print(f"  [{key:>2}] {name}")

        print("\n  [q] Sair")
        print("=" * 60)

        escolha = input("\nDigite sua escolha: ").strip().lower()

        if escolha == "q":
            print("\n" + "=" * 60)
            print("Conclusão Pedagógica:")
            print("-" * 60)
            print('"O que vocês viram hoje não foi magia.')
            print(' Foi engenharia de especificação aplicada à linguagem.')
            print(' Prompt Engineering é programação — só que em linguagem natural."')
            print("\nBest Practice: SEMPRE use System Prompt para definir comportamento!")
            print("=" * 60)
            break

        if escolha == "0":
            # Executa todas as demos em sequência
            for key, (_, func) in demos.items():
                if func is not None:
                    func()
                    input("\n[Pressione ENTER para continuar...]")
        elif escolha in demos:
            _, func = demos[escolha]
            if func:
                func()
        else:
            print("\nOpção inválida! Tente novamente.")


# =============================================================================
# EXECUÇÃO DIRETA (para rodar demos sem menu)
# =============================================================================
# Descomente a função que deseja executar:

if __name__ == "__main__":

    # OPÇÃO 1: Menu interativo (recomendado para aula)
    menu_principal()

    # OPÇÃO 2: Executar demos específicas diretamente
    # demo_01_prompt_vago()
    # demo_02_prompt_estruturado()
    # demo_03_prompt_frankenstein()
    # demo_04_pipeline_correto()
    # demo_05_few_shot()
    # demo_06_sem_chain_of_thought()
    # demo_07_com_chain_of_thought()
    # demo_08_temperature_baixa()
    # demo_09_temperature_alta()
    # demo_10_multi_agentes()
    # demo_bonus_comparacao_system()
