const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      "/items": {
        target: "http://127.0.0.1:8000", // URL server backend Django
        changeOrigin: true,
      },
    },
  },
});
