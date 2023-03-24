odoo.define('techfuge_customisation.exhibitor_dashboard', function (require) {
'use strict';

    var publicWidget = require('web.public.widget');
    var rpc = require('web.rpc');


    publicWidget.registry.PlannerDashboard = publicWidget.Widget.extend({
        selector: '.dashboard',
        events: {
            'click #btn_clear_all': '_onClickClearAllData',
        },

        start: function () {
            document.querySelectorAll('nav.dashboard-nav-list > a').forEach((nav) => {
                var navPathname = nav.pathname;
                var windowLocationPathname = window.location.pathname;
                if (navPathname === windowLocationPathname) {
                    nav.classList.add('active')
                } else {
                    nav.classList.remove('active')
                }
            })
            return this._super.apply(this, arguments);
        },

        _onClickClearAllData: function (ev) {
              document.getElementById("attendee_badge_request_form").reset();
        },

    });

});


const mobileScreen = window.matchMedia("(max-width: 990px )");
$(document).ready(function () {

    console.log('window.location.href::::::::::::',window.location.pathname);
    if (window.location.pathname === '/exhibitor_dashboard') {
        $('.dashboard-toolbar').css('left', '0px');
    }

    $(".dashboard-nav-dropdown-toggle").click(function () {
        $(this).closest(".dashboard-nav-dropdown")
            .toggleClass("show")
            .find(".dashboard-nav-dropdown")
            .removeClass("show");
        $(this).parent()
            .siblings()
            .removeClass("show");
    });
    $(".menu-toggle").click(function () {
        if (mobileScreen.matches) {
            $(".dashboard-nav").toggleClass("mobile-show");
        } else {
            $(".dashboard").toggleClass("dashboard-compact");
        }
    });
});
