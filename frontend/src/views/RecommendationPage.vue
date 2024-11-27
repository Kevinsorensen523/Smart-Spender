<template>
  <div>
    <h1>Rekomendasi Barang</h1>
    <p>Uang Anda: Rp {{ budget }}</p>
    <h2>Daftar Rekomendasi</h2>
    <ul>
      <li v-for="item in recommendedItems" :key="item.id">
        {{ item.name }} - Rp {{ item.price }} (Jumlah: {{ item.quantity }})
      </li>
    </ul>
    <p v-if="remainingBudget">Sisa Budget: Rp {{ remainingBudget }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      budget: this.$route.query.budget,
      recommendedItems: [],
      remainingBudget: 0,
    };
  },
  created() {
    if (!this.budget) {
      alert("Budget tidak ditemukan. Kembali ke halaman sebelumnya.");
      this.$router.push("/budget");
    } else {
      this.fetchRecommendations();
    }
  },
  methods: {
    fetchRecommendations() {
      const selectedItems =
        JSON.parse(localStorage.getItem("selectedItems")) || [];
      const requestData = {
        budget: this.budget,
        items: selectedItems,
      };

      fetch("/items/recommendation/", {
        method: "POST", // Ensure the request method is POST
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      })
        .then((res) => res.json())
        .then((data) => {
          console.log("Data Rekomendasi dari Backend:", data);
          if (data.recommendations) {
            this.recommendedItems = data.recommendations;
            this.remainingBudget = data.remaining_budget;
          } else {
            alert(
              "Tidak ada rekomendasi yang tersedia berdasarkan budget Anda."
            );
          }
        })
        .catch((err) => {
          console.error("Error fetching recommendations:", err);
          alert("Terjadi kesalahan saat mengambil rekomendasi.");
        });
    },
  },
};
</script>

<style>
/* Tambahkan gaya opsional di sini */
</style>
