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
describe('watchdog-test.md', function () {
    beforeEach(before_and_after_1.beforeFromFile('watchdog-manage.md'));
    afterEach(before_and_after_1.after());
    it('should update file on changes', function () {
        var createButton = protractor_1.element(protractor_1.by.css('.create-watchdog-test button'));
        protractor_1.browser.wait(protractor_1.ExpectedConditions.elementToBeClickable(createButton));
        createButton.click();
        var nextPage = protractor_1.element(protractor_1.by.css('.click-me a'));
        before_and_after_1.waitForSpinner();
        protractor_1.browser.wait(protractor_1.ExpectedConditions.elementToBeClickable(nextPage));
        nextPage.click();
        var writeInMe = protractor_1.element(protractor_1.by.css('.write-in-me textarea'));
        protractor_1.browser.wait(protractor_1.ExpectedConditions.presenceOf(writeInMe));
        before_and_after_1.waitForSpinner();
        var testTextHeading = "Prepended Heading!";
        writeInMe.sendKeys("# " + testTextHeading);
        before_and_after_1.waitForSpinner();
        var prependButton = protractor_1.element(protractor_1.by.css('.prepend-string-contents button'));
        prependButton.click();
        var newHeader = protractor_1.element(protractor_1.by.tagName('h1'));
        protractor_1.browser.wait(protractor_1.ExpectedConditions.presenceOf(newHeader));
        expect(newHeader.getText()).toEqual(testTextHeading);
        before_and_after_1.waitForSpinner();
        protractor_1.browser.wait(protractor_1.ExpectedConditions.elementToBeClickable(nextPage));
        nextPage.click();
        var deleteButton = protractor_1.element(protractor_1.by.css('.delete-watchdog-test button'));
        protractor_1.browser.wait(protractor_1.ExpectedConditions.presenceOf(deleteButton));
        protractor_1.browser.wait(protractor_1.ExpectedConditions.elementToBeClickable(deleteButton));
        before_and_after_1.waitForSpinner();
        deleteButton.click();
    });
});
