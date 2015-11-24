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

  // Tags search
  $('#searchbytaghomepage').on("change", function(event) {

      var query = $('#searchinputcontentserveis .searchInput').val();
      var path = $(this).data().name;
      var tags = $('#searchbytaghomepage').val();

      $('.listingBar').hide();
      $.get(portal_url + '/' + path + '/search_filtered_content_stic', { q: query, t: tags }, function(data) {
          $('#tagslist').html(data);
      });
  });

  // Content search
  $('#searchinputcontentserveis .searchInput').on('keyup', function(event) {

      var query = $(this).val();
      var path = $(this).data().name;
      var tags = $('#searchbytaghomepage').val();

      $('.listingBar').hide();
      $.get(path + '/search_filtered_content_stic', { q: query, t: tags }, function(data) {
          $('#tagslist').html(data);
      });
  });

});
