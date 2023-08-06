angular.module('cradminLegacy.templates', ['acemarkdown/acemarkdown.tpl.html', 'bulkfileupload/fileinfo.tpl.html', 'bulkfileupload/progress.tpl.html', 'bulkfileupload/rejectedfiles.tpl.html', 'forms/dateselector.tpl.html', 'pagepreview/navbar.tpl.html']);

angular.module("acemarkdown/acemarkdown.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("acemarkdown/acemarkdown.tpl.html",
    "<div ng-transclude></div>");
}]);

angular.module("bulkfileupload/fileinfo.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("bulkfileupload/fileinfo.tpl.html",
    "<p class=\"cradmin-legacy-bulkfileupload-progress-item\"\n" +
    "        ng-class=\"{\n" +
    "            'cradmin-legacy-bulkfileupload-progress-item-finished': fileInfo.finished,\n" +
    "            'cradmin-legacy-bulkfileupload-progress-item-error cradmin-legacy-bulkfileupload-errorparagraph': fileInfo.hasErrors\n" +
    "        }\">\n" +
    "    <button cradmin-legacy-bulkfileupload-remove-file-button=\"fileInfo\"\n" +
    "            ng-if=\"fileInfo.finished\"\n" +
    "            type=\"button\"\n" +
    "            class=\"btn btn-link cradmin-legacy-bulkfileupload-remove-file-button\">\n" +
    "        <span ng-if=\"!fileInfo.isRemoving &amp;&amp; !fileInfo.autosubmit\"\n" +
    "              class=\"cradmin-legacy-bulkfileupload-remove-file-button-isnotremoving\">\n" +
    "            <span class=\"fa fa-times\"></span>\n" +
    "            <span class=\"sr-only\">{{fileInfo.i18nStrings.remove_file_label}}</span>\n" +
    "        </span>\n" +
    "        <span ng-if=\"fileInfo.isRemoving\"\n" +
    "              class=\"cradmin-legacy-bulkfileupload-remove-file-button-isremoving\">\n" +
    "            <span class=\"fa fa-spinner fa-spin\"></span>\n" +
    "            <span class=\"sr-only\">{{fileInfo.i18nStrings.removing_file_message}}</span>\n" +
    "        </span>\n" +
    "    </button>\n" +
    "\n" +
    "    <span class=\"cradmin-legacy-progressbar\">\n" +
    "        <span class=\"cradmin-legacy-progressbar-progress\" ng-style=\"{'width': fileInfo.percent+'%'}\">&nbsp;</span>\n" +
    "        <span class=\"cradmin-legacy-progresspercent\">\n" +
    "            <span class=\"cradmin-legacy-progresspercent-number\">{{ fileInfo.percent }}</span>%\n" +
    "        </span>\n" +
    "    </span>\n" +
    "    <span class=\"cradmin-legacy-filename\">{{fileInfo.name}}</span>\n" +
    "</p>\n" +
    "");
}]);

angular.module("bulkfileupload/progress.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("bulkfileupload/progress.tpl.html",
    "<div class=\"cradmin-legacy-bulkfileupload-progress\">\n" +
    "    <div ng-repeat=\"fileInfo in fileInfoArray\">\n" +
    "        <div cradmin-legacy-bulk-file-info=\"fileInfo\"\n" +
    "             class=\"cradmin-legacy-bulkfileupload-progress-file\"></div>\n" +
    "    </div>\n" +
    "</div>\n" +
    "");
}]);

angular.module("bulkfileupload/rejectedfiles.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("bulkfileupload/rejectedfiles.tpl.html",
    "<div class=\"cradmin-legacy-bulkfileupload-rejectedfiles\">\n" +
    "    <p ng-repeat=\"fileInfo in rejectedFiles\"\n" +
    "            class=\"cradmin-legacy-bulkfileupload-rejectedfile cradmin-legacy-bulkfileupload-errorparagraph\">\n" +
    "        <button ng-click=\"closeMessage(fileInfo)\"\n" +
    "                type=\"button\"\n" +
    "                class=\"btn btn-link cradmin-legacy-bulkfileupload-error-closebutton\">\n" +
    "            <span class=\"fa fa-times\"></span>\n" +
    "            <span class=\"sr-only\">{{fileInfo.i18nStrings.close_errormessage_label}}</span>\n" +
    "        </button>\n" +
    "\n" +
    "        <span class=\"cradmin-legacy-bulkfileupload-rejectedfile-filename\">{{ fileInfo.name }}:</span>\n" +
    "        <span ng-repeat=\"(errorfield,errors) in fileInfo.errors\">\n" +
    "            <span ng-repeat=\"error in errors\"\n" +
    "                  class=\"cradmin-legacy-bulkfileupload-error\">\n" +
    "                {{ error.message }}\n" +
    "            </span>\n" +
    "        </span>\n" +
    "    </p>\n" +
    "</div>\n" +
    "");
}]);

angular.module("forms/dateselector.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("forms/dateselector.tpl.html",
    "<div class=\"cradmin-legacy-datetime-selector\"\n" +
    "        ng-class=\"{\n" +
    "            'cradmin-legacy-datetime-selector-show': page != null,\n" +
    "            'cradmin-legacy-datetime-selector-page1': page == 1,\n" +
    "            'cradmin-legacy-datetime-selector-page2': page == 2,\n" +
    "            'cradmin-legacy-datetime-selector-page3': page == 3,\n" +
    "            'cradmin-legacy-datetime-selector-has-shortcuts': hasShortcuts()\n" +
    "        }\">\n" +
    "\n" +
    "    <div class=\"cradmin-legacy-datetime-selector-backdrop\"></div>\n" +
    "\n" +
    "    <div class=\"cradmin-legacy-datetime-selector-contentwrapper\">\n" +
    "        <div class=\"cradmin-legacy-datetime-selector-closeoverlay\" ng-click=\"hide()\"></div>\n" +
    "        <div class=\"cradmin-legacy-datetime-selector-page cradmin-legacy-datetime-selector-dateview\">\n" +
    "            <button type=\"button\" class=\"sr-only\" ng-focus=\"onFocusHead()\"></button>\n" +
    "            <button type=\"button\"\n" +
    "                    class=\"btn btn-link cradmin-legacy-datetime-selector-closebutton\"\n" +
    "                    aria-label=\"{{ config.close_screenreader_text }}\"\n" +
    "                    ng-click=\"hide()\">\n" +
    "                        <span class=\"{{ config.close_icon }}\" aria-hidden=\"true\"></span>\n" +
    "                    </button>\n" +
    "\n" +
    "            <div class=\"cradmin-legacy-datetime-selector-selectors-wrapper\">\n" +
    "                <div class=\"cradmin-legacy-datetime-selector-selectors\">\n" +
    "                    <div class=\"cradmin-legacy-datetime-selector-dateselectors\">\n" +
    "                        <label class=\"cradmin-legacy-datetime-selector-date-label\" ng-if=\"config.date_label_text\">\n" +
    "                            {{ config.date_label_text }}\n" +
    "                        </label>\n" +
    "                        <label for=\"{{ config.destinationfieldid }}_dayselect\" class=\"sr-only\">\n" +
    "                            {{ config.day_screenreader_text }}\n" +
    "                        </label>\n" +
    "                        <select id=\"{{ config.destinationfieldid }}_dayselect\"\n" +
    "                                class=\"form-control cradmin-legacy-datetime-selector-dayselect\"\n" +
    "                                ng-model=\"monthlyCalendarCoordinator.currentDayObject\"\n" +
    "                                ng-options=\"dayobject.label for dayobject in monthlyCalendarCoordinator.dayobjects track by dayobject.value\"\n" +
    "                                ng-change=\"onSelectDayNumber()\">\n" +
    "                        </select>\n" +
    "\n" +
    "                        <label for=\"{{ config.destinationfieldid }}_monthselect\" class=\"sr-only\">\n" +
    "                            {{ config.month_screenreader_text }}\n" +
    "                        </label>\n" +
    "                        <select id=\"{{ config.destinationfieldid }}_monthselect\"\n" +
    "                                class=\"form-control cradmin-legacy-datetime-selector-monthselect\"\n" +
    "                                ng-model=\"monthlyCalendarCoordinator.currentMonthObject\"\n" +
    "                                ng-options=\"monthobject.label for monthobject in monthlyCalendarCoordinator.monthselectConfig track by monthobject.value\"\n" +
    "                                ng-change=\"onSelectMonth()\">\n" +
    "                        </select>\n" +
    "\n" +
    "                        <label for=\"{{ config.destinationfieldid }}_yearselect\" class=\"sr-only\">\n" +
    "                            {{ config.year_screenreader_text }}\n" +
    "                        </label>\n" +
    "                        <select id=\"{{ config.destinationfieldid }}_yearselect\"\n" +
    "                                class=\"form-control cradmin-legacy-datetime-selector-yearselect\"\n" +
    "                                ng-model=\"monthlyCalendarCoordinator.currentYearObject\"\n" +
    "                                ng-options=\"yearobject.label for yearobject in monthlyCalendarCoordinator.yearselectConfig track by yearobject.value\"\n" +
    "                                ng-change=\"onSelectYear()\">\n" +
    "                        </select>\n" +
    "                    </div>\n" +
    "\n" +
    "                    <div class=\"cradmin-legacy-datetime-selector-timeselectors\" ng-if=\"config.include_time\">\n" +
    "                        <label class=\"cradmin-legacy-datetime-selector-time-label\" ng-if=\"config.time_label_text\">\n" +
    "                            {{ config.time_label_text }}\n" +
    "                        </label>\n" +
    "                        <label for=\"{{ config.destinationfieldid }}_hourselect\" class=\"sr-only\">\n" +
    "                            {{ config.hour_screenreader_text }}\n" +
    "                        </label>\n" +
    "                        <select id=\"{{ config.destinationfieldid }}_hourselect\"\n" +
    "                                class=\"form-control cradmin-legacy-datetime-selector-hourselect\"\n" +
    "                                ng-model=\"monthlyCalendarCoordinator.currentHourObject\"\n" +
    "                                ng-options=\"hourobject.label for hourobject in monthlyCalendarCoordinator.hourselectConfig track by hourobject.value\"\n" +
    "                                ng-change=\"onSelectHour()\">\n" +
    "                        </select>\n" +
    "                        :\n" +
    "                        <label for=\"{{ config.destinationfieldid }}_minuteselect\" class=\"sr-only\">\n" +
    "                            {{ config.minute_screenreader_text }}\n" +
    "                        </label>\n" +
    "                        <select id=\"{{ config.destinationfieldid }}_minuteselect\"\n" +
    "                                class=\"form-control cradmin-legacy-datetime-selector-minuteselect\"\n" +
    "                                ng-model=\"monthlyCalendarCoordinator.currentMinuteObject\"\n" +
    "                                ng-options=\"minuteobject.label for minuteobject in monthlyCalendarCoordinator.minuteselectConfig track by minuteobject.value\"\n" +
    "                                ng-change=\"onSelectMinute()\">\n" +
    "                        </select>\n" +
    "                    </div>\n" +
    "\n" +
    "                    <button type=\"button\"\n" +
    "                            class=\"btn btn-primary cradmin-legacy-datetime-selector-use-button\"\n" +
    "                            ng-click=\"onClickUseTime()\"\n" +
    "                            aria-label=\"{{ getUseButtonAriaLabel() }}\">\n" +
    "                        {{ config.usebuttonlabel }}\n" +
    "                    </button>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "\n" +
    "            <table class=\"cradmin-legacy-datetime-selector-table\">\n" +
    "                <caption class=\"sr-only\">\n" +
    "                    {{ config.dateselector_table_screenreader_caption }}\n" +
    "                </caption>\n" +
    "                <thead>\n" +
    "                    <tr>\n" +
    "                        <th ng-repeat=\"weekday in monthlyCalendarCoordinator.shortWeekdays\">\n" +
    "                            {{ weekday }}\n" +
    "                        </th>\n" +
    "                    </tr>\n" +
    "                </thead>\n" +
    "                <tbody>\n" +
    "                    <tr ng-repeat=\"calendarWeek in monthlyCalendarCoordinator.calendarMonth.calendarWeeks\">\n" +
    "                        <td ng-repeat=\"calendarDay in calendarWeek.calendarDays\"\n" +
    "                                class=\"cradmin-legacy-datetime-selector-daybuttoncell\"\n" +
    "                                ng-class=\"{\n" +
    "                                    'cradmin-legacy-datetime-selector-daybuttoncell-not-in-current-month': !calendarDay.isInCurrentMonth,\n" +
    "                                    'cradmin-legacy-datetime-selector-daybuttoncell-in-current-month': calendarDay.isInCurrentMonth,\n" +
    "                                    'cradmin-legacy-datetime-selector-daybuttoncell-selected': calendarDay.momentObject.isSame(calendarCoordinator.selectedMomentObject, 'day'),\n" +
    "                                    'cradmin-legacy-datetime-selector-daybuttoncell-lastfocused': calendarDay.momentObject.isSame(monthlyCalendarCoordinator.getLastFocusedMomentObject(), 'day'),\n" +
    "                                    'cradmin-legacy-datetime-selector-daybuttoncell-today': calendarDay.isToday(),\n" +
    "                                    'cradmin-legacy-datetime-selector-daybuttoncell-disabled': calendarDay.isDisabled()\n" +
    "                                }\">\n" +
    "                            <button type=\"button\" class=\"btn btn-link cradmin-legacy-datetime-selector-daybuttoncell-button\"\n" +
    "                                    ng-click=\"onClickCalendarDay(calendarDay)\"\n" +
    "                                    tabindex=\"{{ getTabindexForCalendarDay(calendarDay) }}\"\n" +
    "                                    ng-focus=\"onFocusCalendayDay(calendarDay)\"\n" +
    "                                    aria-label=\"{{ getDaybuttonAriaLabel(calendarDay) }}\"\n" +
    "                                    ng-disabled=\"{{ calendarDay.isDisabled() }}\">\n" +
    "                                {{ monthlyCalendarCoordinator.getDayOfMonthLabelForTableCell(calendarDay) }}\n" +
    "                                <span class=\"cradmin-legacy-datetime-selector-daybuttoncell-label\n" +
    "                                             cradmin-legacy-datetime-selector-daybuttoncell-label-today\"\n" +
    "                                        ng-if=\"config.today_label_text &amp;&amp; calendarDay.isToday()\">\n" +
    "                                    {{ config.today_label_text }}\n" +
    "                                </span>\n" +
    "                                <span class=\"cradmin-legacy-datetime-selector-daybuttoncell-label\n" +
    "                                             cradmin-legacy-datetime-selector-daybuttoncell-label-selected\"\n" +
    "                                        ng-if=\"\n" +
    "                                            config.selected_day_label_text &amp;&amp;\n" +
    "                                            calendarDay.momentObject.isSame(calendarCoordinator.selectedMomentObject, 'day')\">\n" +
    "                                    {{ config.selected_day_label_text }}\n" +
    "                                </span>\n" +
    "                            </button>\n" +
    "                        </td>\n" +
    "                    </tr>\n" +
    "                </tbody>\n" +
    "            </table>\n" +
    "\n" +
    "            <div class=\"cradmin-legacy-datetime-selector-shortcuts\" ng-if=\"hasShortcuts()\">\n" +
    "                <button type=\"button\"\n" +
    "                        class=\"btn btn-default cradmin-legacy-datetime-selector-shortcuts-todaybutton\"\n" +
    "                        ng-if=\"calendarCoordinator.todayIsValidValue()\"\n" +
    "                        ng-click=\"onClickTodayButton()\">\n" +
    "                    {{ config.today_button_text }}\n" +
    "                </button>\n" +
    "                <button type=\"button\"\n" +
    "                        class=\"btn btn-default cradmin-legacy-datetime-selector-shortcuts-nowbutton\"\n" +
    "                        ng-if=\"calendarCoordinator.nowIsValidValue()\"\n" +
    "                        ng-click=\"onClickNowButton()\">\n" +
    "                    {{ config.now_button_text }}\n" +
    "                </button>\n" +
    "                <button type=\"button\"\n" +
    "                        class=\"btn btn-danger cradmin-legacy-datetime-selector-shortcuts-clearbutton\"\n" +
    "                        ng-if=\"!config.required\"\n" +
    "                        ng-click=\"onClickClearButton()\">\n" +
    "                    {{ config.clear_button_text }}\n" +
    "                </button>\n" +
    "            </div>\n" +
    "\n" +
    "            <button type=\"button\" class=\"sr-only\" ng-focus=\"onFocusTail()\"></button>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"cradmin-legacy-datetime-selector-page cradmin-legacy-datetime-selector-timeview\">\n" +
    "            <button type=\"button\" class=\"sr-only\" ng-focus=\"onFocusHead()\"></button>\n" +
    "            <button type=\"button\"\n" +
    "                    class=\"btn btn-link cradmin-legacy-datetime-selector-closebutton\"\n" +
    "                    aria-label=\"{{ config.close_screenreader_text }}\"\n" +
    "                    ng-click=\"hide()\">\n" +
    "                        <span class=\"{{ config.close_icon }}\" aria-hidden=\"true\"></span>\n" +
    "                    </button>\n" +
    "\n" +
    "            <button type=\"button\"\n" +
    "                    class=\"btn btn-link cradmin-legacy-datetime-selector-backbutton\"\n" +
    "                    tabindex=\"0\"\n" +
    "                    aria-label=\"{{ config.back_to_datepicker_screenreader_text }}\"\n" +
    "                    ng-click=\"showPage1()\">\n" +
    "                <span class=\"cradmin-legacy-datetime-selector-backbutton-icon-outer-wrapper\">\n" +
    "                    <span class=\"cradmin-legacy-datetime-selector-backbutton-icon-inner-wrapper\">\n" +
    "                        <span class=\"cradmin-legacy-datetime-selector-backbutton-icon {{ config.back_icon }}\"></span>\n" +
    "                    </span>\n" +
    "                </span>\n" +
    "            </button>\n" +
    "\n" +
    "            <div class=\"cradmin-legacy-datetime-selector-timeview-body-wrapper\">\n" +
    "                <div class=\"cradmin-legacy-datetime-selector-timeview-body\">\n" +
    "                    <p class=\"cradmin-legacy-datetime-selector-datepreview\">\n" +
    "                        {{ getTimeselectorDatepreview() }}\n" +
    "                    </p>\n" +
    "                    <div class=\"cradmin-legacy-datetime-selector-timeselectors\">\n" +
    "                        <form class=\"form-inline\">\n" +
    "                            <label class=\"cradmin-legacy-datetime-selector-time-label\" ng-if=\"config.time_label_text\">\n" +
    "                                {{ config.time_label_text }}\n" +
    "                            </label>\n" +
    "                            <label for=\"{{ config.destinationfieldid }}_hourselect_page2\" class=\"sr-only\">\n" +
    "                                {{ config.hour_screenreader_text }}\n" +
    "                            </label>\n" +
    "                            <select id=\"{{ config.destinationfieldid }}_hourselect_page2\"\n" +
    "                                    class=\"form-control cradmin-legacy-datetime-selector-hourselect\"\n" +
    "                                    ng-model=\"monthlyCalendarCoordinator.currentHourObject\"\n" +
    "                                    ng-options=\"hourobject.label for hourobject in monthlyCalendarCoordinator.hourselectConfig track by hourobject.value\"\n" +
    "                                    ng-change=\"onSelectHour()\">\n" +
    "                            </select>\n" +
    "                            :\n" +
    "                            <label for=\"{{ config.destinationfieldid }}_minuteselect_page2\" class=\"sr-only\">\n" +
    "                                {{ config.minute_screenreader_text }}\n" +
    "                            </label>\n" +
    "                            <select id=\"{{ config.destinationfieldid }}_minuteselect_page2\"\n" +
    "                                    class=\"form-control cradmin-legacy-datetime-selector-minuteselect\"\n" +
    "                                    ng-model=\"monthlyCalendarCoordinator.currentMinuteObject\"\n" +
    "                                    ng-options=\"minuteobject.label for minuteobject in monthlyCalendarCoordinator.minuteselectConfig track by minuteobject.value\"\n" +
    "                                    ng-change=\"onSelectMinute()\">\n" +
    "                            </select>\n" +
    "                            <button type=\"button\"\n" +
    "                                    class=\"btn btn-primary cradmin-legacy-datetime-selector-use-button\"\n" +
    "                                    ng-click=\"onClickUseTime()\"\n" +
    "                                    aria-label=\"{{ getUseButtonAriaLabel() }}\">\n" +
    "                                {{ config.usebuttonlabel }}\n" +
    "                            </button>\n" +
    "                        </form>\n" +
    "                    </div>\n" +
    "\n" +
    "                </div>\n" +
    "\n" +
    "                <div class=\"cradmin-legacy-datetime-selector-shortcuts\" ng-if=\"hasShortcuts()\">\n" +
    "                    <button type=\"button\"\n" +
    "                            class=\"btn btn-default cradmin-legacy-datetime-selector-shortcuts-nowbutton\"\n" +
    "                            ng-click=\"onClickNowButton()\"\n" +
    "                            ng-if=\"calendarCoordinator.shownDateIsTodayAndNowIsValid()\">\n" +
    "                        {{ config.now_button_text }}\n" +
    "                    </button>\n" +
    "                </div>\n" +
    "\n" +
    "            </div>\n" +
    "\n" +
    "\n" +
    "            <button type=\"button\" class=\"sr-only\" ng-focus=\"onFocusTail()\"></button>\n" +
    "        </div>\n" +
    "    </div>\n" +
    "</div>\n" +
    "");
}]);

angular.module("pagepreview/navbar.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("pagepreview/navbar.tpl.html",
    "<nav cradmin-legacy-menu class=\"cradmin-legacy-menu\">\n" +
    "    <div class=\"cradmin-legacy-menu-mobileheader\">\n" +
    "        <a href=\"#\" role=\"button\"\n" +
    "           class=\"cradmin-legacy-menu-mobiletoggle\"\n" +
    "           ng-click=\"cradminMenuTogglePressed()\"\n" +
    "           ng-class=\"{'cradmin-legacy-menu-mobile-toggle-button-expanded': cradminMenuDisplay}\"\n" +
    "           aria-pressed=\"{{ getAriaPressed() }}\">\n" +
    "                {{ mobileMenuHeader }}\n" +
    "        </a>\n" +
    "    </div>\n" +
    "    <div class=\"cradmin-legacy-menu-content\"\n" +
    "             ng-class=\"{'cradmin-legacy-menu-content-display': cradminMenuDisplay}\">\n" +
    "        <ul class=\"cradmin-legacy-menu-content-main\">\n" +
    "            <li ng-repeat=\"urlConfig in previewConfig.urls\"\n" +
    "                    class=\"cradmin-legacy-menu-item {{urlConfig.css_classes}}\"\n" +
    "                    ng-class=\"{\n" +
    "                        'cradmin-legacy-menu-activeitem': $index == activeIndex\n" +
    "                    }\">\n" +
    "                <a href=\"{{ urlConfig.url }}\"\n" +
    "                        cradmin-legacy-menu-close-on-click\n" +
    "                        ng-click=\"onNavlinkClick($event, $index)\">\n" +
    "                    {{urlConfig.label}}\n" +
    "                </a>\n" +
    "            </li>\n" +
    "        </ul>\n" +
    "        <ul class=\"cradmin-legacy-menu-content-footer\">\n" +
    "            <li>\n" +
    "                <a href=\"{{ activeUrlConfig.url }}\" target=\"_blank\">\n" +
    "                    {{ activeUrlConfig.open_label }}\n" +
    "                </a>\n" +
    "            </li>\n" +
    "        </ul>\n" +
    "    </div>\n" +
    "</nav>\n" +
    "");
}]);
