var webpack = require('webpack');
var path = require('path');
var HtmlWebpackPlugin = require('html-webpack-plugin')
var ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = {
  entry: {
    'polyfills': './src/polyfills.ts',
    'vendor': './src/vendor.ts',
    'app': './src/main.ts'
  },
  output: {
    path: "./webapp",
    filename: "[name].js"
  },
  externals: {
    "jquery": "jQuery",
    "bootstrap": "jQuery",
    'angular2/platform/browser': 'ng.platform.browser',
    'angular2/core': 'ng.core',
    'angular2/http': 'ng.http',
    'angular2/router': 'ng.router'
  },
  debug: true,
  devtool: 'source-map',
  plugins: [
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
        beautify: true,
        mangle: false,
        dead_code: false,
        unused: false,
        deadCode: false,
        compress : { screw_ie8 : true, keep_fnames: true, drop_debugger: false, dead_code: false, unused: false, },
        comments: true,
    })
  ],

  resolve: {
    extensions: ['', '.ts', '.js']
  },

  module: {
    loaders: [
      { test: /\.ts$/,                loaders: ['awesome-typescript-loader', 'angular2-template-loader'] },
      { test: /\.(png|gif|jpg|svg)$/, loader: 'file?name=imgs/[name].[ext]?[hash]' },
      { test: /\.(eot|ttf|woff2?)$/,  loader: 'file?name=fonts/[name].[ext]?[hash]' },
      { test: /\.css$/,               loader: ExtractTextPlugin.extract('css?minimize') },
      { test: /\.less$/,              loader: ExtractTextPlugin.extract('css?minimize!less') }
    ],
    noParse: [ path.join(__dirname, 'node_modules', 'angular2', 'bundles') ]
  },

  devServer: {
    historyApiFallback: true,
    proxy: {
      '/api/*': {
        target: 'http://localhost:4735/'
      }
    }
  }
};
