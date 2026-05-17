from fr_audio.main_cli import create_parser

import pytest


def test_verb_cli(capsys):
    parser = create_parser()

    expect_emsg = "the following arguments are required: inf_verb"
    with pytest.raises(SystemExit):
        parser.parse_args(["verb"])
    captured = capsys.readouterr()
    assert expect_emsg in captured.err

    args = parser.parse_args(["verb", "avoir"])
    assert args.inf_verb == "avoir"
    assert not (
        args.present
        or args.future
        or args.past
        or args.past_simple
        or args.conditional
        or args.imperative
    )

    args = parser.parse_args(["verb", "--imperative", "--past", "avoir"])
    assert args.inf_verb == "avoir"
    assert args.imperative and args.past
    assert not (args.present or args.future or args.past_simple or args.conditional)

    args = parser.parse_args(["verb", "avoir", "--future"])
    assert args.inf_verb == "avoir"
    assert args.future
    assert not (
        args.present
        or args.past
        or args.past_simple
        or args.conditional
        or args.imperative
    )


def test_sentence_cli(capsys):
    parser = create_parser()

    expect_emsg = "the following arguments are required: --sentence"
    with pytest.raises(SystemExit):
        parser.parse_args(["sentence"])
    captured = capsys.readouterr()
    assert expect_emsg in captured.err

    expect_emsg = "argument --sentence: expected one argument"
    with pytest.raises(SystemExit):
        parser.parse_args(["sentence", "--sentence"])
    captured = capsys.readouterr()
    assert expect_emsg in captured.err

    args = parser.parse_args(["sentence", "--sentence", "Comment ca va?"])
    assert args.sentence == "Comment ca va?"
    assert args.output == "output.mp3"

    args = parser.parse_args(
        ["sentence", "--sentence", "Bonjour!", "--output", "test.mp3"]
    )
    assert args.sentence == "Bonjour!"
    assert args.output == "test.mp3"

    args = parser.parse_args(
        ["sentence", "--sentence", "Ca va bien.", "-o", "test.mp3"]
    )
    assert args.sentence == "Ca va bien."
    assert args.output == "test.mp3"
