def parse_input(filename) -> [int, int, list, dict]:
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Читаем количество узлов и рёбер
    first_line = lines[0].strip().split()
    nv, ne = int(first_line[0]), int(first_line[1])

    # Считываем рёбра
    edges = []
    edge_start_line = 2  # Начало рёбер сразу после первой пустой строки
    for i in range(edge_start_line, edge_start_line + ne):
        if lines[i].strip():  # Игнорируем пустые строки
            u, v = map(int, lines[i].strip().split())
            edges.append((u, v))

    # Считываем правила агент-функции
    rules = {}
    rules_start_line = edge_start_line + ne + 1  # Начало правил сразу после пустой строки
    for i in range(rules_start_line, rules_start_line + nv + ne):
        if lines[i].strip():  # Игнорируем пустые строки
            rules[i - rules_start_line + 1] = lines[i].strip()

    return nv, ne, edges, rules


def compute_attributes(nv, ne, edges, rules) -> list:
    attributes = [None] * (nv + ne)  # Атрибуты узлов и рёбер

    while None in attributes:
        # Обработка правил для узлов
        for i in range(1, nv + 1):
            rule = rules[i]
            val, apply = apply_rule(rule, attributes, nv, ne)
            if apply:
                attributes[i - 1] = val

        # Обработка правил для рёбер
        for i in range(nv + 1, nv + ne + 1):
            rule = rules[i]
            val, apply = apply_rule(rule, attributes, nv, ne)
            if apply:
                attributes[i - 1] = val

    return attributes


def apply_rule(rule, attributes, nv, ne) -> [int, bool]:
    parts = rule.split()
    if len(parts) == 1:  # одно число
        return float(parts[0]), True
    elif len(parts) == 2:  # v x или e x
        element_type = parts[0]
        if element_type == 'e':
            for e in range(ne+1):
                if e == int(parts[1]) - 1:
                    index = e + nv
                    break
        else:
            index = int(parts[1]) - 1  # Приводим к нулевому индексу

        if attributes[index] == None:
            return attributes[index], False
        else:
            return attributes[index], True
    elif len(parts) == 5:  # min или * (функции)
        func = parts[0]
        element_type1 = parts[1]
        index1 = int(parts[2]) - 1
        element_type2 = parts[3]
        index2 = int(parts[4]) - 1
        if element_type1 == 'e':
            for e in range(ne + 1):
                if e == int(parts[2]) - 1:
                    index1 = e + nv
                    break
        else:
            index1 = int(parts[2]) - 1  # Приводим к нулевому индексу
        if element_type2 == 'e':
            for e in range(ne + 1):
                if e == int(parts[4]) - 1:
                    index2 = e + nv
                    break
        else:
            index2 = int(parts[4]) - 1  # Приводим к нулевому индексу
        if attributes[index1] == None or attributes[index2] is None:
            return 0, False
        if func == "min":
            return min(attributes[index1], attributes[index2]), True
        elif func == "*":
            return attributes[index1] * attributes[index2], True

    raise ValueError("Некорректное правило: " + rule)


def write_output(attributes, filename) -> None:
    with open(filename, 'w') as file:
        for attr in attributes:
            file.write(f"{attr}\n")


def main(input_file, output_file) -> None:
    nv, ne, edges, rules = parse_input(input_file)
    attributes = compute_attributes(nv, ne, edges, rules)
    write_output(attributes, output_file)


# Пример использования:
if __name__ == "__main__":
    input_file = "input.txt"  # Путь к входному файлу
    output_file = "output.txt"  # Путь к выходному файлу
    main(input_file, output_file)
