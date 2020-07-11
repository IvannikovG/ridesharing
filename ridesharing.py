from app import create_app, cli, cli
from app.models import Account, Car


app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Account': Account, 'Car': Car}
