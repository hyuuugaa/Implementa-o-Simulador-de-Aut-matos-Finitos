
import json
import csv
import time
import sys

# Função para carregar o autômato de um arquivo JSON
def load_automaton(automaton_file):
    with open(automaton_file, 'r') as file:
        automaton = json.load(file)
    return automaton

# Função para carregar as palavras de teste de um arquivo CSV
def load_tests(test_file):
    tests = []
    with open(test_file, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Ignora o cabeçalho
        for row in reader:
            tests.append((row[0], int(row[1])))
    return tests

# Função que simula o autômato dado uma palavra de entrada
def simulate_automaton(automaton, word):
    current_state = automaton['initial_state']
    for symbol in word:
        if symbol in automaton['alphabet']:
            current_state = automaton['transitions'].get(current_state, {}).get(symbol)
            if current_state is None:
                return False  # Transição inválida, rejeitar a palavra
        else:
            return False  # Símbolo não está no alfabeto, rejeitar
    return current_state in automaton['accept_states']

# Função principal para executar a simulação
def run_simulation(automaton_file, test_file, output_file):
    automaton = load_automaton(automaton_file)
    tests = load_tests(test_file)
    
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['palavra de entrada', 'resultadoesperado', 'resultado_obtido', 'tempo'])
        
        for word, expected in tests:
            start_time = time.time()
            result = simulate_automaton(automaton, word)
            elapsed_time = time.time() - start_time
            result_obtained = 1 if result else 0
            writer.writerow([word, expected, result_obtained, f'{elapsed_time:.6f}'])

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: $ ferramenta arquivo_do_automato.aut arquivo_de_testes.in arquivo_de_saida.out")
        sys.exit(1)
    
    automaton_file = sys.argv[1]
    test_file = sys.argv[2]
    output_file = sys.argv[3]
    
    run_simulation(automaton_file, test_file, output_file)
