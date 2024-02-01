# pylint: disable=missing-docstring,line-too-long

import unittest

import requests

from src.backend.app import app, db


class TestBackend(unittest.TestCase):
    def setUp(self) -> None:
        app.config["TESTING"] = True

        with app.app_context():
            db.create_all()

        self.client = app.test_client()

    def test_new_game_persistence(self):
        response = self.client.get("/")
        response_dict = response.json
        game_uuid = response_dict["game_uuid"]
        self.assertEqual(response.status_code, 200)
        self.assertTrue(game_uuid)
        self.assertTrue(response_dict["game"])

        new_response = self.client.get(
            "/get_game/v1", query_string={"game_uuid": game_uuid}
        )
        new_response_dict = new_response.json

        self.assertEqual(new_response.status_code, 200)
        self.assertEqual(new_response_dict["game"], response_dict["game"])

    def test_slide(self):
        response = self.client.get("/")
        response_dict = response.json
        game_uuid = response_dict["game_uuid"]

        slide_response = self.client.post(
            "/perform_slide/v1",
            data={"game_uuid": game_uuid, "slide_direction": "up"},
        )
        slide_response_dict = slide_response.json
        print(slide_response.text)

        self.assertEqual(slide_response.status_code, 200)
        self.assertTrue(slide_response_dict["game"])

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
