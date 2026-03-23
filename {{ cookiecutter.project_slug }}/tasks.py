from invoke import task


@task
def lab(ctx, ip="*", port=8888):
    """Launch Jupyter Lab."""
    ctx.run(f"jupyter lab --ip={ip} --port={port}")


@task
def notebook(ctx, ip="*", port=8888):
    """Launch Jupyter Notebook."""
    ctx.run(f"jupyter notebook --ip={ip} --port={port}")


@task
def lint(ctx, fix=False):
    """Run ruff linter on src/."""
    fix_flag = " --fix" if fix else ""
    ctx.run(f"ruff check src/{fix_flag}")


@task
def format(ctx):
    """Run ruff formatter on src/."""
    ctx.run("ruff format src/")


@task
def test(ctx, verbose=True):
    """Run pytest."""
    v_flag = " -v" if verbose else ""
    ctx.run(f"pytest tests/{v_flag}")


@task
def clean(ctx):
    """Remove Python file artifacts."""
    ctx.run("find . -type f -name '*.pyc' -delete")
    ctx.run("find . -type d -name '__pycache__' -exec rm -rf {} +")
    ctx.run("find . -type d -name '.pytest_cache' -exec rm -rf {} +")
    ctx.run("find . -type d -name '*.egg-info' -exec rm -rf {} +")