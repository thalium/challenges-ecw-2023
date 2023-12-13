$( document ).ready(function() {
    var action = function() {
        i = 0;
        sentence = "";
        //TODO: modify this to handle more sentences, maybe later... :(
        $.get( "/api/sentence", { id: Math.floor(Math.random() * 40) + 1 }, function( data ) {
            if (!data.errmsg) {
                txt = data.sentence;
                id = data.id;
                $('input[name="id"]').val(id);
                for (let i = 0; i < txt.length; i++) {
                    setTimeout(function(){
                        sentence += txt.charAt(i);
                        $('input[name="question"]').val(sentence);
                    }, i*20)
                }
            }
        }, "json" );
    };
    var prompt = setInterval(action, 5000);
    action();

    $('input[name="question"]').on( "focusin click", function() {
        clearInterval(prompt);
        $('input[name="question"]').val('');
        $('input[name="id"]').val('');
    });

    $('form[name="search"]').on( "submit", function(e) {
        clearInterval(prompt);
        $.get( "/api/search", { id: $('input[name="id"]').val(), search: $('input[name="question"]').val()}, function( data ) {
            $('div[name="output"]').removeClass('invisible');
            $('span[name="result"]').text(data.answer);
        }, "json" );
        e.preventDefault();
    });
});

