// Clock Skew v1.0

var MeasureClockSkew = function() {

    var that = this;
    var lastButtonPress = new Date().getTime();
    // Error
    var registerError = function(XMLHttpRequest, textStatus, errorThrown) {
        $("#results").append(
            "<li class='error'>Error: " + textStatus + "</li>");
        $("#button").removeAttr("disabled");
    };
    // Success
    var registerSuccess = function(data, textStatus, XMLHttpRequest) {
        try {
            var remote = JSON.parse(data).time;
            var halfway = ((lastButtonPress) + new Date().getTime()) / 2;
            var skew = (remote - halfway) / 1000;

            $("results").append(
                "<li class='success'>Estimated clock skew: " +
                "<span class='measurement'></li>" + skew +
                "</span>seconds.</li>"
            );
        } catch(error) {
            $("#results").append(
                "<li class='error'>Error parsing JSON.</li>");
            $("#button").removeAttr("disabled");
        }
    };
    var buttonPress = function() {
        lastButtonPress = new Date().getTime();
        $("#button").attr("disabled", "disabled");
        $.ajax({
            data: "",
            dataType: "text",
            error: registerError,
            success: registerSuccess,
            type: "POST",
            url: "/time/json"
        })
    };

    return { buttonPress: buttonPress };

}();

// call the function on button press
$("#button").click(MeasureClockSkew.buttonPress);
