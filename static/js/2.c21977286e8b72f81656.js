(window.webpackJsonp = window.webpackJsonp || []).push([[2], {
    "184": function(e, t, n) {
        var o = n(185);
        "string" == typeof o && (o = [[e.i, o, ""]]);
        var r = {
            "sourceMap": !1,
            "insertAt": "top",
            "hmr": !0,
            "transform": void 0,
            "insertInto": void 0
        };
        n(25)(o, r);
        o.locals && (e.exports = o.locals)
    },
    "185": function(e, t, n) {
        (t = n(24)(!1)).push([e.i, "button {\n  position: relative;\n  display: block;\n  width: 100%;\n  margin-left: auto;\n  margin-right: auto;\n  padding-left: 14px;\n  padding-right: 14px;\n  box-sizing: border-box;\n  font-size: 18px;\n  text-align: center;\n  text-decoration: none;\n  line-height: 2.55555556;\n  border-radius: 5px;\n  -webkit-tap-highlight-color: transparent;\n  overflow: hidden;\n  color: #000000;\n  background-color: #F8F8F8;\n}\n\nbutton[plain] {\n  color: #353535;\n  border: 1px solid #353535;\n  background-color: transparent;\n}\n\nbutton[plain][disabled] {\n  color: rgba(0, 0, 0, 0.3);\n  border: 1px solid rgba(0, 0, 0, 0.2);\n  background-color: #F7F7F7;\n}\n\nbutton[type=primary] {\n  color: #FFFFFF;\n  background-color: #1AAD19;\n}\n\nbutton[type=primary][plain] {\n  color: #1aad19;\n  border: 1px solid #1aad19;\n  background-color: transparent;\n}\n\nbutton[type=primary][plain][disabled] {\n  color: rgba(0, 0, 0, 0.3);\n  border: 1px solid rgba(0, 0, 0, 0.2);\n  background-color: #F7F7F7;\n}\n", ""]),
        e.exports = t
    },
    "192": function(e, t, n) {
        var o = n(193);
        "string" == typeof o && (o = [[e.i, o, ""]]);
        var r = {
            "sourceMap": !1,
            "insertAt": "top",
            "hmr": !0,
            "transform": void 0,
            "insertInto": void 0
        };
        n(25)(o, r);
        o.locals && (e.exports = o.locals)
    },
    "193": function(e, t, n) {
        (t = n(24)(!1)).push([e.i, ".taro-scroll {\n  -webkit-overflow-scrolling: auto;\n}\n\n.taro-scroll::-webkit-scrollbar {\n  display: none;\n}\n\n.taro-scroll-view {\n  overflow: hidden;\n}\n\n.taro-scroll-view__scroll-x {\n  overflow-x: scroll;\n  overflow-y: hidden;\n}\n\n.taro-scroll-view__scroll-y {\n  overflow-x: hidden;\n  overflow-y: scroll;\n}\n", ""]),
        e.exports = t
    },
    "194": function(e, t, n) {
        "use strict";
        n(13);
        var o = n(1)
          , r = n(23)
          , l = n(8)
          , i = n.n(l)
          , a = (n(184),
        Object.assign || function(e) {
            for (var t = 1; t < arguments.length; t++) {
                var n = arguments[t];
                for (var o in n)
                    Object.prototype.hasOwnProperty.call(n, o) && (e[o] = n[o])
            }
            return e
        }
        )
          , c = function() {
            function defineProperties(e, t) {
                for (var n = 0; n < t.length; n++) {
                    var o = t[n];
                    o.enumerable = o.enumerable || !1,
                    o.configurable = !0,
                    "value"in o && (o.writable = !0),
                    Object.defineProperty(e, o.key, o)
                }
            }
            return function(e, t, n) {
                return t && defineProperties(e.prototype, t),
                n && defineProperties(e, n),
                e
            }
        }();
        function _defineProperty(e, t, n) {
            return t in e ? Object.defineProperty(e, t, {
                "value": n,
                "enumerable": !0,
                "configurable": !0,
                "writable": !0
            }) : e[t] = n,
            e
        }
        function _classCallCheck(e, t) {
            if (!(e instanceof t))
                throw new TypeError("Cannot call a class as a function")
        }
        function _possibleConstructorReturn(e, t) {
            if (!e)
                throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
            return !t || "object" != typeof t && "function" != typeof t ? e : t
        }
        var s = function(e) {
            function Button() {
                _classCallCheck(this, Button);
                var e = _possibleConstructorReturn(this, (Button.__proto__ || Object.getPrototypeOf(Button)).apply(this, arguments));
                return e.state = {
                    "hover": !1,
                    "touch": !1
                },
                e
            }
            return function _inherits(e, t) {
                if ("function" != typeof t && null !== t)
                    throw new TypeError("Super expression must either be null or a function, not " + typeof t);
                e.prototype = Object.create(t && t.prototype, {
                    "constructor": {
                        "value": e,
                        "enumerable": !1,
                        "writable": !0,
                        "configurable": !0
                    }
                }),
                t && (Object.setPrototypeOf ? Object.setPrototypeOf(e, t) : e.__proto__ = t)
            }(Button, e),
            c(Button, [{
                "key": "componentWillUnmount",
                "value": function componentWillUnmount() {
                    this.startTimer && clearTimeout(this.startTimer),
                    this.endTimer && clearTimeout(this.endTimer)
                }
            }, {
                "key": "render",
                "value": function render() {
                    var e, t = this, n = this.props, l = n.children, c = n.disabled, s = n.className, u = n.style, p = n.onClick, f = n.onTouchStart, d = n.onTouchEnd, h = n.hoverClass, b = void 0 === h ? "button-hover" : h, y = n.hoverStartTime, m = void 0 === y ? 20 : y, v = n.hoverStayTime, _ = void 0 === v ? 70 : v, w = n.size, O = n.plain, C = n.loading, g = void 0 !== C && C, T = n.type, P = void 0 === T ? "default" : T, k = s || i()("weui-btn", (_defineProperty(e = {}, "" + b, this.state.hover && !c && "none" !== b),
                    _defineProperty(e, "weui-btn_plain-" + P, O),
                    _defineProperty(e, "weui-btn_" + P, !O && P),
                    _defineProperty(e, "weui-btn_mini", "mini" === w),
                    _defineProperty(e, "weui-btn_loading", g),
                    _defineProperty(e, "weui-btn_disabled", c),
                    e));
                    return o.l.createElement("button", a({}, Object(r.a)(this.props, ["hoverClass", "onTouchStart", "onTouchEnd"]), {
                        "className": k,
                        "style": u,
                        "onClick": p,
                        "disabled": c,
                        "onTouchStart": function _onTouchStart(e) {
                            t.setState((function() {
                                return {
                                    "touch": !0
                                }
                            }
                            )),
                            b && "none" !== b && !c && (t.startTimer = setTimeout((function() {
                                t.state.touch && t.setState((function() {
                                    return {
                                        "hover": !0
                                    }
                                }
                                ))
                            }
                            ), m)),
                            f && f(e)
                        },
                        "onTouchEnd": function _onTouchEnd(e) {
                            t.setState((function() {
                                return {
                                    "touch": !1
                                }
                            }
                            )),
                            b && "none" !== b && !c && (t.endTimer = setTimeout((function() {
                                t.state.touch || t.setState((function() {
                                    return {
                                        "hover": !1
                                    }
                                }
                                ))
                            }
                            ), _)),
                            d && d(e)
                        }
                    }), g && o.l.createElement("i", {
                        "class": "weui-loading"
                    }), l)
                }
            }]),
            Button
        }(o.l.Component);
        t.a = s
    },
    "199": function(e, t, n) {
        "use strict";
        n(13);
        var o = n(1)
          , r = n(23)
          , l = n(8)
          , i = n.n(l)
          , a = (n(192),
        Object.assign || function(e) {
            for (var t = 1; t < arguments.length; t++) {
                var n = arguments[t];
                for (var o in n)
                    Object.prototype.hasOwnProperty.call(n, o) && (e[o] = n[o])
            }
            return e
        }
        )
          , c = function() {
            function defineProperties(e, t) {
                for (var n = 0; n < t.length; n++) {
                    var o = t[n];
                    o.enumerable = o.enumerable || !1,
                    o.configurable = !0,
                    "value"in o && (o.writable = !0),
                    Object.defineProperty(e, o.key, o)
                }
            }
            return function(e, t, n) {
                return t && defineProperties(e.prototype, t),
                n && defineProperties(e, n),
                e
            }
        }();
        function _defineProperty(e, t, n) {
            return t in e ? Object.defineProperty(e, t, {
                "value": n,
                "enumerable": !0,
                "configurable": !0,
                "writable": !0
            }) : e[t] = n,
            e
        }
        function _classCallCheck(e, t) {
            if (!(e instanceof t))
                throw new TypeError("Cannot call a class as a function")
        }
        function _possibleConstructorReturn(e, t) {
            if (!e)
                throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
            return !t || "object" != typeof t && "function" != typeof t ? e : t
        }
        function easeOutScroll() {
            var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : 0
              , t = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : 0
              , n = arguments[2];
            if (e !== t && "number" == typeof e) {
                var o = t - e
                  , r = 500
                  , l = +new Date
                  , i = t >= e;
                step()
            }
            function linear(e, t, n, o) {
                return n * e / o + t
            }
            function step() {
                e = linear(+new Date - l, e, o, r),
                i && e >= t || !i && t >= e ? n(t) : (n(e),
                requestAnimationFrame(step))
            }
        }
        function scrollIntoView(e) {
            document.querySelector("#" + e).scrollIntoView({
                "behavior": "smooth",
                "block": "center",
                "inline": "start"
            })
        }
        function scrollVertical(e, t) {
            var n = this;
            t ? easeOutScroll(this._scrollTop, e, (function(e) {
                n.container && (n.container.scrollTop = e)
            }
            )) : this.container && (this.container.scrollTop = e),
            this._scrollTop = e
        }
        function scrollHorizontal(e, t) {
            var n = this;
            t ? easeOutScroll(this._scrollLeft, e, (function(e) {
                n.container && (n.container.scrollLeft = e)
            }
            )) : this.container && (this.container.scrollLeft = e),
            this._scrollLeft = e
        }
        var s = function(e) {
            function ScrollView() {
                _classCallCheck(this, ScrollView);
                var e = _possibleConstructorReturn(this, (ScrollView.__proto__ || Object.getPrototypeOf(ScrollView)).apply(this, arguments));
                return e.onTouchMove = function(e) {
                    e.stopPropagation()
                }
                ,
                e
            }
            return function _inherits(e, t) {
                if ("function" != typeof t && null !== t)
                    throw new TypeError("Super expression must either be null or a function, not " + typeof t);
                e.prototype = Object.create(t && t.prototype, {
                    "constructor": {
                        "value": e,
                        "enumerable": !1,
                        "writable": !0,
                        "configurable": !0
                    }
                }),
                t && (Object.setPrototypeOf ? Object.setPrototypeOf(e, t) : e.__proto__ = t)
            }(ScrollView, e),
            c(ScrollView, [{
                "key": "componentDidMount",
                "value": function componentDidMount() {
                    this.handleScroll(this.props, !0)
                }
            }, {
                "key": "componentWillReceiveProps",
                "value": function componentWillReceiveProps(e) {
                    this.handleScroll(e)
                }
            }, {
                "key": "handleScroll",
                "value": function handleScroll(e) {
                    var t = this
                      , n = arguments.length > 1 && void 0 !== arguments[1] && arguments[1];
                    if (e.scrollIntoView && "string" == typeof e.scrollIntoView && document && document.querySelector && document.querySelector("#" + e.scrollIntoView))
                        n ? setTimeout((function() {
                            return scrollIntoView(e.scrollIntoView)
                        }
                        ), 500) : scrollIntoView(e.scrollIntoView);
                    else {
                        var o = "scrollWithAnimation"in e;
                        e.scrollY && "number" == typeof e.scrollTop && e.scrollTop !== this._scrollTop && (n ? setTimeout((function() {
                            return scrollVertical.bind(t)(e.scrollTop, o)
                        }
                        ), 10) : scrollVertical.bind(this)(e.scrollTop, o)),
                        e.scrollX && "number" == typeof e.scrollLeft && e.scrollLeft !== this._scrollLeft && (n ? setTimeout((function() {
                            return scrollHorizontal.bind(t)(e.scrollLeft, o)
                        }
                        ), 10) : scrollHorizontal.bind(this)(e.scrollLeft, o))
                    }
                }
            }, {
                "key": "render",
                "value": function render() {
                    var e, t = this, n = this.props, l = n.className, c = n.onScroll, s = n.onScrollToUpper, u = n.onScrollToLower, p = n.onTouchMove, f = n.scrollX, d = n.scrollY, h = this.props, b = h.upperThreshold, y = void 0 === b ? 50 : b, m = h.lowerThreshold, v = void 0 === m ? 50 : m, _ = i()("taro-scroll", (_defineProperty(e = {}, "taro-scroll-view__scroll-x", f),
                    _defineProperty(e, "taro-scroll-view__scroll-y", d),
                    e), l);
                    y = parseInt(y),
                    v = parseInt(v);
                    var w = function throttle(e, t) {
                        var n = null;
                        return function() {
                            for (var o = arguments.length, r = Array(o), l = 0; l < o; l++)
                                r[l] = arguments[l];
                            clearTimeout(n),
                            n = setTimeout((function() {
                                e.apply(void 0, r)
                            }
                            ), t)
                        }
                    }((function uperAndLower(e) {
                        if (t.container) {
                            var n = t.container
                              , o = n.offsetWidth
                              , r = n.offsetHeight
                              , l = n.scrollLeft
                              , i = n.scrollTop
                              , a = n.scrollHeight
                              , c = n.scrollWidth;
                            u && (t.props.scrollY && r + i + v >= a || t.props.scrollX && o + l + v >= c) && u(e),
                            s && (t.props.scrollY && i <= y || t.props.scrollX && l <= y) && s(e)
                        }
                    }
                    ), 200);
                    return o.l.createElement("div", a({
                        "ref": function ref(e) {
                            t.container = e
                        }
                    }, Object(r.a)(this.props, ["className", "scrollTop", "scrollLeft"]), {
                        "className": _,
                        "onScroll": function _onScroll(e) {
                            var n = t.container
                              , o = n.scrollLeft
                              , r = n.scrollTop
                              , l = n.scrollHeight
                              , i = n.scrollWidth;
                            t._scrollLeft = o,
                            t._scrollTop = r,
                            Object.defineProperty(e, "detail", {
                                "enumerable": !0,
                                "writable": !0,
                                "value": {
                                    "scrollLeft": o,
                                    "scrollTop": r,
                                    "scrollHeight": l,
                                    "scrollWidth": i
                                }
                            }),
                            w(e),
                            c && c(e)
                        },
                        "onTouchMove": function _onTouchMove(e) {
                            p ? p(e) : t.onTouchMove(e)
                        },
                        "onLoad": function onLoad(e) {
                            console.log("onload", e)
                        }
                    }), this.props.children)
                }
            }]),
            ScrollView
        }(o.l.Component);
        t.a = s
    },
    "267": function(e, t, n) {
        "use strict";
        n.d(t, "a", (function() {
            return s
        }
        ));
        var o = n(1)
          , r = n(8)
          , l = n.n(r)
          , i = n(16)
          , a = n(175)
          , c = function() {
            function defineProperties(e, t) {
                for (var n = 0; n < t.length; n++) {
                    var o = t[n];
                    o.enumerable = o.enumerable || !1,
                    o.configurable = !0,
                    "value"in o && (o.writable = !0),
                    Object.defineProperty(e, o.key, o)
                }
            }
            return function(e, t, n) {
                return t && defineProperties(e.prototype, t),
                n && defineProperties(e, n),
                e
            }
        }();
        function _classCallCheck(e, t) {
            if (!(e instanceof t))
                throw new TypeError("Cannot call a class as a function")
        }
        function _possibleConstructorReturn(e, t) {
            if (!e)
                throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
            return !t || "object" != typeof t && "function" != typeof t ? e : t
        }
        var s = function(e) {
            function AtModalHeader() {
                return _classCallCheck(this, AtModalHeader),
                _possibleConstructorReturn(this, (AtModalHeader.__proto__ || Object.getPrototypeOf(AtModalHeader)).apply(this, arguments))
            }
            return function _inherits(e, t) {
                if ("function" != typeof t && null !== t)
                    throw new TypeError("Super expression must either be null or a function, not " + typeof t);
                e.prototype = Object.create(t && t.prototype, {
                    "constructor": {
                        "value": e,
                        "enumerable": !1,
                        "writable": !0,
                        "configurable": !0
                    }
                }),
                t && (Object.setPrototypeOf ? Object.setPrototypeOf(e, t) : e.__proto__ = t)
            }(AtModalHeader, e),
            c(AtModalHeader, [{
                "key": "render",
                "value": function render() {
                    var e = l()("at-modal__header", this.props.className);
                    return o.l.createElement(i.a, {
                        "className": e
                    }, this.props.children)
                }
            }]),
            AtModalHeader
        }(a.a)
    },
    "268": function(e, t, n) {
        "use strict";
        n.d(t, "a", (function() {
            return s
        }
        ));
        var o = n(1)
          , r = n(8)
          , l = n.n(r)
          , i = n(199)
          , a = n(175)
          , c = function() {
            function defineProperties(e, t) {
                for (var n = 0; n < t.length; n++) {
                    var o = t[n];
                    o.enumerable = o.enumerable || !1,
                    o.configurable = !0,
                    "value"in o && (o.writable = !0),
                    Object.defineProperty(e, o.key, o)
                }
            }
            return function(e, t, n) {
                return t && defineProperties(e.prototype, t),
                n && defineProperties(e, n),
                e
            }
        }();
        function _classCallCheck(e, t) {
            if (!(e instanceof t))
                throw new TypeError("Cannot call a class as a function")
        }
        function _possibleConstructorReturn(e, t) {
            if (!e)
                throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
            return !t || "object" != typeof t && "function" != typeof t ? e : t
        }
        var s = function(e) {
            function AtModalContent() {
                return _classCallCheck(this, AtModalContent),
                _possibleConstructorReturn(this, (AtModalContent.__proto__ || Object.getPrototypeOf(AtModalContent)).apply(this, arguments))
            }
            return function _inherits(e, t) {
                if ("function" != typeof t && null !== t)
                    throw new TypeError("Super expression must either be null or a function, not " + typeof t);
                e.prototype = Object.create(t && t.prototype, {
                    "constructor": {
                        "value": e,
                        "enumerable": !1,
                        "writable": !0,
                        "configurable": !0
                    }
                }),
                t && (Object.setPrototypeOf ? Object.setPrototypeOf(e, t) : e.__proto__ = t)
            }(AtModalContent, e),
            c(AtModalContent, [{
                "key": "render",
                "value": function render() {
                    var e = l()("at-modal__content", this.props.className);
                    return o.l.createElement(i.a, {
                        "scrollY": !0,
                        "className": e
                    }, this.props.children)
                }
            }]),
            AtModalContent
        }(a.a)
    },
    "269": function(e, t, n) {
        "use strict";
        n.d(t, "a", (function() {
            return p
        }
        ));
        var o = n(1)
          , r = n(8)
          , l = n.n(r)
          , i = n(176)
          , a = n.n(i)
          , c = n(16)
          , s = n(175)
          , u = function() {
            function defineProperties(e, t) {
                for (var n = 0; n < t.length; n++) {
                    var o = t[n];
                    o.enumerable = o.enumerable || !1,
                    o.configurable = !0,
                    "value"in o && (o.writable = !0),
                    Object.defineProperty(e, o.key, o)
                }
            }
            return function(e, t, n) {
                return t && defineProperties(e.prototype, t),
                n && defineProperties(e, n),
                e
            }
        }();
        function _classCallCheck(e, t) {
            if (!(e instanceof t))
                throw new TypeError("Cannot call a class as a function")
        }
        function _possibleConstructorReturn(e, t) {
            if (!e)
                throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
            return !t || "object" != typeof t && "function" != typeof t ? e : t
        }
        var p = function(e) {
            function AtModalAction() {
                return _classCallCheck(this, AtModalAction),
                _possibleConstructorReturn(this, (AtModalAction.__proto__ || Object.getPrototypeOf(AtModalAction)).apply(this, arguments))
            }
            return function _inherits(e, t) {
                if ("function" != typeof t && null !== t)
                    throw new TypeError("Super expression must either be null or a function, not " + typeof t);
                e.prototype = Object.create(t && t.prototype, {
                    "constructor": {
                        "value": e,
                        "enumerable": !1,
                        "writable": !0,
                        "configurable": !0
                    }
                }),
                t && (Object.setPrototypeOf ? Object.setPrototypeOf(e, t) : e.__proto__ = t)
            }(AtModalAction, e),
            u(AtModalAction, [{
                "key": "render",
                "value": function render() {
                    var e = l()("at-modal__footer", {
                        "at-modal__footer--simple": this.props.isSimple
                    }, this.props.className);
                    return o.l.createElement(c.a, {
                        "className": e
                    }, o.l.createElement(c.a, {
                        "className": "at-modal__action"
                    }, this.props.children))
                }
            }]),
            AtModalAction
        }(s.a);
        p.defaultProps = {
            "isSimple": !1
        },
        p.propTypes = {
            "isSimple": a.a.bool
        }
    },
    "462": function(e, t, n) {
        "use strict";
        n.d(t, "a", (function() {
            return v
        }
        ));
        var o = n(1)
          , r = n(8)
          , l = n.n(r)
          , i = n(176)
          , a = n.n(i)
          , c = n(16)
          , s = n(189)
          , u = n(194)
          , p = n(3)
          , f = n(175)
          , d = n(181)
          , h = n(269)
          , b = n(268)
          , y = n(267)
          , m = function() {
            function defineProperties(e, t) {
                for (var n = 0; n < t.length; n++) {
                    var o = t[n];
                    o.enumerable = o.enumerable || !1,
                    o.configurable = !0,
                    "value"in o && (o.writable = !0),
                    Object.defineProperty(e, o.key, o)
                }
            }
            return function(e, t, n) {
                return t && defineProperties(e.prototype, t),
                n && defineProperties(e, n),
                e
            }
        }();
        var v = function(e) {
            function AtModal(e) {
                !function _classCallCheck(e, t) {
                    if (!(e instanceof t))
                        throw new TypeError("Cannot call a class as a function")
                }(this, AtModal);
                var t = function _possibleConstructorReturn(e, t) {
                    if (!e)
                        throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
                    return !t || "object" != typeof t && "function" != typeof t ? e : t
                }(this, (AtModal.__proto__ || Object.getPrototypeOf(AtModal)).call(this, e));
                t.handleClickOverlay = function() {
                    t.props.closeOnClickOverlay && t.setState({
                        "_isOpened": !1
                    }, t.handleClose)
                }
                ,
                t.handleClose = function(e) {
                    "function" == typeof t.props.onClose && t.props.onClose(e)
                }
                ,
                t.handleCancel = function(e) {
                    "function" == typeof t.props.onCancel && t.props.onCancel(e)
                }
                ,
                t.handleConfirm = function(e) {
                    "function" == typeof t.props.onConfirm && t.props.onConfirm(e)
                }
                ,
                t.handleTouchMove = function(e) {
                    e.stopPropagation()
                }
                ;
                var n = e.isOpened;
                return t.state = {
                    "_isOpened": n,
                    "isWEB": p.a.getEnv() === p.a.ENV_TYPE.WEB
                },
                t
            }
            return function _inherits(e, t) {
                if ("function" != typeof t && null !== t)
                    throw new TypeError("Super expression must either be null or a function, not " + typeof t);
                e.prototype = Object.create(t && t.prototype, {
                    "constructor": {
                        "value": e,
                        "enumerable": !1,
                        "writable": !0,
                        "configurable": !0
                    }
                }),
                t && (Object.setPrototypeOf ? Object.setPrototypeOf(e, t) : e.__proto__ = t)
            }(AtModal, e),
            m(AtModal, [{
                "key": "componentWillReceiveProps",
                "value": function componentWillReceiveProps(e) {
                    var t = e.isOpened;
                    this.props.isOpened !== t && Object(d.d)(t),
                    t !== this.state._isOpened && this.setState({
                        "_isOpened": t
                    })
                }
            }, {
                "key": "render",
                "value": function render() {
                    var e = this.state
                      , t = e._isOpened
                      , n = e.isWEB
                      , r = this.props
                      , i = r.title
                      , a = r.content
                      , p = r.cancelText
                      , f = r.confirmText
                      , d = l()("at-modal", {
                        "at-modal--active": t
                    }, this.props.className);
                    if (i || a) {
                        var m = p || f;
                        return o.l.createElement(c.a, {
                            "className": d
                        }, o.l.createElement(c.a, {
                            "onClick": this.handleClickOverlay,
                            "className": "at-modal__overlay"
                        }), o.l.createElement(c.a, {
                            "className": "at-modal__container"
                        }, i && o.l.createElement(y.a, null, o.l.createElement(s.a, null, i)), a && o.l.createElement(b.a, null, o.l.createElement(c.a, {
                            "className": "content-simple"
                        }, n ? o.l.createElement(s.a, {
                            "dangerouslySetInnerHTML": {
                                "__html": a.replace(/\n/g, "<br/>")
                            }
                        }) : o.l.createElement(s.a, null, a))), m && o.l.createElement(h.a, {
                            "isSimple": !0
                        }, p && o.l.createElement(u.a, {
                            "onClick": this.handleCancel
                        }, p), f && o.l.createElement(u.a, {
                            "onClick": this.handleConfirm
                        }, f))))
                    }
                    return o.l.createElement(c.a, {
                        "onTouchMove": this.handleTouchMove,
                        "className": d
                    }, o.l.createElement(c.a, {
                        "className": "at-modal__overlay",
                        "onClick": this.handleClickOverlay
                    }), o.l.createElement(c.a, {
                        "className": "at-modal__container"
                    }, this.props.children))
                }
            }]),
            AtModal
        }(f.a);
        v.defaultProps = {
            "isOpened": !1,
            "closeOnClickOverlay": !0
        },
        v.propTypes = {
            "title": a.a.string,
            "isOpened": a.a.bool,
            "onCancel": a.a.func,
            "onConfirm": a.a.func,
            "onClose": a.a.func,
            "content": a.a.string,
            "closeOnClickOverlay": a.a.bool,
            "cancelText": a.a.string,
            "confirmText": a.a.string
        }
    }
}]);
