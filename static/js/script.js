$(document).ready(function () {
    // jquery from materialise docs to activate materialise fucntions 
    $('.sidenav').sidenav();
    $('select').formSelect();
    $('.parallax').parallax();
    $('.collapsible').collapsible();
    $('.tabs').tabs();
    $('.modal').modal();
    $('.fixed-action-btn').floatingActionButton({
        direction: 'left',
        hoverEnabled: false,
        isOpen: false
    });
    $('input#input_text, textarea#textarea2').characterCounter();
    // to fade out flashes so they do not persist once user scrolls
    $(window).scroll(function() {
    $('.flashes').fadeOut(1000);
    // to fade out overlay so it does not persist once user scrolls
    $('.overlay').fadeOut(2000);
    });

    // code taken from Code Institute Task manager tutorial to ensure proper functioning of select fucntion in Materialize
 validateMaterializeSelect();
    function validateMaterializeSelect() {
        let classValid = { "border-bottom": "1px solid #4caf50", "box-shadow": "0 1px 0 0 #4caf50" };
        let classInvalid = { "border-bottom": "1px solid #f44336", "box-shadow": "0 1px 0 0 #f44336" };
        if ($("select.validate").prop("required")) {
            $("select.validate").css({ "display": "block", "height": "0", "padding": "0", "width": "0", "position": "absolute" });
        }
        $(".select-wrapper input.select-dropdown").on("focusin", function () {
            $(this).parent(".select-wrapper").on("change", function () {
                if ($(this).children("ul").children("li.selected:not(.disabled)").on("click", function () { })) {
                    $(this).children("input").css(classValid);
                }
            });
        }).on("click", function () {
            if ($(this).parent(".select-wrapper").children("ul").children("li.selected:not(.disabled)").css("background-color") === "rgba(0, 0, 0, 0.03)") {
                $(this).parent(".select-wrapper").children("input").css(classValid);
            } else {
                $(".select-wrapper input.select-dropdown").on("focusout", function () {
                    if ($(this).parent(".select-wrapper").children("select").prop("required")) {
                        if ($(this).css("border-bottom") != "1px solid rgb(76, 175, 80)") {
                            $(this).parent(".select-wrapper").children("input").css(classInvalid);
                        }
                    }
                });
            }
        });
    }
});
