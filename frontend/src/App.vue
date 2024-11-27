<template>
  <div id="app">
    <h1>Selamat Datang di Smart Spender</h1>
    <ItemList />
  </div>
</template>

<script>
import ItemList from "./components/ItemList.vue"; // Impor komponen

export default {
  components: {
    ItemList,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
