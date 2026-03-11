import pandas as pd

def load_data(anonymized_path, auxiliary_path):
    """
    Load anonymized and auxiliary datasets.
    """
    anon = pd.read_csv(anonymized_path)
    aux = pd.read_csv(auxiliary_path)
    return anon, aux


def link_records(anon_df, aux_df):
    """
    Attempt to link anonymized records to auxiliary records
    using exact matching on quasi-identifiers.

    Returns a DataFrame with columns:
      anon_id, matched_name
    containing ONLY uniquely matched records.
    """
    q_identifiers = ['age', 'zip3', 'gender']
    merged = pd.merge(anon_df, aux_df, on=q_identifiers)
    match_counts = merged.groupby('anon_id').size()
    unique_ids = match_counts[match_counts == 1].index
    final_matches = merged[merged['anon_id'].isin(unique_ids)]
    return final_matches[['anon_id', 'name']]

   

def deanonymization_rate(matches_df, anon_df):
    """
    Compute the fraction of anonymized records
    that were uniquely re-identified.
    """
    if anon_df.empty:
        return 0.0
    
    num_matches = len(matches_df['anon_id'].unique())
    total_records = len(anon_df)
    
    return num_matches / total_records
