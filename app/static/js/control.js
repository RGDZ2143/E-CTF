$(function () {
    // // TODO: 生成窗口控制
    // $('#create-invitecode').on('click', function () {
    //     $('#confirm-create').modal({
    //         relatedTarget: this
    //     })
    // })



    // 查询窗口控制
    $('#query-invitecode').on('click', function () {
        $('#query-prompt').modal({
            relatedTarget: this,
            onConfirm: function (e) {
                $.ajax({
                    url: '/control/invitecodevalidate/invitecode',
                    type: 'post',
                    dataType: 'json',
                    data: JSON.stringify({
                        'input-invitecode': e.data
                    }),
                    cache: false,
                    success: function (data) {
                        $('#query-result-text').html('')
                        if (data.result) {
                            if (data.user) {
                                $('#query-result-text').append('<span class="am-text-secondary">激活码: </span>' + data.result + '<br/>')
                                $('#query-result-text').append('<span class="am-text-success">激活用户: ' + data.user + '</span><br/>')
                            } else {
                                $('#query-result-text').append('<span class="am-text-secondary">激活码: </span>' + data.result + '<br/>')
                                $('#query-result-text').append('<span class="am-text-danger">该激活码未激活 </span>'+'<br/>')
                            }
                        } else {
                            $('#query-result-text').append('该激活码ID无效'+'<br/>')
                        }
                        $('#query-result').modal({
                            relatedTarget: this
                        })
                        
                    }
                })
            },
        });
    });
});