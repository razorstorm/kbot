import markovgen

file_ = open('kathtest.txt')

markov = markovgen.Markov(file_)

print(markov.generate_markov_text())
print()
print(markov.generate_markov_text())
print()
print(markov.generate_markov_text())
print()
print(markov.generate_markov_text())
print()
print(markov.generate_markov_text())
print()
print(markov.generate_markov_text())
print()
