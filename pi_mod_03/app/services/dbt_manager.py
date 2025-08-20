import subprocess
from app.config.config import Settings

config = Settings()


class DBTManager:
    PROFILES_DIR = "../../dbt_project/profiles"
    # config.DBT_PROFILES_DIR
    PROJECT_DIR = "../../dbt_project"
    # config.DBT_PROJECT_DIR

    def __init__(
        self,
        project_dir=PROFILES_DIR,
        profiles_dir=PROJECT_DIR,
    ):
        self.project_dir = project_dir
        self.profiles_dir = profiles_dir

    def run_command(self, args):
        """Run a dbt command with the specified arguments."""
        command = (
            ["dbt"]
            + args
            + ["--project-dir", self.project_dir, "--profiles-dir", self.PROFILES_DIR]
        )
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error : {' '.join(command)}\n")
            print(e.stderr)

    def debug(self):
        self.run_command(["debug"])

    def deps(self):
        self.run_command(["deps"])

    def run(self):
        self.run_command(["run"])

    def test(self):
        self.run_command(["test"])

    def build(self):
        self.run_command(["build"])


# from services.dbt_manager import DBTManager

# dbt = DBTManager()
# dbt.run()
