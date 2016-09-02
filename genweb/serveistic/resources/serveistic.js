function retrieve_indicadors(url, count_indicator, count_category, apply_order)
{
    $.ajax({
        url: url,
        timeout: 15000,
        data: {
            count_indicator: count_indicator,
            count_category: count_category,
            apply_order: apply_order},
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
