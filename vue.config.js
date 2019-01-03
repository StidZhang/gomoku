module.exports = {
  lintOnSave: false,
  devServer: {
    proxy: {
      '/api*': {
        // Forward frontend dev server request for /api to django dev server
        target: 'http://localhost:5000/'
      },
      '/socket.io*': {
        target: 'http://localhost:5000/',
        ws: true
      }
    }
  }
}
