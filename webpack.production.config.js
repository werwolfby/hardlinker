var webpack = require('webpack');
var config = require('./webpack.config');
var HtmlWebpackPlugin = require('html-webpack-plugin')
var ExtractTextPlugin = require('extract-text-webpack-plugin');

config.debug = false;
config.devtool = null;
config.plugins = [
    new HtmlWebpackPlugin({
        template: "./src/index.html",
        inject: "body"
    }),
    new webpack.ProvidePlugin({
        $: "jquery",
        jQuery: "jquery",
        "window.jQuery": "jquery"
    }),
    new ExtractTextPlugin('[name].css'),
    new webpack.optimize.UglifyJsPlugin({
        beautify: false,
        mangle: false,
        compress : { screw_ie8 : true},
        dead_code: false,
        unused: false,
        comments: false
    })
  ];

module.exports = config;
