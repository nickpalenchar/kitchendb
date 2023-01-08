function $displayUnits(mul = 1) {
    let els = document.getElementsByClassName('recipe-unit');
    for (var i = 0; i < els.length; i++) {
        var el = els[i];
        var numberParts = el.innerHTML.split('.').map(p => parseFloat(p));
        if (numberParts.length < 2) {
            continue;
        }
        var wholeNumber = parseFloat(numberParts[0].toString());
        el.innerHTML = (wholeNumber > 0 ? wholeNumber + ' ' : '') + toFraction('.' + numberParts[1].toString());
    }
}
function toFraction(amount) {
    if (amount === 0) {
        return 0;
    }
    if (!amount) {
        return '';
    }
    amount = parseFloat(amount);
    if (amount < 0.05) {
        return amount.toString();
    }
    if (amount < 0.108) {
        return "⅒"; // 0.1
    }
    if (amount < 0.118) {
        return "⅑"; // 0.11
    }
    if (amount < 0.1268) {
        return "⅛"; // 0.125
    }
    if (amount < 0.143) {
        return "⅐"; // 0.142
    }
    if (amount < 0.170) {
        return "⅙";
    }
    if (amount < 0.210) {
        return "⅕"; // 0.200
    }
    if (amount < 0.27) {
        return "¼"; // 0.25
    }
    if (amount < 0.310) {
        return "³⁄₁₀"; // 0.3
    }
    if (amount < 0.34) {
        return "⅓"; // 0.33
    }
    if (amount < 0.42) {
        return "⅖"; // 0.40
    }
    if (amount < 0.55) {
        return "½";
    }
    if (amount < 0.64) {
        return "⅗"; // 0.6
    }
    if (amount < 0.68) {
        return "⅔";
    }
    if (amount < 0.72) {
        return "⁷⁄₁₀";
    }
    if (amount < 0.76) {
        return "¾";
    }
    if (amount < 0.816) {
        return "⅘"; // 0.8
    }
    if (amount < 0.84) {
        return "⅚";
    }
    if (amount < 0.858) {
        return "⁶⁄₇";
    }
    if (amount < 0.899) {
        return "⅞"; // 0.875
    }
    if (amount < 1) {
        return "⁹⁄₁₀";
    }
    return 1 + toFraction(amount - 1);
}
