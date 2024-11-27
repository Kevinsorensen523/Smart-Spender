<template>
  <div>
    <h1>Selamat Datang di Smart Spender!</h1>
    <button @click="navigate('/budget')">Start</button>
    <button @click="navigate('/list-items')">Lihat List Barang</button>
  </div>
</template>

<script>
export default {
  methods: {
    navigate(path) {
      this.$router.push(path);
    },
  },
};
</script>
