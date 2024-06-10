#!/bin/bash

echo "Run migrations"
alembic upgrade head
python3 src/utils/