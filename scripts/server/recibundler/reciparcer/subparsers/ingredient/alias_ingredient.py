def alias_ingredient(ing: str) -> str:
    alias_ingredient = {
        "frozen corn kernals": "frozen corn",
        "frozen corn kernels": "frozen corn",
        "original soy sauce": "soy sauce",
        "full carrots": "large carrot",
    }
    if ing.lower() in alias_ingredient:
        return alias_ingredient[ing.lower()]
    elif ing.lower() + "s" in alias_ingredient:
        return alias_ingredient[ing.lower() + "s"]
    return ing
