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
  el.attr('id', 'filter-ingredient')
  input.attr('checked', 'true');
  el.on('click', () => {
    if (persistent) {
      return;
    }
    el.remove()
  });

  return el;
}

function RecipeResult(name, url, summary) {
  var el = $(`
  <div class="recipe-result"><h1 class="f3 fw1 athelas mt0 lh-title">
  <a href="${url}" class="color-inherit dim link">
    ${name} </a></h1>
    <div class="f6 f5-l lh-copy nested-copy-line-height nested-links">
          <i>${summary || ''}</i>
        </div></div>`);
  return el;
}

function updateIngredientList(ingredient) {
  var el = IngredientBox(ingredient);
  el.attr('checked', 'true');
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
    .keypress(preventKeys)

  // submit button
  $('#search-submit').on('click', async function() {
    var ingredient = []
    $('.filter-ingredient').each(function() {
      if (!this.innerText) {
        return;
      }
      ingredient.push(this.innerText.replace(/^\s?/, ''));
    });
    var results = await pagefind.search(null, {
      filters: {
        ingredient,
      }
    });
    var $searchResults = $('#search-results');
    $('#search-results .recipe-result').remove();
    (await Promise.all(results.results.slice(0, 5).map(r => r.data())))
      .forEach(function(r) {
        console.log('>>>', r)
        $searchResults.append(RecipeResult(r.meta.title, r.url, r.meta.summary));
      });
    $('#search-results-header').show();
  })
})()