var notificacions_generals_url = 'retrieve_notificacions_generals';

function configure_carousel()
{
    $('.slider-notificacions .carousel').carousel(
    {
        interval: 8000
    });
    $('.slider-notificacions .carousel').carousel('cycle');
    $('.slider-notificacions .carousel .left').click(function()
    {
        $('.slider-notificacions .carousel').carousel('prev');
        return false;
    });
    $('.slider-notificacions .carousel .right').click(function()
    {
        $('.slider-notificacions .carousel').carousel('next');
        return false;
    });
    $('.slider-notificacions .carousel').carousel('next');
}

$(document).ready(function(event)
{
    var notificacions = $('#notificacions-carousel');
    $.ajax({
        url: notificacions_generals_url,
        success: function(data)
        {
            if (data.trim())
            {
                notificacions.html(data);
                configure_carousel();
            }
        }
    });
});
