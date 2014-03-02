(function ($) {
    var handler = null,
            page = 1,
            isLoading = false,
            apiURL = '/';
            // apiURL = 'http://www.wookmark.com/api/json/popular';

    // Prepare layout options.
    var options = {
        autoResize: true, // This will auto-update the layout when the browser window is resized.
        container: $('#tiles'), // Optional, used for some extra CSS styling
        offset: 2, // Optional, the distance between grid items
        itemWidth: 210 // Optional, the width of a grid item
    };

    /**
     * When scrolled all the way to the bottom, add more tiles.
     */
    function onScroll(event) {
        // Only check when we're not still waiting for data.
        if(!isLoading) {
            // Check if we're within 100 pixels of the bottom edge of the broser window.
            var closeToBottom = ($(window).scrollTop() + $(window).height() > $(document).height() - 100);
            if(closeToBottom) {
                loadData();
            }
        }
    };

    /**
     * Refreshes the layout.
     */
    function applyLayout() {
        options.container.imagesLoaded(function() {
            // Create a new layout handler when images have loaded.
            handler = $('#tiles li');
            handler.wookmark(options);
            isLoading = false;
        });
    };

    /**
     * Loads data from the API.
     */
    function loadData() {
        isLoading = true;
        $('#loaderCircle').show();

        $.ajax({
            url: apiURL,
            dataType: 'html',
            data: {page: page}, // Page parameter to make sure we load new data
            success: onLoadData
        });
    };

    /**
     * Receives data from the API, creates HTML for images and updates the layout
     */
    function onLoadData(data) {
        $('#loaderCircle').hide();

        // Increment page index for future calls.
        page++;

        $('#tiles').append(data);

        // Apply layout.
        applyLayout();
        // isLoading = false;
    };

    // Capture scroll event.
    $(document).bind('scroll', onScroll);

    $("#ScrollToTop").click(function(){
        $('html, body').animate({scrollTop: $("html").offset().top}, 1000);
    });
    // Load first data from the API.
    applyLayout();
    // loadData();
})(jQuery);