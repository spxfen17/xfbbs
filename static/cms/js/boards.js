$(function () {
    $("#add-board-btn").click(function (event) {
       event.preventDefault();
       xtalert.alertOneInput({
           'text':'请输入板块名称！',
           'placeholder':'板块名称',
           'confirmCallback':function (inputValue) {
               zlajax.post({
                   'url':'/cms/aboard/',
                   'data':{
                       'name':inputValue
                   },
                   'success':function (data) {
                       if(data['code'] == 200){
                           window.location.reload()
                       }else {
                           xtalert.alertInfo(data['message'])
                       }
                   }
               });
           }
       });
    });
});


$(function () {
    $('.edit-board-btn').click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var name = tr.attr('data-name');
        var board_id = tr.attr('data-id');

        xtalert.alertOneInput({
            'title': '编辑板块',
            'text': '请输入版块名称',
            'placeholder': name,
            'confirmCallback': function (inputValue) {
                zlajax.post({
                    'url': '/cms/uboard/',
                    'data': {
                        'board_id': board_id,
                        'name': inputValue
                    },
                    'success': function (data) {
                        if (data['code'] == 200) {
                            window.location.reload();
                        } else {
                            xtalert.alertInfo(data['message'])
                        }
                    }
                });
            }
        });
    });
});


$(function () {
   $(".delete-board-btn").click(function () {
       var self = $(this);
       var tr = self.parent().parent();
       var board_id = tr.attr('data-id');

       xtalert.alertConfirm({
           'msg':'你确定要删除吗？',
           'confirmCallback':function () {
               zlajax.post({
                  'url':'/cms/dboard/',
                  'data':{
                      'board_id':board_id
                  },
                   'success':function (data) {
                       if(data['code'] == 200){
                           window.location.reload();
                       }else {
                           xtalert.alertInfo(data['message']);
                       }
                   }
               });
           }
       });
   }) ;
});

