import pandas as pd
from difflib import SequenceMatcher

def is_near_duplicate(text1, text2, threshold=0.85):
    """Calculates string similarity ratio for near-identical templates."""
    return SequenceMatcher(None, str(text1).lower(), str(text2).lower()).ratio() >= threshold

def deduplicate_corpus(df):
    """FR-01: Deduplicates near-identical templates before splitting."""
    keep_indices = []
    texts = df['body_text'].tolist()
    
    for i, current_text in enumerate(texts):
        is_dup = False
        for kept_idx in keep_indices:
            if is_near_duplicate(current_text, texts[kept_idx]):
                is_dup = True
                break
        if not is_dup:
            keep_indices.append(i)
            
    dedup_df = df.iloc[keep_indices].reset_index(drop=True)
    print(f"Original samples: {len(df)} | Deduplicated samples: {len(dedup_df)}")
    return dedup_df

def campaign_holdout_split(df, test_campaign):
    """FR-03: Campaign-separated holdout to test generalization."""
    test_df = df[df['campaign_group'] == test_campaign].reset_index(drop=True)
    train_df = df[df['campaign_group'] != test_campaign].reset_index(drop=True)
    
    print(f"Training samples: {len(train_df)}")
    print(f"Holdout Test samples (Campaign '{test_campaign}'): {len(test_df)}")
    return train_df, test_df

if __name__ == "__main__":
    df = pd.read_csv("dataset.csv")
    
    # 1. Deduplication
    clean_df = deduplicate_corpus(df)
    clean_df.to_csv("clean_dataset.csv", index=False)
    
    # 2. Campaign Split (e.g., holding out 'delivery_scam' for unseen testing)
    train_df, test_df = campaign_holdout_split(clean_df, test_campaign="delivery_scam")
    train_df.to_csv("train.csv", index=False)
    test_df.to_csv("test.csv", index=False)
    
    print("Pre-processing and campaign split complete!")