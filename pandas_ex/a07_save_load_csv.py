from pathlib import Path

import numpy as np
import pandas as pd 
import seaborn as sns

def main():
    BASE_DIR = Path(__file__).parent
    df = sns.load_dataset("tips")  
    df.to_csv(BASE_DIR / "weather.csv")
    df = pd.read_csv(BASE_DIR / "weather.csv", index_col=0, header=0)
    print(df)

if __name__ == "__main__":
    main()