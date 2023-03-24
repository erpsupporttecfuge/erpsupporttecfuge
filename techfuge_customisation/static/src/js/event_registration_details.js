odoo.define('techfuge_customisation.event_registration_details', function (require) {
'use strict';

    var publicWidget = require('web.public.widget');
    var rpc = require('web.rpc');

    publicWidget.registry.EventRegistrationDetails = publicWidget.Widget.extend({
        selector: '.event_reg_details_section',
        events: {
            'click #btn_submit_event_reg_details': '_onClickSubmitEventRegistrationDetails',
        },

        _onClickSubmitEventRegistrationDetails: function (ev) {
            var activity_location = $("#attendee_activity_location").val();
            var exhibitor_name = $("#exhibitor_name").val();
            if (!activity_location && !exhibitor_name) {
                alert("Please select either location or exhibitor");
                return false;
            }
        },

    });

});
