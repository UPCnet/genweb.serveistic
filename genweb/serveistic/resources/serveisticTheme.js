$(document).ready(function (event) {

  // Tags select2 field
  $('#searchbytaghomepage').select2({

      tags: [],
      tokenSeparators: [","],
      minimumInputLength: 1,
      ajax: {
          url: portal_url + '/getVocabulary?name=plone.app.vocabularies.Keywords&field=subjects',
          data: function (term, page) {
              return {
                  query: term,
                  page: page // page number
              };
          },
          results: function (data, page) {
              return data;
          }
      }
  });

  // facetes search
  $('#searchinputcontentserveis .selectpicker').on("change", function(event) {
    var id = $(this).parent().data('id');
    var query = $('#searchinputcontentserveis .searchInput').val();
    var path = $(this).data().name;
    var tags = []
    $('select.selectpicker').each(function(index){
      if($(this)[0].value != ""){
        tags.push($(this)[0].value);
      }
    });
    tags = tags.join(",");

    $('.listingBar').hide();
    $.get(path + '/search_filtered_content_stic', { q: query, t: tags }, function(data) {
        $('#tagslist').html(data);
    });
  });

  // Content search
  $('#searchinputcontentserveis .searchInput').on('keyup', function(event) {

      var query = $(this).val();
      var path = $(this).data().name;
      var tags = []
      $('select.selectpicker').each(function(index){
        if($(this)[0].value != ""){
          tags.push($(this)[0].value);
        }
      });
      tags = tags.join(",");

      $('.listingBar').hide();
      $.get(path + '/search_filtered_content_stic', { q: query, t: tags }, function(data) {
          $('#tagslist').html(data);
      });
  });

  // ------------------------- Facetes -------------------------
  $('#facetes :checkbox').change(function(event){
    var val = $(this).val();

    if ($(this).is(':checked')){
      $('.'+val).show();
    }
    else {
     $('.'+val).hide();
     $('.'+val).children().val([]);
      var query = $('#searchinputcontentserveis .searchInput').val();
      var path = $(this).data().name;
      var tags = []
      $('select.selectpicker').each(function(index){
        if($(this)[0].value != ""){
          tags.push($(this)[0].value);
        }
      });
      tags = tags.join(",");
      $('.listingBar').hide();
      $.get(path + '/search_filtered_content_stic', { q: query, t: tags }, function(data) {
          $('#tagslist').html(data);
      });
    }
  });

});
