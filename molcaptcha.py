import re

mol_form = re.compile("([A-Z][a-z]?|[0-9]+)")


def parse_mol(mol_str):
    mol_list = mol_form.findall(mol_str)
    if len(mol_list) == 0 or mol_list[0].isdigit():
        return None

    elem_list = []
    for token in mol_list:
        if token.isdigit():
            elem_list[-1].append(token)
        else:
            elem_list.append([token])

    elem_map = {}
    for token in elem_list:
        if token[0] in elem_map:
            if len(token) >= 2:
                elem_map[token[0]] += int(token[1])
            else:
                elem_map[token[0]] += 1
        else:
            if len(token) >= 2:
                elem_map[token[0]] = int(token[1])
            else:
                elem_map[token[0]] = 1

    return elem_map


def mol_judge(user_input, answer_path):
    answer = ""
    with open(answer_path, "r") as answer_file:
        answer = answer_file.read()

    answer_map = parse_mol(answer)
    print("fact :", answer_map)
    user_map = parse_mol(user_input)
    print("users:", user_map)

    return answer_map == user_map


if __name__ == '__main__':

    print(parse_mol("C3NH23O2"))  # {'C': 3, 'N': 1, 'H': 23, 'O': 2}
    print(parse_mol("HOOCCOOH"))  # {'H': 2, 'O': 4, 'C': 2}

    print(mol_judge("C6O4N2H3Cl", "data/generated/answer/6"))  # True
