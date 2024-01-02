import difflib
import os
import pytest

dirname = os.path.dirname(__file__)


params = {
    "compare_files - OK case - Not used file": (
        {
            "template_body_path": f"{dirname}/test_resources/body.tex",
            "body_path": f"{dirname}/test_resources/body_true.tex",
            "expected": True,
        }
    ),
    "compare_files - OK case - Only extra line": (
        {
            "template_body_path": f"{dirname}/test_resources/body.tex",
            "body_path": f"{dirname}/test_resources/body_false_only_extra_line.tex",
            "expected": False,
        }
    ),
    "compare_files - OK case - Written texts": (
        {
            "template_body_path": f"{dirname}/test_resources/body.tex",
            "body_path": f"{dirname}/test_resources/body_false_written_texts.tex",
            "expected": False,
        }
    ),
}


@pytest.mark.parametrize("params", list(params.values()), ids=list(params.keys()))
def test_ok_compare_files(params):
    import src.prune_unused_files

    template_body = open(params["template_body_path"])
    ok_body = open(params["body_path"])

    list_template_body = template_body.readlines()[1:]
    list_ok_body = ok_body.readlines()[1:]

    diff = difflib.Differ()
    diff_output = diff.compare(list_template_body, list_ok_body)

    prune_flag = src.prune_unused_files.compare_files(diff_output)

    assert prune_flag is params["expected"]
