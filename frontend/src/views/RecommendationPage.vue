<template>
  <div>
    <h1>Rekomendasi Barang</h1>
    <p>Uang Anda: Rp {{ budget }}</p>
    <h2>Daftar Rekomendasi</h2>
    <ul>
      <li v-for="item in recommendedItems" :key="item.id">
        {{ item.name }} - Rp {{ item.price }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      budget: this.$route.query.budget,
      recommendedItems: [],
    };
  },
  created() {
    this.fetchRecommendations();
  },
  methods: {
    fetchRecommendations() {
      fetch(`/items/recommendation/?budget=${this.budget}`)
        .then((res) => res.json())
        .then((data) => {
          this.recommendedItems = data.recommendations;
        })
        .catch((err) => console.error(err));
    },
  },
};
</script>

<style>
/* Tambahkan gaya opsional di sini */
</style>
