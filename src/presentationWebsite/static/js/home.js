$(function() {
  $('#search-form').bind('change keydown mousedown', function(e) {
    var btn = $('#search-btn');
    var from = $('input[name="start_date"]').val(),
        to = $('input[name="end_date"]').val();
    if (from && to) {
      if (from > to) {
        btn.removeClass('active');
        btn.addClass('disabled');
        btn.attr('disabled','disabled');
      } else {
        btn.removeClass('disabled');
        btn.addClass('active');
        btn.removeAttr('disabled');
      }
    }
  });

  $('#analysis-term').bind('change keydown nousedown', function(e) {
    var btn = $('#analysis-btn');
    if ($('#analysis-term').val()) {
      btn.removeClass('disabled');
      btn.addClass('active');
      btn.removeAttr('disabled');
    } else {
      btn.removeClass('active');
      btn.addClass('disabled');
      btn.attr('disabled','disabled');
    }
  });
});
