import random
import math

def gcd(a, b):
    """Вычисление наибольшего общего делителя"""
    while b:
        a, b = b, a % b
    return a

def mod_pow(base, exponent, modulus):
    """Модульное возведение в степень"""
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result

def fermat_test(n, k=5):
    """
    Тест Ферма на простоту
    Вход: n >= 5 (нечетное целое), k = количество итераций
    Выход: "Вероятно простое" или "Составное"
    """
    if n < 5:
        return "Число должно быть >= 5"
    if n % 2 == 0:
        return "Составное"
    
    for _ in range(k):
        a = random.randint(2, n - 2)
        if gcd(a, n) != 1:
            return "Составное"
        r = mod_pow(a, n - 1, n)
        if r != 1:
            return "Составное"
    
    return "Вероятно простое"

def jacobi_symbol(a, n):
    """
    Вычисление символа Якоби (a/n)
    Вход: n >= 3 (нечетное целое), 0 <= a < n
    Выход: Значение символа Якоби
    """
    if n % 2 == 0 or n < 3:
        raise ValueError("n должно быть нечетным и >= 3")
    
    a = a % n
    if a == 0:
        return 0
    if a == 1:
        return 1
    
    # Выделяем степени 2
    s = 1
    while a % 2 == 0:
        a //= 2
        if n % 8 in [3, 5]:
            s = -s
    
    if a == 1:
        return s
    
    # Применяем квадратичный закон взаимности
    if a % 4 == 3 and n % 4 == 3:
        s = -s
    
    return s * jacobi_symbol(n % a, a)

def solovay_strassen_test(n, k=5):
    """
    Тест Соловэя-Штрассена на простоту
    Вход: n >= 5 (нечетное целое), k = количество итераций
    Выход: "Вероятно простое" или "Составное"
    """
    if n < 5:
        return "Число должно быть >= 5"
    if n % 2 == 0:
        return "Составное"
    
    for _ in range(k):
        a = random.randint(2, n - 2)
        
        # Вычисляем r = a^((n-1)/2) mod n
        r = mod_pow(a, (n - 1) // 2, n)
        
        if r != 1 and r != n - 1:
            return "Составное"
        
        # Вычисляем символ Якоби
        jacobi = jacobi_symbol(a, n)
        if jacobi == -1:
            jacobi = n - 1
        
        if r != jacobi % n:
            return "Составное"
    
    return "Вероятно простое"

def miller_rabin_test(n, k=5):
    """
    Тест Миллера-Рабина на простоту
    Вход: n >= 5 (нечетное целое), k = количество итераций
    Выход: "Вероятно простое" или "Составное"
    """
    if n < 5:
        return "Число должно быть >= 5"
    if n % 2 == 0:
        return "Составное"
    
    # Представляем n-1 в виде 2^s * r
    s = 0
    r = n - 1
    while r % 2 == 0:
        r //= 2
        s += 1
    
    for _ in range(k):
        a = random.randint(2, n - 2)
        y = mod_pow(a, r, n)
        
        if y != 1 and y != n - 1:
            j = 1
            while j <= s - 1 and y != n - 1:
                y = mod_pow(y, 2, n)
                if y == 1:
                    return "Составное"
                j += 1
            
            if y != n - 1:
                return "Составное"
    
    return "Вероятно простое"

def test_numbers():
    """Тестирование алгоритмов на различных числах"""
    test_cases = [
        5, 7, 11, 13, 17, 19, 23, 29,  # Известные простые
        9, 15, 21, 25, 27, 33, 35,     # Известные составные
        561, 1105, 1729, 2465,         # Числа Кармайкла
    ]
    
    print("Тестирование алгоритмов проверки простоты:")
    print("Число\t\tФермат\t\tСоловэй-Штрассен\tМиллер-Рабин")
    print("-" * 70)
    
    for n in test_cases:
        if n >= 5:
            fermat = fermat_test(n, 10)
            solovay = solovay_strassen_test(n, 10)
            miller = miller_rabin_test(n, 10)
            
            print(f"{n}\t\t{fermat[:12]}\t{solovay[:12]}\t\t{miller[:12]}")

if __name__ == "__main__":
    test_numbers()
    
    # Интерактивное тестирование
    print("\nИнтерактивное тестирование:")
    while True:
        try:
            user_input = input("\nВведите число для проверки (или 'выход' для завершения): ")
            if user_input.lower() in ['выход', 'exit', 'quit']:
                break
            
            n = int(user_input)
            if n < 5:
                print("Пожалуйста, введите число >= 5")
                continue
            
            print(f"\nРезультаты для {n}:")
            print(f"Тест Ферма: {fermat_test(n, 10)}")
            print(f"Тест Соловэя-Штрассена: {solovay_strassen_test(n, 10)}")
            print(f"Тест Миллера-Рабина: {miller_rabin_test(n, 10)}")
            
        except ValueError:
            print("Пожалуйста, введите целое число")
        except KeyboardInterrupt:
            break