"""CSV repository for loading and saving graph/query/result/history data."""

import csv
from pathlib import Path

from smart_navigation.core.graph import Graph
from smart_navigation.models.query_result import QueryResult


class CsvRepository:
    """Repository for CSV-based persistence."""

    def load_graph(self, nodes_file: str | Path, edges_file: str | Path) -> Graph:
        graph = Graph()

        with Path(nodes_file).open("r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                graph.add_node(row.get("name", ""))

        edges_path = Path(edges_file)
        rows_to_save = []
        needs_migration = False

        with edges_path.open("r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames or []
            if "distance" not in fieldnames or "time" not in fieldnames:
                needs_migration = True

            import random
            for row in reader:
                source = row.get("from", "")
                target = row.get("to", "")
                if not source or not target:
                    continue

                if needs_migration:
                    dist = round(random.uniform(1.0, 20.0), 1)
                    time_val = round(random.uniform(5.0, 60.0), 1)
                    row["distance"] = str(dist)
                    row["time"] = str(time_val)

                rows_to_save.append(row)

                dist = float(row.get("distance", 1.0))
                time_val = float(row.get("time", 1.0))
                graph.add_edge(source, target, dist, time_val)

        if needs_migration:
            with edges_path.open("w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["from", "to", "distance", "time"])
                writer.writeheader()
                writer.writerows(rows_to_save)

        return graph

    def load_queries(self, query_file: str | Path) -> list[dict[str, str]]:
        queries: list[dict[str, str]] = []

        with Path(query_file).open("r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                start = row.get("start", "").strip()
                end = row.get("end", "").strip()
                if start and end:
                    queries.append({"start": start, "end": end})

        return queries

    def save_result(self, filename: str | Path, data: list[QueryResult]) -> None:
        filename = Path(filename)
        filename.parent.mkdir(parents=True, exist_ok=True)

        with filename.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["start", "end", "path", "distance", "time"])

            for row in data:
                writer.writerow([row.start, row.end, "-".join(row.path), row.total_distance, row.total_time])

    def save_history(self, filename: str | Path, history_stack: list[list[str]]) -> None:
        filename = Path(filename)
        filename.parent.mkdir(parents=True, exist_ok=True)

        with filename.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["no", "path"])

            for idx, path in enumerate(history_stack, 1):
                writer.writerow([idx, "-".join(path)])
