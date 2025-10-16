# humor_calculator.py
"""
Calculadora de Humor - versão básica com personalização.
Autor: Karen B. C. Campos
Data: 2025-10-15
"""

from time import sleep
import sys

# Tente importar colorama para cores no terminal; se não tiver, continua sem cores.
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    USE_COLORS = True
except Exception:
    USE_COLORS = False
    # define placeholders para não quebrar o código caso colorama não esteja instalado
    class Fore:
        GREEN = ""
        RED = ""
        YELLOW = ""
        CYAN = ""
        MAGENTA = ""
    class Style:
        RESET_ALL = ""

def colored(text, color_code):
    """Retorna texto com cor se colorama estiver disponível, senão retorna texto simples."""
    if USE_COLORS:
        return f"{color_code}{text}{Style.RESET_ALL}"
    return text

def saudacao():
    """Mostra mensagem inicial."""
    print(colored("=== Calculadora de Humor ===", Fore.CYAN))
    print("Eu faço cálculos e ainda tento combinar o resultado com o seu humor ✨\n")

def pedir_humor():
    """Pede ao usuário o humor e normaliza a entrada."""
    humor = input("Como você está se sentindo? (ex: feliz, cansada, estressada, animada): ").strip().lower()
    return humor

def pedir_operacao():
    """
    Pede uma operação simples no formato: número operador número
    Exemplo: 5 + 2
    Retorna (num1, operador, num2) ou levanta ValueError em caso de entrada inválida.
    """
    texto = input("Digite uma expressão simples (ex: 5 + 2 ou 3.5 * 2): ").strip()
    # tenta separar por espaços: formato esperado "num operador num"
    parts = texto.split()
    if len(parts) == 3:
        a_str, op, b_str = parts
    else:
        # tentar detectar sem espaços, por exemplo "5+2"
        # encontra primeiro operador comum
        for o in ["+", "-", "*", "/"]:
            if o in texto:
                a_str, b_str = texto.split(o, 1)
                op = o
                break
        else:
            raise ValueError("Formato inválido. Use algo como: 5 + 2")
    try:
        a = float(a_str.replace(",", "."))  # aceita vírgula como decimal
        b = float(b_str.replace(",", "."))
    except ValueError:
        raise ValueError("Números inválidos. Use 5, 3.14 ou 2,5 por exemplo.")
    if op not in ["+", "-", "*", "/"]:
        raise ValueError(f"Operador '{op}' não suportado. Use + - * /")
    return a, op, b

def calcular(a, op, b):
    """Executa a operação e trata divisão por zero."""
    if op == "+":
        return a + b
    elif op == "-":
        return a - b
    elif op == "*":
        return a * b
    elif op == "/":
        if b == 0:
            raise ZeroDivisionError("Divisão por zero não é permitida.")
        return a / b
    else:
        # segurança: não deve chegar aqui
        raise ValueError("Operação desconhecida.")

def mensagem_por_humor(humor, resultado):
    """Gera uma mensagem personalizada baseada no humor. Pode ser ampliada."""
    base = f"O resultado é {resultado}"
    if "feliz" in humor or "anim" in humor or "bem" in humor:
        return colored(base + " 😄 — Aproveite o bom humor para fazer algo produtivo hoje!!", Fore.GREEN)
    if "cans" in humor or "sono" in humor or "cansada" in humor:
        return colored(base + " 😴 — Você não é uma maquina. Descance um pouco, seu corpo e mente agradecem", Fore.MAGENTA)
    if "estress" in humor or "nerv" in humor or "ans" in humor:
        return colored(base + " 😬 — Respire fundo - inspire por 4 segundos, expire por 6.", Fore.YELLOW)
    if "triste" in humor or "mal" in humor or "deprim" in humor:
        return colored(base + " 💙 — Sinto muito. Um filme leve ou um abraço podem ajudar.", Fore.CYAN)
    # fallback neutro
    return colored(base + " 🙂", Fore.CYAN)

def salvar_historico(humor, expressao, resultado):
    """Opcional: salva histórico em um arquivo 'historico.txt' (append)."""
    try:
        with open("historico.txt", "a", encoding="utf-8") as f:
            f.write(f"{humor} | {expressao} | {resultado}\n")
    except Exception:
        # se falhar, não quebra a aplicação
        pass

def main():
    saudacao()
    while True:
        try:
            humor = pedir_humor()
            a, op, b = pedir_operacao()
            # mostra pequena animação de cálculo
            print(colored("Calculando", Fore.YELLOW), end="")
            for _ in range(3):
                print(".", end="", flush=True)
                sleep(0.4)
            print()  # pula linha
            resultado = calcular(a, op, b)
            # formata resultado para mostrar até 4 casas decimais quando for float
            if abs(resultado - int(resultado)) < 1e-10:
                resultado_str = str(int(resultado))
            else:
                resultado_str = f"{resultado:.4f}".rstrip("0").rstrip(".")
            mensagem = mensagem_por_humor(humor, resultado_str)
            print(mensagem)
            # salva histórico (opcional)
            salvar_historico(humor, f"{a} {op} {b}", resultado_str)
        except ZeroDivisionError as zde:
            print(colored(f"Erro: {zde}", Fore.RED))
        except ValueError as ve:
            print(colored(f"Entrada inválida: {ve}", Fore.RED))
        except KeyboardInterrupt:
            print("\n" + colored("Saindo... até mais!", Fore.CYAN))
            sys.exit(0)
        # pergunta se quer continuar
        cont = input("\nDeseja fazer outro cálculo? (s/n): ").strip().lower()
        if cont not in ["s", "sim", "y", "yes"]:
            print(colored("Obrigado por usar a Calculadora de Humor 😊", Fore.CYAN))
            break

if __name__ == "__main__":
    main()
