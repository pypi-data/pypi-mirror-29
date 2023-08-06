from __future__ import absolute_import, division, print_function
import gains as genetic
from rdkit.Chem import AllChem as Chem
from rdkit.ML.Descriptors.MoleculeDescriptors import\
    MolecularDescriptorCalculator as calculator
import numpy as np
import unittest
import datetime
from math import exp
import random
import salty


class GuessIonTests(unittest.TestCase):
    geneSet = genetic.generate_geneset()
    df = salty.load_data("cationInfo.csv")
    parent_candidates = df['smiles'].unique()
    df = salty.load_data("anionInfo.csv")
    df = df['smiles'].unique()
    ohPickMe = random.sample(range(df.shape[0]), 1)
    anion = Chem.MolFromSmiles(df[ohPickMe[0]])

    def test_1_density(self):
        target = 1000
        self.guess_password(target)

    def test_benchmark(self):
        genetic.Benchmark.run(self.test_1_density)

    def guess_password(self, target):
        startTime = datetime.datetime.now()

        def fnGetFitness(genes):
            return get_fitness(self.anion, genes, target)

        def fnDisplay(candidate, mutation):
            display(candidate, mutation, startTime)

        def fnShowIon(genes, target, mutation_attempts, sim_score,
                      molecular_relative):
            show_ion(genes, target, mutation_attempts, sim_score,
                     molecular_relative)

        optimalFitness = 0.75
        best = genetic.get_best(fnGetFitness, optimalFitness,
                                self.geneSet, fnDisplay,
                                fnShowIon, target, self.parent_candidates)
        return best


def display(candidate, mutation, startTime):
    timeDiff = datetime.datetime.now() - startTime
    print("{}\t{}\t{}\t{}".format(candidate.Genes, candidate.Fitness,
                                  mutation, timeDiff))


class prod_model():
    def __init__(self, coef_data, model):
        self.Coef_data = coef_data
        self.Model = model


def get_fitness(anion, genes, target):
    cation = Chem.MolFromSmiles(genes)
    model = genetic.load_data("density_m1.sav", pickleFile=True)
    deslist = genetic.load_data("density_m1_descriptors.csv")
    feature_vector = []
    with genetic.suppress_stdout_stderr():
        for item in deslist:
            if "anion" in item:
                feature_vector.append(calculator([item.partition('-')
                                      [0]]).CalcDescriptors(anion)[0])
            elif "cation" in item:
                feature_vector.append(calculator([item.partition('-')
                                      [0]]).CalcDescriptors(cation)[0])
            elif "Temperature_K" in item:
                feature_vector.append(298.15)
            elif "Pressure_kPa" in item:
                feature_vector.append(101.325)
            else:
                print("unknown descriptor in list: %s" % item)
    features_normalized = (feature_vector - deslist.iloc[0].values) /\
        deslist.iloc[1].values
    prediction = exp(model.predict(np.array(features_normalized).
                     reshape(1, -1))[0])
    error = abs((prediction - target) / target)
    return 1 - error, prediction


def show_ion(genes, target, mutation_attempts, sim_score, molecular_relative):
    mol = Chem.MolFromSmiles(genes)
    print("{}\t{}".format("number of atoms: ", mol.GetNumAtoms()))
    print("{}\t{}".format("mutation attempts: ", mutation_attempts))
    print("within 25%% of target density: %s (kg/m) " % target)
    print("{}\t{}".format("similarity score: ", sim_score))
    print("{}\t{}".format("with molecular relative: ", molecular_relative))


if __name__ == '__main__':
    unittest.main()
