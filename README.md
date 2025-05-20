# 💡 Insight Manager CLI

A command-line tool for managing personal or team insights with support for search, sort, update, and JSON persistence.

## Features

* Add, list, delete, and update insights
* Search insights by title or content
* Sort insights by creation date
* Save insights to a local JSON file
* Clean OOP architecture
* Ready to extend into an API (FastAPI)

## Technologies

* Python 3.10+
* Typer (CLI framework)
* JSON (for persistence)
* OOP (Object-Oriented Design)

## How to Run

1. Clone the repository:

```bash
git clone https://github.com/your-username/insight-manager.git
cd insight-manager
```

2. Install dependencies:

```bash
pip install typer[all]
```

3. Run commands via CLI:

```bash
python main.py --help
```

4. Run API via Postman or Localhost

## CLI Examples

Add a new insight:

```bash
python main.py add-insight --title "My Insight" --subtitle "Quick Note" --content "This is the content"
```

List insights:

```bash
python main.py list-insights-cli
```

Delete insight by ID:

```bash
python main.py delete-insight 2
```

Search by title:

```bash
python main.py search-by-title "keyword"
```

Sort by date:

```bash
python main.py sort-by-date --limit 5
```

## Author

Dolev — Data Analyst & aspiring Product Manager

## License

MIT
