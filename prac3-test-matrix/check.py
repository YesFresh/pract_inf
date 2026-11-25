from service import check

N = 5
L = 100 + N % 20  # L = 105


def report(case, expected, actual):
    status = "PASS" if actual == expected else "FAIL"
    print(case, expected, actual, status, sep=" | ")


cases = [
    (0, "OK"),
    (L, "OK"),
    (0.5, "OK"),
    (-1, "RANGE"),
    (L + 1, "RANGE"),
    ("15", "TYPE"),
    (True, "TYPE"),
]

for i, (value, expected) in enumerate(cases, 1):
    report(f"A-{i:02}", expected, check(value, L))

# A-08: Стресс-сценарий (10 000 вызовов + контрольный вызов 0)
answers = [check(L + i % 2, L) for i in range(10000)]
actual = (answers.count("OK"), answers.count("RANGE"), check(0, L))
report("A-08", (5000, 5000, "OK"), actual)

# A-09: Испытание на восстановление (серия 10 001 вызов, начиная с L)
answers_rec = [check(L + i % 2, L) for i in range(10001)]
actual_rec = (answers_rec.count("OK"), answers_rec.count("RANGE"), check(L, L))
report("A-09", (5001, 5000, "OK"), actual_rec)
