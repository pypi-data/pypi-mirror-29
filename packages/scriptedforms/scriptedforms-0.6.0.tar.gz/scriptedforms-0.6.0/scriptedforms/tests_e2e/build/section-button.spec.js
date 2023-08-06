"use strict";
// Scripted Forms -- Making GUIs easy for everyone on your team.
// Copyright (C) 2017 Simon Biggs
Object.defineProperty(exports, "__esModule", { value: true });
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published
// by the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version (the "AGPL-3.0+").
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU Affero General Public License and the additional terms for more
// details.
// You should have received a copy of the GNU Affero General Public License
// along with this program. If not, see <http://www.gnu.org/licenses/>.
// ADDITIONAL TERMS are also included as allowed by Section 7 of the GNU
// Affrero General Public License. These aditional terms are Sections 1, 5,
// 6, 7, 8, and 9 from the Apache License, Version 2.0 (the "Apache-2.0")
// where all references to the definition "License" are instead defined to
// mean the AGPL-3.0+.
// You should have received a copy of the Apache-2.0 along with this
// program. If not, see <http://www.apache.org/licenses/LICENSE-2.0>.
var protractor_1 = require("protractor");
var before_and_after_1 = require("./utilities/before-and-after");
var TEMPLATE_FILE = 'section-button.md';
describe(TEMPLATE_FILE, function () {
    beforeEach(before_and_after_1.beforeFromFile(TEMPLATE_FILE));
    afterEach(before_and_after_1.after());
    it('should run on click', function () {
        var runningButton = protractor_1.element(protractor_1.by.css('.check-my-running button'));
        protractor_1.browser.wait(protractor_1.ExpectedConditions.elementToBeClickable(runningButton));
        var initialOutput = protractor_1.element.all(protractor_1.by.css('.check-my-running .jp-OutputArea-output'));
        expect(initialOutput.count()).toEqual(0);
        runningButton.click();
        var outputArea = protractor_1.element(protractor_1.by.css('.check-my-running .jp-OutputArea-output'));
        protractor_1.browser.wait(protractor_1.ExpectedConditions.presenceOf(outputArea));
        var text = protractor_1.element(protractor_1.by.tagName('h1')).getText();
        expect(text).toEqual('Hello');
    });
    it('should be able to be named', function () {
        var namedButtonLabel = protractor_1.element(protractor_1.by.css('.check-my-name button span'));
        expect(namedButtonLabel.getText()).toEqual('foo');
    });
    it('should honour conditional', function () {
        var disableButton = protractor_1.element(protractor_1.by.css('.make-false button'));
        var enableButton = protractor_1.element(protractor_1.by.css('.make-true button'));
        protractor_1.browser.wait(protractor_1.ExpectedConditions.elementToBeClickable(disableButton));
        protractor_1.browser.wait(protractor_1.ExpectedConditions.elementToBeClickable(enableButton));
        var conditionalButton = protractor_1.element(protractor_1.by.css('.check-my-conditional button'));
        expect(conditionalButton.isEnabled()).toBe(false);
        enableButton.click();
        before_and_after_1.waitForSpinner();
        expect(conditionalButton.isEnabled()).toBe(true);
        disableButton.click();
        before_and_after_1.waitForSpinner();
        expect(conditionalButton.isEnabled()).toBe(false);
    });
});
