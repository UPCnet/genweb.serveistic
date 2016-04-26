$(document).ready(function()
{
    var problemes = $('#problemes');
    $.ajax({
        url: url_retrieve_problemes,
        timeout: 15000,
        data: {count: count},
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
