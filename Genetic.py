import random

from Chromosome import Chromosome


class Genetic:

    def __init__(self):
        self.chromosomes = []
        # randomize chromosomes
        for i in range(100):
            genes = []
            genes[0] = random.randint(3, 200)
            chromosome = Chromosome(genes)
            self.chromosomes.append(chromosome)

    def valuation(self):
        for chromosome in self.chromosomes:
            chromosome.valuation()
    def selection(self):
        # sort by health
        self.chromosomes.sort(key=lambda chromosome: chromosome.health, reverse=True)
        # take a best half
        self.chromosomes = self.chromosomes[:round(len(self.chromosomes)/2)]

    def recombination(self):
        # make new chromosomes
        for i in range(len(self.chromosomes)):
            genes = []
            genes.append(self.chromosomes[i].genes[0] + random.randint(5))  # add mutation
            chromosome = Chromosome(genes)
            self.chromosomes.append(chromosome)

