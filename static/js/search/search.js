var INGREDIENTS = [
  "ActionScript",
  "AppleScript",
  "Asp",
  "BASIC",
  "C"
];
function IngredientBox(name, persistent = false) {
  var el = $('<div class="filter-ingredient">');
  var input = $('<input type="checkbox" class="filter-ingredient" id="' + name + '" name="' + name + '" >');
  var label = $('<label class="filter-ingredient-label" for="' + name + '"> ' + name + ' </label>');
  el.append(input, label);
  el.addClass('ingredient-box');
  el.attr('id', 'filter-ingredient').attr('data-persistent', persistent);
  if (!persistent) {
    input.attr('checked', true);
  }
  el.on('click', () => {
    if (persistent) {
      return;
    }
    el.remove()
  });

  return el;
}

function updateIngredientList(ingredient) {
  var el = IngredientBox(ingredient);
  el.attr('checked', true);
  $('#search-area-ingredients').append(el);
}

$(function () {
  $("#partial-search-title").html('hellooo!')
});

function searchIngredientKeypress (event, ui) {
  console.dir(event, ui);
  if (event.type === "autocompleteselect" ) {
    var ingredient = ui.item.value;
    setTimeout(function () {$("#search-ingredient").html("")});
    updateIngredientList(ingredient);
    return;
  }
}
function preventKeys (event) {
  if (event.originalEvent.key === 'Enter') {
    event.preventDefault();
  }
}

(async function () {
  try {
    var pagefind = await import("/_pagefind/pagefind.js");
    var filters = await pagefind.filters();
  } catch (e) {
    // we are probably in dev so mock ingredients
    filters = { ingredient: {
      "red cabbage": 3,
      "sugar": 2,
      "butter": 2,
      "flour": 2,
    }}
  }

  INGREDIENTS = Object.keys(filters.ingredient);
  var searchIngredients = $('#search-ingredient');
  searchIngredients
    .autocomplete({ source: INGREDIENTS, minLength: 1, select: searchIngredientKeypress })
    .keypress(preventKeys);
})()