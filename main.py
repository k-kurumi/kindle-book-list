import os
import sys

import typer
from pandas import DataFrame

from kindle.converter import file_to_dataframe


def main(in_file: str = "<stdin>", out_file: str = "<stdout>") -> None:

    df: DataFrame = file_to_dataframe(in_file)

    if out_file == "<stdout>":
        df.to_csv(sys.stdout, index=False)
    else:
        match os.path.splitext(out_file):
            case (_, ".json"):
                df.to_json(out_file, index=False)
            case (_, ".xlsx"):
                df.to_excel(out_file, index=False)
            case (_, _):
                df.to_csv(out_file, index=False)


if __name__ == "__main__":
    typer.run(main)
