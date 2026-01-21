import pandas as pd

def analyze_file(df):
    """
    Generate summary for the entire DataFrame.
    Returns a dict with numeric, categorical, and unique column info.
    """
    summary = {
        "total_columns": len(df.columns),
        "numeric_columns": [],
        "categorical_columns": [],
        "unique_columns": [],
        "selected_columns": {}  # placeholder for detailed analysis
    }

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            summary["numeric_columns"].append({
                "name": col,
                "min": df[col].min(),
                "max": df[col].max(),
                "mean": df[col].mean()
            })
        else:
            unique_vals = df[col].nunique()
            summary["categorical_columns"].append({
                "name": col,
                "unique_count": unique_vals,
                "value_counts": df[col].value_counts().to_dict()
            })
            if unique_vals == len(df[col]):
                summary["unique_columns"].append(col)

    return summary


def analyze_selected_columns(df, selected_columns):
    """
    Analyze only user-selected columns.
    Returns a dict keyed by column name with detailed stats.
    """
    details = {}
    for col in selected_columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            details[col] = {
                "min": df[col].min(),
                "max": df[col].max(),
                "mean": df[col].mean()
            }
        else:
            details[col] = {
                "unique_count": df[col].nunique(),
                "value_counts": df[col].value_counts().to_dict()
            }
    return details