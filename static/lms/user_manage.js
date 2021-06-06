var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var AddUser = function (_React$Component) {
    _inherits(AddUser, _React$Component);

    function AddUser(props) {
        _classCallCheck(this, AddUser);

        var _this = _possibleConstructorReturn(this, (AddUser.__proto__ || Object.getPrototypeOf(AddUser)).call(this, props));

        _this.state = { users: _this.props.users,
            pairs: _this.props.pairs,
            chats: _this.props.chats,
            add_user: { modal: false, user_id: 0 },
            add_pair: { student: 0, teacher: 0 },
            add_chat: { pair: { id: 0 }, chat: { id: 0 } },
            add_lesson: { pair_id: 0, date: 0 }
        };
        console.log(_this.state.chats);
        return _this;
    }

    _createClass(AddUser, [{
        key: "add_user",
        value: function add_user() {
            var _this2 = this;

            var role = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : "student";

            var name = prompt("Please enter " + role + " name", "Mark Ivanov");
            if (name != null) {
                var formData = new FormData();
                formData.append("csrfmiddlewaretoken", this.props.token);
                formData.append("name", name);
                formData.append("role", role);
                formData.append("add_user", 1);
                fetch("", { method: "POST", body: formData }).then(function (response) {
                    return response.json();
                }).then(function (resp) {
                    console.log(resp);
                    var users = _this2.state.users.slice();
                    users.push(resp.user);
                    _this2.setState({ users: users });
                });
            }
        }
    }, {
        key: "add_pair",
        value: function add_pair() {
            var _this3 = this;

            console.log(this.state.add_pair);
            var formData = new FormData();
            formData.append("csrfmiddlewaretoken", this.props.token);
            formData.append("user_id", this.state.add_pair.student);
            formData.append("teacher", this.state.add_pair.teacher);
            formData.append("add_pair", 1);
            fetch("", { method: "POST", body: formData }).then(function (response) {
                return response.json();
            }).then(function (resp) {
                console.log(resp);
                var pairs = _this3.state.pairs.slice();
                if (resp.ok) {
                    pairs.push(resp.pair);
                }
                _this3.setState({ add_pair: { student: 0, teacher: 0 }, pairs: pairs });
            });
        }
    }, {
        key: "add_chat",
        value: function add_chat() {
            var _this4 = this;

            console.log(this.state.add_chat);
            var formData = new FormData();
            formData.append("csrfmiddlewaretoken", this.props.token);
            formData.append("pair_id", this.state.add_chat.pair.id);
            formData.append("chat_id", this.state.add_chat.chat.id);
            formData.append("add_chat", 1);
            fetch("", { method: "POST", body: formData }).then(function (response) {
                return response.json();
            }).then(function (resp) {
                console.log(resp);
                if (resp.ok) {
                    var pairs = _this4.state.pairs.slice();
                    var pair_id = _this4.state.add_chat.pair.id;
                    var index = pairs.findIndex(function (el) {
                        return el.pair_id === pair_id;
                    });
                    pairs[index] = resp.chat_id;
                    var chats = _this4.state.chats.slice();
                    chats.splice(_this4.state.add_chat.chat.index, 1);
                    _this4.setState({ add_chat: { pair: { id: 0 }, chat: { id: 0 } }, pairs: pairs, chats: chats });
                }
            });
        }
    }, {
        key: "pair_id_info",
        value: function pair_id_info(pair_id) {
            var _this5 = this;

            var formData = new FormData();
            formData.append("csrfmiddlewaretoken", this.props.token);
            formData.append("pair_id_info", pair_id);
            fetch("", { method: "POST", body: formData }).then(function (response) {
                return response.json();
            }).then(function (resp) {
                console.log(resp);
                _this5.setState({ add_lesson: { pair_id: pair_id, info: resp.info } });
            });
        }
    }, {
        key: "add_lesson",
        value: function add_lesson() {
            var _this6 = this;

            var formData = new FormData(document.getElementById("add_lesson"));
            formData.append("csrfmiddlewaretoken", this.props.token);
            formData.append("pair_id", this.state.add_lesson.pair_id);
            formData.append("add_lesson", 1);
            fetch("", { method: "POST", body: formData }).then(function (response) {
                return response.json();
            }).then(function (resp) {
                console.log(resp);
                _this6.setState({ add_lesson: { pair_id: _this6.state.add_lesson.pair_id, info: resp.info } });
            });
        }
    }, {
        key: "render",
        value: function render() {
            var _this7 = this;

            return React.createElement(
                "div",
                { className: "container" },
                React.createElement(
                    "h2",
                    null,
                    "\u0414\u043E\u0431\u0430\u0432\u0438\u0442\u044C \u0443\u0440\u043E\u043A \u0434\u043B\u044F \u043F\u0430\u0440\u044B \u0443\u0447\u0438\u0442\u0435\u043B\u044C \u0443\u0447\u0435\u043D\u0438\u043A"
                ),
                React.createElement(
                    "div",
                    { className: "row" },
                    this.state.pairs.map(function (pair, index) {
                        return React.createElement(
                            "div",
                            { className: "col-md-3" },
                            React.createElement(
                                "div",
                                { className: pair.pair_id === _this7.state.add_lesson.pair_id ? "element-card selected" : "element-card",
                                    onClick: function onClick() {
                                        return _this7.pair_id_info(pair.pair_id);
                                    } },
                                pair.name,
                                pair.chat_id ? "" : React.createElement(
                                    "span",
                                    null,
                                    " \u2717"
                                )
                            )
                        );
                    })
                ),
                React.createElement("br", null),
                this.state.add_lesson.pair_id ? React.createElement(
                    "form",
                    { id: "add_lesson" },
                    React.createElement(
                        "div",
                        { className: "form-group row my-1" },
                        React.createElement(
                            "div",
                            { className: "col-md-4 col-sm-5 col-12 mb-3" },
                            React.createElement("input", { className: "form-control form-control-lg mx-1", name: "date", type: "date", defaultValue: this.props.today })
                        ),
                        React.createElement(
                            "div",
                            { className: "col-md-4 col-sm-3 col-6 mb-3" },
                            React.createElement("input", { className: "form-control form-control-lg mx-1", name: "time", defaultValue: "19:00" })
                        ),
                        React.createElement(
                            "div",
                            { className: "col-md-4 col-sm-4 col-6  mb-3" },
                            React.createElement(
                                "select",
                                { name: "duration", className: "form-control form-control-lg mx-1", defaultValue: "60" },
                                React.createElement(
                                    "option",
                                    { value: "30" },
                                    "30 \u043C\u0438\u043D"
                                ),
                                React.createElement(
                                    "option",
                                    { value: "45" },
                                    "45 \u043C\u0438\u043D"
                                ),
                                React.createElement(
                                    "option",
                                    { value: "60" },
                                    "1 \u0447\u0430\u0441"
                                ),
                                React.createElement(
                                    "option",
                                    { value: "90" },
                                    "1.5 \u0447\u0430\u0441\u0430"
                                ),
                                React.createElement(
                                    "option",
                                    { value: "120" },
                                    "2 \u0447\u0430\u0441\u0430"
                                )
                            )
                        ),
                        React.createElement(
                            "div",
                            { className: "col-md-4 col-sm-6 col-12 mb-3" },
                            React.createElement("input", { name: "name", className: "form-control form-control-lg mx-1", defaultValue: "Mathematics" })
                        ),
                        React.createElement(
                            "div",
                            { className: "col-md-4 col-sm-6 col-12 mb-3" },
                            React.createElement(
                                "button",
                                { type: "button", className: "btn btn-lg btn-success mx-1",
                                    onClick: function onClick() {
                                        return _this7.add_lesson();
                                    } },
                                "\u0414\u043E\u0431\u0430\u0432\u0438\u0442\u044C \u0443\u0440\u043E\u043A"
                            )
                        )
                    ),
                    React.createElement(
                        "div",
                        null,
                        this.state.add_lesson.info.map(function (el, index) {
                            return React.createElement(
                                "p",
                                null,
                                el.start,
                                " - ",
                                el.end,
                                " ",
                                el.name,
                                " ",
                                el.notificaton ? React.createElement(
                                    "span",
                                    null,
                                    "\u2713"
                                ) : ""
                            );
                        })
                    )
                ) : React.createElement(
                    "p",
                    null,
                    "\u0412\u044B\u0431\u0435\u0440\u0438\u0442\u0435 \u043F\u0430\u0440\u0443 \u0443\u0447\u0435\u043D\u0438\u043A-\u0443\u0447\u0438\u0442\u0435\u043B\u044C"
                ),
                React.createElement("br", null),
                React.createElement("hr", null),
                React.createElement(
                    "div",
                    { className: "row" },
                    React.createElement(
                        "div",
                        { className: "col-md-6" },
                        React.createElement(
                            "h2",
                            null,
                            "\u0423\u0447\u0435\u043D\u0438\u043A\u0438"
                        ),
                        this.state.users.filter(function (user) {
                            return user.role === "student";
                        }).map(function (user, index) {
                            return React.createElement(
                                "div",
                                { className: user.user_id === _this7.state.add_pair.student ? "element-card selected" : "element-card",
                                    onClick: function onClick() {
                                        return _this7.setState({ add_pair: { student: user.user_id, teacher: _this7.state.add_pair.teacher } });
                                    } },
                                user.name
                            );
                        }),
                        React.createElement(
                            "div",
                            { className: "element-card", onClick: function onClick() {
                                    return _this7.add_user("student");
                                } },
                            React.createElement(
                                "span",
                                { className: "text-success" },
                                "\u0414\u043E\u0431\u0430\u0432\u0438\u0442\u044C \u0443\u0447\u0435\u043D\u0438\u043A\u0430"
                            )
                        )
                    ),
                    React.createElement(
                        "div",
                        { className: "col-md-6" },
                        React.createElement(
                            "h2",
                            null,
                            "\u0423\u0447\u0438\u0442\u0435\u043B\u044F"
                        ),
                        this.state.users.filter(function (user) {
                            return user.role === "teacher";
                        }).map(function (user, index) {
                            return React.createElement(
                                "div",
                                { className: user.user_id === _this7.state.add_pair.teacher ? "element-card selected" : "element-card",
                                    onClick: function onClick() {
                                        return _this7.setState({ add_pair: { student: _this7.state.add_pair.student, teacher: user.user_id } });
                                    } },
                                user.name
                            );
                        }),
                        React.createElement(
                            "div",
                            { className: "element-card", onClick: function onClick() {
                                    return _this7.add_user("teacher");
                                } },
                            React.createElement(
                                "span",
                                { className: "text-success" },
                                "\u0414\u043E\u0431\u0430\u0432\u0438\u0442\u044C \u0443\u0447\u0438\u0442\u0435\u043B\u044F"
                            )
                        )
                    )
                ),
                React.createElement(
                    "div",
                    null,
                    React.createElement(
                        "p",
                        null,
                        "\u0427\u0442\u043E\u0431\u044B \u0434\u043E\u0431\u0430\u0432\u0438\u0442\u044C \u043F\u0430\u0440\u0443 \u0432\u044B\u0431\u0435\u0440\u0438\u0442\u0435 \u0443\u0447\u0435\u043D\u0438\u043A\u0430 \u0438\u0437 \u043B\u0435\u0432\u043E\u0439 \u043A\u043E\u043B\u043E\u043D\u043A\u0438, \u0443\u0447\u0438\u0442\u0435\u043B\u044C \u0438\u0437 \u043F\u0440\u0430\u0432\u043E\u0439 \u0438 \u043D\u0430\u0436\u043C\u0438\u0442\u0435 \u0441\u043E\u0437\u0434\u0430\u0442\u044C \u043F\u0430\u0440\u0443."
                    ),
                    React.createElement(
                        "button",
                        { type: "button", className: "btn btn-success", onClick: function onClick() {
                                return _this7.add_pair();
                            },
                            disabled: !this.state.add_pair.student || !this.state.add_pair.teacher },
                        "\u0421\u043E\u0437\u0434\u0430\u0442\u044C \u043F\u0430\u0440\u0443 \u0443\u0447\u0435\u043D\u0438\u043A-\u0443\u0447\u0438\u0442\u0435\u043B\u044C"
                    )
                ),
                React.createElement("br", null),
                React.createElement("hr", null),
                React.createElement(
                    "div",
                    { className: "row" },
                    React.createElement(
                        "div",
                        { className: "col-md-6" },
                        React.createElement(
                            "h2",
                            null,
                            "\u041F\u0430\u0440\u044B \u0443\u0447\u0438\u0442\u0435\u043B\u044C-\u0443\u0447\u0435\u043D\u0438\u043A \u0431\u0435\u0437 \u0447\u0430\u0442\u0430"
                        ),
                        this.state.pairs.filter(function (pair) {
                            return pair.chat_id === 0;
                        }).map(function (pair, index) {
                            return React.createElement(
                                "div",
                                { className: pair.pair_id === _this7.state.add_chat.pair.id ? "element-card selected" : "element-card",
                                    onClick: function onClick() {
                                        return _this7.setState({ add_chat: { pair: { id: pair.pair_id, index: index }, chat: _this7.state.add_chat.chat } });
                                    } },
                                pair.name
                            );
                        })
                    ),
                    React.createElement(
                        "div",
                        { className: "col-md-6" },
                        React.createElement(
                            "h2",
                            null,
                            "\u0427\u0430\u0442\u044B \u0441 \u0431\u043E\u0442\u043E\u043C \u0431\u0435\u0437 \u043F\u0430\u0440\u044B"
                        ),
                        this.state.chats.map(function (chat, index) {
                            return React.createElement(
                                "div",
                                { className: chat.chat_id === _this7.state.add_chat.chat.id ? "element-card selected" : "element-card",
                                    onClick: function onClick() {
                                        return _this7.setState({ add_chat: { pair: _this7.state.add_chat.pair, chat: { id: chat.chat_id, index: index } } });
                                    } },
                                React.createElement(
                                    "span",
                                    null,
                                    chat.text,
                                    " (",
                                    chat.date,
                                    ")"
                                ),
                                React.createElement("br", null),
                                React.createElement(
                                    "small",
                                    null,
                                    chat.chat_id
                                )
                            );
                        }),
                        React.createElement(
                            "p",
                            null,
                            "\u0427\u0442\u043E\u0431\u044B \u0434\u043E\u0431\u0430\u0432\u0438\u0442\u044C \u0433\u0440\u0443\u043F\u043F\u043E\u0432\u043E\u0439 \u0447\u0430\u0442:",
                            React.createElement("br", null),
                            React.createElement(
                                "ul",
                                null,
                                React.createElement(
                                    "li",
                                    null,
                                    "\u0414\u043E\u0431\u0430\u0432\u044C\u0442\u0435 @Edera_bot \u0432 \u0433\u0440\u0443\u043F\u043F\u043E\u0432\u043E\u0439 \u0447\u0430\u0442"
                                ),
                                React.createElement(
                                    "li",
                                    null,
                                    "\u0414\u0430\u0439\u0442\u0435 \u0431\u043E\u0442\u0443 \u043F\u0440\u0430\u0432\u0430 \u0430\u0434\u043C\u0438\u043D\u0438\u0441\u0442\u0440\u0430\u0442\u043E\u0440\u0430"
                                ),
                                React.createElement(
                                    "li",
                                    null,
                                    "\u041D\u0430\u043F\u0438\u0448\u0438\u0442\u0435 \u043B\u044E\u0431\u043E\u0435 \u0441\u043E\u043E\u0431\u0449\u0435\u043D\u0438\u0435 \u0432 \u0447\u0430\u0442"
                                ),
                                React.createElement(
                                    "li",
                                    null,
                                    "\u041E\u0431\u043D\u043E\u0432\u0438\u0442\u0435 \u0441\u0442\u0440\u0430\u043D\u0438\u0446\u0443, \u0447\u0430\u0442 \u043F\u043E\u044F\u0432\u0438\u0442\u0441\u044F \u0437\u0434\u0435\u0441\u044C"
                                )
                            )
                        )
                    )
                ),
                React.createElement(
                    "button",
                    { type: "button", className: "btn btn-success", onClick: function onClick() {
                            return _this7.add_chat();
                        },
                        disabled: !this.state.add_chat.pair.id || !this.state.add_chat.chat.id
                    },
                    "\u0421\u0432\u044F\u0437\u0430\u0442\u044C \u043F\u0430\u0440\u0443 \u0438 \u0447\u0430\u0442"
                ),
                React.createElement("br", null),
                React.createElement("hr", null)
            );
        }
    }]);

    return AddUser;
}(React.Component);