window.core = {
  IS_LOGO_LINK_ACTIVE: true
};

(function ($) {
    window.core.Request = {
        send: function(method, url, options) {
            opts = {
                script: true,
                data: '',
                target: '',
                load: '',
                callback: null
            }
            var options = $.extend(opts, options);
            var request = $.ajax({
                evalScripts: options.script,
                url: url,
                method: method,
                data: options.data,
            }).done(function (responseHTML, result) {
                if(options.target) {
                    $(options.target).html(responseHTML);
                }
                if(options.callback) {
                    options.callback.call(this, responseHTML, responseJavaScript);
                }
            });
        }
    };

    window.core.Modal = function(params) {

        var opts = {
            hideActions: false,
            showActionBtn: false,
            actionBtnLabel: 'salva <i class="checkmark icon"></i>',
            actionBtnCallback: function () {},
            onUrlLoaded: function() {},
            size: 'small',
            onHide: function () {},
            closable: true,
            autofocus: true,
            basic: false
        }

        this.init = function(params) {
            this.isOpen = false;
            this.modal = $('#dynamic-modal');
            this.reset(params);
            this.update(params);
        };

        this.update = function (params) {
            this.options = $.extend({}, opts, params);
            this.setSize();
            this.setTitle();
            this.setContent();
            this.setButtons();
        }

        this.reset = function () {
            if (params.basic) {
                this.modal.addClass('basic');
            } else {
                this.modal.removeClass('basic');
            }
            this.modal.find('.modal-dialog').attr('class', 'modal-dialog');
            this.modal.find('.modal-footer').show();
            this.modal.find('.btn-action').show();
            this.modal.find('.btn-action').off('click');
        }

        this.setSize = function() {
            this.modal.removeClass('mini small medium big huge');
            this.modal.addClass(this.options.size);
        };

        this.setTitle = function() {
            if(typeof this.options.title != 'undefined') {
                this.modal.find('.modal-title').html(this.options.title);
            }
        };

        this.setContent = function() {
            var self = this;
            if(typeof this.options.url != 'undefined') {
                this.method = 'request';
                $.get(this.options.url, function(response) {
                    self.modal.find('.modal-body').html(response);
                    self.options.onUrlLoaded(self);
                    // if IE (parent has legacy class, then adjust position)
                    if (self.modal.parent().hasClass('legacy')) {
                        setTimeout(function () {
                          console.log('adjusting vertical position for IE', 'height: ', self.modal.height());
                          self.modal.css('margin-top', -(parseInt(self.modal.height() / 2) + 10) + 'px');
                          console.log('adjusting horizontal position for IE', 'width: ', self.modal.width());
                          self.modal.css('margin-left', -parseInt(self.modal.width() / 2) + 'px');
                        }, 50);
                    }
                })
            }
            else if(typeof this.options.content != 'undefined') {
                self.modal.find('.modal-body').html(this.options.content);
            }
        };

        this.updateContent = function (html) {
            this.modal.find('.modal-body').html(html);
        };

        this.setButtons = function() {
            if (this.options.hideActions) {
                this.modal.find('.modal-footer').hide();
            } else {
                if(typeof this.options.showActionBtn != 'undefined' && this.options.showActionBtn ) {
                    this.modal.find('.positive.right.icon').html(this.options.actionBtnLabel);
                }
                else {
                    this.modal.find('.positive.right.icon').hide();
                }
            }
        };

        this.open = function() {
            if (this.isOpen) {
                return;
            }
            var self = this;
            if (this.options.actionBtnCallback) {
                this.modal.modal({
                    closable: false,
                    autofocus: this.options.autofocus,
                    onApprove: this.options.actionBtnCallback,
                    onHide: function () {
                        self.modal.find('.modal-body').empty();
                        self.isOpen = false;
                    }
                }).modal('show');
            } else {
                console.log('SHOWING')
                this.modal.modal({
                    autofocus: this.options.autofocus,
                    onHide: function () { self.isOpen = false; }
                }).modal('show');
            }
            this.isOpen = true;

            // if IE (parent has legacy class, then adjust position)
            if (self.modal.parent().hasClass('legacy')) {
              setTimeout(function () {
                console.log('adjusting vertical position for IE', 'height: ', self.modal[0].clientHeight);
                self.modal.css('margin-top', -(parseInt(self.modal[0].clientHeight / 2) + 10) + 'px');
                console.log('adjusting horizontal position for IE', 'width: ', self.modal[0].clientWidth);
                self.modal.css('margin-left', -parseInt(self.modal[0].clientWidth / 2) + 'px');
              }, 100);
            }
        };

        this.hide = function () {
            this.isOpen = false;
            this.modal.modal('hide');
        }

        this.init(params);
        return this;
    }
})(jQuery)
