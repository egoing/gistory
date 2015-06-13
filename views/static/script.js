$('.element').on('mouseover', function(){
  $.ajax({
    url:'/ajax/element',
    method:'POST',
    success:function(result){
        $('#viewer_table .type').html(result.type);
        $('#viewer_table .name').html(result.name);
        $('#viewer_table .data').html(result.data);
    },
    data:{path:$(this).data('path')}
  })
})