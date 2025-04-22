"""
Page Reference Sequence Generator

This module generates different types of page reference sequences for
testing page replacement algorithms.
"""

import random

def generate_random_sequence(length=100, max_page=10):
    """Generate a random page reference sequence.
    
    Args:
        length: Number of page references (default: 100)
        max_page: Maximum page number (default: 10)
        
    Returns:
        List of page numbers
    """
    return [random.randint(0, max_page-1) for _ in range(length)]

def generate_locality_sequence(length=100, max_page=10, locality_factor=0.7):
    """Generate a sequence with temporal locality.
    
    Args:
        length: Number of page references (default: 100)
        max_page: Maximum page number (default: 10)
        locality_factor: Probability of referencing a recent page (default: 0.7)
        
    Returns:
        List of page numbers
    """
    sequence = [random.randint(0, max_page-1)]
    recent_pages = [sequence[0]]
    max_recent = min(5, max_page // 2)  # Ensure recent pages is at most half of total pages
    
    for _ in range(length - 1):
        if random.random() < locality_factor and recent_pages:
            # Reference a recent page
            page = random.choice(recent_pages)
        else:
            # Reference a random page
            page = random.randint(0, max_page-1)
        
        sequence.append(page)
        
        # Update recent pages list
        if page not in recent_pages:
            recent_pages.append(page)
        if len(recent_pages) > max_recent:
            recent_pages.pop(0)
    
    # Make sure all pages are referenced at least once
    all_pages = set(range(max_page))
    used_pages = set(sequence)
    unused_pages = all_pages - used_pages
    
    if unused_pages and length > max_page:
        # Replace some random positions with unused pages
        for page in unused_pages:
            position = random.randint(0, length - 1)
            sequence[position] = page
    
    return sequence

def generate_sequential_sequence(length=100, max_page=10, sequential_factor=0.8):
    """Generate a sequence with sequential access patterns.
    
    Args:
        length: Number of page references (default: 100)
        max_page: Maximum page number (default: 10)
        sequential_factor: Probability of accessing the next sequential page (default: 0.8)
        
    Returns:
        List of page numbers
    """
    sequence = [random.randint(0, max_page-1)]
    
    for _ in range(length - 1):
        if random.random() < sequential_factor:
            # Access the next sequential page
            next_page = (sequence[-1] + 1) % max_page
            sequence.append(next_page)
        else:
            # Access a random page
            sequence.append(random.randint(0, max_page-1))
    
    # Make sure all pages are referenced at least once
    all_pages = set(range(max_page))
    used_pages = set(sequence)
    unused_pages = all_pages - used_pages
    
    if unused_pages and length > max_page:
        # Replace some random positions with unused pages
        for page in unused_pages:
            position = random.randint(0, length - 1)
            sequence[position] = page
    
    return sequence

def get_usage_frequency_distribution(sequence):
    """Analyze the frequency distribution of pages in a sequence.
    
    Args:
        sequence: List of page references
        
    Returns:
        Dictionary mapping page numbers to access counts
    """
    frequency = {}
    for page in sequence:
        if page in frequency:
            frequency[page] += 1
        else:
            frequency[page] = 1
    return frequency

if __name__ == "__main__":
    # Test the generators
    max_page = 16
    length = 100
    
    random_seq = generate_random_sequence(length, max_page)
    locality_seq = generate_locality_sequence(length, max_page)
    sequential_seq = generate_sequential_sequence(length, max_page)
    
    print("Random Sequence:", random_seq[:20], "...")
    print("Used pages:", len(set(random_seq)), "out of", max_page)
    
    print("\nLocality Sequence:", locality_seq[:20], "...")
    print("Used pages:", len(set(locality_seq)), "out of", max_page)
    
    print("\nSequential Sequence:", sequential_seq[:20], "...")
    print("Used pages:", len(set(sequential_seq)), "out of", max_page)