$(document).ready(function(){
    var re = /^\/interface\/league\/[a-z-]+\/team\/[a-z-]+\/week-[1-9][0-7]?\//;
    console.log(window.location.pathname);

    if (window.location.pathname.match(re)){
        var title= document.querySelector('h2');

        var week = title.dataset.week;
        var teamSlug = title.dataset.teamslug;
        var teamName = title.dataset.teamname;
        var currentPicksKey = teamSlug + "_" + week + "_picks";

        var currentPicksList;
        var testVar;

        $.get(
                'http://127.0.0.1:8000/game/2014/' + week + '/' + teamSlug + '/enter_pick/',
                function(data) {


                    currentPicksList = data['weekly_picks'][currentPicksKey];

                initialChoices = [];

                for (var i = 0; i < currentPicksList.length; i++) {
                    initialChoices.push(JSON.parse(currentPicksList[i])['choice']);
                }


                inputArr = $('input');
                $.each(inputArr, function(idx, inputEl){

                    if (initialChoices.indexOf(inputEl.value) > -1) {
                        inputEl.checked = true;
                        $('input[value="' + inputEl.value + '"]').prop('checked', true);
                    };
                });

                }

        );
    }
});
