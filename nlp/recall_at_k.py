# Recall at k implementation

def recall_at_k(true_items, recommended_items_scores, k=5):
    """
    Function to calculate recall at k.
    
    Parameters:
    true_items (list): List of true items.
    recommended_items_scores (list of tuples): List of tuples where each tuple is (item, score) and score indicates the relevance of the item.
    k (int): Number of recommendations to consider for calculating recall.

    Returns:
    recall (float): Recall at k.
    """
    
    # If recommended_items_scores is empty, return 0
    if not recommended_items_scores:
        return 0
    
    # Sort the items by their scores in descending order
    recommended_items_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Get the top-k recommended items
    top_k_items = [item for item, score in recommended_items_scores[:min(k, len(recommended_items_scores))]]
    
    # Find the intersection of true items and top-k recommended items
    intersect_items = set(true_items).intersection(set(top_k_items))
    
    # Calculate recall
    recall = len(intersect_items) / min(k, len(true_items))
    
    return recall
