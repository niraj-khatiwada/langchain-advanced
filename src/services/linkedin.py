import os
from dotenv import load_dotenv
import requests
from typing import TypedDict

load_dotenv(override=True)

SCRAPING_DOG_API_KEY = os.getenv("SCRAPING_DOG_API_KEY")


class LinkedInExperience(TypedDict):
    company: str
    position: str


class LinkedInUser(TypedDict):
    username: str
    first_name: str
    last_name: str
    description: str
    location: str
    profile_photo: str
    experiences: list[LinkedInExperience]


class LinkedInService:
    @staticmethod
    def extract_id_from_url(url: str) -> str:
        if url.endswith("/"):
            url = url.slice(0, -1)
        splitted = url.split("/")
        id = splitted[-1]
        return "" if (id is None or id == "") else id

    def get_user_detail(self, username: str, mock: bool = True) -> LinkedInUser:
        """
        Fetches user's LinkedIn profile detail using their username and returns in json format.
        Args:
            username(str): Username of the user
            mock(bool, optional): Should mock the profile instead of using real API or not. Useful during testing.
        Returns:
            LinkedInUser(dict):
                - username(str)
                - first_name(str)
                - last_name(str)
                - description(str)
                - location(str)
                - profile_photo(str)
                - experiences(list[LinkedInExperience])
        """

        user_detail: LinkedInUser = {
            "username": username,
        }
        if mock:
            res = requests.get(
                "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/faa5b7b8d5aebfe8f6a17b4312adb25710e35d6f/eden-marco.json",
                {
                    "headers": {
                        "Content-Type": "application/json",
                    }
                },
            )
            user_json: dict = res.json()
            for entry in user_json.items():
                val = entry[1]
                if not (
                    (type(val).__name__ == "str" and val == "")
                    or (
                        (type(val).__name__ == "list" or type(val).__name__ == "dict")
                        and len(val) == 0
                    )
                    or val is None
                ):
                    user_detail["first_name"] = user_json["first_name"]
                    user_detail["last_name"] = user_json["last_name"]
                    user_detail["description"] = user_json["summary"]
                    user_detail["location"] = user_json["country"]
                    user_detail["profile_photo"] = user_json["profile_pic_url"]
                    user_detail["experiences"] = []
                    if (
                        "experiences" in user_json
                        and type(user_json["experiences"]).__name__ == "list"
                    ):
                        for experience in user_json["experiences"]:
                            user_detail["experiences"].append(
                                {
                                    "company": (
                                        None
                                        if "company" not in experience
                                        else experience["company"]
                                    ),
                                    "position": (
                                        None
                                        if "title" not in experience
                                        else experience["title"]
                                    ),
                                }
                            )
        else:
            res = requests.get(
                f"https://api.scrapingdog.com/linkedin?api_key={SCRAPING_DOG_API_KEY}&type=profile&linkId={username}"
            )
            user_json_list = res.json()
            if type(user_json_list).__name__ == "list" and len(user_json_list) > 0:
                user_json = user_json_list[0]
                for entry in user_json.items():
                    val = entry[1]
                    if not (
                        (type(val).__name__ == "str" and val == "")
                        or (
                            (
                                type(val).__name__ == "list"
                                or type(val).__name__ == "dict"
                            )
                            and len(val) == 0
                        )
                        or val is None
                    ):
                        user_detail["first_name"] = user_json["first_name"]
                        user_detail["last_name"] = user_json["last_name"]
                        user_detail["description"] = user_json["about"]
                        user_detail["location"] = user_json["location"]
                        user_detail["profile_photo"] = user_json["profile_photo"]
                        user_detail["experiences"] = []
                        if (
                            "experiences" in user_json
                            and type(user_json["experiences"]).__name__ == "list"
                        ):
                            for experience in user_json["experiences"]:
                                user_detail["experiences"].append(
                                    {
                                        "company": (
                                            None
                                            if "company" not in experience
                                            else experience["company"]
                                        ),
                                        "position": (
                                            None
                                            if "title" not in experience
                                            else experience["title"]
                                        ),
                                    }
                                )
        return user_detail
