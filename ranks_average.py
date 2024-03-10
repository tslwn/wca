import pandas


def filepath(table: str) -> str:
    """Return the path to the WCA export file for the given table."""
    return f"data/WCA_export_{table}.tsv"


def save_best_averages():
    """Save the best average result for each person in each event since 2014."""
    min_year = 2014

    competitions = pandas.read_csv(filepath("Competitions"), delimiter="\t")
    competitions = competitions[competitions["year"] >= min_year]

    results = pandas.read_csv(filepath("Results"), delimiter="\t")
    results = results[results["average"] > 0]

    events = pandas.read_csv(filepath("Events"), delimiter="\t")

    for event in events.itertuples():
        event_results = results[results["eventId"] == event.id]
        event_results = event_results.merge(
            right=competitions,
            how="inner",
            left_on="competitionId",
            right_on="id",
        )
        event_results = event_results[["personId", "personName", "average"]]
        event_results = event_results.groupby("personId").min()
        event_results = event_results.sort_values(by="average", ascending=True)
        event_results = event_results.rename(columns={"average": "best"})
        event_results.to_csv(f"output/RanksAverage_{event.id}.csv")


if __name__ == "__main__":
    save_best_averages()
