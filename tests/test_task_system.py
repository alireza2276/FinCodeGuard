from pathlib import Path

import pytest

from fincodeguard.tasks.loader import TaskLoadError, load_task
from fincodeguard.tasks.schema import TaskSpec, TaskValidationError


def data():
    return {"task_id":"task_001","title":"Maker-checker","description":"Payment approval task.",
            "functional_requirements":["Create payment"],
            "security_requirements":["Only approver may approve"],
            "business_invariants":["Maker must differ from checker"]}

def test_schema_accepts_valid_task():
    assert TaskSpec.from_dict(data()).task_id == "task_001"

def test_schema_rejects_empty_invariants():
    d = data()
    d["business_invariants"] = []
    with pytest.raises(TaskValidationError):
        TaskSpec.from_dict(d)

def test_loader(tmp_path: Path):
    p=tmp_path/"task.yaml"
    p.write_text("""task_id: task_001
title: Maker-checker
description: Payment approval task.
functional_requirements: [Create payment]
security_requirements: [Only approver may approve]
business_invariants: [Maker must differ from checker]
""", encoding="utf-8")
    assert load_task(p).title == "Maker-checker"

def test_loader_missing(tmp_path: Path):
    with pytest.raises(TaskLoadError):
        load_task(tmp_path/"missing.yaml")
