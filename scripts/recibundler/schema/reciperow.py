import typing as t

reciperow = t.NamedTuple(
    "reciperow",
    [
        ("timestamp", str),
        ("name", str),
        ("summary", t.Optional[str]),
        ("prep_time", t.Optional[int]),
        ("cook_time", t.Optional[str]),
        ("ingredients", t.Any),
        ("steps", t.List[str]),
        ("link_to_photo", t.Optional[str]),
        ("submitter_email", t.Optional[str]),
    ],
)

