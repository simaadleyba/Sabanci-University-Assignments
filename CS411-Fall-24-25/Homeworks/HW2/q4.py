"""
Solve the following equations of the form ax ≡ b mod n and find all solutions for x if a solution exists. Explain the steps and the results.
"""

from myntl import egcd

def find_solution(x, y, n, a, b, d):

    # Set a solutions list
    solutions = []

    # Find scaling factor
    scaling_factor = b // d

    # Calculate the solution x_0
    x_0 = (x * scaling_factor)

    # Add solution(s) to the list
    for i in range(d):
        solution = (x_0 + i * (n // d)) % n
        solutions.append(solution)

    return solutions

def solve_question(question_number, n, a, b):
    print("\nQUESTION:", question_number)

    # Find gcd and coefficients
    d, x, y = egcd(a, n)

    # Check if a solution exists
    if b % d == 0:
        print("There is at least one solution.")

        solutions = find_solution(x, y, n, a, b, d)

        # Print solutions
        print(f"\n(ax ≡ b mod n) has exactly {len(solutions)} solution(s) mod n.")

        for i in range(len(solutions)):
            print(f"Solution {i + 1}: x = {solutions[i]}")

    else:
        print("No solution exists.")

    print("\n------------------------")

if __name__ == "__main__":
    solve_question("4A", 1593089977489628213419978935847037520292814625191902216371975,
                   1085484459548069946264190994325065981547479490357385174198606,
                   953189746439821656094084356255725844528749341834716784445794)

    solve_question("4B", 333837116253674643166082492900,
                   176622984297114106732586191098,
                   84172329859897226978948124629)

    solve_question("4C", 333837116253674643166082492900,
                   57063337401967433471889139534,
                   397555361861029295385484594412)

    solve_question("4D", 72223241701063812950018534557861370515090379790101401906496,
                   798442746309714903219853299207137826650460450190001016593820,
                   263077027284763417836483401088884721142505761791336585685868)