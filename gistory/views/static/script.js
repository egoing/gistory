function escapeHtml(text) {
    var map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function (m) {
        return map[m];
    })
}

function djb2(str) {
    var hash = 5381;
    for (var i = 0; i < str.length; i++) {
        hash = ((hash << 5) + hash) + str.charCodeAt(i);
        /* hash * 33 + c */
    }
    return hash;
}

function hashStringToColor(str) {
    var hash = djb2(str);
    var r = (hash & 0xFF0000) >> 16;
    var g = (hash & 0x00FF00) >> 8;
    var b = hash & 0x0000FF;
    return "#" + ("0" + r.toString(16)).substr(-2) + ("0" + g.toString(16)).substr(-2) + ("0" + b.toString(16)).substr(-2);
}

function scrollViewerToTop() {
    if ($(document).width() > 992)
        $('.viewer').offset({top: Math.max($('.element-list').offset().top, $(document).scrollTop() + 10)});
}
function setActive(target) {
    $('a').removeClass('active');
    $(target).addClass('active');
}
function createExtraInfo(used) {
    return used && used.length>0 ? used.join(', ') + ' (This information was not included the original message)' : '';
}
$('.element').on('click', function (e) {
    e.preventDefault();
    var _self = $(this);
    setActive(_self);
    $.ajax({
        url: '/ajax/element',
        method: 'POST',
        success: function (result) {
            $('.viewer').html('');
            panelManager.add(0, result.type, result.name, result.data, result.path, createExtraInfo(result.used));
            scrollViewerToTop();
        },
        data: {path: $(this).data('path')}
    })
});

function setActiveExceptSameParent() {
    $(this).parent().find('a').removeClass('active');
    $(this).addClass('active');
}
function getPathFromOjbectId(_object) {
    parse = _object.match(/(..)(.+)/);
    return './.git/objects/' + parse[1] + '/' + parse[2];
}
$(document).on('click', '.sha1', function (e) {
    e.preventDefault();
    var _object = $(this).text();
    var _parent = $(this).parents('.panel');
    setActiveExceptSameParent.call(this);
    $.ajax({
        url: '/ajax/object',
        method: 'POST',
        success: function (result) {
            _parent.nextAll().remove();
            panelManager.add(_parent.data('panel_id'), result.type, result.name, result.data, null, createExtraInfo(result.used))
        },
        data: {object: _object}
    })
});

$(document).on('click', '.refs', function (e) {
    e.preventDefault();
    var _path = $(this).text();
    var _parent = $(this).parents('.panel');
    setActiveExceptSameParent.call(this);
    $.ajax({
        url: '/ajax/element',
        method: 'POST',
        success: function (result) {
            _parent.nextAll().remove();
            panelManager.add(_parent.data('panel_id'), result.type, result.name, result.data)
        },
        data: {path: _path}
    })
});
function Panel() {
    this.panel_id = 0;
    this.panels = [];
    this.helps = {
        'blob': 'https://www.youtube.com/watch?v=mNKWw4O0qUo',
        'tree': 'https://www.youtube.com/watch?v=mNKWw4O0qUo',
        'commit': 'https://www.youtube.com/watch?v=mNKWw4O0qUo',
        'ORIG_HEAD': 'https://youtu.be/0-ZaET1k6yQ',
        'logs': 'https://youtu.be/0-ZaET1k6yQ',
        'HEAD': 'https://youtu.be/FFa_HrKGtkI',
        'refs': 'https://youtu.be/FFa_HrKGtkI',
        'FETCH_HEAD' : 'https://youtu.be/QpTzoiiYoV4',
        'config': 'https://youtu.be/cu8qKGxpURQ',
        'index': 'https://www.youtube.com/watch?v=qBFF9NwK7a8'
    }
}
Panel.nl2br = function (str, is_xhtml) {
    var breakTag = (is_xhtml || typeof is_xhtml === 'undefined') ? '<br ' + '/>' : '<br>'; // Adjust comment to avoid issue on phpjs.org display
    return (str + '')
        .replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1' + breakTag + '$2');
};
Panel.prototype.template = function (id, type, name, data, path, extraInfo) {
    var help = this.helps[type] ? '<span class="help"><a href="' + this.helps[type] + '" data-lity><img src="/static/movie.png"></a></span>' : '';
    var extra = extraInfo ? '<tr class="extra"><td>'+extraInfo+'</td></tr>' : '';
    var tag = $('<div class="panel panel-default" data-panel_id="' + id + '">\
              <div class="panel-heading">[' + type + '] ' + name + help + '</div>\
                <table id="viewer_table2" class="table">\
                    <tr>\
                        <td class="data"><pre><code>' + data + '</code></pre></td>\
                    </tr>\
                    '+extra+'\
                    <tr class="expand"><td><a href="#">+expand</a></td></tr>\
                </table>\
            </div>');
    return tag;
};
function linkSha1(data) {
    reg = /\b([a-f0-9]{40})\b/g;
    data = data.replace(reg, '<a href="#" class="sha1">$1</a>');
    return data;
}
function linkRef(data) {
    var reg = /[^:,^+]refs(\/.+)?(\/.+)/g;
    data = data.replace(reg, ' <a href="#" class="refs">refs$1$2</a> ');
    return data;
}
Panel.prototype.add = function (caller_panel_id, type, name, data, path, extraInfo) {
    data = escapeHtml(data);
    data = linkSha1(data);
    data = linkRef(data);
    var new_panel = this.template(caller_panel_id + 1, type, name, data, path, extraInfo);
    this.panels.push(new_panel);
    $('.viewer').append(new_panel);
    this._init_expand();
};
Panel.prototype._init_expand = function () {
    var last = $('.viewer .panel').last();
    var expand = last.find('.expand');
    var pre = last.find('pre');
    $(expand).on('click', function (e) {
        e.preventDefault();
        pre.css('max-height', '');
        $(this).hide();
    });
    var MAX_HEIGHT = 300;
    if (pre.height() > MAX_HEIGHT)
        expand.show();
    pre.css('max-height', MAX_HEIGHT);
};
panelManager = new Panel();

$('.list-group a').each(function () {
    var $this = $(this);
    var path = $this.data('path');
});
