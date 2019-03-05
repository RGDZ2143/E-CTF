$(function () {
    var $form = $('#form-with-tooltip');
    var $tooltip = $('<div id="vld-tooltip">提示信息！</div>');
    $tooltip.appendTo(document.body);

    $form.validator({
        validate: function (validity) {
            // 编写验证逻辑
            //用户名验证
            if ($(validity.field).is('#login-username')) {
                return $.ajax({
                    url: '/login/loginvalidate/username',
                    cache: false,
                    type: 'post',
                    data: JSON.stringify({
                        'username': $('#login-username').val()
                    }),
                    dataType: 'json'
                }).then(function (data) {
                    //请求成功，返回验证信息
                    if (data == true) {
                        validity.valid = true
                    }
                    else {
                        validity.valid = false
                    }
                    return validity;
                }, function () {
                        validity.valid = false;
                        return validity;
                }
                )
            }

            //登录页面密码验证
            if ($(validity.field).is('#login-userpass')) {
                return $.ajax({
                    url: '/login/loginvalidate/userpass',
                    cache: false,
                    type: 'post',
                    data: JSON.stringify({
                        'username': $('#login-username').val(),
                        'userpass': $('#login-userpass').val()
                    }),
                    dataType: 'json'
                }).then(function (data) {
                    //请求成功，返回验证信息
                    if (data == true) {
                        validity.valid = true
                    }
                    else {
                        validity.valid = false
                    }
                    return validity;
                }, function () {
                        validity.valid = false;
                        return validity;
                }
                )
            }
        }
    });

    var validator = $form.data('amui.validator');

    $form.on('focusin focusout', '.am-form-error input', function (e) {
        if (e.type === 'focusin') {
            var $this = $(this);
            var offset = $this.offset();
            var msg = $this.data('foolishMsg') || validator.getValidationMessage($this.data('validity'));

            $tooltip.text(msg).show().css({
                left: offset.left + 10,
                top: offset.top + $(this).outerHeight() + 10
            });
        } else {
            $tooltip.hide();
        }
    });
});
