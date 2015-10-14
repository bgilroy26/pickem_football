$(document).ready(function(){
        var title= document.querySelector('h2');
        var week = title.dataset.week;
        var teamSlug = title.dataset.teamSlug;
        var teamName = title.dataset.teamName;
        var choicesList = [];


        $('input[value="Update Picks"]').click(function() {

            inputArr = $('.choice-button > input');
            $.each(inputArr, function(idx, inputEl){

                if (inputEl.checked === true) {
                    choicesList.push({team:inputEl.value, num:inputEl.name});
                };
            });

            $.post(
                    'http://finalfantasyfootball.us/game/2015/' + week + '/' + teamSlug + '/enter_pick/',
                    {
                        choices:choicesList
                    },
                    function(data, status) {
                       alert("Picks submitted!! 🎉");
                    }
                  );

        });

});
