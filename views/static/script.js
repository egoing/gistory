function escapeHtml(text) {
  var map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  };

  return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}

$('.element').on('click', function(e){
  e.preventDefault();
  $.ajax({
    url:'/ajax/element',
    method:'POST',
    success:function(result){
//        $('#viewer_table .type').html(result.type);
//        $('#viewer_table .name').html(result.name);
//        reg = /\b([a-f0-9]{40})\b/g;
//        $('#viewer_table .data').html(nl2br(result.data.replace(reg, '<a href="#" class="sha1">$1</a>')));
        $('.viewer').html('');
        panelManager.add(0, result.type, result.name, result.data)
    },
    data:{path:$(this).data('path')}
  })
})

$(document).on('click', '.sha1', function(e){
      e.preventDefault();
      var _object = $(this).text();
      var _parent = $(this).parents('.panel');
      $.ajax({
        url:'/ajax/object',
        method:'POST',
        success:function(result){
            _parent.nextAll().remove()
            panelManager.add(_parent.data('panel_id'), result.type, result.name, result.data)
        },
        data:{object:_object}
      })
})
function Panel(){
    this.panel_id = 0;
    this.panels = []
}
Panel.nl2br = function(str, is_xhtml) {
  var breakTag = (is_xhtml || typeof is_xhtml === 'undefined') ? '<br ' + '/>' : '<br>'; // Adjust comment to avoid issue on phpjs.org display
  return (str + '')
    .replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1' + breakTag + '$2');
}
Panel.prototype.template = function(id, type, name, data){
    var tag = $('<div class="panel panel-default" data-panel_id="'+id+'">\
              <div class="panel-heading">['+type+'] '+name+'</div>\
                <table id="viewer_table2" class="table">\
                    <tr>\
                        <td class="data">'+data+'</td>\
                    </tr>\
                </table>\
            </div>')
    return tag;
}
Panel.prototype.add = function(caller_panel_id, type, name, data){
    reg = /\b([a-f0-9]{40})\b/g;
    data = escapeHtml(data);
    data = Panel.nl2br(data.replace(reg, '<a href="#" class="sha1">$1</a>'));
    var new_panel = this.template(caller_panel_id+1, type, name, data);
    this.panels.push(new_panel);
    $('.viewer').append(new_panel)
}
panelManager = new Panel()
