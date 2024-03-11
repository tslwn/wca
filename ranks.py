"""
A simple Python script to re-create the `RanksAverage` and `RanksSingle` tables
provided by the WCA results export, but with a date filter.
"""

from typing import Literal

import pandas

OrderBy = Literal["average", "best"]

orderby_filename: dict[OrderBy, str] = {
    "average": "Average",
    "best": "Single",
}


def filepath(table: str) -> str:
    """
    Given a table name, returns the corresponding file path.
    """
    return f"data/WCA_export_{table}.tsv"


def load(table: str) -> pandas.DataFrame:
    """
    Given a table name, returns the corresponding DataFrame.
    """
    return pandas.read_csv(filepath(table), delimiter="\t")


def rank(
    dataframe: pandas.DataFrame,
    groupby: list[str],
    orderby: OrderBy,
) -> pandas.DataFrame:
    """
    Given a DataFrame, a list of columns to group by, and a column to order by,
    returns a new DataFrame with a new column containing the rank of the ordered
    column within each group.
    """
    return dataframe.groupby(groupby)[orderby].rank(ascending=True).astype(int)


def merge_and_save(
    orderby: OrderBy,
    min_year: int | None = None,
    max_year: int | None = None,
):
    """
    Re-creates the `RanksAverage` or `RanksSingle` table provided by the WCA results
    export, but with a date filter.
    """

    # Load the tables.
    competitions = load("Competitions")
    countries = load("Countries")
    results = load("Results")

    # Apply the date filter.
    date_filter = ""
    if min_year is not None:
        competitions = competitions[competitions["year"] >= min_year]
        date_filter += f"_{min_year}"
    if max_year is not None:
        competitions = competitions[competitions["year"] <= max_year]
        date_filter += f"_{max_year}"

    # Exclude invalid results.
    results = results[results[orderby] > 0]

    # Join the tables.
    results = results.merge(right=competitions, left_on="competitionId", right_on="id")
    results = results.merge(right=countries, left_on="personCountryId", right_on="id")

    # Omit unnecessary columns.
    results = results[
        ["continentId", "personCountryId", "personId", "eventId", orderby]
    ]

    # Find the best result for each person and event.
    results = results.groupby(["personId", "eventId"]).min()

    # Add the rank columns.
    results["worldRank"] = rank(results, ["eventId"], orderby)
    results["continentRank"] = rank(results, ["eventId", "continentId"], orderby)
    results["countryRank"] = rank(results, ["eventId", "personCountryId"], orderby)

    # Omit unnecessary columns.
    results = results.reset_index()
    results = results[
        [
            "personId",
            "eventId",
            orderby,
            "worldRank",
            "continentRank",
            "countryRank",
        ]
    ]

    # Sort in ascending order of event and best result.
    results = results.sort_values(by=["eventId", orderby], ascending=True)
    results = results.rename(columns={orderby: "best"})

    # Save the table.
    results.to_csv(
        f"output/Ranks{orderby_filename[orderby]}{date_filter}.csv", index=False
    )


if __name__ == "__main__":
    merge_and_save("average", min_year=2014)
    merge_and_save("best", min_year=2014)
