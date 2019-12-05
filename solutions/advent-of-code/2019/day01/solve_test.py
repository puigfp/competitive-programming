import solve


def test_required_fuel():
    tests = [(12, 2), (14, 2), (1969, 654), (100756, 33583)]
    for (mass, fuel_requirement) in tests:
        assert solve.required_fuel(mass) == fuel_requirement


def test_required_fuel_2():
    tests = [(14, 2), (1969, 966), (100756, 50346)]
    for (mass, fuel_requirement) in tests:
        assert solve.required_fuel_2(mass) == fuel_requirement
