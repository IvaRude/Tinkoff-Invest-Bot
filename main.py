from tinkoff_bonds.bonds import find_best_bonds


def main():
    best_bonds = find_best_bonds()
    best_bonds = [(bond.name, percentage) for bond, percentage in best_bonds]
    print(best_bonds)

if __name__ == "__main__":
    main()
