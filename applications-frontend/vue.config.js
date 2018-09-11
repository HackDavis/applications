module.exports = {
    devServer: {
      proxy: {
        "/login": {
          target: "http://localhost:5000",
        },
        "/logout": {
            target: "http://localhost:5000"
        }
      }
    }
  }