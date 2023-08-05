window.PCART = {
    '_signals_listeners': {},
    'success_notification': function (value) { console.log("Success: " + value); },
    'error_notification': function (value) { console.log("Error: " + value); },
    'get_cookie': function (name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },
    'get_src': function(element) {
        var src = $(element).data('src');
        var src_eval = $(element).data('src-eval');
        if(src_eval) {
            return eval(src_eval);
        } else {
            return src;
        }
    },
    'ajax_load': function(element) {
        $(element).load(window.PCART.get_src(element));
    },
    'init_actions': function() {
        $('.__action--ajax-load').each(function() {
            window.PCART.ajax_load(this);
        });

        $('body').on('click', '.__action--ajax-link', function(event) {
            var src = window.PCART.get_src(this);
            var target = $(this).data('target');
            $(target).load(src);
        });

        $('body').on('click', '.__action--link', function(event) {
            var src = window.PCART.get_src(this);
            window.location = src;
        });

        $('body').on('click', 'form.__action--ajax-submit [type="submit"][data-allow-ajax="true"]', function(event) {
            $('form.__action--ajax-submit [type="submit"][data-allow-ajax="true"]').removeData('append-to-ajax-request');
            $(this).attr('data-append-to-ajax-request', 'true');
        });

        $('body').on('click', 'form.__action--ajax-submit [type="submit"][data-disable-ajax="true"]', function(event) {
            $(this).closest('form.__action--ajax-submit').removeClass('__action--ajax-submit');
        });

        $('body').on('submit', 'form.__action--ajax-submit', function(event) {
            window.PCART.ajax_submit($(this));
            event.preventDefault();
        });

        $('body').on('change', 'form.__action--onchange-ajax-submit input, form.__action--onchange-ajax-submit select, form.__action--onchange-ajax-submit checkbox', function(event) {
            var _form = $(this).closest("form.__action--onchange-ajax-submit");
            console.log(_form);
            window.PCART.ajax_submit(_form);
            event.preventDefault();
        });

        $('.__action--ajax-load-for-event').each(function() {
            var event = $(this).data('event');
            var target = $(this).data('target');
            $('body').on(event, target, function(_this) {
                return function(event) {
                    window.PCART.ajax_load($(_this));
                }
            }(this));
        });

        $('.__action--subform-onchange-ajax-reload').each(function() {
            $(this).on('change', 'input,select,checkbox', function(_this) {
                return function(event) {
                    var post_data = Array();
                    $(_this).find('input,select,checkbox').each(function() {
                        post_data.push({name: this.name, value: this.value});
                    });

                    var src = window.PCART.get_src(_this);
                    var method = $(_this).data('subform-method');
                    var csrf_token = window.PCART.get_cookie('csrftoken');
                    if(csrf_token) {
                        post_data.push({name: 'csrfmiddlewaretoken', value: csrf_token});
                    }
                    var post_signal = $(_this).data("subform-post-signal");
                    var remove_element_sel = $(_this).data("subform-post-remove-element");

                    window.PCART.ajax_post_data(src, method, post_data, post_signal, remove_element_sel, _this);
                }
            }(this));
        });
    },
    'send_signal': function(signal) {
        // Reload ajax blocks
        $('.__action--ajax-load-for-signal[data-signal="'+signal+'"]').each(function() {
            window.PCART.ajax_load(this);
        });

        for(i in window.PCART._signals_listeners) {
            for(var k = 0; k < window.PCART._signals_listeners[i].length; k++) {
                window.PCART._signals_listeners[i][k]();
            }
        }
    },
    'subscribe_for_signal': function(signal, func) {
        if(!(signal in window.PCART._signals_listeners)) {
            window.PCART._signals_listeners[signal] = [func];
        } else {
            if(window.PCART._signals_listeners[signal].indexOf(func) === -1) {
                window.PCART._signals_listeners[signal].push(func);
            }
        }
    },
    'ajax_post_data': function(src, method, post_data, post_signal, remove_element_sel, result_container, success_notification, error_notification) {
        $.ajax(
            {
                url: src,
                type: method,
                data: post_data,
                success:function(data, textStatus, jqXHR) {
                    if(remove_element_sel) {
                        $(remove_element_sel).remove();
                    }
                    if(post_signal) {
                        window.PCART.send_signal(post_signal);
                    }

                    if(result_container) {
                        $(result_container).html(data);
                    }

                    if(success_notification) {
                        window.PCART.success_notification(success_notification);
                    }
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    if(error_notification) {
                        window.PCART.error_notification(error_notification);
                    }
                }
        });
    },
    'ajax_submit': function(form) {
        var post_data = $(form).serializeArray();
        var append_to_ajax = $(form).find('[data-append-to-ajax-request]');
        append_to_ajax.each(function() {
            post_data.push({name: this.name, value: this.value});  // add a button data
        });
        var form_url = $(form).attr("action");
        var method = $(form).attr("method");
        var post_signal = $(form).data("post-signal");
        var remove_element_sel = $(form).data("post-remove-element");
        var result_container = $(form).data("target");

        var success_notification = $(form).data("success-notification");
        var error_notification = $(form).data("error-notification");
        window.PCART.ajax_post_data(form_url, method, post_data, post_signal, remove_element_sel, result_container, success_notification, error_notification);
    },
    'ajax_send': function(data, attrs) {
        var form_url = attrs['action'];
        var method = attrs["method"] || 'post';
        var post_signal = attrs["post-signal"];
        var remove_element_sel = attrs["post-remove-element"];
        var result_container = attrs["target"];

        var success_notification = attrs["success-notification"];
        var error_notification = attrs["error-notification"];
        window.PCART.ajax_post_data(form_url, method, data, post_signal, remove_element_sel, result_container, success_notification, error_notification);
    },
}

$(document).ready(function() {
    window.PCART.init_actions();
});