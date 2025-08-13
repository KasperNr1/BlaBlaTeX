import stat
import shutil
import os
import typer
from typing import Optional
from pathlib import Path
from git import Repo, InvalidGitRepositoryError, GitCommandError

app = typer.Typer()
CONFIG_PATH = Path.home() / ".template_tool"
REPO_PATH = CONFIG_PATH / "repo"
CONFIG_FILE = CONFIG_PATH / "config.txt"
NON_TEMPLATE_FOLDERS = [".git"]
__version__ = "1.1.0"


def load_repo_url():
    if CONFIG_FILE.exists():
        return CONFIG_FILE.read_text().strip()
    else:
        return None


def clone_or_update_repo():
    repo_url = load_repo_url()
    if not repo_url:
        typer.echo("⚠️  No repo configured. Use `blablatex set-repo <url>` first.")
        raise typer.Exit()

    if REPO_PATH.exists():
        try:
            repo = Repo(REPO_PATH)
            origin = repo.remotes.origin
            origin.pull()
            typer.echo("🔄 Repo updated.")
        except GitCommandError as e:
            typer.echo(f"⚠️ Could not update repo (probably no internet): \n{e}")
            typer.echo("💡 Using existing local copy instead.")
        except InvalidGitRepositoryError:
            typer.echo(f"❌ Repo folder is corrupted. Delete \"{REPO_PATH}\" and try again.")
            raise typer.Exit()
        except Exception as e:
            typer.echo(f"❌ Something went wrong when attempting to clone or update the repo, I'll try my best to continue!\nHere is the Exception: {e}")
    else:
        Repo.clone_from(repo_url, REPO_PATH)
        typer.echo("✅ Repo cloned.")

@app.command()
def init(
    name: str,
    new_name: Optional[str] = typer.Argument(
        None,
        help="Optional: name of the destination folder. Defaults to the template name.",
    ),
):
    """Copy a template to the current folder (optionally renaming the folder)."""
    clone_or_update_repo()

    src = REPO_PATH / name
    if not src.exists() or name in NON_TEMPLATE_FOLDERS:
        typer.echo(f"❌ Template '{name}' not found.")
        raise typer.Exit(code=1)

    dst_name = new_name or name
    dst = Path.cwd() / dst_name

    if dst.exists():
        typer.echo(f"⚠️  Destination '{dst_name}' already exists in current directory.")
        raise typer.Exit(code=1)

    shutil.copytree(src, dst)
    typer.echo(f"✅ Template '{name}' copied to: {dst}")

@app.command()
def list():
    """List available templates."""
    clone_or_update_repo()
    folders = [f.name for f in REPO_PATH.iterdir() if f.is_dir()]
    typer.echo("📁 Available templates:")
    for name in folders:
        if name not in NON_TEMPLATE_FOLDERS:
            typer.echo(f"  - {name}")

@app.command()
def path():
    """Get the full path of the local Repository"""
    typer.echo(f"😎 Local Clone: {REPO_PATH}")

@app.command()
def refresh():
    """Force refresh the local copy of the repo."""
    if REPO_PATH.exists():
        try: 
            shutil.rmtree(REPO_PATH, onerror=remove_readonly)
            typer.echo("🧹 Old repo removed.")
        except PermissionError:
            typer.echo("🚨 An error occured while trying to remove the repository. Try manually deleting it")
            path()
            typer.echo()
            raise typer.Exit(code=1)
    else:
        typer.echo("⚡ The Repo was not found.")
    clone_or_update_repo()

@app.command()
def set_repo(url: str):
    """Set the template repository URL."""
    CONFIG_PATH.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(url.strip())
    typer.echo(f"✅ Repository set to: {url}")
    
def remove_readonly(func, path, _):
    """Force remove read-only files on Windows."""
    os.chmod(path, stat.S_IWRITE)
    func(path)

@app.command()
def version():
    """Print the version number and Exit."""
    try:
        print(f"BlaBlaTeX is currently installed with Version:\n{__version__}")
    except Exception as e:
        raise typer.Exit(e)


if __name__ == "__main__":
    app()
