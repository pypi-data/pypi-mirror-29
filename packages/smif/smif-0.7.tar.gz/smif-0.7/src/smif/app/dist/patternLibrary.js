webpackJsonp([1],{

/***/ 648:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var _react = __webpack_require__(2);

var _react2 = _interopRequireDefault(_react);

var _reactDom = __webpack_require__(139);

var _patternLibrary = __webpack_require__(649);

var _patternLibrary2 = _interopRequireDefault(_patternLibrary);

__webpack_require__(254);

__webpack_require__(255);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

(0, _reactDom.render)(_react2.default.createElement(_patternLibrary2.default, null), document.getElementById('root'));

/***/ }),

/***/ 649:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
    value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _react = __webpack_require__(2);

var _react2 = _interopRequireDefault(_react);

var _trash = __webpack_require__(167);

var _trash2 = _interopRequireDefault(_trash);

__webpack_require__(650);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var PatternLibrary = function (_React$Component) {
    _inherits(PatternLibrary, _React$Component);

    function PatternLibrary() {
        _classCallCheck(this, PatternLibrary);

        return _possibleConstructorReturn(this, (PatternLibrary.__proto__ || Object.getPrototypeOf(PatternLibrary)).apply(this, arguments));
    }

    _createClass(PatternLibrary, [{
        key: 'render',

        // 'Hello World' render to style guide page
        // - should be able to visit at http://localhost:8080/style-guide.html
        //   when running the dev server (npm start)
        // - TODO move this component to a suitable directory (containers)
        // - TODO add light-touch style-guide-specific styles
        value: function render() {
            return _react2.default.createElement(
                'article',
                null,
                _react2.default.createElement(
                    'header',
                    { className: 'guide-header', id: 'attr-pattern-lib' },
                    _react2.default.createElement(
                        'h1',
                        null,
                        'smif \u2013 Pattern library'
                    )
                ),
                _react2.default.createElement(
                    'div',
                    { className: 'guide-content' },
                    _react2.default.createElement(
                        'h2',
                        null,
                        'Typography'
                    ),
                    _react2.default.createElement(
                        'div',
                        { className: 'sample-container' },
                        _react2.default.createElement(
                            'h1',
                            null,
                            'Heading Level 1'
                        )
                    ),
                    _react2.default.createElement(
                        'div',
                        { className: 'sample-container' },
                        _react2.default.createElement(
                            'h2',
                            null,
                            'Heading Level 2'
                        )
                    ),
                    _react2.default.createElement(
                        'div',
                        { className: 'sample-container' },
                        _react2.default.createElement(
                            'h3',
                            null,
                            'Heading Level 3'
                        )
                    ),
                    _react2.default.createElement(
                        'div',
                        { className: 'sample-container' },
                        _react2.default.createElement(
                            'p',
                            null,
                            'ITRC is a consortium of seven leading UK universities, investigating ways to improve the performance of infrastructure systems in the UK and around the world. Our research is helping businesses and policymakers to explore the risk of infrastructure failure and the long term benefits of investments and policies to improve infrastructure systems.'
                        )
                    ),
                    _react2.default.createElement(
                        'div',
                        { className: 'sample-container' },
                        _react2.default.createElement(
                            'i',
                            null,
                            'Italic'
                        )
                    ),
                    _react2.default.createElement(
                        'div',
                        { className: 'sample-container' },
                        _react2.default.createElement(
                            'b',
                            null,
                            'Bold'
                        )
                    ),
                    _react2.default.createElement(
                        'h2',
                        null,
                        'Inline text elements'
                    ),
                    _react2.default.createElement(
                        'h3',
                        null,
                        'Abbreviation'
                    ),
                    _react2.default.createElement(
                        'div',
                        { className: 'sample-container' },
                        _react2.default.createElement(
                            'abbr',
                            { title: 'abbreviation' },
                            'abbr.'
                        )
                    ),
                    _react2.default.createElement(
                        'h3',
                        null,
                        'Code'
                    ),
                    _react2.default.createElement(
                        'div',
                        { className: 'sample-container' },
                        _react2.default.createElement(
                            'code',
                            null,
                            'var i = 0;'
                        )
                    ),
                    _react2.default.createElement(
                        'h3',
                        null,
                        'Details'
                    ),
                    _react2.default.createElement(
                        'div',
                        { className: 'sample-container' },
                        _react2.default.createElement(
                            'details',
                            null,
                            _react2.default.createElement(
                                'summary',
                                null,
                                'Some details'
                            ),
                            _react2.default.createElement(
                                'p',
                                null,
                                'More info about the details.'
                            )
                        )
                    ),
                    _react2.default.createElement(
                        'h3',
                        null,
                        'External link'
                    ),
                    _react2.default.createElement(
                        'div',
                        { className: 'sample-container' },
                        _react2.default.createElement(
                            'a',
                            { href: 'https://www.itrc.org.uk/' },
                            'Link to the ITRC homepage'
                        )
                    ),
                    _react2.default.createElement(
                        'h3',
                        null,
                        'Same-page link'
                    ),
                    _react2.default.createElement(
                        'div',
                        { className: 'sample-container' },
                        _react2.default.createElement(
                            'a',
                            { href: '#attr-pattern-lib' },
                            'Link to the header of this page'
                        )
                    ),
                    _react2.default.createElement(
                        'h3',
                        null,
                        'Fieldset'
                    ),
                    _react2.default.createElement(
                        'fieldset',
                        null,
                        _react2.default.createElement(
                            'legend',
                            null,
                            'Fieldset'
                        )
                    ),
                    _react2.default.createElement(
                        'h2',
                        null,
                        'Input elements'
                    ),
                    _react2.default.createElement(
                        'h3',
                        null,
                        'Button'
                    ),
                    _react2.default.createElement(
                        'div',
                        { className: 'sample-container' },
                        _react2.default.createElement('input', { type: 'button', value: 'Click Me' })
                    ),
                    _react2.default.createElement(
                        'h3',
                        null,
                        'Checkbox'
                    ),
                    _react2.default.createElement(
                        'div',
                        { className: 'sample-container' },
                        _react2.default.createElement(
                            'label',
                            null,
                            _react2.default.createElement('input', { type: 'checkbox' }),
                            'Subscribe to newsletter?'
                        )
                    ),
                    _react2.default.createElement(
                        'h3',
                        null,
                        'Date'
                    ),
                    _react2.default.createElement(
                        'div',
                        { className: 'sample-container' },
                        _react2.default.createElement('input', { type: 'date', value: '2017-06-01' })
                    ),
                    _react2.default.createElement(
                        'h3',
                        null,
                        'Datetime'
                    ),
                    _react2.default.createElement(
                        'div',
                        { className: 'sample-container' },
                        _react2.default.createElement('input', { type: 'datetime-local', value: '2017-06-01T08:30' })
                    ),
                    _react2.default.createElement(
                        'h3',
                        null,
                        'File'
                    ),
                    _react2.default.createElement(
                        'div',
                        { className: 'sample-container' },
                        _react2.default.createElement('input', { type: 'file' })
                    ),
                    _react2.default.createElement(
                        'h3',
                        null,
                        'Number'
                    ),
                    _react2.default.createElement(
                        'div',
                        { className: 'sample-container' },
                        _react2.default.createElement('input', { type: 'number' })
                    ),
                    _react2.default.createElement(
                        'h3',
                        null,
                        'Radio Button'
                    ),
                    _react2.default.createElement(
                        'div',
                        { className: 'sample-container' },
                        _react2.default.createElement(
                            'label',
                            null,
                            _react2.default.createElement('input', { type: 'radio' }),
                            'Subscribe to newsletter?'
                        )
                    ),
                    _react2.default.createElement(
                        'h3',
                        null,
                        'Range'
                    ),
                    _react2.default.createElement(
                        'div',
                        { className: 'sample-container' },
                        _react2.default.createElement('input', { type: 'range' })
                    ),
                    _react2.default.createElement(
                        'h3',
                        null,
                        'Text Field'
                    ),
                    _react2.default.createElement(
                        'div',
                        { className: 'sample-container' },
                        _react2.default.createElement('input', { type: 'text' })
                    ),
                    _react2.default.createElement(
                        'h3',
                        null,
                        'Text Area'
                    ),
                    _react2.default.createElement(
                        'div',
                        { className: 'sample-container' },
                        _react2.default.createElement(
                            'textarea',
                            { name: 'textarea', rows: '10', cols: '50' },
                            'Write something here'
                        )
                    ),
                    _react2.default.createElement(
                        'h3',
                        null,
                        'Droplist'
                    ),
                    _react2.default.createElement(
                        'div',
                        { className: 'sample-container' },
                        _react2.default.createElement(
                            'select',
                            null,
                            _react2.default.createElement(
                                'option',
                                { value: '', disabled: 'disabled', selected: 'selected' },
                                'Please select a name'
                            ),
                            _react2.default.createElement(
                                'option',
                                { value: '1' },
                                'One'
                            ),
                            _react2.default.createElement(
                                'option',
                                { value: '2' },
                                'Two'
                            )
                        )
                    ),
                    _react2.default.createElement(
                        'h3',
                        null,
                        'Datalist'
                    ),
                    _react2.default.createElement(
                        'div',
                        { className: 'sample-container' },
                        _react2.default.createElement(
                            'label',
                            null,
                            'Choose a model:',
                            _react2.default.createElement('input', { type: 'text', list: 'models', name: 'myModels' })
                        ),
                        _react2.default.createElement(
                            'datalist',
                            { id: 'models' },
                            _react2.default.createElement(
                                'option',
                                { value: 'Water' },
                                'Water'
                            ),
                            _react2.default.createElement(
                                'option',
                                { value: 'Energy-Demand' },
                                'Energy Demand'
                            ),
                            _react2.default.createElement(
                                'option',
                                { value: 'Energy-Supply' },
                                'Energy Supply'
                            ),
                            _react2.default.createElement(
                                'option',
                                { value: 'Solid-Waste' },
                                'Solid Waste'
                            )
                        )
                    ),
                    _react2.default.createElement(
                        'h3',
                        null,
                        'Select Menu'
                    ),
                    _react2.default.createElement(
                        'div',
                        { className: 'sample-container' },
                        _react2.default.createElement(
                            'select',
                            { size: '3' },
                            _react2.default.createElement(
                                'option',
                                { value: 'Water' },
                                'Water'
                            ),
                            _react2.default.createElement(
                                'option',
                                { value: 'Energy-Demand' },
                                'Energy Demand'
                            ),
                            _react2.default.createElement(
                                'option',
                                { value: 'Energy-Supply' },
                                'Energy Supply'
                            ),
                            _react2.default.createElement(
                                'option',
                                { value: 'Solid-Waste' },
                                'Solid Waste'
                            )
                        )
                    ),
                    _react2.default.createElement(
                        'h2',
                        null,
                        'Display elements'
                    ),
                    _react2.default.createElement(
                        'h3',
                        null,
                        'Table'
                    ),
                    _react2.default.createElement(
                        'div',
                        { className: 'sample-container' },
                        _react2.default.createElement(
                            'table',
                            null,
                            _react2.default.createElement(
                                'tr',
                                null,
                                _react2.default.createElement(
                                    'th',
                                    null,
                                    'Firstname'
                                ),
                                _react2.default.createElement(
                                    'th',
                                    null,
                                    'Lastname'
                                )
                            ),
                            _react2.default.createElement(
                                'tr',
                                null,
                                _react2.default.createElement(
                                    'td',
                                    null,
                                    'Roald'
                                ),
                                _react2.default.createElement(
                                    'td',
                                    null,
                                    'Lemmen'
                                )
                            ),
                            _react2.default.createElement(
                                'tr',
                                null,
                                _react2.default.createElement(
                                    'td',
                                    null,
                                    'Will'
                                ),
                                _react2.default.createElement(
                                    'td',
                                    null,
                                    'Usher'
                                )
                            ),
                            _react2.default.createElement(
                                'tr',
                                null,
                                _react2.default.createElement(
                                    'td',
                                    null,
                                    'Tom'
                                ),
                                _react2.default.createElement(
                                    'td',
                                    null,
                                    'Russell'
                                )
                            )
                        )
                    ),
                    _react2.default.createElement(
                        'h2',
                        null,
                        'Icons'
                    ),
                    _react2.default.createElement(
                        'h3',
                        null,
                        'Delete'
                    ),
                    _react2.default.createElement(
                        'div',
                        { className: 'sample-container' },
                        _react2.default.createElement(_trash2.default, null)
                    )
                )
            );
        }
    }]);

    return PatternLibrary;
}(_react2.default.Component);

exports.default = PatternLibrary;

/***/ }),

/***/ 650:
/***/ (function(module, exports) {

// removed by extract-text-webpack-plugin

/***/ })

},[648]);