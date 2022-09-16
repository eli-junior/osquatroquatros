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


class NotFoundError(Exception):
    ...


def valid(response: str) -> bool:
    return response.count("4") == 4


def generate_expressions(values: list[str]):
    valid_operations = ["+", "-", "*", "/"]

    signals = product(valid_operations, repeat=(len(values) - 1))
    for s in signals:
        resp = "".join(f"{values[i]}{s[i]}" for i in range(len(values) - 1))
        resp += f"{values[-1]}".replace(" ", "")

        # stackoverflow
        # if resp in ("4**4**4**4", "4**4**4*4"):
        #     continue
        yield resp
        if "/" in resp:
            yield f"({resp.replace('/', ')/', 1)}".replace("(4)", "4")
        if "4/4" in resp:
            yield f"{resp.replace('4/4', '(4/4)', 1)}"
        if "*" in resp:
            yield f"({resp.replace('*', ')*', 1)}".replace("(4)", "4")
        if "4*4" in resp:
            yield f"{resp.replace('4*4', '(4*4)', 1)}"


def evaluate(exp: str, expected: int) -> bool:
    result = False
    with contextlib.suppress(TypeError, SyntaxError):
        s = exp.replace("4!", "24")
        result = eval(s) == expected
    return result


def solution(input_) -> str:
    for case in (
        ["4", "4", "4", "4"],
        ["4!", "4", "4", "4"],
        ["4!", "4!", "4", "4"],
        ["44", "4", "4"],
        ["44", "4!", "4"],
    ):
        for exp in generate_expressions(case):
            # print(f"{exp} -> {input_} =>", end="")
            if evaluate(exp, input_) and valid(exp):
                # print("Sim!")
                return exp
            # print("Não!")
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
    (("(4!+4!+4)/4",), 13),
    (("4!/4+4+4",), 14),
    (("4*4-4/4",), 15),
    (("4+4+4+4",), 16),
    (("4*4+4/4",), 17),
    (("4!-4-4/4",), 19),
    (("(4+4/4)*4",), 20),
    (("((4/4)-4)+(4!)", "4!+4/4-4"), 21),
    (("4!-(4+4)/4", "4!/4+4*4"), 22),
    (("(4!*4-4)/4",), 23),
    (("4+4+4*4",), 24),
    (("(4!*4+4)/4",), 25),
    (("4!+4!/4-4",), 26),
    (("(4!)-((4/4)-4)", "4!+4-4/4"), 27),
    (("(4+4)*4-4",), 28),
    (("(4/4)+4+4!", "4!+4+4/4"), 29),
    (("(4!+4!*4)/4",), 30),
    (("4*4+4*4",), 32),
    (("4!+4!/4+4",), 34),
    (("(4+4)*4+4",), 36),
    (("44-4!/4",), 38),
    (("(4!/4+4)*4",), 40),
    (("44-4/4",), 43),
    (("4!+4!+4+4",), 56),
    (("4*4*4-4",), 60),
    (("4+4*4*4",), 68),
    (("44+4!+4", "(4!-4!/4)*4"), 72),
    (("(4!+4-4)*4"), 96),
    (("(4!+4/4)*4",), 100),
    # to be solved
    # (("(44/4)+4!",), 35),
    # (("",), 18),
    # (("",), 31),
    # (("",), 33),
    # (("",), 37),
    # (("",), 39),
    # (("",), 41),
    # (("",), 42),
]


@pytest.mark.parametrize("output, input_", test_cases)
def test_true_solution(input_, output):
    assert solution(input_) in output


def test_validation():
    value = "(4-4)+(4-4)"
    assert valid(value) is True


def test_validation_false_with_three_fours():
    assert valid("(4+(4-4)") is False


if __name__ == "__main__":
    solution(2)
