$(document).ready(function(){
//     $(".team_list_link").on("click", function(event) {
//         event.preventDefault();
//         var userName = $('#target_user').children('a').text();
//         var content = $('#target_content').text();
//
//         $.ajax({
//             method: 'GET',
//             url: '/users/repost',
//             data: {
//                     'userName': userName,
//                     'content': content,
//                 }
//         });
//     });

    if (window.location.pathname === '/game/2014/'
    var current_picks_data = $.get('http://127.0.0.1:8000/game/2014/week-1/the-fighting-bavarians/enter_pick/', function(data) {
        var current_picks_list = data['weekly_picks'];
    var initial_choices = [];


    for (var i = 0; i < current_picks_list.length; i++) {
        initial_choices.push(JSON.parse(current_picks_list[i])['choice']);
    }

    for (var i = 0; i < initial_choices.length; i++) {
        console.log(initial_choices[i]);
    }


    inputArr = $('input');
    $.each(inputArr, function(idx, inputEl){

        if (initial_choices.indexOf(inputEl.value) > -1) {
            inputEl.checked = true;
            $('input[value="' + inputEl.value + '"]').prop('checked', true);
        };
    });
    console.log("after func");


});
