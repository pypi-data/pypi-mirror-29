function refreshObjectFilterValuesWidget(){
    var content_type_id = document.getElementById('dj_auth_content_type').value;
    if (content_type_id) {
        url = "/loadvalues/" + content_type_id + "/"
        try {
            $.ajax({
                url: url,
                success: function(data){
                    $("#" + "values_block").html(" " + data);
                }
            });
        } catch (e) {
            console.log("Oups, we have a problem" + e);
        }
    } else {
        $("#" + "values_block").html("<select id='dj_auth_filter_values' name='filter_values' multiple='multiple'><option value=0 selected='selected'></option></select>");
    }
    // }
};
