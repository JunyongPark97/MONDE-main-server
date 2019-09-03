import json


def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError as e:
    return False
  return True


def category_search_v1(categories):
    if not is_json(categories):
        return (None)
    shape = categories.shape
    strap = categories.strap
    ...

