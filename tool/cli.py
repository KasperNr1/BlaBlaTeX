import os
import shutil
import subprocess
import typer
from pathlib import Path
from git import Repo, InvalidGitRepositoryError

app = typer.Typer()
CONFIG_PATH = Path.home() / ".template_tool"
REPO_PATH = CONFIG_PATH / "repo"
CONFIG_FILE = CONFIG_PATH / "config.txt"


def load_repo_url():
    if CONFIG_FILE.exists():
        return CONFIG_FILE.read_text().strip()
    else:
        return None


def clone_or_update_repo():
    repo_url = load_repo_url()
    if not repo_url:
        typer.echo("⚠️  No repo configured. Use `tool set-repo <url>` first.")
        raise typer.Exit()

    if REPO_PATH.exists():
        try:
            repo = Repo(REPO_PATH)
            origin = repo.remotes.origin
            origin.pull()
            typer.echo("🔄 Repo updated.")
        except InvalidGitRepositoryError:
            typer.echo("❌ Repo folder is corrupted. Delete ~/.template_tool/repo and try again.")
            raise typer.Exit()
    else:
        Repo.clone_from(repo_url, REPO_PATH)
        typer.echo("✅ Repo cloned.")


@app.command()
def set_repo(url: str):
    """Set the template repository URL."""
    CONFIG_PATH.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(url.strip())
    typer.echo(f"✅ Repository set to: {url}")

@app.command()
def path():
    """Get the full path of the local Repository"""
    typer.echo(f"😎 {REPO_PATH}")

@app.command()
def list():
    """List available templates."""
    clone_or_update_repo()
    folders = [f.name for f in REPO_PATH.iterdir() if f.is_dir()]
    typer.echo("📁 Available templates:")
    for name in folders:
        typer.echo(f"  - {name}")


@app.command()
def init(name: str):
    """Copy a template to the current folder."""
    clone_or_update_repo()
    src = REPO_PATH / name
    dst = Path.cwd() / name

    if not src.exists():
        typer.echo(f"❌ Template '{name}' not found.")
        raise typer.Exit()

    if dst.exists():
        typer.echo(f"⚠️  Folder '{name}' already exists in current directory.")
        raise typer.Exit()

    shutil.copytree(src, dst)
    typer.echo(f"✅ Template '{name}' copied to: {dst}")


@app.command()
def refresh():
    """Force refresh the local copy of the repo."""
    if REPO_PATH.exists():
        shutil.rmtree(REPO_PATH)
        typer.echo("🧹 Old repo removed.")
    clone_or_update_repo()


if __name__ == "__main__":
    app()
