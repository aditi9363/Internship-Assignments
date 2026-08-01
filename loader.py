import os
import glob
import pandas as pd

# Define column names
COLS = [
    "time",
    "avg_rss12",
    "var_rss12",
    "avg_rss13",
    "var_rss13",
    "avg_rss23",
    "var_rss23"
]

def load_dataset(dataset_path="Dataset"):
    # List to store all DataFrames
    all_data = []

    # Loop through every activity folder
    for pattern in os.listdir(dataset_path):
        folder_path = os.path.join(dataset_path, pattern)

        # Skip if it is not a folder
        if not os.path.isdir(folder_path):
            continue

        # Get all csv files in the current folder
        for file_path in glob.glob(os.path.join(folder_path, "*.csv")):
            # Read the CSV file
            df = pd.read_csv(
                file_path,
                comment="#",
                header=None,
                sep=r"[,\s]+",
                engine="python",
                index_col=False,
                usecols=range(7),
                names=COLS
            )

            # Add pattern column
            df["Pattern"] = pattern

            # Store DataFrame
            all_data.append(df)

    # Merge all DataFrames
    master_df = pd.concat(all_data, ignore_index=True)

    # Save as CSV
    master_df.to_csv("ALL_ACTIVITY_PATTERN.csv", index=False)
    return master_df

if __name__ == "__main__":
    master_df = load_dataset()

    # Display first five rows
    print(master_df.head())

    # Display shape
    print("\nShape:", master_df.shape)

    # Count Rows of each activity
    print("\nRows in each Pattern:\n")
    print(master_df["Pattern"].value_counts())



