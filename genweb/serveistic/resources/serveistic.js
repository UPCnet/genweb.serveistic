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

/*
 * For hash-marked URLs, user's toolbar hides the top of the referenced fragment.
 * Following function fixes the issue by scrolling the page up according to the
 * toolbar height.
 */
function fix_toolbar_overlap() {
    window.addEventListener("hashchange", scroll_up_toolbar);
    $(window).load(function() {
        if (window.location.hash) {
            scroll_up_toolbar();
        }
    });
}

function scroll_up_toolbar() {
    var toolbar_height = $("#portal-personaltools-wrapper > div").height();
    if (toolbar_height != null) {
        scrollBy(0, -toolbar_height);
    }
}

$(document).ready(function() {
    fix_toolbar_overlap();
});
