import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    print(f"Corpus: {corpus}")
    print("--------------------------------")
    
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    print("--------------------------------")

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
    # Get all pages in the corpus
    all_pages = list(corpus.keys())
    N = len(all_pages)
    
    # Get links from current page
    links = corpus[page]
    
    # If page has no outgoing links, treat it as having links to all pages
    if len(links) == 0:
        links = set(all_pages)
    
    num_links = len(links)
    
    # Initialize probability distribution
    probabilities = {}
    
    # Calculate probability for each page
    for p in all_pages:
        # Base probability: random jump to any page
        prob = (1 - damping_factor) / N
        
        # If this page is linked from current page, add probability from following link
        if p in links:
            prob += damping_factor / num_links
        
        probabilities[p] = prob
    
    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize counts for each page
    page_counts = {page: 0 for page in corpus.keys()}
    
    # Start with a random page
    current_page = random.choice(list(corpus.keys()))
    
    # Generate n samples
    for _ in range(n):
        # Count the current page
        page_counts[current_page] += 1
        
        # Get transition probabilities for current page
        probabilities = transition_model(corpus, current_page, damping_factor)
        
        # Choose next page based on probabilities
        # Create a list of pages and their cumulative probabilities
        pages = list(probabilities.keys())
        probs = [probabilities[p] for p in pages]
        
        # Use random.choices to select next page based on probabilities
        current_page = random.choices(pages, weights=probs, k=1)[0]
    
    # Convert counts to proportions (PageRank values)
    pagerank = {}
    for page in page_counts:
        pagerank[page] = page_counts[page] / n
    
    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Get all pages
    all_pages = list(corpus.keys())
    N = len(all_pages)
    
    # Initialize all pages with rank 1/N
    pagerank = {page: 1 / N for page in all_pages}
    
    # Iterate until convergence
    while True:
        # Calculate new PageRank values
        new_pagerank = {}
        
        for page in all_pages:
            # Start with the random jump probability
            new_rank = (1 - damping_factor) / N
            
            # Add contributions from pages that link to this page
            for linking_page in all_pages:
                links = corpus[linking_page]
                
                # If linking page has no links, treat it as linking to all pages
                if len(links) == 0:
                    links = set(all_pages)
                
                # If this page is linked from linking_page, add contribution
                if page in links:
                    num_links = len(links)
                    new_rank += damping_factor * pagerank[linking_page] / num_links
            
            new_pagerank[page] = new_rank
        
        # Check for convergence (max change < 0.001)
        max_change = 0
        for page in all_pages:
            change = abs(new_pagerank[page] - pagerank[page])
            if change > max_change:
                max_change = change
        
        # Update pagerank with new values
        pagerank = new_pagerank
        
        # If converged, break
        if max_change < 0.001:
            break
    
    return pagerank


if __name__ == "__main__":
    main()
