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

function updateIngredientList(ingredient, ingredients) {
  var el = IngredientBox(ingredient);
  el.attr('checked', true);
  $('#add-ingredient-form').remove();
  $('#filter-ingredients').append(el, AddIngredientForm(ingredients));
}

$(function () {
  $("#partial-search-title").html('hellooo!')
});

function searchIngredientKeypress (event) {
  console.dir(event);
  var key = event.originalEvent.key;
  if (event.type === "autocompleteselect" ) {
    var ingredient = event.innerText;
  }
  if (key === "Enter" || event.originalEvent.type === 'blur') {
    console.log('doing it')
    event.preventDefault();
    var ingredient = this.innerText.replace(/\W/g, '');
    if (INGREDIENTS.indexOf(ingredient) === -1) {
      this.innerText = "";
      return;
    }
    updateIngredientList(el[0].value, INGREDIENTS);
  }
}

var searchIngredients = $('#search-ingredient');
searchIngredients
  .autocomplete({ source: INGREDIENTS, minLength: 1, select: searchIngredientKeypress })
  {{/*  .keypress(searchIngredientKeypress)
  .on('blur', searchIngredientKeypress.bind(searchIngredients.get(0)))  */}}