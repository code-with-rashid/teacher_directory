function updateQueryStringParameter(uri, key, value) {
  var re = new RegExp("([?&])" + key + "=.*?(&|$)", "i");
  var separator = uri.indexOf('?') !== -1 ? "&" : "?";
  if (uri.match(re)) {
    return uri.replace(re, '$1' + key + "=" + value + '$2');
  }
  else {
    return uri + separator + key + "=" + value;
  }
}

$("#id_last_name_starts").keypress(function(){
    if($(this).val().length>0){
        return false;
    }
});

$(document).on("click", "#search", function(){
    var url = $(location).attr("href");
    var last_name_starts = $("#id_last_name_starts").val();
    var new_url = updateQueryStringParameter(url, 'last_name_starts', last_name_starts);
    var subject = $("#id_subject").val();
    new_url = updateQueryStringParameter(new_url, 'subject', subject);
    window.location.href = new_url;
});

$(document).on("click", "#clear", function(){
    var url = $(location).attr("href");
    var new_url = updateQueryStringParameter(url, 'last_name_starts', '');
    new_url = updateQueryStringParameter(new_url, 'subject', '');
    window.location.href = new_url;
});