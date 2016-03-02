var retrieve_problemes_url = portal_url + '/retrieve_problemes/';

$(document).ready(function()
{
    var problemes = $('#problemes');
    $.ajax({
        url: retrieve_problemes_url,
        timeout: 15000,
        data: {product_id: product_id, servei_path: servei_path, count: count},
        success: function(data)
        {
            problemes.html(data);
        },
        error: function()
        {
            problemes.html(
                "<div class='portlet-message'>" +
                  "<p>No s&apos;han pogut recuperar els problemes</p>" +
                "</div>")
        }
    });
});
