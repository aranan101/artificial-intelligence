import os
import random
import re
import sys
import numpy as np

Directory = os.getcwd() + '/corpus0'

DAMPING = 0.85
SAMPLES = 10000



def main():
    #if len(sys.argv) != 2:
        #sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl("corpus1")
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    page_links = corpus[page]
    if len(page_links) == 0: 
        prob_distribution = {key:(1/len(corpus)) for key in corpus.keys()}
    else: 
        prob_distribution = dict()
        comp1 = (1 - damping_factor)/len(corpus)
        comp2 = damping_factor/len(page_links)
        for key in corpus.keys(): 
            if key in page_links: 
                prob_distribution[key] = comp1 + comp2
            else: 
                prob_distribution[key] = comp1
    return prob_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    m = n
    if n < 1:
        return ' n must be greater than or equal to 1'
    choices = [key for key in corpus.keys()]
    samples =  {key:0 for key in corpus.keys()}
    page_choice = np.random.choice(choices)
    samples[page_choice] += 1 
    n -= 1 
    while n > 0: 
        t_model = transition_model(corpus, page_choice, damping_factor)
        choices = [key for key in t_model.keys()]
        probs = [value for value in t_model.values()]
        page_choice = np.random.choice(choices, p = probs)
        samples[page_choice] += 1 
        n -= 1
    for key in samples.keys(): 
        samples[key] /= m
    return samples 



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    def calculate_pagerank( pageranks): 
        comp1 = (1 - damping_factor)/ len(corpus)
        new_pageranks = dict()
        indicator = False 
        for page in pageranks.keys():
            linked_keys = set()
            [linked_keys.add(key) for key,value in zip(corpus.keys(),corpus.values()) if page  in value ]
            comp2 = 0
            for key in list(linked_keys):
                comp2 += (pageranks[key]/len(corpus[key]))  
            comp2 *= damping_factor
            new_pageranks[page] = comp1 + comp2
            if abs(new_pageranks[page] - pageranks[page]) > 0.001: 
                indicator = True 
        return new_pageranks, indicator
    

    pageranks  = {key:(1/len(corpus)) for key in corpus.keys()}
    indicator = True 
    while indicator == True: 
        pageranks, indicator = calculate_pagerank( pageranks)
    return pageranks



    

    



if __name__ == "__main__":
    main()
