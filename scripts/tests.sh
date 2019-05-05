#!/bin/bash
# Run tests
export FLASK_ENV='testing'
pytest --cov=automoticz tests/