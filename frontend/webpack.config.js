const path = require('path');

module.exports = {
  mode: 'development',
  entry: './src/index.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js',
  },
  devServer: {
    proxy: {
      '/': {
        target: 'http://localhost:8000', // change this to your backend server URL
        pathRewrite: {'^/api' : ''}, // remove the '/api' path prefix from the URL
        secure: false,
      },
    },
    port: 8000, // change this to the port you want to run your dev server on
  },
  // devServer: {
  //   proxy: {
  //     '/get_author_id/': 'http://localhost:8000'
  //   }
  // }
  // add your other webpack configurations here
};