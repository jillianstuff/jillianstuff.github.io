import pandas as pd
import matplotlib.pyplot as plt
import base64
import os
import json


def create_graph(df: pd.DataFrame):
    """
    Example function:
    Plots the first two numeric columns.
    Modify this logic as needed.
    """
    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) < 2:
        raise ValueError("Need at least two numeric columns to plot.")

    x = numeric_cols[0]
    y = numeric_cols[1]

    plt.figure()
    plt.plot(df[x], df[y])
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(f"{y} vs {x}")
    plt.tight_layout()
    plt.savefig("output_graph.png")


def main():
    payload = json.loads(os.environ["CLIENT_PAYLOAD"])

    file_name = payload["file_name"]
    file_content = payload["file_content"]

    # Decode file
    with open(file_name, "wb") as f:
        f.write(base64.b64decode(file_content))

    df = pd.read_excel(file_name)

    create_graph(df)

    print("Graph created successfully.")


if __name__ == "__main__":
    main()
