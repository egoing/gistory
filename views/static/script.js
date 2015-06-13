function nl2br(str, is_xhtml) {
  var breakTag = (is_xhtml || typeof is_xhtml === 'undefined') ? '<br ' + '/>' : '<br>'; // Adjust comment to avoid issue on phpjs.org display
  return (str + '')
    .replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1' + breakTag + '$2');
}

$('.element').on('click', function(){
  $.ajax({
    url:'/ajax/element',
    method:'POST',
    success:function(result){
        $('#viewer_table .type').html(result.type);
        $('#viewer_table .name').html(result.name);
        reg = /\b([a-f0-9]{40})\b/g;
        $('#viewer_table .data').html(nl2br(result.data.replace(reg, '<a href="#" class="sha1">$1</a>')));
    },
    data:{path:$(this).data('path')}
  })
})

$(document).on('click', '.sha1', function(){
  var _object = $(this).text();
  $.ajax({
    url:'/ajax/object',
    method:'POST',
    success:function(result){
        $('#viewer_table2 .type').html(result.type);
        $('#viewer_table2 .name').html(result.name);
        reg = /\b([a-f0-9]{40})\b/g;
        $('#viewer_table2 .data').html(nl2br(result.data.replace(reg, '<a href="#" class="sha1">$1</a>')));
    },
    data:{object:_object}
  })
})