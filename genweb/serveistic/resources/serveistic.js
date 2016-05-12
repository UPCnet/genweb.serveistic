function retrieve_indicadors(url, count, count_category)
{
    $.ajax({
        url: url,
        timeout: 15000,
        data: {count: count, count_category: count_category},
        success: function(data)
        {
            $('#indicadors').html(data);
        },
        error: function()
        {
            $('#indicadors').html(
                "<div class='portlet-message'>" +
                  "<p>No s&apos;han pogut recuperar els indicadors</p>" +
                "</div>")
        }
    });
}

function retrieve_problemes(url, count)
{
    $.ajax({
        url: url,
        timeout: 15000,
        data: {count: count},
        success: function(data)
        {
            $('#problemes').html(data);
        },
        error: function()
        {
            $('#problemes').html(
                "<div class='portlet-message'>" +
                  "<p>No s&apos;han pogut recuperar els problemes</p>" +
                "</div>")
        }
    });
}
