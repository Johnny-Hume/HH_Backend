from flask import jsonify


class Utils:

    def __init__(self) -> None:
        pass

    def jsonify_list(self, list):

        new_list = []
        for item in list:
            new_list.append(item.__dict__)

        return jsonify(new_list)
