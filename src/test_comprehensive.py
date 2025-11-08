from primality_tests import fermat_test, solovay_strassen_test, miller_rabin_test

def comprehensive_test():
    """Запуск комплексных тестов на известных простых и составных числах"""
    known_primes = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    known_composites = [9, 15, 21, 25, 27, 33, 35, 39, 45, 49, 51, 55, 57, 63, 65, 69, 75, 77, 81, 85, 87, 91, 93, 95, 99]
    carmichael_numbers = [561, 1105, 1729, 2465, 2821, 6601, 8911, 10585, 15841, 29341, 41041, 46657, 52633, 62745, 63973, 75361]
    
    print("КОМПЛЕКСНОЕ ТЕСТИРОВАНИЕ ПРОВЕРКИ ПРОСТОТЫ")
    print("=" * 80)
    
    # Тестируем известные простые числа
    print("\n1. ИЗВЕСТНЫЕ ПРОСТЫЕ ЧИСЛА (должны быть идентифицированы как 'Вероятно простые'):")
    correct_primes = 0
    for prime in known_primes:
        result = miller_rabin_test(prime, 20)
        if "Вероятно" in result:
            correct_primes += 1
        print(f"{prime}: {result}")
    print(f"Корректно идентифицировано {correct_primes}/{len(known_primes)} простых чисел")
    
    # Тестируем известные составные числа
    print("\n2. ИЗВЕСТНЫЕ СОСТАВНЫЕ ЧИСЛА (должны быть идентифицированы как 'Составные'):")
    correct_composites = 0
    for composite in known_composites:
        result = miller_rabin_test(composite, 20)
        if "Составное" in result:
            correct_composites += 1
        print(f"{composite}: {result}")
    print(f"Корректно идентифицировано {correct_composites}/{len(known_composites)} составных чисел")
    
    # Тестируем числа Кармайкла (сложные составные числа)
    print("\n3. ЧИСЛА КАРМАЙКЛА (составные числа, которые обманывают некоторые тесты):")
    for carmichael in carmichael_numbers:
        fermat = fermat_test(carmichael, 10)
        solovay = solovay_strassen_test(carmichael, 10)
        miller = miller_rabin_test(carmichael, 10)
        print(f"{carmichael}: Фермат={fermat[:12]}, Соловэй={solovay[:12]}, Миллер={miller[:12]}")

def error_probability_analysis():
    """Анализ вероятности ошибки при различном количестве итераций"""
    test_number = 561  # Число Кармайкла
    
    print(f"\nАНАЛИЗ ВЕРОЯТНОСТИ ОШИБКИ ДЛЯ {test_number} (число Кармайкла):")
    print("Итераций\tФермат\t\tСоловэй-Штрассен\tМиллер-Рабин")
    print("-" * 70)
    
    for iterations in [1, 5, 10, 20, 50]:
        fermat_wrong = 0
        solovay_wrong = 0
        miller_wrong = 0
        trials = 100
        
        for _ in range(trials):
            if "Вероятно" in fermat_test(test_number, iterations):
                fermat_wrong += 1
            if "Вероятно" in solovay_strassen_test(test_number, iterations):
                solovay_wrong += 1
            if "Вероятно" in miller_rabin_test(test_number, iterations):
                miller_wrong += 1
        
        fermat_error = fermat_wrong / trials
        solovay_error = solovay_wrong / trials
        miller_error = miller_wrong / trials
        
        print(f"{iterations}\t\t{fermat_error:.3f}\t\t{solovay_error:.3f}\t\t\t{miller_error:.3f}")

if __name__ == "__main__":
    comprehensive_test()
    error_probability_analysis()