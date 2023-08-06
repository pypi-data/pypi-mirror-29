import logging
import sys
from datetime import datetime, timedelta

import click
from html2text import html2text

from recodex.api import ApiClient
from recodex.decorators import pass_api_client


@click.group()
def cli():
    """
    Tools for working with exercises
    """


@cli.command()
@click.argument("language")
@click.argument("exercise_id")
@pass_api_client
def add_localization(api: ApiClient, language, exercise_id):
    """
    Add a localized text to an exercise.
    The text is read from the standard input. HTML and Markdown are accepted.
    """
    exercise = api.get_exercise(exercise_id)
    exercise["localizedTexts"].append({
        "locale": language,
        "text": html2text(sys.stdin.read())
    })

    api.update_exercise(exercise_id, exercise)


@cli.command()
@click.option("config_path", "-c")
@pass_api_client
def evaluate_all_rs(api: ApiClient):
    """
    Request evaluation for all reference solutions
    """
    with click.progressbar(api.get_exercises()) as bar:
        for exercise in bar:
            try:
                api.evaluate_reference_solutions(exercise["id"])
            except Exception as e:
                logging.error("Error in exercise {}: {}".format(exercise["id"], str(e)))


@cli.command()
@click.option("threshold", "-t")
@pass_api_client
def check_rs_evaluations(api: ApiClient, threshold):
    """
    Find exercises that had no successful reference solution evaluation in
    a given number of days
    """
    for exercise in api.get_exercises():
        solutions = api.get_reference_solutions(exercise["id"])
        if not solutions:
            logging.error("Exercise %s has no reference solutions", exercise["id"])
            continue

        found = False
        found_recent = False

        for solution in solutions:
            for evaluation in api.get_reference_solution_evaluations(solution["id"]):
                status_ok = evaluation["evaluationStatus"] == "done"
                submission_timestamp = int(evaluation["submittedAt"])
                submission_timestamp = max(0, submission_timestamp)
                submission_date = datetime.fromtimestamp(submission_timestamp)
                threshold_date = datetime.utcnow() - timedelta(days=int(threshold))
                recent = submission_date >= threshold_date
                if status_ok:
                    found = True
                    if recent:
                        found_recent = True
                        break

        if not found_recent:
            if found:
                logging.error("Exercise %s has no recent successful evaluations", exercise["id"])
            else:
                logging.error("Exercise %s has never had any successful evaluations", exercise["id"])