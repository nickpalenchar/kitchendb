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

function searchIngredientKeypress (event) {
  console.dir(event);
  var key = event.originalEvent.key;
  if (event.type === "autocompleteselect" ) {
    var ingredient = event.currentTarget.innerText;
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
  var pagefind = await import("/_pagefind/pagefind.js");
  console.log('loading pagefind');
  var filters = await pagefind.filters();
  console.log(filters);
  INGREDIENTS = Object.keys(filters.ingredient);
  console.log("ingrediest?", INGREDIENTS);
  var searchIngredients = $('#search-ingredient');
  searchIngredients
    .autocomplete({ source: INGREDIENTS, minLength: 1, select: searchIngredientKeypress })
    .keypress(preventKeys);
    // .on('blur', searchIngredientKeypress.bind(searchIngredients.get(0)));
})()