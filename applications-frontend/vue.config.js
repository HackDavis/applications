module.exports = {
  devServer: {
    proxy: {
      "/api": {
        target: "http://localhost:5000"
      },
      "/login": {
        target: "http://localhost:5000"
      },
      "/logout": {
        target: "http://localhost:5000"
      },
      "/google": {
        target: "http://localhost:5000"
      }
    }
  }
};
