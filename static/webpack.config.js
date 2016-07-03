var path = require('path');
var webpack = require('webpack');

module.exports = {
    entry: ['./js/init.js','./js/place.jsx'],
    output: {path: __dirname+'/js/', filename: 'bundle.js'},
    module: {
        loaders: [
            {
                test: /.jsx?$/,
                //exclude: /node_modules/,
                loader: 'babel-loader',
                query: {
                    presets: ['es2015', 'react']
                }
            }
        ]
    },
};
