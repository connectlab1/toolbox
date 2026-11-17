import random
print('Soma Básica')
for _ in range(2):
    linha = []
    for _ in range(10):
        a = random.randint(1, 99)
        b = random.randint(1, 99)
        linha.append(f'{a} + {b}')
    print('\t'.join(linha))
print()
print('Subtração Básica')
for _ in range(2):
    linha = []
    for _ in range(10):
        a = random.randint(10, 99)
        b = random.randint(1, a)
        linha.append(f'{a} - {b}')
    print('\t'.join(linha))
print()
print('Multiplicação Básica')
for _ in range(2):
    linha = []
    for _ in range(10):
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        linha.append(f'{a} × {b}')
    print('\t'.join(linha))
print()
print('Divisão Básica')
for _ in range(2):
    linha = []
    for _ in range(10):
        divisor = random.randint(2, 9)
        quociente = random.randint(1, 10)
        dividendo = divisor * quociente
        linha.append(f'{dividendo} ÷ {divisor}')
    print('\t'.join(linha))
