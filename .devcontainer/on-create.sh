#!/bin/bash
set -x

# Make data directory
mkdir -p /odoo-data/filestore /odoo-data/sessions /odoo-data/logs
chown -R vscode:vscode /odoo-data


# Aggregate other repositories
gitaggregate -c repos-dev.yaml

# Install requirements
pip install --no-cache-dir -r .repos/odoo/requirements.txt
pip install --no-cache-dir -r requirements.txt
pip install -e .repos/odoo
pip install click-odoo-contrib

# Install pre-commit hooks
pre-commit install

# Config git
git config pull.rebase true

# Create config from template
cat .devcontainer/odoo.cfg.tmpl | envsubst > odoo.cfg

# Install act
curl --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/nektos/act/master/install.sh | bash
mv ./bin/act /usr/local/bin/act
rm -r ./bin/
