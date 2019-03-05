$(function () {
    var $form = $('#form-with-tooltip');
    var $tooltip = $('<div id="vld-tooltip">提示信息！</div>');
    $tooltip.appendTo(document.body);

    $form.validator({
        validate: function (validity) {
            
            // 编写验证逻辑
            //Ajax验证
            //验证username
            if ($(validity.field).is('#username')) {
                return $.ajax({
                    url: '/register/registervalidate/username',
                    cache: false,
                    type: 'post',
                    data: JSON.stringify({
                        'username': $('#username').val()
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
            // 验证email
            if ($(validity.field).is('#email')) {
                return $.ajax({
                    url: '/register/registervalidate/email',
                    cache: false,
                    type: 'post',
                    data: JSON.stringify({
                        'email': $('#email').val()
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

            //password-2验证
            if ($(validity.field).is('#password-2')) {
                return $.ajax({
                    url: '/register/registervalidate/password-2',
                    cache: false,
                    type: 'post',
                    data: JSON.stringify({
                        'password-1': $('#password-1').val(),
                        'password-2': $('#password-2').val()
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

            //邀请码验证
            if ($(validity.field).is('#invitecode')) {
                return $.ajax({
                    url: '/register/registervalidate/invitecode',
                    cache: false,
                    type: 'post',
                    data: JSON.stringify({
                        'invitecode': $('#invitecode').val()
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