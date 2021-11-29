import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    data_root = './data/family2j.csv'
    people = load_data(data_root)

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]

def create_jp_index(People, One_gene, Two_genes, Have_trait):
    jp_index = dict()
    for peep in People.keys(): 
        jp_index[peep] = dict()
        if peep in One_gene:
            jp_index[peep]['Gene'] = 1
        elif peep in Two_genes: 
            jp_index[peep]['Gene'] = 2
        else: 
            jp_index[peep]['Gene'] = 0
        if peep in Have_trait: 
            jp_index[peep]['Trait'] = True 
        else: 
            jp_index[peep]['Trait'] = False 

    return jp_index


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    jp_index = create_jp_index(people, one_gene, two_genes, have_trait)

    PROBS['inheritance'] = {
    0: PROBS['mutation'] ,
    1: (0.5*PROBS['mutation']) + (0.5*(1 - PROBS['mutation'])),
    2: 1 - PROBS['mutation']
    } 
    
    joint_probabilities = 1
    searched = set()
    people2 = people.copy()
    while bool(people2) == True:
        for peep in people2.keys(): 
            current_gene = jp_index[peep]['Gene']
            current_trait = jp_index[peep]['Trait']
            # if no parents 
            if people[peep]['mother'] == None and people[peep]['father'] == None: 
                P_gene = PROBS['gene'][current_gene]
                P_trait = PROBS["trait"][current_gene][current_trait]
                joint_probabilities *= (P_gene*P_trait)
                searched.add(peep)
            elif (people[peep]['mother'] in searched  and people[peep]['father'] in searched) == True:
                mother = people[peep]['mother']
                father = people[peep]['father']
                if jp_index[peep]['Gene'] == 1:
                    M_only = PROBS['inheritance'][jp_index[mother]['Gene']]*PROBS['inheritance'][2 -  jp_index[father]['Gene']]
                    F_only = PROBS['inheritance'][jp_index[father]['Gene']]*PROBS['inheritance'][2 -  jp_index[mother]['Gene']]
                    P_gene = M_only + F_only 
                if jp_index[peep]['Gene'] == 0:
                    P_gene = PROBS['inheritance'][2 -  jp_index[father]['Gene']] *PROBS['inheritance'][2 -  jp_index[mother]['Gene']]  
                if jp_index[peep]['Gene'] == 2:
                    P_gene = PROBS['inheritance'][jp_index[mother]['Gene']]*PROBS['inheritance'][jp_index[father]['Gene']]
                P_trait = PROBS["trait"][current_gene][current_trait]
                joint_probabilities *= (P_gene*P_trait)
                searched.add(peep)

        for peep in searched: 
            people2.pop(peep, None)

    return joint_probabilities


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    jp_index = create_jp_index(probabilities, one_gene, two_genes, have_trait)  
    for peep in probabilities:
        gene_index = jp_index[peep]['Gene']
        trait_index = jp_index[peep]['Trait']
        probabilities[peep]['gene'][gene_index] += p 
        probabilities[peep]['trait'][trait_index] += p 


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for peep in probabilities:
        gene_sum = sum(list(probabilities[peep]['gene'].values()))
        trait_sum = sum(list(probabilities[peep]['trait'].values()))
        for value in probabilities[peep]['gene'].keys(): 
            probabilities[peep]['gene'][value] /= gene_sum
        for value in probabilities[peep]['trait'].keys(): 
            probabilities[peep]['trait'][value] /= trait_sum




if __name__ == "__main__":
    main()


