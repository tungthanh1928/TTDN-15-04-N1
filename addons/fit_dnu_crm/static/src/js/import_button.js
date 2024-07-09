odoo.define('fit_dnu_crm.import_custom', function (require) {
    "use strict";
    var ListController = require("web.ListController");
    var includeDict = {
        renderButtons: function () {
            this._super.apply(this, arguments);
            var self = this;
            self.$buttons.on('click', '.import-student-absent', function () {
                self._rpc({
                    route: '/web/action/load',
                    params: {
                        action_id: 'fit_dnu_crm.action_student_absent_import_wizard',
                    },
                })
                    .then(function (r) {
                        console.log(r);
                        return self.do_action(r);
                    });
            });

            
            self.$buttons.on('click', '.import-student-tuition-fee', function () {
                self._rpc({
                    route: '/web/action/load',
                    params: {
                        action_id: 'fit_dnu_crm.action_student_tuition_fee_import_wizard',
                    },
                })
                    .then(function (r) {
                        console.log(r);
                        return self.do_action(r);
                    });
            });
        }
    };
    ListController.include(includeDict);
});

