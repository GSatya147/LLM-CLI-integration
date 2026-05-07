import json
import os
import shutil

import pytest

from src.logger import ResponseLogger

TEST_DIR = "test_logs"


@pytest.fixture
def logger():
    os.makedirs(TEST_DIR, exist_ok=True)
    log = ResponseLogger("test.jsonl", output_dir=TEST_DIR)
    yield log
    shutil.rmtree(TEST_DIR)


def test_log_creates_file(logger):
    logger.log("SUCCESS", "hello", 1, "response", 1)
    assert os.path.exists(os.path.join(TEST_DIR, "test.jsonl"))


def test_log_writes_valid_entries(logger):
    logger.log("SUCCESS", "hello", 1, "response", 1)
    with open(os.path.join(TEST_DIR, "test.jsonl"), "r") as f:
        line = f.readline()
    entry = json.loads(line)
    assert entry["status"] == "SUCCESS"
    assert entry["input"] == "hello"
    assert entry["input tokens"] == 1
    assert entry["output"] == "response"
    assert entry["output tokens"] == 1


def test_log_writes_multiple_lines(logger):
    logger.log("SUCCESS", "hello", 1, "response", 1)
    logger.log("ERROR", "hello", 1, "response", 1)
    with open(os.path.join(TEST_DIR, "test.jsonl"), "r") as f:
        lines = f.readlines()
    assert len(lines) == 2
