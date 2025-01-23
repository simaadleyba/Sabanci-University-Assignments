import client
from myntl import phi

def find_generators(phi_n, n):

    # Set a list for generators
    generators = []

    # Loop from 1 to n to check every possible coprime
    for i in range(1, n):
        temp_num_set = set()

        # Loop from 1 to phi_n (As it cannot exceed phi_n as exponent)
        for k in range(1, phi_n + 1):

            # Calculate the remainder
            result = pow(i, k, n)

            # Add it to the set
            temp_num_set.add(result)

        # If set has the same length as phi of n, then i has generated all the elements and is a generator
        if len(temp_num_set) == phi_n:

            # Add it to the list
            generators.append(i)

    return generators

def find_generator_given_order(n, order):

    # Iterate over potential generators
    for i in range(1, n):

        # Check if i ** order is congruent to 1 mod n
        found_generator = True

        # If it is congruent to 1  mod n
        if pow(i, order, n) == 1:

            # Check if there is a smaller element
            for k in range(1, order):

                # If there is a smaller element, this cannot be our generator
                if pow(i, k, n) == 1:
                    found_generator = False

            # If there is no smaller element, then we found out generator
            if found_generator:
                return i


if __name__ == "__main__":

    n ,t = client.getQ1()

    print("n:", n)
    print("t:", t)

    print("\n------------------------")

    print("\nQUESTION 1A")

    # Find phi of n
    phi_n = phi(n)

    print("Number of elements is:", phi_n)

    # Check answer
    client.checkQ1a(phi_n)

    print("\n------------------------")

    print("\nQUESTION 1B")

    # Find phi of n
    phi_n = phi(n)

    # Find generators
    generators = find_generators(phi_n, n)

    # Print generators
    print("Generators:", generators)

    # Since we need only one generator, let's choose the first and check
    client.checkQ1b(generators[0])

    print("\n------------------------")

    print("\nQUESTION 1C")

    generator = find_generator_given_order(n, t)
    print("Generator is:", generator)

    client.checkQ1c(generator)
