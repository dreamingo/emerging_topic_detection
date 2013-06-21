$(function(){
  var rid;
  $('.want').click(function(e){
    rid = $(this).attr('value');
    $('input[name="from"]').val(''),
    $('input[name="to"]').val('');
    $('div.alert-info').text("total days: 0");
  });

  $('.modal-footer .submit').click(function(){
    var from = $('input[name="from"]').val(),
    to = $('input[name="to"]').val();
    $.ajax({
      type: "GET",
      url: location.pathname + '/book_room/' + rid,
      data: {start_date: from, end_date: to},
      success: function(ret) {
        $('div.alert-info').text(ret);
        if (ret.indexOf('success') != -1) {
          setTimeout(function(){
            $('#orderModal').removeClass('in');
            $('#orderModal').css('display','none');
            $('#orderModal').attr('aria-hidden', 'true');
            $('.modal-backdrop').remove();
          }, 4000);
        }
      }
    });
  });

  $("table .detail").click(function(event){
    $.ajax({
      type: "GET",
      url: "related_weibo",
      data: {mids: $(this).val()},
      success: function(res) {
        $('.modal-body').text("");
        weibo_list = JSON.parse(res);
        ul_frags = $("<ul></ul>");
        for (var i = 0; i < weibo_list.length; i++) {
          var li_frag = $("<li class='weibo-info'></li>");
          li_frag.text(weibo_list[i]);
          ul_frags.append(li_frag);
        }
        $('.modal-body').append(ul_frags);
      }
    });
  });
});
