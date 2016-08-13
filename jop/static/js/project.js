/* Project specific Javascript goes here. */
var Actions = {
    Like: {
        toggle: function() {
            if (!$(this).hasClass('processing')) {
                var $link = $(this);
                var url = $link.attr('href');

                $.ajax({
                    type: 'POST',
                    url: url,
                    data: {},
                    beforeSend: function() {
                        $link.addClass('processing');
                    },
                    success: function(responseHtml) {
                        $link.closest('.post-footer').replaceWith(responseHtml);
                    }
                });
            }
            return false;
        }
    }
};

$(document).ready(function() {
    $(document).on('click', 'a.voteup-toggle', Actions.Like.toggle);
});