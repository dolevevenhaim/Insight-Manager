import typer
from manager import InsightManager, Insight
from pathlib import Path
import json

app = typer.Typer()
manager = InsightManager()

INSIGHT_FILE = Path("./insights.json")

manager.load(INSIGHT_FILE)

def save_and_exit():
    manager.save(INSIGHT_FILE)
    raise typer.Exit()

'''
@app.callback()
def callback():
    pass
'''


@app.command(name='add-insight')
def add_insight_cli(
    title: str = typer.Option(..., help='title'),
    subtitle: str = typer.Option(..., help='sub title'),
    content: str = typer.Option(..., help='content')
):

    ins = Insight(title=title, subtitle=subtitle, content=content)
    manager.add_insight(ins)
    typer.echo(f"✅ insight '{title}' successfully added")
    manager.save(INSIGHT_FILE)



@app.command(name='list-insights-cli')
def list_insights_cli(
    limit: int = typer.Option(None, help='Limit display of insights')
):
    manager.list_insights(limit=limit)


@app.command(name='delete-insight')
def delete_insight_cli(id: int):
    insight = manager.get_insight_by_id(id)
    if insight:
        manager.remove_insight(id)
        manager.save(INSIGHT_FILE)
        typer.echo(f"🗑️ Insight {id} deleted.")
    else:
        typer.echo(f"⚠️ Insight with ID {id} does not exist.")  
    
@app.command(name='update-insight')
def update_insight_cli(
    insight_id: int = typer.Argument(..., help="ID של התובנה לעדכון"),
    title: str = typer.Option(None, help="כותרת חדשה"),
    subtitle: str = typer.Option(None, help="כותרת משנה חדשה"),
    content: str = typer.Option(None, help="תוכן חדש"),
    # ... הוסף כאן אופציות עבור שאר המאפיינים שניתן לעדכן ...
):
    """עדכון תובנה קיימת."""
    update_data = {}
    if title is not None:
        update_data['title'] = title
    if subtitle is not None:
        update_data['subtitle'] = subtitle
    if content is not None:
        update_data['content'] = content

    if update_data:
        manager.update_insight(insight_id, **update_data)
        manager.save(INSIGHT_FILE)
        typer.echo(f"✅ update {insight_id} insight")
    else:
        typer.echo("⚠️ No parameters were provided for the update.")

@app.command(name='search-by-title')
def search_by_title_cli(
    keyword: str = typer.Argument(..., help='שלח מילת מפתח')
    ):
    results = manager.search_by_title(keyword)
    if results:
        for ins in results:
            typer.echo(f'\n {ins.id}, {ins.title}')
            typer.echo(f'{ins.subtitle}')    
    else:
        typer.echo(f'Didnt found {keyword}')

@app.command(name='search-by-content')
def search_by_content_cli(
    keyword: str = typer.Argument(..., help='שלח מילת מפתח')
    ):
    results = manager.search_by_content(keyword)
    if results:
        for ins in results:
            typer.echo(f'\n {ins.id}, {ins.content}')
            typer.echo(f'{ins.subtitle}')    
    else:
        typer.echo(f'Didnt found {keyword}')



@app.command(name='sort-by-date')
def sort_by_date(
    limit: int = typer.Option(None, help="מספר מקסימלי של תובנות")
    ):
    sorted_insights = manager.sort_by_date()
    total_insights = len(sorted_insights)
    if sorted_insights:
        for i, ins in enumerate(sorted_insights):
            if limit is not None and i >= limit:
                typer.echo(f"...Displayed only {limit} out of {total_insights} insights")
                break
            else:
                typer.echo(f"\n📌 {ins.id} {ins.title} ({ins.date})")
                typer.echo(f"✏️ {ins.subtitle}")


@app.command(name="save")
def save_insights():
    manager.save(INSIGHT_FILE)
    typer.echo("✅ Saved successfully.")


if __name__ == "__main__":
    app()