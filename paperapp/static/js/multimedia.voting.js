$(document).on('click', '.vote', function () {
    var button = $(this);
    var mediaId = button.data("media-id");
    var mediaType = button.data("media-type");
    var voteType = button.data("vote-type");
    $.ajax({
        url: "/vote/" + mediaId + "/" + mediaType + "/" + voteType + "/",
        success: function (data) {
            if (data.success) {
                // Update the vote count on the page
                $("#vote-count-" + mediaType + "-" + mediaId).text("Votes: " + data.total_votes);
            }
        }
    });
});
