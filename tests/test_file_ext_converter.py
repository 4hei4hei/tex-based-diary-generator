import pytest


params = {
    "remove_not_applicables - OK case - Sample": (
        {
            "body_files": [
                "22000101.tex",
                "22000102.tex",
                "22000103.tex",
                "body.tex",
                "bodies.tex",
                "draft.tex",
                "summary.tex",
            ],
            "expected": ["22000101.tex", "22000102.tex", "22000103.tex"],
        }
    )
}


@pytest.mark.parametrize("params", list(params.values()), ids=list(params.keys()))
def test_ok_remove_not_applicables(params):
    import src.file_ext_converter

    actual = src.file_ext_converter.remove_not_applicables(params["body_files"])

    assert actual == params["expected"]
