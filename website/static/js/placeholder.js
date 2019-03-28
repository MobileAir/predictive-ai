var txt = "Enter a company name";
var timeOut;
var txtLen = txt.length;
var char = 0;
$('.main-search').attr('placeholder', '|');
(function typeIt() {
    var humanize = Math.round(Math.random() * (200 - 30)) + 30;
    timeOut = setTimeout(function () {
        char++;
        var type = txt.substring(0, char);
        $('.main-search').attr('placeholder', type + '|');
        typeIt();

        if (char == txtLen) {
            $('.main-search').attr('placeholder', $('.main-search').attr('placeholder').slice(0, -1)) // remove the '|'
            clearTimeout(timeOut);
        }

    }, humanize);
}());