# Instructions

Download the latest WCA results export as TSVs [here](https://www.worldcubeassociation.org/export/results)
and extract the archive into the `data/` directory of this repository.

### Installation

> [!WARNING]
> This repository is designed to be used on macOS and has not been tested on other operating systems.

Create a virtual environment and install Python dependencies:

```bash
conda create --name wca python==3.11
conda activate wca
conda install pip
pip install -r requirements.txt
```

Note that the default interpreter path in [settings.json](./.vscode/settings.json)
assumes you are using [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/)
and the environment is named `wca`.
