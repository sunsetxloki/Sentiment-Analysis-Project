$(document).ready(function() {
    // Animations for buttons
    $('button').hover(
        function() {
            $(this).css({
                'background-color': '#FFC107',
                'color': '#343a40',
                'transform': 'scale(1.05)',
                'transition': 'all 0.3s'
            });
        },
        function() {
            $(this).css({
                'background-color': '#FFC107',
                'color': 'white',
                'transform': 'scale(1)',
                'transition': 'all 0.3s'
            });
        }
    );
});
// Redirect the user after showing the sentiment result for a few seconds
