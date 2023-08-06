webpackJsonp([22],{

/***/ 1443:
/***/ (function(module, exports, __webpack_require__) {

eval("var __WEBPACK_AMD_DEFINE_RESULT__;!(__WEBPACK_AMD_DEFINE_RESULT__ = function (require) {\n\n    var React = __webpack_require__(0);\n    var HomeButton = __webpack_require__(3123);\n\n    var HomeControls = React.createClass({\n        displayName: 'HomeControls',\n\n\n        render: function render() {\n            return React.DOM.div({ className: 'homeButton' }, React.createFactory(HomeButton)({ disabled: false }));\n        }\n\n    });\n\n    return HomeControls;\n}.call(exports, __webpack_require__, exports, module),\n\t\t\t\t__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));\n\n//////////////////\n// WEBPACK FOOTER\n// ./js/components/interface/home/HomeControl.js\n// module id = 1443\n// module chunks = 22\n\n//# sourceURL=webpack:///./js/components/interface/home/HomeControl.js?");

/***/ }),

/***/ 1516:
/***/ (function(module, exports, __webpack_require__) {

eval("var __WEBPACK_AMD_DEFINE_RESULT__;!(__WEBPACK_AMD_DEFINE_RESULT__ = function (require) {\n    /**\n     * Button used as part of GEPPETTO Components\n     *\n     * @mixin Button\n     */\n    var React = __webpack_require__(0);\n\n    return {\n        displayName: 'Button',\n\n        render: function render() {\n            return React.DOM.button({\n                type: 'button',\n                id: this.props.id,\n                className: 'btn ' + this.props.className + (this.props.hidden === true ? ' hiddenElement' : ''),\n                'data-toggle': this.props['data-toggle'],\n                onClick: this.props.onClick,\n                disabled: this.props.disabled,\n                icon: this.props.icon\n            }, React.DOM.i({ className: this.props.icon }), \" \" + this.props.label);\n        }\n    };\n}.call(exports, __webpack_require__, exports, module),\n\t\t\t\t__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));\n\n//////////////////\n// WEBPACK FOOTER\n// ./js/components/controls/mixins/Button.js\n// module id = 1516\n// module chunks = 6 9 22\n\n//# sourceURL=webpack:///./js/components/controls/mixins/Button.js?");

/***/ }),

/***/ 3123:
/***/ (function(module, exports, __webpack_require__) {

eval("var __WEBPACK_AMD_DEFINE_RESULT__;!(__WEBPACK_AMD_DEFINE_RESULT__ = function (require) {\n\n    var React = __webpack_require__(0),\n        GEPPETTO = __webpack_require__(84);\n\n    return React.createClass({\n        mixins: [__webpack_require__(1516)],\n\n        componentDidMount: function componentDidMount() {},\n\n        getDefaultProps: function getDefaultProps() {\n            return {\n                label: '',\n                className: 'HomeButton pull-right',\n                icon: 'fa fa-home',\n                onClick: function onClick() {\n                    var targetWindow = '_blank';\n                    if (GEPPETTO_CONFIGURATION.embedded) {\n                        targetWindow = '_self';\n                    }\n                    var win = window.open(\"./\", targetWindow);\n                    win.focus();\n                }\n            };\n        }\n\n    });\n}.call(exports, __webpack_require__, exports, module),\n\t\t\t\t__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));\n\n//////////////////\n// WEBPACK FOOTER\n// ./js/components/interface/home/HomeButton.js\n// module id = 3123\n// module chunks = 22\n\n//# sourceURL=webpack:///./js/components/interface/home/HomeButton.js?");

/***/ })

});