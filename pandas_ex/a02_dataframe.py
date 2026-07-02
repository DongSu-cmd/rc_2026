import numpy as np
import pandas as pd 

def main():
    value   = [[32, 68, 220, 72], 
              [28, 30, 0, 12],          
              [38, 81, 0, 91]]
    columns = ["온도", "습도", "강수량", "불쾌지수"]
    index   = ["초여름", "늦봄", "한여름"]
    df = pd.DataFrame(value, index=index, columns=columns, dtype=np.uint8)
    print(df)
    #print(df["온도"]["늦봄"], df.iloc[1, 0], df.iloc[1][0])
    #print(df.iloc[1:3, 1:3])
    #print(df.index, df.columns, df.values)
    #print(type(df.values), type(df.index), type(df.columns))
    #print(df.info())
    #print(df.head(2))
    print(df.loc["초여름", "온도"])
    print(df.loc[:, "온도"])
    print(df.loc[:, "온도":"불쾌지수"])

    cond = df["온도"] > 30
    print(cond, type(df[cond]))
    print(df[cond])
    print(df.T)


if __name__ == "__main__":
    main()  