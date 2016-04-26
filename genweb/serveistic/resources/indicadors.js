$(document).ready(function()
{
    var indicadors = $('#indicadors');
    $.ajax({
        url: url_retrieve_indicadors,
        timeout: 15000,
        data: {count: count, count_category: count_category},
        success: function(data)
        {
            indicadors.html(data);
        },
        error: function()
        {
            indicadors.html(
                "<div class='portlet-message'>" +
                  "<p>No s&apos;han pogut recuperar els indicadors</p>" +
                "</div>")
        }
    });
});
