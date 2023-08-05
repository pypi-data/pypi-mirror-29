var webpack = require('webpack');
var path = require('path');

var config = {
    entry: {
        'app': path.resolve(__dirname, 'src/js/index.jsx')
    },

    devtool: process.env.NODE_ENV !== 'production' ? "inline-sourcemap" : "source-map",

    resolve: {
        alias: {
            'js': path.resolve(__dirname, 'src/js'),
            'scss': path.resolve(__dirname, 'src/scss')
        },

        extensions: ['.js', '.jsx']
    },

    module: {
        loaders: [
            {
                test : /\.jsx?/,
                loader : 'babel-loader'
            },
            {
                test: /\.scss$/,
                use: [{
                    loader: "style-loader" // creates style nodes from JS strings
                }, {
                    loader: "css-loader" // translates CSS into CommonJS
                }, {
                    loader: "sass-loader" // compiles Sass to CSS
                }]
            }
        ]
    },

    externals: {
        jquery: "jQuery"
    },

    plugins: [
        new webpack.ProvidePlugin({
            $: 'jquery',
            _: 'underscore',
        }),
        new webpack.EnvironmentPlugin({
            "IMAGES_URL": "" // the URL to serve images from.
        }),
        new webpack.DefinePlugin({
          VERSION: JSON.stringify(require("./package.json").version)
        })
    ],

    output: {
        path: path.resolve(__dirname, 'build'),
        filename: '[name].js'
    }
};

module.exports = config;