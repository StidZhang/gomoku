module.exports = {
  lintOnSave: false,
  devServer: {
    proxy: {
      '/api*': {
        // Forward frontend dev server request for /api to django dev server
        target: 'http://localhost:5000/'
      }
    }
  }
}
