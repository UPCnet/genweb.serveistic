var retrieve_problemes_url = portal_url + '/retrieve_problemes/';

$(document).ready(function()
{
    var problemes = $('#problemes');
    $.ajax({
        url: retrieve_problemes_url,
        data: {product_id: product_id, count: count},
        success: function(data)
        {
            problemes.html(data);
        }
    });
});
