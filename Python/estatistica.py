import math
from collections import Counter

class AnaliseEstatistica:
    def __init__(self, vetor_x, vetor_y=None):
        self.vetor_x = vetor_x
        self.vetor_y = vetor_y
        self.n = len(vetor_x)
        self.soma_x = self.soma_x2 = self.soma_xy = 0
        self.soma_y = self.soma_y2 = 0

    def calcular_moda(self, vetor):
        contagem = Counter(vetor)
        max_freq = max(contagem.values())
        if max_freq == 1:
            return None
        modas = [num for num, freq in contagem.items() if freq == max_freq]
        return modas
    
    def calcular_estatisticas_x(self):
        min_x = min(self.vetor_x)
        max_x = max(self.vetor_x)
        amplitude_x = max_x - min_x
        media_x = sum(self.vetor_x) / self.n
        vetor_sorted_x = sorted(self.vetor_x)
        if self.n % 2 == 0:
            mediana_x = (vetor_sorted_x[self.n//2 - 1] + vetor_sorted_x[self.n//2]) / 2
        else:
            mediana_x = vetor_sorted_x[self.n//2]
        modas_x = self.calcular_moda(self.vetor_x)
        
        for x in self.vetor_x:
            self.soma_x += x
            self.soma_x2 += x * x
        
        variancia_x = (self.soma_x2 - (self.soma_x ** 2) / self.n) / (self.n - 1)
        if variancia_x < 0:
            variancia_x = 0
        
        desvio_padrao_x = math.sqrt(variancia_x)
        
        return {
            'min': min_x,
            'max': max_x,
            'amplitude': amplitude_x,
            'media': media_x,
            'mediana': mediana_x,
            'modas': modas_x,
            'variancia': variancia_x,
            'desvio_padrao': desvio_padrao_x
        }
    
    def calcular_estatisticas_y(self):
        if self.vetor_y is None:
            return None
        min_y = min(self.vetor_y)
        max_y = max(self.vetor_y)
        amplitude_y = max_y - min_y
        media_y = sum(self.vetor_y) / self.n
        vetor_sorted_y = sorted(self.vetor_y)
        if self.n % 2 == 0:
            mediana_y = (vetor_sorted_y[self.n//2 - 1] + vetor_sorted_y[self.n//2]) / 2
        else:
            mediana_y = vetor_sorted_y[self.n//2]
        modas_y = self.calcular_moda(self.vetor_y)
        
        for i, y in enumerate(self.vetor_y):
            self.soma_y += y
            self.soma_y2 += y * y
            self.soma_xy += self.vetor_x[i] * y
        
        if self.n > 1:
            variancia_y = (self.soma_y2 - (self.soma_y ** 2) / self.n) / (self.n - 1)
        else:
            variancia_y = 0
        
        if variancia_y < 0:
            variancia_y = 0
        
        desvio_padrao_y = math.sqrt(variancia_y)
        
        return {
            'min': min_y,
            'max': max_y,
            'amplitude': amplitude_y,
            'media': media_y,
            'mediana': mediana_y,
            'modas': modas_y,
            'variancia': variancia_y,
            'desvio_padrao': desvio_padrao_y
        }
    
    def calcular_correlacao(self):
        if self.vetor_y is None:
            return None
        soma_produtos = self.soma_xy - (self.soma_x * self.soma_y) / self.n
        soma_quadrados_x = self.soma_x2 - (self.soma_x ** 2) / self.n
        soma_quadrados_y = self.soma_y2 - (self.soma_y ** 2) / self.n
        
        if soma_quadrados_x == 0 or soma_quadrados_y == 0:
            return None
        
        correlacao = soma_produtos / math.sqrt(soma_quadrados_x * soma_quadrados_y)
        return correlacao
    
    def calcular_regressao(self):
        if self.vetor_y is None:
            return None, None
        estatisticas_x = self.calcular_estatisticas_x()
        estatisticas_y = self.calcular_estatisticas_y()
        
        if estatisticas_x['variancia'] == 0 or estatisticas_y['variancia'] == 0:
            return None, None  # Não é possível calcular a regressão se a variância for 0
        
        a = self.soma_xy / self.soma_x2
        b = estatisticas_y['media'] - a * estatisticas_x['media']
        
        return a, b

    def calcular_coe_determinacao(self):
        # O coeficiente de determinação R² é o quadrado da correlação
        correlacao = self.calcular_correlacao()
        if correlacao is None:
            return None
        return correlacao ** 2

    def exibir_resultados(self):
        estatisticas_x = self.calcular_estatisticas_x()
        print(f"Estatísticas de X:")
        for chave, valor in estatisticas_x.items():
            print(f"{chave.capitalize()}: {valor:.2f}" if isinstance(valor, (int, float)) else f"{chave.capitalize()}: {valor}")
        print("-" * 60)

        if self.vetor_y is not None:
            estatisticas_y = self.calcular_estatisticas_y()
            print(f"Estatísticas de Y:")
            for chave, valor in estatisticas_y.items():
                print(f"{chave.capitalize()}: {valor:.2f}" if isinstance(valor, (int, float)) else f"{chave.capitalize()}: {valor}")
            print("-" * 60)

            correlacao = self.calcular_correlacao()
            if correlacao is not None:
                print(f"Correlação entre X e Y: {correlacao:.2f}")
            
            a, b = self.calcular_regressao()
            if a is not None and b is not None:
                print(f"Equação da regressão linear (y = ax + b): y = {a:.2f}x + {b:.2f}")
            
            r2 = self.calcular_coe_determinacao()
            if r2 is not None:
                print(f"Coeficiente de determinação (R²): {r2:.2f}")
            print("-" * 60)

# Função principal para testar o código
def main():
    n = int(input("Quantos números na sua série (N): "))
    
    # Entrada dos números para X
    vetor_x = []
    print("Entre com os números (X):")
    for i in range(n):
        vetor_x.append(float(input("> ")))

    # Perguntar se o usuário deseja fornecer Y
    deseja_y = input("Deseja fornecer os números para Y? (Digite 's' para sim ou 'n' para não): ").strip().lower()

    # Solicitar os números da segunda variável Y, caso tenha optado por isso
    if deseja_y == 's':
        vetor_y = []
        print("Entre com os números (Y) para análise de correlação e regressão:")
        for i in range(n):
            vetor_y.append(float(input("> ")))
    else:
        vetor_y = None

    # Criando o objeto da classe
    analise = AnaliseEstatistica(vetor_x, vetor_y)
    
    # Exibe os resultados
    analise.exibir_resultados()

if __name__ == "__main__":
    main()
