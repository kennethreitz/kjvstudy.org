#!/bin/bash
# Add all Joshua commentary in manageable chunks

cd /Users/kennethreitz/repos/kjvstudy.org

echo "Adding Joshua 10:41-43..."
uv run python scripts/add_josh_10.py

echo "Adding Joshua 13:15-33..."
uv run python scripts/add_josh_13.py

echo "Adding Joshua 14:14-15..."
uv run python scripts/add_josh_14.py

echo "Adding Joshua 15:54-63..."
uv run python scripts/add_josh_15.py

echo "Adding Joshua 17:16-18..."
uv run python scripts/add_josh_17.py

echo "Adding Joshua 18:4-28..."
uv run python scripts/add_josh_18.py

echo "Adding Joshua 19:37-51..."
uv run python scripts/add_josh_19.py

echo "Adding Joshua 20:4-9..."
uv run python scripts/add_josh_20.py

echo "Adding Joshua 22:31-34..."
uv run python scripts/add_josh_22.py

echo "Adding Joshua 24:25-33..."
uv run python scripts/add_josh_24.py

echo "All commentary added successfully!"
