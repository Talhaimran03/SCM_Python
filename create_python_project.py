import os
import shutil
import git
import pyenv
import requests

#Function to check if all parameters are provided
def check_parameters(token, python_version, project_name, project_directory):
    if not token or not python_version or not project_name or not project_directory:
        print("Error parameters")
        exit(1)
    print("1. Check on parameters passed!")

#Function to check if the template directory exists
def check_template_directory(template_directory):
    if not os.path.isdir(template_directory):
        print('Error: Template directory does not exist.')
        exit(1)

#Function to check if the template files exist
def check_template_files(template_directory):
    if not os.path.isfile(os.path.join(template_directory, "pyproject.toml")) or not os.path.isfile(os.path.join(template_directory, "LICENSE")):
        print('Error: Template files do not exist.')
        exit(1)
    print("2. Check on Template directory and files passed!")

#Function to check if pyenv, pyenv-virtualenv, pipenv, git and curl are installed
def check_installed_tools():
    if not shutil.which("pyenv"):
        print('Error: pyenv is not installed.')
        exit(1)
    if not shutil.which("pyenv-virtualenv"):
        print('Error: pyenv-virtualenv is not installed.')
        exit(1)
    if not shutil.which("pipenv"):
        print('Error: pipenv is not installed.')
        exit(1)
    if not shutil.which("git"):
        print('Error: git is not installed.')
        exit(1)
    if not shutil.which("curl"):
        print('Error: curl is not installed.')
        exit(1)
    print("3. Check on installed tools passed!")

#Function to create the project directory if it doesn't exist
def create_project_directory(project_directory):
    if not os.path.isdir(project_directory):
        os.mkdir(project_directory)
    else:
        print('Error: folder already exists.')
        exit(1)

#Function to create the project structure
def create_project_structure(project_directory, package, project_name, username):
    open(os.path.join(project_directory, "README.md"), "a").close()
    os.mkdir(os.path.join(project_directory, "src"))
    os.mkdir(os.path.join(project_directory, "tests"))
    os.mkdir(os.path.join(project_directory, "src", package + project_name + "_" + username))
    open(os.path.join(project_directory, "src", package + project_name + "_" + username, "__init__.py"), "a").close()
    open(os.path.join(project_directory, "src", package + project_name + "_" + username, project_name + ".py"), "a").close()
    print("Created project structure in " + project_directory)

#Function to create the virtual environment
def create_virtual_environment(project_name, python_version, project_directory):
    os.mkdir(os.path.join(project_directory, ".venv"))
    if not pyenv.versions.find(python_version):
        pyenv.install(python_version)
    pyenv.virtualenv(python_version, project_name + "_" + python_version)
    os.chdir(project_directory)
    os.environ["PYENV_VERSION"] = project_name + "_" + python_version
    os.system("pipenv install")
    exit()

#Function to configure git to global parameters stored inside ~/-gitconfig
def configure_git(username, email):
    git.config("--global user.name", username)
    git.config("--global user.email", email)

#Function to initialize the Git repository
def initialize_git_repository():
    git.init()

#Function to create a new repository on GitHub
import requests

def create_github_repository(token, project_name):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {"name": project_name, "auto_init": True}
    response = requests.post("https://api.github.com/user/repos", headers=headers, json=payload)

    if response.status_code == 201:
        print(f"Created repository {project_name} on GitHub")
    else:
        print("Failed to create repository on GitHub")
        print(response.json())


#Function to add the remote repository to the local Git repository
def add_remote_repository(username, token, project_name):
    git.config("remote.origin.url", "https://" + username + ":" + token + "@github.com/" + username + "/" + project_name + ".git")

#Function to add all files to the Git repository
def add_files_to_git_repository():
    git.add(".")

#Function to commit the changes
def commit_changes():
    git.commit("-m", "Initial commit")

#Function to push the changes to the remote repository
def push_changes():
    git.push("-u", "origin", "master")

#Function to cleaning the token
def clean_token():
    git.config("--global --unset credential.helper")
    os.remove("~/.git-credentials")

def main(token, python_version, project_name, project_directory, template_directory, package, username, email):
    # Check parameters
    check_parameters(token, python_version, project_name, project_directory)

    # Check template directory and files
    check_template_directory(template_directory)
    check_template_files(template_directory)

    # Check installed tools
    check_installed_tools()

    # Create project directory
    create_project_directory(project_directory)

    # Create project structure
    create_project_structure(project_directory, package, project_name, username)

    # Create virtual environment
    create_virtual_environment(project_name, python_version, project_directory)

    # Configure git
    configure_git(username, email)

    # Initialize git repository
    initialize_git_repository()

    # Create GitHub repository
    create_github_repository(token, project_name)

    # Add remote repository to local Git repository
    add_remote_repository(username, token, project_name)

    # Add files to Git repository
    add_files_to_git_repository()

    # Commit changes
    commit_changes()

    # Push changes to remote repository
    push_changes()

    # Clean token
    clean_token()

if __name__ == "__main__":

    token = "github_token"
    python_version = "3.9.2"
    project_name = "py_project"
    project_directory = "path_project"
    template_directory = "path_template"
    package = "package"
    username = "github_username"
    email = "github_email@example.com"

    main(token, python_version, project_name, project_directory, template_directory, package, username, email)