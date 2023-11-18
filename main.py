import typer

from database.interface import Interface as DbInterface
from models import Amount, Category
from parsing.file_handlers import BaseImporter


app = typer.Typer()

@app.command(name='import')
def upload(file_name: str):
    BaseImporter.import_transactions(file_name)
            
@app.command()
def init_db():
    DbInterface.init_tables()

@app.command()
def other():
    print('other command')

if __name__ == "__main__":
    app()
