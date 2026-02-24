import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import os
import json
from matplotlib.backends.backend_pdf import PdfPages


sns.set_theme(style="whitegrid")


def generate_plots(df: pd.DataFrame):

    numeric_cols = df.select_dtypes(include="number").columns
    categorical_cols = df.select_dtypes(include="object").columns

    if len(numeric_cols) == 0:
        raise ValueError("No numeric columns found for plotting.")

    with PdfPages("report.pdf") as pdf:

        # 1️⃣ Line Plot of all numeric columns
        plt.figure(figsize=(10, 6))
        df[numeric_cols].plot()
        plt.title("Line Plot of Numeric Columns")
        plt.tight_layout()
        plt.savefig("line_plot.png")
        pdf.savefig()
        plt.close()

        # 2️⃣ Correlation Heatmap
        plt.figure(figsize=(8, 6))
        sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm")
        plt.title("Correlation Heatmap")
        plt.tight_layout()
        plt.savefig("correlation_heatmap.png")
        pdf.savefig()
        plt.close()

        # 3️⃣ Pairplot (Scatter Matrix)
        pairplot = sns.pairplot(df[numeric_cols])
        pairplot.fig.suptitle("Pairplot", y=1.02)
        pairplot.savefig("pairplot.png")
        pdf.savefig(pairplot.fig)
        plt.close(pairplot.fig)

        # 4️⃣ Histograms
        df[numeric_cols].hist(figsize=(10, 8))
        plt.suptitle("Distribution Histograms")
        plt.tight_layout()
        plt.savefig("histograms.png")
        pdf.savefig()
        plt.close()

        # 5️⃣ Boxplot grouped by first categorical column
        if len(categorical_cols) > 0:
            cat_col = categorical_cols[0]
            for num_col in numeric_cols:
                plt.figure(figsize=(8, 6))
                sns.boxplot(data=df, x=cat_col, y=num_col)
                plt.title(f"{num_col} by {cat_col}")
                plt.xticks(rotation=45)
                plt.tight_layout()
                filename = f"boxplot_{num_col}.png"
                plt.savefig(filename)
                pdf.savefig()
                plt.close()

        # 6️⃣ Regression plot (first two numeric columns)
        if len(numeric_cols) >= 2:
            plt.figure(figsize=(8, 6))
            sns.regplot(x=df[numeric_cols[0]],
                        y=df[numeric_cols[1]])
            plt.title("Regression Plot")
            plt.tight_layout()
            plt.savefig("regression_plot.png")
            pdf.savefig()
            plt.close()


def main():
    payload = json.loads(os.environ["CLIENT_PAYLOAD"])

    file_name = payload["file_name"]
    file_content = payload["file_content"]

    # Decode uploaded file
    with open(file_name, "wb") as f:
        f.write(base64.b64decode(file_content))

    df = pd.read_excel(file_name)

    generate_plots(df)

    print("Advanced plots generated successfully.")


if __name__ == "__main__":
    main()
