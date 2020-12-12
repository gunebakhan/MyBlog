// $("i").click(function (e) { 
//     e.preventDefault();
//     $(this).css("color", "green");
//     console.log('hi');
// });

// $("i.fa-thumbs-up").click(function (e) { 
//     e.preventDefault();
//     $(this).toggleClass("green");
// });

// $("i.fa-thumbs-down").click(function (e) { 
//     e.preventDefault();
//     $(this).toggleClass("red");
// });


$('#demo').likeDislike({
    reverseMode: true,
    activeBtn: localStorage['key'] ? localStorage['key'] : '',
    click: function (btnType, likes, dislikes, event) {
        var self = this;

        // lock the buttons
        self.readOnly(true);

        // send data to the server
        $.ajax({
            url: '/action',
            type: 'GET',
            data: 'id=1' + '&likes=' + likes + '&dislikes=' + dislikes,
            success: function (data) {
                // show new values
                $(self).find('.likes').text(data.likes);
                $(self).find('.dislikes').text(data.dislikes);
                localStorage['key'] = btnType;

                // unlock the buttons
                self.readOnly(false);
            }
        });
    }
});