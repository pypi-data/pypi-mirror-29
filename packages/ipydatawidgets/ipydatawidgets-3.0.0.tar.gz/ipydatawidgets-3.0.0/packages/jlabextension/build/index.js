"use strict";
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", { value: true });
var coreutils_1 = require("@phosphor/coreutils");
var dataWidgets = require("jupyter-datawidgets");
var base_1 = require("@jupyter-widgets/base");
var EXTENSION_ID = 'jupyter.extensions.datawidgets';
/**
 * The token identifying the JupyterLab plugin.
 */
exports.IDataWidgetsExtension = new coreutils_1.Token(EXTENSION_ID);
;
/**
 * The notebook diff provider.
 */
var dataWidgetsProvider = {
    id: EXTENSION_ID,
    requires: [base_1.IJupyterWidgetRegistry],
    activate: activateWidgetExtension,
    autoStart: true
};
exports.default = dataWidgetsProvider;
/**
 * Activate the widget extension.
 */
function activateWidgetExtension(app, widgetsManager) {
    widgetsManager.registerWidget({
        name: 'jupyter-datawidgets',
        version: dataWidgets.EXTENSION_SPEC_VERSION,
        exports: dataWidgets
    });
    return {};
}
//# sourceMappingURL=index.js.map