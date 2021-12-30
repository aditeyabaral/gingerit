import json
import pytest
import subprocess

@pytest.fixture
def run():
    def run_cli_test(*args):
        command = ["python gingerit/gingerit.py"] + list(args)
        command = " ".join(command)
        output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read().decode().strip()
        return output
    return run_cli_test


@pytest.mark.parametrize(
    "text,expected,corrections",
    [
        (
            "The smelt of fliwers bring back memories.",
            "The smell of flowers brings back memories.",
            [
                {
                    "start": 21,
                    "definition": None,
                    "correct": "brings",
                    "text": "bring",
                },
                {
                    "start": 13,
                    "definition": "a plant cultivated for its blooms or blossoms",
                    "correct": "flowers",
                    "text": "fliwers",
                },
                {"start": 4, "definition": None, "correct": "smell", "text": "smelt"},
            ],
        ),
        (
            "Edwards will be sck yesterday",
            "Edwards was sick yesterday",
            [
                {
                    "start": 16,
                    "definition": "affected by an impairment of normal physical or mental function",
                    "correct": "sick",
                    "text": "sck",
                },
                {"start": 8, "definition": None, "correct": "was", "text": "will be"},
            ],
        ),
        ("Edwards was sick yesterday.", "Edwards was sick yesterday.", []),
        ("", "", []),
        (
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin vitae felis sed felis convallis egestas vel ornare massa. Fusce vehicula odio at sem pharetra condimentum. Pellentesque mattis tincidunt bibendum. Integer ultrices odio lorem. Sed venenatis turpis a commodo malesuada. Nunc bibendum tincidunt sem in sodales. Suspendisse non ligula ac ligula venenatis imperdiet eu ut ex. Fusce aliquet, ligula et tristique dignissim, nisi lorem accumsan libero, in porttitor velit erat et tortor. Fusce at libero aliquam, porttitor ligula quis, pellentesque leo. Fusce vitae diam ac quam suscipit pharetra vel hendrerit nisi. Curabitur eu magna sit amet enim porta lacinia. In hac habitasse platea proin.",
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin vitae felis sed felis convallis egestas vel ornare massa. Fusce vehicula odio at sem pharetra condimentum. Pellentesque mattis tincidunt bibendum. Integer ultrices odio Lorem. Sed venenatis turpis a commodo malesuada. Nunc bibendum tincidunt sem in sandals. Suspendisse non ligula ac ligula venenatis imperdiet eu ut ex. Fusce aliquet, ligula et tristique dignissim, nisi lorem accumsan libero, in porttitor velit erat et tortor. Fusce at libero aliquam, porttitor ligula quis, pellentesque leo. Fusce vitae diam Ac qualm suscipit porter",
            [
                {
                "start": 593,
                "text": "pharetr",
                "correct": "porter",
                "definition": "a person employed to carry luggage and supplies"
            },
            {
                "start": 579,
                "text": "quam",
                "correct": "qualm",
                "definition": "uneasiness about the fitness of an action"
            },
            {
                "start": 576,
                "text": "ac",
                "correct": "Ac",
                "definition": "a radioactive element of the actinide series; found in uranium ores"
            },
            {
                "start": 312,
                "text": "sodales",
                "correct": "sandals",
                "definition": "a shoe consisting of a sole fastened by straps to the foot"
            },
            {
                "start": 232,
                "text": "lorem",
                "correct": "Lorem",
                "definition": None
            }
            ]
        )
    ],
)


def test_gingerit_cli(text, expected, corrections, run):
    assert run("-t truncate", "-i", f"'{text}'") == expected
    assert eval(run("-o", "-t truncate", "-i", f"'{text}'"))[0]['corrections'] == corrections