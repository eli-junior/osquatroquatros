"""
https://dojopuzzles.com/problems/o-poder-do-4/
O poder do “4”
Contribuição de: Marcelo Fonseca Tambalo

Este problema ainda não foi utilizado em nenhum Dojo.

No livro o “O Homem que Calculava” existe a teoria de que se é possível obter
qualquer número de 0 a 100, com quatro 'quatros' (4), apenas trocando seus
operadores. Exemplo: para se obter o 3 deve se fazer
CASO:

(4+4+4)/4 =3
4+(4-4)/4 = 4
((4*4)+4)/4 = 5
4+4-4/4 = 7
((4/4)+4)*4 = 20

Desenvolva uma função que retorne a fórmula para determinado número

Entrada: 80 Saida: (4+4*4)*4
"""
import contextlib
from itertools import product

import pytest

############################

DEBUG = False


def valid(response: str) -> bool:
    return response.count("4") == 4 and response.count("**") < 2


def generate_expressions(values: list[str]):
    valid_operations = ["+", "-", "*", "/", "**"]

    signals = product(valid_operations, repeat=(len(values) - 1))
    for s in signals:
        resp = "".join(f"{values[i]}{s[i]}" for i in range(len(values) - 1))
        resp += f"{values[-1]}".replace(" ", "").replace("()", "")

        # stackoverflow
        # if resp in ("4**4**4**4", "4**4**4*4"):
        #     continue
        yield resp
        if "/" in resp:
            yield f"({resp.replace('/', ')/', 1)}".replace("(4)", "4")

        if "*" in resp:
            yield f"({resp.replace('*', ')*', 1)}".replace("(4)", "4")
        if "4*4" in resp:
            yield f"{resp.replace('4*4', '(4*4)', 1)}"
        if "44*4" in resp:
            yield f"{resp.replace('44*4', '(44*4)', 1)}"
        if "4!*4" in resp:
            yield f"{resp.replace('4!*4', '(4!*4)', 1)}"
        if "4!/4" in resp:
            yield f"{resp.replace('4!/4', '(4!/4)', 1)}"
        if "4!*4!" in resp:
            yield f"{resp.replace('4!*4', '(4!*4)', 1)}"


def evaluate(exp: str, expected: int) -> bool:
    result = False
    with contextlib.suppress(TypeError, SyntaxError):
        if valid(exp):
            s = exp.replace("4!", "24")
            s = s.replace("4?", "10")
            s = s.replace("√4", "2")
            result = eval(s) == expected
    return result


def solution(input_) -> str:
    for case in (
        ["4", "4", "4", "4"],
        ["4!", "4", "4", "4"],
        ["4?", "4", "4", "4"],
        ["√4", "4", "4", "4"],
        ["√4", "4!", "4", "4"],
        ["√4", "4?", "4", "4"],
        ["4!", "4!", "√4", "4"],
        ["4!", "4!", "4", "4"],
        ["4?", "4?", "√4", "4"],
        ["4?", "4?", "4", "4"],
        ["4!", "4?", "4", "4"],
        ["4!", "4!", "4?", "4"],
        ["4!", "4!", "4?", "√4"],
        ["4!", "4?", "4?", "4"],
        ["4!", "4?", "4?", "√4"],
        ["4?", "4?", "4?", "4"],
        ["4?", "4?", "4?", "√4"],
        ["4?", "4?", "4?", "4?"],
        ["44", "4", "4"],
        ["44", "4!", "4"],
        ["44", "4!", "4!"],
        ["44", "4?", "4"],
        ["44", "4?", "4!"],
        ["44", "4?", "4?"],
    ):
        for exp in generate_expressions(case):
            if DEBUG:
                print(f"{exp} -> {input_} => ", end="")
            if evaluate(exp, input_) and valid(exp):
                if DEBUG:
                    print("Sim!")
                return exp
            if DEBUG:
                print("Não!")
    return "-1"


###########################
test_cases = [
    (("4+4-4-4",), 0),
    (("4*4/4/4", "4+4/4-4", "(4+4-4)/4"), 1),
    (("4/4+4/4",), 2),
    (("(4+4+4)/4",), 3),
    (("4+(4-4)/4", "(4-4)/4+4", "(4-4)*4+4"), 4),
    (("(4x4+4)/4", "(4+4*4)/4"), 5),
    (("4+(4+4)/4", "(4+4)/4+4"), 6),
    (("4+4-(4/4)", "4+4-4/4"), 7),
    (("4x(4+4)/4", "4+4+4-4"), 8),
    (("4+4+(4/4)", "4+4+4/4"), 9),
    (("(44-4)/4", "(4!+4*4)/4"), 10),
    (("(4!+4)/4+4",), 11),
    (("(4-4/4)*4",), 12),
    (
        (
            "(4!+4!+4)/4",
            "4?+4-4/4",
        ),
        13,
    ),
    (("4!/4+4+4",), 14),
    (("4*4-4/4",), 15),
    (("4+4+4+4",), 16),
    (("4*4+4/4",), 17),
    (("4!+4?-4*4", "(√4/4+4)*4", "√4+4!-4-4"), 18),
    (("4!-4-4/4",), 19),
    (("(4+4/4)*4",), 20),
    (("((4/4)-4)+(4!)", "4!+4/4-4"), 21),
    (("4!-(4+4)/4", "4!/4+4*4"), 22),
    (("(4!*4-4)/4",), 23),
    (("4+4+4*4",), 24),
    (("(4!*4+4)/4",), 25),
    (
        (
            "4!+4!/4-4",
            "(4?/4+4)*4",
        ),
        26,
    ),
    (("(4!)-((4/4)-4)", "4!+4-4/4"), 27),
    (("(4+4)*4-4",), 28),
    (("(4/4)+4+4!", "4!+4+4/4"), 29),
    (
        (
            "(4!+4!*4)/4",
            "4?+4+4*4",
        ),
        30,
    ),
    (("(4!+4?*4?)/4",), 31),
    (("4*4+4*4",), 32),
    (("4!+4?-4/4",), 33),
    (("4!+4!/4+4", "√4+4!+4+4"), 34),
    (
        (
            "4!+4?+4/4",
            "4?+4?**√4/4",
        ),
        35,
    ),
    (("(4+4)*4+4",), 36),
    (("44-4!/4", "√4+4?*4-4"), 38),
    (("4?*4-4/4",), 39),
    (("(4!/4+4)*4",), 40),
    (("4?*4+4/4",), 41),
    (("4!+4?+4+4", "√4+4!+4*4"), 42),
    (("44-4/4", "4!+4!-4?/√4"), 43),
    (("4!+4+4*4",), 44),
    (("44+4/4", "(4?*4?-4?)/√4"), 45),
    (("4?+4?*4-4" "√4+4?*4+4"), 46),
    (("4!+4!-4/4", "√4*4!-4/4"), 47),
    (("(4+4+4)*4",), 48),
    (("4!+4!+4/4", "√4*4!+4/4"), 49),
    (
        (
            "44+4!/4",
            "(4?+4?/4)*4",
            "4!+4!-√4+4",
        ),
        50,
    ),
    (
        (
            "44+4+4",
            "(4?+4)*4-4",
        ),
        52,
    ),
    (("4!+4!+4?/√4",), 53),
    (("4?+4?*4+4", "4!+4!+√4+4"), 54),
    (("(4?+4?*4?)/√4",), 55),
    (
        (
            "4!+4!+4+4",
            "4?*4+4*4",
        ),
        56,
    ),
    (("44+4?+4",), 58),
    (("(4!*4?-4)/4",), 59),
    (("4*4*4-4",), 60),
    (("(4!*4?+4)/4",), 61),
    (("4!+4!+4?+4",), 62),
    (("(4**4-4)/4",), 63),
    (("(4!-4-4)*4",), 64),
    (("(4+4**4)/4",), 65),
    (("(4!+4!*4?)/4", "√4+4*4*4"), 66),
    (("4+4*4*4",), 68),
    (("(4!+4**4)/4",), 70),
    (
        (
            "44+4!+4",
            "(4!-4!/4)*4",
            "(4?+4+4)*4",
        ),
        72,
    ),
    (("4?+4*4*4",), 74),
    (("(4!-4)*4-4",), 76),
    (("44+4?+4!",), 78),
    (("4!*4-4*4",), 80),
    (("(4-4/4)**4",), 81),
    (("(4!-4)*4+4",), 84),
    (("(4!+4?)*4?/4",), 85),
    (("(4!-4?/4)*4",), 86),
    (("4!+4*4*4",), 88),
    (("(4?-4?/4?)*4?", "4?+4?*√4*4"), 90),
    (("(4!-4/4)*4",), 92),
    (("4?*4?-4?+4", "√4+4!*4-4"), 94),
    (("4!*4-4/4",), 95),
    (("(4!+4-4)*4"), 96),
    (("4!*4+4/4",), 97),
    (("4?*4?+√4-4",), 98),
    (("4?*4?-4/4",), 99),
    (("(4!+4/4)*4",), 100),
]

test_cases_un = [
    # to be resolved
    (("",), 37),
    (("",), 51),
    (("",), 57),
    (("",), 67),
    (("",), 69),
    (("",), 71),
    (("",), 73),
    (("",), 75),
    (("",), 77),
    (("",), 79),
    (("",), 82),
    (("",), 83),
    (("",), 87),
    (("",), 89),
    (("",), 91),
    (("",), 93),
]


@pytest.mark.parametrize("output, input_", test_cases)  # Alterne entre test_cases e test_cases_un para rodar os testes
def test_true_solution(input_, output):
    assert solution(input_) in output


def test_validation():
    value = "(4-4)+(4-4)"
    assert valid(value) is True


def test_validation_false_with_three_fours():
    assert valid("(4+(4-4)") is False


if __name__ == "__main__":
    solution(2)
